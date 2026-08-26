import secrets
import smtplib
from email.mime.text import MIMEText
import requests as http
from urllib.parse import urlencode
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from flask import Blueprint, render_template, redirect, url_for, request, session, current_app
from flask_login import login_user, logout_user, login_required
from extensions import db, bcrypt
from models import User

auth = Blueprint('auth', __name__, url_prefix='/auth')

RESET_TOKEN_MAX_AGE = 3600  # ลิงก์ลืมรหัสผ่านใช้ได้ 1 ชั่วโมง


def _get_serializer():
    return URLSafeTimedSerializer(current_app.config['SECRET_KEY'])


def _generate_reset_token(user):
    return _get_serializer().dumps(user.email, salt=current_app.config['SECURITY_PASSWORD_SALT'])


def _verify_reset_token(token):
    try:
        email = _get_serializer().loads(
            token, salt=current_app.config['SECURITY_PASSWORD_SALT'], max_age=RESET_TOKEN_MAX_AGE)
    except (BadSignature, SignatureExpired):
        return None
    return User.query.filter_by(email=email).first()


def _send_reset_email(user, reset_url):
    """พยายามส่งอีเมลจริงถ้ามีการตั้งค่า SMTP ไว้ ถ้าไม่ได้ตั้งค่า/ส่งไม่สำเร็จ จะคืนค่า False"""
    cfg = current_app.config
    if not (cfg.get('MAIL_SERVER') and cfg.get('MAIL_USERNAME') and cfg.get('MAIL_PASSWORD')):
        return False
    try:
        msg = MIMEText(
            f'สวัสดีคุณ {user.username},\n\n'
            f'คลิกลิงก์ด้านล่างเพื่อตั้งรหัสผ่านใหม่ (ลิงก์นี้จะหมดอายุใน 1 ชั่วโมง):\n{reset_url}\n\n'
            f'หากคุณไม่ได้ร้องขอ กรุณาเพิกเฉยต่ออีเมลนี้'
        )
        msg['Subject'] = 'รีเซ็ตรหัสผ่าน - Travel Recommend'
        msg['From']    = cfg['MAIL_SENDER']
        msg['To']      = user.email
        with smtplib.SMTP(cfg['MAIL_SERVER'], cfg['MAIL_PORT']) as server:
            if cfg['MAIL_USE_TLS']:
                server.starttls()
            server.login(cfg['MAIL_USERNAME'], cfg['MAIL_PASSWORD'])
            server.sendmail(cfg['MAIL_SENDER'], [user.email], msg.as_string())
        return True
    except Exception:
        return False


def _get_or_create_user(username, email=None):
    user = User.query.filter_by(email=email).first() if email else None
    if not user:
        base = username.replace(' ', '_')
        uname = base
        i = 1
        while User.query.filter_by(username=uname).first():
            uname = f"{base}_{i}"; i += 1
        pw = bcrypt.generate_password_hash(secrets.token_hex(16)).decode()
        user = User(username=uname, email=email, password=pw)
        db.session.add(user)
        db.session.commit()
    return user


@auth.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        email    = request.form.get('email',  '').strip() or None
        phone    = request.form.get('phone',  '').strip() or None
        if User.query.filter_by(username=username).first():
            error = 'ชื่อผู้ใช้นี้มีแล้ว'
        elif email and User.query.filter_by(email=email).first():
            error = 'อีเมลนี้ถูกใช้แล้ว'
        elif phone and User.query.filter_by(phone=phone).first():
            error = 'เบอร์โทรนี้ถูกใช้แล้ว'
        else:
            pw   = bcrypt.generate_password_hash(request.form['password']).decode()
            user = User(username=username, password=pw, email=email, phone=phone)
            db.session.add(user); db.session.commit()
            return redirect(url_for('auth.login'))
    return render_template('auth/register.html', error=error)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        ident = request.form['identifier'].strip()
        pw    = request.form['password']
        user  = (User.query.filter_by(username=ident).first() or
                 User.query.filter_by(email=ident).first()    or
                 User.query.filter_by(phone=ident).first())
        if user is None:
            error = 'ไม่พบชื่อผู้ใช้ อีเมล หรือเบอร์โทรนี้ในระบบ'
        elif not bcrypt.check_password_hash(user.password, pw):
            error = 'รหัสผ่านไม่ถูกต้อง'
        else:
            login_user(user)
            return redirect(url_for('places.home'))
    return render_template('auth/login.html', error=error)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('places.home'))


@auth.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    error = None
    info = None
    reset_link = None  # ใช้แสดงลิงก์บนหน้าเว็บกรณียังไม่ได้ตั้งค่าเซิร์ฟเวอร์อีเมลจริง

    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        user = User.query.filter_by(email=email).first() if email else None

        if not email:
            error = 'กรุณากรอกอีเมล'
        elif not user:
            error = 'ไม่พบอีเมลนี้ในระบบ'
        else:
            token = _generate_reset_token(user)
            reset_url = url_for('auth.reset_password', token=token, _external=True)
            sent = _send_reset_email(user, reset_url)
            if sent:
                info = f'เราได้ส่งลิงก์สำหรับตั้งรหัสผ่านใหม่ไปที่อีเมล {user.email} แล้ว (ลิงก์หมดอายุใน 1 ชั่วโมง)'
            else:
                # ยังไม่ได้ตั้งค่าเซิร์ฟเวอร์อีเมล -> แสดงลิงก์ให้กดตรงนี้แทน
                info = 'ระบบยังไม่ได้เชื่อมต่ออีเมลผู้ส่ง คลิกลิงก์ด้านล่างเพื่อตั้งรหัสผ่านใหม่ได้เลย (ใช้ได้ภายใน 1 ชั่วโมง)'
                reset_link = reset_url

    return render_template('auth/forgot_password.html', error=error, info=info, reset_link=reset_link)


