import math
from flask import Blueprint, render_template, redirect, url_for, request, jsonify, abort
from flask_login import login_required, current_user
from extensions import db
from models import Place, PlaceImage, Category, Review, ReviewReply, Favorite

places = Blueprint('places', __name__)


# ── helpers ──────────────────────────────────────────────────────────────────
def _avg_ratings(place_list):
    return {p.id: p.avg_rating for p in place_list}

def _favorites():
    if not current_user.is_authenticated:
        return set()
    return {f.place_id for f in Favorite.query.filter_by(user_id=current_user.id).all()}

def place_sort_key(p):
    """
    Multi-Tier Ranking Algorithm:
    1. คะแนนดาวเฉลี่ยสูงสุด (Quality)
    2. จำนวนผู้รีวิวมากที่สุด (Popularity / Review Volume)
    3. มีรูปภาพสมบูรณ์ (Media completeness)
    4. ID ลำดับสถานที่
    """
    avg = p.avg_rating if p.avg_rating is not None else -1
    review_count = len(p.reviews) if p.reviews else 0
    has_image = 1 if (p.images and len(p.images) > 0) else 0
    return (avg, review_count, has_image, p.id)


# ── Home ──────────────────────────────────────────────────────────────────────
@places.route('/')
def home():
    all_places = Place.query.all()
    categories = Category.query.all()

    sorted_places = sorted(all_places, key=place_sort_key, reverse=True)

    places_by_cat = {}
    for c in categories:
        cat_places = [p for p in all_places if p.category_id == c.id]
        places_by_cat[c.id] = sorted(cat_places, key=place_sort_key, reverse=True)

    return render_template('places/home.html',
                           places=sorted_places,
                           places_by_cat=places_by_cat,
                           avg_ratings=_avg_ratings(all_places),
                           favorites=_favorites(),
                           categories=categories)


# ── เอกสารบทที่ 3 (System Analysis & Design) ─────────────────────────────────
@places.route('/chapter3')
def chapter3():
    return render_template('docs/chapter3.html')


# ── List + Search ─────────────────────────────────────────────────────────────
@places.route('/places')
def list_places():
    q = request.args.get('q', '').strip()
    cat = request.args.get('cat', type=int)

    query = Place.query
    if q:
        query = query.join(Category, Place.category_id == Category.id).filter(
            Place.name.ilike(f'%{q}%') |
            Category.name.ilike(f'%{q}%')
        )
    if cat:
        query = query.filter(Place.category_id == cat)

    all_places = query.all()
    # เรียงตาม Multi-Tier Ranking (ดาวเฉลี่ย -> จำนวนรีวิว -> มีรูป)
    all_places = sorted(all_places, key=place_sort_key, reverse=True)
    categories = Category.query.all()
    return render_template('places/list.html',
                           places=all_places,
                           avg_ratings=_avg_ratings(all_places),
                           favorites=_favorites(),
                           categories=categories,
                           q=q, active_cat=cat)


# ── Detail + Review ───────────────────────────────────────────────────────────
@places.route('/place/<int:id>', methods=['GET', 'POST'])
def detail(id):
    place = Place.query.get_or_404(id)
    reviews = place.reviews

    is_favorite   = False
    user_reviewed = False
    if current_user.is_authenticated:
        is_favorite   = Favorite.query.filter_by(user_id=current_user.id, place_id=id).first() is not None
        user_reviewed = Review.query.filter_by(user_id=current_user.id, place_id=id).first() is not None

    if request.method == 'POST':
        if not current_user.is_authenticated:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.args.get('format') == 'json':
                return jsonify({'success': False, 'error': 'unauthenticated'}), 401
            return redirect(url_for('auth.login'))

        comment = request.form.get('comment','').strip()
        rating_raw = request.form.get('rating','').strip()
        # ต้องมีอย่างน้อย comment หรือ rating
        if comment or rating_raw:
            r = Review(comment=comment or '-',
                       rating=int(rating_raw) if rating_raw else 0,
                       user_id=current_user.id, place_id=id)
            db.session.add(r)
            db.session.commit()
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.args.get('format') == 'json':
                return jsonify({
                    'success': True,
                    'review': {
                        'id': r.id,
                        'comment': r.comment,
                        'rating': r.rating,
                        'username': current_user.username,
                        'is_admin': current_user.is_admin,
                        'user_id': current_user.id
                    },
                    'avg_rating': place.avg_rating,
                    'review_count': len(place.reviews)
                })
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.args.get('format') == 'json':
            return jsonify({'success': False, 'error': 'empty_comment'})
        return redirect(url_for('places.detail', id=id))

    # หาสถานที่ใกล้เคียง (ใช้ Haversine formula)
    nearby_places = []
    if place.latitude and place.longitude:
        all_others = Place.query.filter(
            Place.id != id,
            Place.latitude.isnot(None),
            Place.longitude.isnot(None)
        ).all()

        def haversine(lat1, lon1, lat2, lon2):
            R = 6371  # km
            dlat = math.radians(lat2 - lat1)
            dlon = math.radians(lon2 - lon1)
            a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
            return R * 2 * math.asin(math.sqrt(a))

        with_dist = [(p, haversine(place.latitude, place.longitude, p.latitude, p.longitude))
                     for p in all_others]
        with_dist.sort(key=lambda x: x[1])
        # เอาสถานที่ที่อยู่ภายใน 100 กม. สูงสุด 6 แห่ง
        nearby_places = [(p, round(d, 1)) for p, d in with_dist if d <= 100][:6]

    return render_template('places/detail.html',
                           place=place, reviews=reviews,
                           is_favorite=is_favorite, user_reviewed=user_reviewed,
                           nearby_places=nearby_places)


