from flask import Blueprint, render_template, redirect, url_for, request, abort
from flask_login import login_required, current_user
from extensions import db
from models import User, Place, Category, Review

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


def _admin_required():
    if not current_user.is_authenticated or not current_user.is_admin:
        abort(403)


@admin_bp.route('/')
@login_required
def dashboard():
    _admin_required()
    return render_template('admin/dashboard.html',
                           users=User.query.all(),
                           places=Place.query.all(),
                           categories=Category.query.all())


@admin_bp.route('/category/add', methods=['POST'])
@login_required
def add_category():
    _admin_required()
    name = request.form.get('name', '').strip()
    if name and not Category.query.filter_by(name=name).first():
        db.session.add(Category(name=name))
        db.session.commit()
    return redirect(url_for('admin.dashboard'))


@admin_bp.route('/category/delete/<int:id>', methods=['POST'])
@login_required
def delete_category(id):
    _admin_required()
    cat = Category.query.get_or_404(id)
    # ถ้ามีสถานที่ในหมวดนี้ให้ set เป็น null ก่อน
    for p in Place.query.filter_by(category_id=id).all():
        p.category_id = None
    db.session.delete(cat)
    db.session.commit()
    return redirect(url_for('admin.dashboard'))


@admin_bp.route('/user/delete/<int:id>', methods=['POST'])
@login_required
def delete_user(id):
    _admin_required()
    if current_user.id == id:
        return redirect(url_for('admin.dashboard'))

    user = User.query.get_or_404(id)
    from models import ReviewReply, Favorite

    # เคลียร์ข้อมูลที่เกี่ยวข้องของ User
    ReviewReply.query.filter_by(user_id=id).delete()
    Favorite.query.filter_by(user_id=id).delete()
    Review.query.filter_by(user_id=id).delete()

    # ถ้าผู้ใช้เคยสร้างสถานที่ไว้ ให้โอนสิทธิ์ความเป็นเจ้าของให้ Admin ผู้ลบ
    for p in Place.query.filter_by(user_id=id).all():
        p.user_id = current_user.id

    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('admin.dashboard'))
