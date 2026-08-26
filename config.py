import os
from dotenv import load_dotenv

load_dotenv()

# สร้างโฟลเดอร์ instance อัตโนมัติถ้ายังไม่มี
_base     = os.path.abspath(os.path.dirname(__file__))
_instance = os.path.join(_base, 'instance')
os.makedirs(_instance, exist_ok=True)

def _build_db_uri():
    """
    ถ้ามี DATABASE_URL (เช่น จาก Render Postgres) ให้ใช้ตัวนั้น
    ถ้าไม่มี ให้ fallback ไปใช้ SQLite ไฟล์ในเครื่อง (สำหรับ dev)
    """
    url = os.getenv('DATABASE_URL')
    if url:
        # Render (และผู้ให้บริการอื่น ๆ) มักให้ URL ขึ้นต้นด้วย postgres://
        # แต่ SQLAlchemy รุ่นใหม่ต้องการ postgresql:// จึงต้องแปลงให้ตรงกัน
        if url.startswith('postgres://'):
            url = url.replace('postgres://', 'postgresql://', 1)
        return url
    return 'sqlite:///' + os.path.join(_instance, 'site.db')


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'secret123')
    SQLALCHEMY_DATABASE_URI = _build_db_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        # ป้องกัน connection ที่ค้าง/หลุดเวลาเชื่อมต่อกับฐานข้อมูล remote อย่าง Render
        'pool_pre_ping': True,
    }

    # Google OAuth
    GOOGLE_CLIENT_ID     = os.getenv('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
    GOOGLE_REDIRECT_URI  = os.getenv('GOOGLE_REDIRECT_URI', 'http://127.0.0.1:5000/auth/google/callback')

    # LINE OAuth
    LINE_CHANNEL_ID      = os.getenv('LINE_CHANNEL_ID')
    LINE_CHANNEL_SECRET  = os.getenv('LINE_CHANNEL_SECRET')
    LINE_REDIRECT_URI    = os.getenv('LINE_REDIRECT_URI', 'http://127.0.0.1:5000/auth/line/callback')

    # Facebook OAuth
    FB_APP_ID            = os.getenv('FB_APP_ID')
    FB_APP_SECRET        = os.getenv('FB_APP_SECRET')
    FB_REDIRECT_URI      = os.getenv('FB_REDIRECT_URI', 'http://127.0.0.1:5000/auth/facebook/callback')

    # ใช้เข้ารหัส token สำหรับลิงก์ลืมรหัสผ่าน (ใช้ SECRET_KEY เป็นค่า default ก็ได้)
    SECURITY_PASSWORD_SALT = os.getenv('SECURITY_PASSWORD_SALT', 'password-reset-salt')

    # ตั้งค่าอีเมลสำหรับส่งลิงก์ลืมรหัสผ่าน (ถ้าไม่ตั้งค่า ระบบจะแสดงลิงก์ให้บนหน้าเว็บแทนการส่งอีเมลจริง)
    MAIL_SERVER   = os.getenv('MAIL_SERVER')
    MAIL_PORT     = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS  = os.getenv('MAIL_USE_TLS', 'true').lower() == 'true'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_SENDER   = os.getenv('MAIL_SENDER', MAIL_USERNAME)