# ── Add ───────────────────────────────────────────────────────────────────────
@places.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if not current_user.is_admin:
        abort(403)

    categories = Category.query.all()
    if request.method == 'POST':
        lat    = request.form.get('latitude',  '').strip()
        lng    = request.form.get('longitude', '').strip()
        cat_id = request.form.get('category_id', '').strip()

        place = Place(
            name        = request.form['name'],
            detail      = request.form['detail'],
            location    = request.form['location'],
            category_id = int(cat_id) if cat_id else None,
            user_id     = current_user.id,
            latitude    = float(lat) if lat else None,
            longitude   = float(lng) if lng else None,
        )
        db.session.add(place)
        db.session.flush()   # ได้ place.id ก่อน commit

        # บันทึกภาพหลายรูป
        for i, url in enumerate(request.form.getlist('image_urls')):
            url = url.strip()
            if url:
                caption = request.form.getlist('image_captions')[i] if i < len(request.form.getlist('image_captions')) else ''
                db.session.add(PlaceImage(url=url, caption=caption, order=i, place_id=place.id))

        db.session.commit()
        return redirect(url_for('places.detail', id=place.id))

    return render_template('places/add.html', categories=categories)


# ── Edit ──────────────────────────────────────────────────────────────────────
@places.route('/place/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    if not current_user.is_admin:
        abort(403)
    place = Place.query.get_or_404(id)
    categories = Category.query.all()

    if request.method == 'POST':
        lat    = request.form.get('latitude',  '').strip()
        lng    = request.form.get('longitude', '').strip()
        cat_id = request.form.get('category_id', '').strip()

        place.name        = request.form['name']
        place.detail      = request.form['detail']
        place.location    = request.form['location']
        place.category_id = int(cat_id) if cat_id else None
        place.latitude    = float(lat) if lat else None
        place.longitude   = float(lng) if lng else None

        # ลบภาพที่ถูกทำเครื่องหมายลบ
        delete_ids = request.form.getlist('delete_images')
        for img_id in delete_ids:
            img = PlaceImage.query.get(int(img_id))
            if img and img.place_id == place.id:
                db.session.delete(img)

        # เพิ่มภาพใหม่
        new_urls     = request.form.getlist('new_image_urls')
        new_captions = request.form.getlist('new_image_captions')
        existing_count = PlaceImage.query.filter_by(place_id=place.id).count()
        for i, url in enumerate(new_urls):
            url = url.strip()
            if url:
                cap = new_captions[i] if i < len(new_captions) else ''
                db.session.add(PlaceImage(url=url, caption=cap, order=existing_count + i, place_id=place.id))

        db.session.commit()
        return redirect(url_for('places.detail', id=place.id))

    return render_template('places/edit.html', place=place, categories=categories)


# ── Delete ────────────────────────────────────────────────────────────────────
@places.route('/place/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    if not current_user.is_admin:
        abort(403)
    place = Place.query.get_or_404(id)
    db.session.delete(place)
    db.session.commit()
    return redirect(url_for('places.list_places'))


# ── Favorites ─────────────────────────────────────────────────────────────────
@places.route('/favorite/<int:place_id>', methods=['GET', 'POST'])
@login_required
def toggle_favorite(place_id):
    fav = Favorite.query.filter_by(user_id=current_user.id, place_id=place_id).first()
    is_favorite = False
    if fav:
        db.session.delete(fav)
    else:
        db.session.add(Favorite(user_id=current_user.id, place_id=place_id))
        is_favorite = True
    db.session.commit()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.args.get('format') == 'json':
        return jsonify({'success': True, 'is_favorite': is_favorite, 'place_id': place_id})

    return redirect(request.args.get('next', url_for('places.detail', id=place_id)))


@places.route('/favorites')
@login_required
def my_favorites():
    fav_places = [f.place for f in Favorite.query.filter_by(user_id=current_user.id).all()]
    return render_template('places/favorites.html',
                           places=fav_places,
                           avg_ratings=_avg_ratings(fav_places))


# ── Review delete ─────────────────────────────────────────────────────────────
@places.route('/review/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete_review(id):
    r = Review.query.get_or_404(id)
    if r.user_id != current_user.id and not current_user.is_admin:
        abort(403)
    place_id = r.place_id
    place = r.place
    db.session.delete(r)
    db.session.commit()
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.args.get('format') == 'json':
        return jsonify({
            'success': True,
            'review_id': id,
            'avg_rating': place.avg_rating,
            'review_count': len(place.reviews)
        })
    return redirect(url_for('places.detail', id=place_id))


# ── Review Reply (Admin & User ตอบโต้กันได้) ──────────────────────────────────
@places.route('/review/<int:review_id>/reply', methods=['POST'])
@login_required
def reply_review(review_id):
    review = Review.query.get_or_404(review_id)
    content = request.form.get('content', '').strip()
    if content:
        reply = ReviewReply(content=content, review_id=review.id, user_id=current_user.id)
        db.session.add(reply)
        db.session.commit()
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.args.get('format') == 'json':
            return jsonify({
                'success': True,
                'reply': {
                    'id': reply.id,
                    'content': reply.content,
                    'username': current_user.username,
                    'is_admin': current_user.is_admin,
                    'is_author': (reply.user_id == review.user_id),
                    'user_id': current_user.id
                },
                'review_id': review.id,
                'replies_count': len(review.replies)
            })
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.args.get('format') == 'json':
        return jsonify({'success': False, 'error': 'empty_content'})
    return redirect(url_for('places.detail', id=review.place_id) + f'#review-{review.id}')


@places.route('/review-reply/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete_review_reply(id):
    reply = ReviewReply.query.get_or_404(id)
    if reply.user_id != current_user.id and not current_user.is_admin:
        abort(403)
    place_id = reply.review.place_id
    review_id = reply.review_id
    review = reply.review
    db.session.delete(reply)
    db.session.commit()
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.args.get('format') == 'json':
        return jsonify({
            'success': True,
            'reply_id': id,
            'review_id': review_id,
            'replies_count': len(review.replies)
        })
    return redirect(url_for('places.detail', id=place_id) + f'#review-{review_id}')



# ── Nearby places by user GPS (หมวดเดียวกับสถานที่ที่กำลังดู) ────────────────
@places.route('/api/nearby')
def api_nearby():
    import math
    try:
        user_lat = float(request.args.get('lat'))
        user_lng = float(request.args.get('lng'))
        exclude_id = request.args.get('exclude', type=int)
    except (TypeError, ValueError):
        return jsonify([])

    def haversine(lat1, lon1, lat2, lon2):
        R = 6371
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
        return R * 2 * math.asin(math.sqrt(a))

    # หาหมวดหมู่ของสถานที่ที่กำลังดูอยู่ (exclude_id) แล้วแนะนำเฉพาะหมวดเดียวกัน
    # เช่น กำลังดูวัด -> แนะนำวัด, กำลังดูหอพัก -> แนะนำหอพัก
    current_place = Place.query.get(exclude_id) if exclude_id else None

    candidates_query = Place.query.filter(
        Place.latitude.isnot(None),
        Place.longitude.isnot(None)
    )
    if current_place and current_place.category_id:
        candidates_query = candidates_query.filter(Place.category_id == current_place.category_id)
    candidates = candidates_query.all()

    if exclude_id:
        candidates = [p for p in candidates if p.id != exclude_id]

    with_dist = [(p, haversine(user_lat, user_lng, p.latitude, p.longitude))
                 for p in candidates]
    with_dist.sort(key=lambda x: x[1])
    nearby = [(p, round(d, 1)) for p, d in with_dist if d <= 100][:6]
    # Fallback: หากเปิดจากคอมพิวเตอร์หรือตำแหน่งห่างเกิน 100 กม. ให้ดึงสถานที่ใกล้ที่สุด 6 แห่งเสมอ
    if not nearby and with_dist:
        nearby = [(p, round(d, 1)) for p, d in with_dist][:6]

    result = []
    for p, dist in nearby:
        result.append({
            'id': p.id,
            'name': p.name,
            'location': p.location,
            'image_url': p.primary_image or '',
            'avg_rating': p.avg_rating,
            'dist': dist,
            'category': p.category.name if p.category else '',
        })
    return jsonify(result)


# ── Nearby hotels/accommodations ──────────────────────────────────────────────
@places.route('/api/nearby-hotels')
def api_nearby_hotels():
    import math
    try:
        user_lat = float(request.args.get('lat'))
        user_lng = float(request.args.get('lng'))
        exclude_id = request.args.get('exclude', type=int)
    except (TypeError, ValueError):
        return jsonify([])

    def haversine(lat1, lon1, lat2, lon2):
        R = 6371
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
        return R * 2 * math.asin(math.sqrt(a))

    from models import Category
    # หาหมวดหมู่ที่ชื่อมีคำว่า ห้องพัก หรือ โรงแรม หรือ ที่พัก
    hotel_cats = Category.query.filter(
        Category.name.ilike('%ห้องพัก%') |
        Category.name.ilike('%โรงแรม%') |
        Category.name.ilike('%ที่พัก%') |
        Category.name.ilike('%รีสอร์ท%') |
        Category.name.ilike('%เกสต์เฮ้าส์%')
    ).all()

    if not hotel_cats:
        return jsonify([])

    hotel_cat_ids = [cat.id for cat in hotel_cats]
    candidates = Place.query.filter(
        Place.latitude.isnot(None),
        Place.longitude.isnot(None),
        Place.category_id.in_(hotel_cat_ids)
    ).all()

    if exclude_id:
        candidates = [p for p in candidates if p.id != exclude_id]

    with_dist = [(p, haversine(user_lat, user_lng, p.latitude, p.longitude))
                 for p in candidates]
    with_dist.sort(key=lambda x: x[1])
    nearby = [(p, round(d, 1)) for p, d in with_dist if d <= 100][:6]
    # Fallback: หากเปิดจากคอมพิวเตอร์หรือตำแหน่งห่างเกิน 100 กม. ให้ดึงที่พักใกล้ที่สุด 6 แห่งเสมอ
    if not nearby and with_dist:
        nearby = [(p, round(d, 1)) for p, d in with_dist][:6]

    result = []
    for p, dist in nearby:
        result.append({
            'id': p.id,
            'name': p.name,
            'location': p.location,
            'image_url': p.primary_image or '',
            'avg_rating': p.avg_rating,
            'dist': dist,
            'category': p.category.name if p.category else '',
        })
    return jsonify(result)

# ── Map ───────────────────────────────────────────────────────────────────────
@places.route('/map')
def map_view():
    focus_id = request.args.get('id', type=int)
    return render_template('places/map.html', focus_id=focus_id)


@places.route('/api/places')
def api_places():
    result = []
    for p in Place.query.filter(Place.latitude.isnot(None)).all():
        result.append({
            'id': p.id, 'name': p.name, 'location': p.location,
            'image_url': p.primary_image or '',
            'latitude': p.latitude, 'longitude': p.longitude,
            'avg_rating': p.avg_rating,
        })
    return jsonify(result)


# ── Image Proxy (แก้ปัญหา hotlink block) ─────────────────────────────────────
import requests as http
from flask import Response

@places.route('/proxy-image')
def proxy_image():
    import re
    url = request.args.get('url', '')
    if not url:
        return '', 400

    # แปลง Google Drive URL อัตโนมัติถ้ายังไม่ได้แปลง
    match = re.search(r'/file/d/([a-zA-Z0-9_-]+)', url)
    if match:
        url = f'https://drive.google.com/uc?export=view&id={match.group(1)}'

    try:
        resp = http.get(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': 'https://drive.google.com/',
        }, timeout=15, allow_redirects=True)
        content_type = resp.headers.get('Content-Type', 'image/jpeg')
        # ถ้า Google Drive redirect ไปหน้า confirm ให้ดึง confirm link
        if 'text/html' in content_type and 'drive.google.com' in url:
            confirm = re.search(r'href="(/uc[?]export=download[^"]+)"', resp.text)
            if confirm:
                confirm_url = 'https://drive.google.com' + confirm.group(1).replace('&amp;', '&')
                resp = http.get(confirm_url, headers={
                    'User-Agent': 'Mozilla/5.0',
                    'Referer': 'https://drive.google.com/',
                }, timeout=15)
                content_type = resp.headers.get('Content-Type', 'image/jpeg')
        return Response(resp.content, content_type=content_type,
                       headers={'Cache-Control': 'public, max-age=3600'})
    except Exception:
        return '', 404


# ── Tile Proxy (ดึงจาก OSM France HOT ความเร็วสูง ไม่มีลายน้ำ) ────────
@places.route('/tile/<int:z>/<int:x>/<int:y>.png')
def tile_proxy(z, x, y):
    """Flask ไปดึง tile จาก OSM France HOT → สะอาด ไม่มีลายน้ำ และโหลดเร็ว 100%"""
    sources = [
        f'https://a.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png',
        f'https://b.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png',
        f'https://c.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png'
    ]
    for url in sources:
        try:
            resp = http.get(url, timeout=5)
            if resp.status_code == 200:
                return Response(
                    resp.content,
                    content_type=resp.headers.get('Content-Type', 'image/png'),
                    headers={'Cache-Control': 'public, max-age=86400'}  # cache 1 วัน
                )
        except Exception:
            continue
    return '', 404