@auth.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    user = _verify_reset_token(token)
    if not user:
        return render_template('auth/reset_password.html', invalid=True)

    error = None
    if request.method == 'POST':
        pw  = request.form.get('password', '')
        pw2 = request.form.get('password2', '')
        if not pw or len(pw) < 6:
            error = 'รหัสผ่านต้องมีอย่างน้อย 6 ตัวอักษร'
        elif pw != pw2:
            error = 'รหัสผ่านทั้งสองช่องไม่ตรงกัน'
        else:
            user.password = bcrypt.generate_password_hash(pw).decode()
            db.session.commit()
            return redirect(url_for('auth.login', reset='success'))

    return render_template('auth/reset_password.html', invalid=False, error=error, token=token)


# ── Google ──
@auth.route('/google')
def google_login():
    state = secrets.token_urlsafe(16)
    session['oauth_state'] = state
    cfg = current_app.config
    params = dict(client_id=cfg['GOOGLE_CLIENT_ID'], redirect_uri=cfg['GOOGLE_REDIRECT_URI'],
                  response_type='code', scope='openid email profile', state=state)
    return redirect('https://accounts.google.com/o/oauth2/v2/auth?' + urlencode(params))

@auth.route('/google/callback')
def google_callback():
    cfg  = current_app.config
    code = request.args.get('code')
    if not code: return redirect(url_for('auth.login'))
    tok  = http.post('https://oauth2.googleapis.com/token', data=dict(
        code=code, client_id=cfg['GOOGLE_CLIENT_ID'],
        client_secret=cfg['GOOGLE_CLIENT_SECRET'],
        redirect_uri=cfg['GOOGLE_REDIRECT_URI'], grant_type='authorization_code')).json()
    token = tok.get('access_token')
    if not token: return redirect(url_for('auth.login'))
    info  = http.get('https://www.googleapis.com/oauth2/v2/userinfo',
                     headers={'Authorization': f'Bearer {token}'}).json()
    email = info.get('email')
    name  = info.get('name') or (email.split('@')[0] if email else 'google_user')
    login_user(_get_or_create_user(name, email=email))
    return redirect(url_for('places.home'))


# ── LINE ──
@auth.route('/line')
def line_login():
    state = secrets.token_urlsafe(16)
    session['oauth_state'] = state
    cfg = current_app.config
    params = dict(response_type='code', client_id=cfg['LINE_CHANNEL_ID'],
                  redirect_uri=cfg['LINE_REDIRECT_URI'], state=state, scope='profile openid email')
    return redirect('https://access.line.me/oauth2/v2.1/authorize?' + urlencode(params))

@auth.route('/line/callback')
def line_callback():
    cfg  = current_app.config
    code = request.args.get('code')
    if not code: return redirect(url_for('auth.login'))
    tok  = http.post('https://api.line.me/oauth2/v2.1/token', data=dict(
        grant_type='authorization_code', code=code,
        redirect_uri=cfg['LINE_REDIRECT_URI'],
        client_id=cfg['LINE_CHANNEL_ID'], client_secret=cfg['LINE_CHANNEL_SECRET'])).json()
    token = tok.get('access_token')
    if not token: return redirect(url_for('auth.login'))
    profile = http.get('https://api.line.me/v2/profile',
                       headers={'Authorization': f'Bearer {token}'}).json()
    login_user(_get_or_create_user(profile.get('displayName', 'LINE_User')))
    return redirect(url_for('places.home'))


# ── Facebook ──
@auth.route('/facebook')
def facebook_login():
    state = secrets.token_urlsafe(16)
    session['oauth_state'] = state
    cfg = current_app.config
    params = dict(client_id=cfg['FB_APP_ID'], redirect_uri=cfg['FB_REDIRECT_URI'],
                  state=state, scope='email,public_profile')
    return redirect('https://www.facebook.com/v18.0/dialog/oauth?' + urlencode(params))

@auth.route('/facebook/callback')
def facebook_callback():
    cfg  = current_app.config
    code = request.args.get('code')
    if not code: return redirect(url_for('auth.login'))
    tok  = http.get('https://graph.facebook.com/v18.0/oauth/access_token', params=dict(
        client_id=cfg['FB_APP_ID'], client_secret=cfg['FB_APP_SECRET'],
        redirect_uri=cfg['FB_REDIRECT_URI'], code=code)).json()
    token = tok.get('access_token')
    if not token: return redirect(url_for('auth.login'))
    info  = http.get('https://graph.facebook.com/me',
                     params=dict(fields='id,name,email', access_token=token)).json()
    login_user(_get_or_create_user(info.get('name', 'FB_User'), email=info.get('email')))
    return redirect(url_for('places.home'))
