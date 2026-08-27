import os
import subprocess
import sys

# HTML Template with Academic Book / Thesis Styling and Thai Sarabun font
html_content = """<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <title>บทที่ 3 การวิเคราะห์และออกแบบระบบ (System Analysis and Design)</title>
    <link href="https://fonts.googleapis.com/css2?family=Sarabun:wght@300;400;500;600;700;800&family=Fira+Code:wght@400;600&display=swap" rel="stylesheet">
    <style>
        @page {
            size: A4;
            margin: 2.5cm 2.0cm 2.0cm 2.5cm;
            @bottom-right {
                content: counter(page);
                font-family: 'Sarabun', sans-serif;
                font-size: 11pt;
            }
        }

        body {
            font-family: 'Sarabun', sans-serif;
            font-size: 13pt;
            line-height: 1.6;
            color: #111827;
            background-color: #ffffff;
            margin: 0;
            padding: 20px;
        }

        @media print {
            body { padding: 0; }
            .no-print { display: none; }
            .page-break { page-break-before: always; }
        }

        .cover {
            text-align: center;
            padding: 60px 20px 40px 20px;
            border-bottom: 2px solid #2563eb;
            margin-bottom: 30px;
        }

        .cover h1 {
            font-size: 24pt;
            font-weight: 800;
            color: #1e3a8a;
            margin-bottom: 10px;
        }

        .cover h2 {
            font-size: 17pt;
            font-weight: 600;
            color: #4b5563;
            margin-bottom: 25px;
        }

        .cover .meta {
            font-size: 12pt;
            color: #6b7280;
            line-height: 1.8;
        }

        h2.section-title {
            font-size: 16pt;
            font-weight: 700;
            color: #1e40af;
            border-bottom: 2px solid #e5e7eb;
            padding-bottom: 6px;
            margin-top: 35px;
            margin-bottom: 15px;
        }

        h3.sub-title {
            font-size: 14pt;
            font-weight: 600;
            color: #1f2937;
            margin-top: 25px;
            margin-bottom: 10px;
        }

        h4 {
            font-size: 13pt;
            font-weight: 600;
            color: #374151;
            margin-top: 18px;
            margin-bottom: 8px;
        }

        p {
            margin-bottom: 12px;
            text-align: justify;
            text-indent: 1.25cm;
        }

        p.no-indent {
            text-indent: 0;
        }

        ul, ol {
            margin-top: 6px;
            margin-bottom: 14px;
            padding-left: 30px;
        }

        li {
            margin-bottom: 6px;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin: 18px 0;
            font-size: 11pt;
        }

        table, th, td {
            border: 1px solid #cbd5e1;
        }

        th {
            background-color: #f1f5f9;
            color: #0f172a;
            font-weight: 700;
            text-align: center;
            padding: 8px 10px;
        }

        td {
            padding: 7px 10px;
            vertical-align: top;
        }

        tr:nth-child(even) {
            background-color: #f8fafc;
        }

        .code-box {
            background-color: #f8fafc;
            border: 1px solid #e2e8f0;
            border-left: 4px solid #2563eb;
            padding: 12px 16px;
            border-radius: 6px;
            font-family: 'Fira Code', monospace;
            font-size: 10pt;
            line-height: 1.5;
            margin: 14px 0;
            overflow-x: auto;
            white-space: pre-wrap;
        }

        .formula-card {
            background: #eff6ff;
            border: 1px solid #bfdbfe;
            border-radius: 8px;
            padding: 14px 18px;
            margin: 16px 0;
            text-align: center;
            font-size: 12pt;
        }

        .diagram-box {
            background: #ffffff;
            border: 1px solid #d1d5db;
            border-radius: 8px;
            padding: 14px;
            margin: 18px 0;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }

        .diagram-box pre {
            font-family: 'Fira Code', monospace;
            font-size: 9.5pt;
            line-height: 1.4;
            color: #1e293b;
            margin: 0;
        }

        .badge {
            display: inline-block;
            padding: 2px 8px;
            font-size: 9.5pt;
            font-weight: 600;
            border-radius: 10px;
            background: #e0f2fe;
            color: #0369a1;
        }

        .caption {
            text-align: center;
            font-size: 11pt;
            color: #4b5563;
            margin-top: 6px;
            margin-bottom: 16px;
            font-style: italic;
        }
    </style>
</head>
<body>

    <!-- ปกหัวข้อบท -->
    <div class="cover">
        <h1>บทที่ 3</h1>
        <h2>การวิเคราะห์และออกแบบระบบ (System Analysis and Design)</h2>
        <div class="meta">
            <strong>โครงงาน:</strong> ระบบแนะนำสถานที่ท่องเที่ยวอัจฉริยะ (Travel Recommend System)<br>
            <strong>สถาปัตยกรรม:</strong> Model-View-Controller (Flask Modular Architecture & PostgreSQL/SQLite)
        </div>
    </div>

    <!-- 3.1 ภาพรวม -->
    <h2 class="section-title">3.1 ภาพรวมของระบบ (System Overview)</h2>
    <p>
        ระบบแนะนำสถานที่ท่องเที่ยว (Travel Recommend System) ได้รับการพัฒนาขึ้นโดยมีเป้าหมายเพื่อเป็นศูนย์กลางข้อมูลการท่องเที่ยวที่มีความทันสมัย ใช้งานสะดวก และมีประสิทธิภาพสูง รองรับทั้งการค้นหาสถานที่ท่องเที่ยว แนะนำสถานที่ใกล้เคียงด้วยพิกัดภูมิศาสตร์ (GPS) คำนวณระยะทางด้วยสูตร Haversine แนะนำที่พักและร้านอาหารรอบข้าง การจัดเก็บรายการโปรดส่วนตัวแบบไร้รอยต่อ และระบบชุมชนตอบโต้แสดงความคิดเห็นสไตล์ YouTube (Interactive Threaded Comments & Replies) ที่ช่วยให้ผู้ดูแลระบบ (Admin) และผู้ใช้งานทั่วไปสามารถแลกเปลี่ยนข้อมูลและรีวิวกันได้อย่างอิสระ
    </p>

    <!-- 3.2 ความต้องการของระบบ -->
    <h2 class="section-title">3.2 การวิเคราะห์ความต้องการของระบบ (Requirements Analysis)</h2>
    <p>การวิเคราะห์ความต้องการของระบบแบ่งออกเป็น 2 ส่วนหลัก ได้แก่ ความต้องการเชิงหน้าที่ และความต้องการที่ไม่ใช่เชิงหน้าที่ ดังนี้:</p>

    <h3 class="sub-title">3.2.1 ความต้องการเชิงหน้าที่ (Functional Requirements: FR)</h3>
    <table>
        <thead>
            <tr>
                <th style="width: 15%;">รหัส</th>
                <th style="width: 35%;">ฟังก์ชันการทำงาน</th>
                <th style="width: 50%;">คำอธิบายรายละเอียด</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td style="text-align:center;"><strong>FR-01</strong></td>
                <td>ระบบจัดการสมาชิกและการยืนยันตัวตน</td>
                <td>รองรับการสมัครสมาชิก เข้าสู่ระบบ ลืมรหัสผ่าน รีเซ็ตรหัสผ่าน และการเข้าสู่ระบบผ่าน Google OAuth และ Facebook Login</td>
            </tr>
            <tr>
                <td style="text-align:center;"><strong>FR-02</strong></td>
                <td>ระบบสืบค้นและคัดกรองสถานที่</td>
                <td>ค้นหาสถานที่ตามชื่อ คำอธิบาย ตำแหน่งที่ตั้ง และตัวกรองแยกตามหมวดหมู่ (ธรรมชาติ, คาเฟ่, วัด ฯลฯ)</td>
            </tr>
            <tr>
                <td style="text-align:center;"><strong>FR-03</strong></td>
                <td>ระบบพิกัดแผนที่และการนำทาง</td>
                <td>แสดงผลแผนที่แบบโต้ตอบ (Leaflet & OpenStreetMap) ปักหมุดสถานที่จริง และเชื่อมต่อระบบนำทางผ่าน Google Maps API</td>
            </tr>
            <tr>
                <td style="text-align:center;"><strong>FR-04</strong></td>
                <td>ระบบแนะนำสถานที่ใกล้เคียง</td>
                <td>คำนวณระยะทางจากพิกัด GPS ปัจจุบันของผู้ใช้ไปยังสถานที่ต่าง ๆ ในหมวดเดียวกันด้วยสูตร Haversine ภายในรัศมี 100 กม.</td>
            </tr>
            <tr>
                <td style="text-align:center;"><strong>FR-05</strong></td>
                <td>ระบบแนะนำที่พักและร้านอาหารรอบข้าง</td>
                <td>ค้นหาโรงแรมและร้านอาหารในรัศมีรอบสถานที่ท่องเที่ยวผ่าน Overpass API พร้อมบอกระยะห่างและตำแหน่งพิกัด</td>
            </tr>
            <tr>
                <td style="text-align:center;"><strong>FR-06</strong></td>
                <td>ระบบบันทึกรายการโปรด (AJAX Favorites)</td>
                <td>ผู้ใช้งานสามารถกดบันทึกหรือยกเลิกสถานที่โปรดได้ทันทีแบบ In-place ไม่มีการรีโหลดหน้าเว็บและไม่เลื่อนหน้าจอ</td>
            </tr>
            <tr>
                <td style="text-align:center;"><strong>FR-07</strong></td>
                <td>ระบบความคิดเห็นและการตอบกลับสไตล์ YouTube</td>
                <td>ผู้ใช้และ Admin สามารถให้คะแนน (1-5 ดาว) เขียนรีวิว และพิมพ์ตอบกลับข้อความในเธรดการสนทนาได้แบบ Real-time In-place</td>
            </tr>
            <tr>
                <td style="text-align:center;"><strong>FR-08</strong></td>
                <td>ระบบแกลเลอรีรูปภาพและ Image Proxy</td>
                <td>รองรับรูปภาพหลายรูปต่อหนึ่งสถานที่ พร้อมแปลงลิงก์ Google Drive อัตโนมัติและส่งผ่าน Image Proxy เพื่อเลี่ยงปัญหา Referer Block</td>
            </tr>
            <tr>
                <td style="text-align:center;"><strong>FR-09</strong></td>
                <td>ระบบจัดการข้อมูลสำหรับผู้ดูแลระบบ (Admin)</td>
                <td>Admin สามารถเพิ่ม ลบ แก้ไขข้อมูลสถานที่ จัดการหมวดหมู่ ตรวจสอบบัญชีผู้ใช้ และดูแลความคิดเห็นทั้งหมดได้</td>
            </tr>
            <tr>
                <td style="text-align:center;"><strong>FR-10</strong></td>
                <td>ระบบจัดการโปรไฟล์ผู้ใช้งาน</td>
                <td>สมาชิกสามารถดูประวัติการบันทึกรายการโปรด รีวิวที่เคยเขียน และแก้ไขข้อมูลส่วนตัวได้</td>
            </tr>
        </tbody>
    </table>

    <h3 class="sub-title">3.2.2 ความต้องการที่ไม่ใช่เชิงหน้าที่ (Non-Functional Requirements: NFR)</h3>
    <table>
        <thead>
            <tr>
                <th style="width: 15%;">รหัส</th>
                <th style="width: 30%;">คุณสมบัติ</th>
                <th style="width: 55%;">เกณฑ์มาตรฐานและการออกแบบ</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td style="text-align:center;"><strong>NFR-01</strong></td>
                <td>การตอบสนองบนทุกหน้าจอ (Mobile Responsiveness)</td>
                <td>รองรับการแสดงผลอย่างสมบูรณ์บนสมาร์ทโฟน แท็บเล็ต และคอมพิวเตอร์ (Bootstrap 5 Responsive Grid & Media Queries)</td>
            </tr>
            <tr>
                <td style="text-align:center;"><strong>NFR-02</strong></td>
                <td>ความปลอดภัยของข้อมูล (Security)</td>
                <td>การเข้ารหัสรหัสผ่านด้วย Bcrypt Hashing, ป้องกัน CSRF/XSS, การคุ้มครองเซสชันด้วย Flask-Login และ Role-based Access Control</td>
            </tr>
            <tr>
                <td style="text-align:center;"><strong>NFR-03</strong></td>
                <td>ประสิทธิภาพความเร็ว (Performance)</td>
                <td>การส่งข้อมูลส่วนติดต่อผู้ใช้ด้วย AJAX Fetch API (JSON Data Transfer) ช่วยลดการโหลดซ้ำของหน้าเว็บและประหยัด Bandwidth</td>
            </tr>
            <tr>
                <td style="text-align:center;"><strong>NFR-04</strong></td>
                <td>ความเข้ากันได้ของฐานข้อมูล (Portability)</td>
                <td>ใช้ SQLAlchemy ORM รองรับทั้ง SQLite สำหรับการพัฒนาในเครื่อง (Local Dev) และ PostgreSQL สำหรับระบบจริง (Production)</td>
            </tr>
            <tr>
                <td style="text-align:center;"><strong>NFR-05</strong></td>
                <td>ความพร้อมใช้งาน (Availability & Resilience)</td>
                <td>มีระบบสำรองพิกัดแผนที่ (OSM Tile Fallback) และระบบดึงภาพสำรองเมื่อเกิดข้อผิดพลาดของเครือข่ายภายนอก</td>
            </tr>
        </tbody>
    </table>

    <div class="page-break"></div>

    <!-- 3.3 Use Case Analysis -->
    <h2 class="section-title">3.3 การวิเคราะห์การทำงานของระบบ (Use Case Analysis)</h2>
    <p>
        ผู้ใช้งานระบบแบ่งออกเป็น 3 กลุ่มบทบาท (Actors) ได้แก่:
    </p>
    <ul>
        <li><strong>1. ผู้ใช้งานทั่วไป (Guest / General User):</strong> ผู้ที่ยังไม่ได้เข้าสู่ระบบ สามารถค้นหาสถานที่ ดูรายละเอียด ดูแผนที่ และค้นหาโรงแรมใกล้เคียงได้</li>
        <li><strong>2. สมาชิก (Member):</strong> ผู้ใช้งานที่ผ่านการเข้าสู่ระบบ สามารถบันทึกรายการโปรด เขียนรีวิว ให้คะแนน และพิมพ์ตอบกลับความคิดเห็นได้</li>
        <li><strong>3. ผู้ดูแลระบบ (Admin):</strong> ผู้ดูแลที่มีสิทธิ์พิเศษ สามารถจัดการสถานที่ จัดการหมวดหมู่ ลบรีวิวที่ไม่เหมาะสม และตรวจสอบสถิติระบบได้</li>
    </ul>

    <div class="diagram-box">
        <pre>
                               +---------------------------------------------------+
                               |        Travel Recommend System (Use Case)         |
                               +---------------------------------------------------+
                               |                                                   |
      +------------------+     |  (UC-01: ค้นหาและดูรายละเอียดสถานที่)                |
      |                  |---->|  (UC-02: ดูพิกัดบนแผนที่และนำทาง)                 |
      |  Guest (ทั่วไป)  |---->|  (UC-03: ค้นหาโรงแรมและร้านอาหารใกล้เคียง)          |
      |                  |---->|  (UC-04: เข้าสู่ระบบ / สมัครสมาชิก / Social Login)  |
      +------------------+     |                                                   |
               ^               |                                                   |
               | (extends)     |                                                   |
      +------------------+     |  (UC-05: บันทึก / ลบสถานที่โปรด - In-place)       |
      |                  |---->|  (UC-06: เขียนรีวิว ให้คะแนน 1-5 ดาว)              |
      |  Member (สมาชิก) |---->|  (UC-07: พิมพ์ตอบกลับความคิดเห็นแบบ YouTube)       |
      |                  |---->|  (UC-08: จัดการโปรไฟล์ส่วนตัว)                     |
      +------------------+     |                                                   |
               ^               |                                                   |
               | (extends)     |                                                   |
      +------------------+     |  (UC-09: เพิ่ม / แก้ไข / ลบ สถานที่ท่องเที่ยว)      |
      |  Admin (ผู้ดูแล) |---->|  (UC-10: จัดการหมวดหมู่สถานที่)                     |
      |                  |---->|  (UC-11: ดู Dashboard สถิติและจัดการรีวิวทั้งหมด)    |
      +------------------+     |                                                   |
                               +---------------------------------------------------+
        </pre>
    </div>
    <div class="caption">รูปที่ 3.1 Use Case Diagram แสดงความสัมพันธ์ระหว่าง Actors และฟังก์ชันการทำงานของระบบ</div>

    <div class="page-break"></div>

    <!-- 3.4 Activity Diagrams -->
    <h2 class="section-title">3.4 แผนภาพแสดงลำดับขั้นตอนการทำงาน (Activity Diagrams)</h2>

    <h3 class="sub-title">3.4.1 แผนภาพการทำงาน: การค้นหาและแนะนำสถานที่ใกล้เคียง (Haversine Recommendation)</h3>
    <div class="diagram-box">
        <pre>
   [User เข้าสู่หน้าสถานที่]
              |
              v
   [ร้องขอพิกัด GPS อุปกรณ์] ------------(ปฏิเสธ/ไม่มี GPS)---------> [แสดงเฉพาะข้อมูลสถานที่]
              | (อนุญาต)                                                       |
              v                                                                |
   [รับค่า Latitude, Longitude ปัจจุบัน]                                        |
              |                                                                |
              v                                                                |
   [ดึงรายการสถานที่ในหมวดหมู่เดียวกันทั้งหมด]                                      |
              |                                                                |
              v                                                                |
   [คำนวณระยะทางด้วยสูตร Haversine (กม.)]                                       |
              |                                                                |
              v                                                                |
   [คัดกรองระยะทาง <= 100 กม. และเรียงลำดับจากน้อยไปมาก]                           |
              |                                                                |
              v                                                                |
   [ส่งข้อมูล JSON ผ่าน AJAX /places/api/nearby]                                |
              |                                                                |
              +--------------------------+-------------------------------------+
                                         |
                                         v
                      [แสดงผลสถานที่และระยะทางบนหน้าจอ]
        </pre>
    </div>
    <div class="caption">รูปที่ 3.2 Activity Diagram การคำนวณและแนะนำสถานที่ใกล้เคียงด้วยพิกัดภูมิศาสตร์</div>

    <h3 class="sub-title">3.4.2 แผนภาพการทำงาน: การแสดงความคิดเห็นและตอบกลับแบบ YouTube (Interactive Comments)</h3>
    <div class="diagram-box">
        <pre>
   [User พิมพ์ความคิดเห็น / คะแนน หรือ ข้อความตอบกลับ]
                          |
                          v
               [กดปุ่มส่งความคิดเห็น / ตอบกลับ]
                          |
                          v
         [JavaScript ดักจับ Event (preventDefault)]
                          |
                          v
      [ส่งคำขอแบบ Asynchronous Fetch API (JSON Header)]
                          |
                          v
           [Backend ตรวจสอบ Session และความถูกต้องของข้อมูล]
                          |
             +------------+------------+
             |                         |
         (ถูกต้อง)                 (ไม่ถูกต้อง)
             |                         |
             v                         v
     [บันทึกเข้า Review /      [ส่งสถานะ Error JSON]
       ReviewReply Model]              |
             |                         v
             v             [แจ้งเตือนข้อผิดพลาดบนหน้าจอ]
  [ส่งข้อมูลชุดใหม่กลับเป็น JSON]
             |
             v
 [DOM แทรกความคิดเห็น/ข้อความตอบกลับทันที]
             |
             v
 [เคลียร์ฟอร์ม พร้อมรับคอมเมนต์ใหม่ โดยไม่เลื่อน Scroll หน้าจอ]
        </pre>
    </div>
    <div class="caption">รูปที่ 3.3 Activity Diagram กระบวนการแสดงความคิดเห็นและตอบกลับแบบ Seamless AJAX</div>

    <div class="page-break"></div>

    <!-- 3.5 Sequence Diagrams -->
    <h2 class="section-title">3.5 แผนภาพแสดงลำดับเวลาและปฏิสัมพันธ์ (Sequence Diagrams)</h2>

    <h3 class="sub-title">3.5.1 Sequence Diagram: ระบบกดบันทึกรายการโปรด (AJAX Favorite Toggle)</h3>
    <div class="diagram-box">
        <pre>
  User Browser                places Blueprint (Flask)          SQLAlchemy / DB
       |                               |                              |
       |--- 1. คลิกปุ่มหัวใจ (Fav) --->|                              |
       |    [Fetch: /favorite/<id>]    |                              |
       |                               |--- 2. Query Favorite Check ->|
       |                               |<-- 3. คืนผลลัพธ์ว่ามีอยู่หรือไม่---|
       |                               |                              |
       |                               |--- 4. Insert หรือ Delete --->|
       |                               |<-- 5. Commit สำเร็จ ---------|
       |                               |                              |
       |<-- 6. ส่ง JSON Response ------|                              |
       |    {success:true, is_fav:true}|                              |
       |                               |                              |
       |--- 7. สลับไอคอน bi-heart-fill  |                              |
       |       โดยไม่เกิด Page Reload   |                              |
        </pre>
    </div>
    <div class="caption">รูปที่ 3.4 Sequence Diagram การทำงานของระบบรายการโปรดแบบ Seamless AJAX</div>

    <h3 class="sub-title">3.5.2 Sequence Diagram: ระบบตอบกลับความคิดเห็น (YouTube-Style Reply)</h3>
    <div class="diagram-box">
        <pre>
  User / Admin Browser         places Blueprint               Database (ReviewReply)
       |                               |                              |
       |--- 1. พิมพ์ข้อความตอบกลับ ---->|                              |
       |    [POST: /review/<id>/reply] |                              |
       |                               |--- 2. ตรวจสอบ Role & ID ---->|
       |                               |--- 3. บันทึก ReviewReply --->|
       |                               |<-- 4. ยืนยันการบันทึก --------|
       |                               |                              |
       |<-- 5. คืนข้อมูล Reply JSON ---|                              |
       |    {id, content, username,    |                              |
       |     is_admin, replies_count}  |                              |
       |                               |                              |
       |--- 6. DOM แทรกกล่องตอบกลับใหม่ |                              |
       |       อัปเดตปุ่ม '▼ การตอบกลับ'|                              |
       |       Scroll ไม่ขยับเด้งขึ้นบน |                              |
        </pre>
    </div>
    <div class="caption">รูปที่ 3.5 Sequence Diagram การส่งและแสดงผลข้อความตอบกลับแบบ In-place</div>

    <div class="page-break"></div>

    <!-- 3.6 Database Design -->
    <h2 class="section-title">3.6 การออกแบบฐานข้อมูล (Database Design)</h2>
    <p>
        โครงสร้างฐานข้อมูลได้รับการออกแบบตามหลักบรรทัดฐาน (Normalization) เพื่อลดความซ้ำซ้อนของข้อมูล และสร้างความสัมพันธ์เชิงโครงสร้างแบบ Relational Database ดังนี้:
    </p>

    <h3 class="sub-title">3.6.1 แผนภาพความสัมพันธ์ของข้อมูล (Entity-Relationship Diagram: ERD)</h3>
    <div class="diagram-box">
        <pre>
    +------------------+         1:N         +--------------------+
    |       USER       |-------------------->|       PLACE        |
    +------------------+                     +--------------------+
    | *id (PK)         |                     | *id (PK)           |
    |  username        |         1:N         |  name              |
    |  password        |--------+            |  detail            |
    |  email           |        |            |  location          |
    |  phone           |        |            |  latitude          |
    |  is_admin        |        |            |  longitude         |
    +------------------+        |            |  category_id (FK)  |
       | 1             | 1      |            |  user_id (FK)      |
       |               |        |            +--------------------+
       | 1:N           | 1:N    |               | 1        | 1
       v               v        |               |          |
    +----------+ +-----------+  | 1:N           | 1:N      | 1:N
    | FAVORITE | |  REVIEW   |<-+               v          v
    +----------+ +-----------+            +------------+ +-------------+
    | *id (PK) | | *id (PK)  |            | PLACE_IMAGE| |  CATEGORY   |
    |  user_id | |  comment  |            +------------+ +-------------+
    |  place_id| |  rating   |            | *id (PK)   | | *id (PK)    |
    +----------+ |  user_id  |            |  url       | |  name       |
                 |  place_id |            |  caption   | +-------------+
                 +-----------+            |  order     |
                       | 1                |  place_id  |
                       | 1:N              +------------+
                       v
                 +--------------+
                 | REVIEW_REPLY |
                 +--------------+
                 | *id (PK)     |
                 |  content     |
                 |  review_id   |
                 |  user_id     |
                 +--------------+
        </pre>
    </div>
    <div class="caption">รูปที่ 3.6 Entity-Relationship Diagram (ERD) ของระบบ Travel Recommend</div>

    <div class="page-break"></div>

    <h3 class="sub-title">3.6.2 พจนานุกรมข้อมูล (Data Dictionary)</h3>

    <h4>1. ตาราง user (ข้อมูลผู้ใช้งานระบบ)</h4>
    <table>
        <thead>
            <tr>
                <th style="width: 20%;">ชื่อฟิลด์</th>
                <th style="width: 20%;">ชนิดข้อมูล</th>
                <th style="width: 15%;">คีย์</th>
                <th style="width: 15%;">ค่าว่าง (Null)</th>
                <th style="width: 30%;">คำอธิบาย</th>
            </tr>
        </thead>
        <tbody>
            <tr><td>id</td><td>INTEGER</td><td>PK</td><td>No</td><td>รหัสประจำตัวผู้ใช้ (Auto Increment)</td></tr>
            <tr><td>username</td><td>VARCHAR(100)</td><td>Unique</td><td>No</td><td>ชื่อผู้ใช้งานสำหรับเข้าสู่ระบบ</td></tr>
            <tr><td>password</td><td>VARCHAR(200)</td><td>-</td><td>No</td><td>รหัสผ่านที่ผ่านการแฮชด้วย Bcrypt</td></tr>
            <tr><td>email</td><td>VARCHAR(200)</td><td>Unique</td><td>Yes</td><td>อีเมลผู้ใช้งาน</td></tr>
            <tr><td>phone</td><td>VARCHAR(20)</td><td>Unique</td><td>Yes</td><td>เบอร์โทรศัพท์ติดต่อ</td></tr>
            <tr><td>is_admin</td><td>BOOLEAN</td><td>-</td><td>No</td><td>สถานะผู้ดูแลระบบ (Default: False)</td></tr>
        </tbody>
    </table>

    <h4>2. ตาราง category (หมวดหมู่สถานที่ท่องเที่ยว)</h4>
    <table>
        <thead>
            <tr>
                <th style="width: 20%;">ชื่อฟิลด์</th>
                <th style="width: 20%;">ชนิดข้อมูล</th>
                <th style="width: 15%;">คีย์</th>
                <th style="width: 15%;">ค่าว่าง (Null)</th>
                <th style="width: 30%;">คำอธิบาย</th>
            </tr>
        </thead>
        <tbody>
            <tr><td>id</td><td>INTEGER</td><td>PK</td><td>No</td><td>รหัสหมวดหมู่ (Auto Increment)</td></tr>
            <tr><td>name</td><td>VARCHAR(100)</td><td>-</td><td>No</td><td>ชื่อหมวดหมู่ (เช่น ธรรมชาติ, คาเฟ่, วัด)</td></tr>
        </tbody>
    </table>

    <h4>3. ตาราง place (ข้อมูลสถานที่ท่องเที่ยว)</h4>
    <table>
        <thead>
            <tr>
                <th style="width: 20%;">ชื่อฟิลด์</th>
                <th style="width: 20%;">ชนิดข้อมูล</th>
                <th style="width: 15%;">คีย์</th>
                <th style="width: 15%;">ค่าว่าง (Null)</th>
                <th style="width: 30%;">คำอธิบาย</th>
            </tr>
        </thead>
        <tbody>
            <tr><td>id</td><td>INTEGER</td><td>PK</td><td>No</td><td>รหัสสถานที่ (Auto Increment)</td></tr>
            <tr><td>name</td><td>VARCHAR(200)</td><td>-</td><td>No</td><td>ชื่อสถานที่ท่องเที่ยว</td></tr>
            <tr><td>detail</td><td>TEXT</td><td>-</td><td>No</td><td>รายละเอียดและข้อมูลแนะนำ</td></tr>
            <tr><td>location</td><td>VARCHAR(200)</td><td>-</td><td>No</td><td>ที่อยู่ อำเภอ หรือจังหวัด</td></tr>
            <tr><td>latitude</td><td>FLOAT</td><td>-</td><td>Yes</td><td>พิกัดละติจูด (Latitude)</td></tr>
            <tr><td>longitude</td><td>FLOAT</td><td>-</td><td>Yes</td><td>พิกัดลองจิจูด (Longitude)</td></tr>
            <tr><td>user_id</td><td>INTEGER</td><td>FK (user.id)</td><td>Yes</td><td>รหัสผู้สร้างสถานที่</td></tr>
            <tr><td>category_id</td><td>INTEGER</td><td>FK (category.id)</td><td>Yes</td><td>รหัสหมวดหมู่สังกัด</td></tr>
        </tbody>
    </table>

    <h4>4. ตาราง place_image (รูปภาพของสถานที่)</h4>
    <table>
        <thead>
            <tr>
                <th style="width: 20%;">ชื่อฟิลด์</th>
                <th style="width: 20%;">ชนิดข้อมูล</th>
                <th style="width: 15%;">คีย์</th>
                <th style="width: 15%;">ค่าว่าง (Null)</th>
                <th style="width: 30%;">คำอธิบาย</th>
            </tr>
        </thead>
        <tbody>
            <tr><td>id</td><td>INTEGER</td><td>PK</td><td>No</td><td>รหัสรูปภาพ (Auto Increment)</td></tr>
            <tr><td>url</td><td>VARCHAR(500)</td><td>-</td><td>No</td><td>URL ลิงก์รูปภาพ หรือ Google Drive ID</td></tr>
            <tr><td>caption</td><td>VARCHAR(200)</td><td>-</td><td>Yes</td><td>คำบรรยายใต้ภาพ</td></tr>
            <tr><td>order</td><td>INTEGER</td><td>-</td><td>No</td><td>ลำดับการแสดงผลในแกลเลอรี</td></tr>
            <tr><td>place_id</td><td>INTEGER</td><td>FK (place.id)</td><td>No</td><td>รหัสสถานที่ที่เป็นเจ้าของภาพ</td></tr>
        </tbody>
    </table>

    <h4>5. ตาราง review (รีวิวและความคิดเห็น)</h4>
    <table>
        <thead>
            <tr>
                <th style="width: 20%;">ชื่อฟิลด์</th>
                <th style="width: 20%;">ชนิดข้อมูล</th>
                <th style="width: 15%;">คีย์</th>
                <th style="width: 15%;">ค่าว่าง (Null)</th>
                <th style="width: 30%;">คำอธิบาย</th>
            </tr>
        </thead>
        <tbody>
            <tr><td>id</td><td>INTEGER</td><td>PK</td><td>No</td><td>รหัสรีวิว (Auto Increment)</td></tr>
            <tr><td>comment</td><td>TEXT</td><td>-</td><td>No</td><td>ข้อความรีวิว / ความคิดเห็น</td></tr>
            <tr><td>rating</td><td>INTEGER</td><td>-</td><td>No</td><td>คะแนนประเมิน (1 ถึง 5 ดาว)</td></tr>
            <tr><td>user_id</td><td>INTEGER</td><td>FK (user.id)</td><td>No</td><td>รหัสผู้เขียนรีวิว</td></tr>
            <tr><td>place_id</td><td>INTEGER</td><td>FK (place.id)</td><td>No</td><td>รหัสสถานที่ที่ถูกรีวิว</td></tr>
        </tbody>
    </table>

    <h4>6. ตาราง review_reply (ข้อความตอบกลับรีวิว)</h4>
    <table>
        <thead>
            <tr>
                <th style="width: 20%;">ชื่อฟิลด์</th>
                <th style="width: 20%;">ชนิดข้อมูล</th>
                <th style="width: 15%;">คีย์</th>
                <th style="width: 15%;">ค่าว่าง (Null)</th>
                <th style="width: 30%;">คำอธิบาย</th>
            </tr>
        </thead>
        <tbody>
            <tr><td>id</td><td>INTEGER</td><td>PK</td><td>No</td><td>รหัสข้อความตอบกลับ (Auto Increment)</td></tr>
            <tr><td>content</td><td>TEXT</td><td>-</td><td>No</td><td>เนื้อหาข้อความตอบกลับ</td></tr>
            <tr><td>review_id</td><td>INTEGER</td><td>FK (review.id)</td><td>No</td><td>รหัสรีวิวต้นทางที่ถูกตอบกลับ</td></tr>
            <tr><td>user_id</td><td>INTEGER</td><td>FK (user.id)</td><td>No</td><td>รหัสผู้ตอบกลับ (Admin หรือ User)</td></tr>
        </tbody>
    </table>

    <h4>7. ตาราง favorite (รายการโปรดของผู้ใช้)</h4>
    <table>
        <thead>
            <tr>
                <th style="width: 20%;">ชื่อฟิลด์</th>
                <th style="width: 20%;">ชนิดข้อมูล</th>
                <th style="width: 15%;">คีย์</th>
                <th style="width: 15%;">ค่าว่าง (Null)</th>
                <th style="width: 30%;">คำอธิบาย</th>
            </tr>
        </thead>
        <tbody>
            <tr><td>id</td><td>INTEGER</td><td>PK</td><td>No</td><td>รหัสรายการโปรด (Auto Increment)</td></tr>
            <tr><td>user_id</td><td>INTEGER</td><td>FK (user.id)</td><td>No</td><td>รหัสผู้ใช้ที่กดบันทึกโปรด</td></tr>
            <tr><td>place_id</td><td>INTEGER</td><td>FK (place.id)</td><td>No</td><td>รหัสสถานที่ที่ถูกบันทึก</td></tr>
        </tbody>
    </table>

    <div class="page-break"></div>

    <!-- 3.7 System Architecture -->
    <h2 class="section-title">3.7 สถาปัตยกรรมระบบและการออกแบบเชิงโมดูล (System Architecture)</h2>
    <p>
        โครงสร้างของระบบพัฒนาด้วยรูปแบบ <strong>Model-View-Controller (MVC)</strong> โดยใช้ <strong>Flask Blueprints</strong> แยกหน้าที่การทำงานตามโดเมนอย่างชัดเจน:
    </p>

    <div class="code-box">
travel_recommend/
├── app.py                     # Application Factory, Extension Init & DB Auto-creation
├── config.py                  # Environment Configuration (Database URI, Secret Key)
├── extensions.py              # Extensions Singleton (SQLAlchemy, Bcrypt, LoginManager)
├── models.py                  # Database Models (User, Place, Category, PlaceImage, Review, ReviewReply, Favorite)
├── blueprints/
│   ├── auth.py                # ระบบล็อกอิน สมัครสมาชิก ลืมรหัสผ่าน รีเซ็ตรหัสผ่าน OAuth
│   ├── places.py              # แสดงสถานที่ ค้นหา แผนที่ แนะนำสถานที่ใกล้เคียง รีวิว และรายการโปรด
│   ├── admin_bp.py            # ส่วนจัดการระบบ Dashboard สถิติ และจัดการหมวดหมู่
│   └── user_bp.py             # หน้าโปรไฟล์ผู้ใช้และประวัติการทำกิจกรรม
└── templates/                 # Jinja2 Templates (Responsive Bootstrap 5 & Custom UI)
    ├── base.html              # โครงสร้างหลัก แถบ Navbar และ Modal ยืนยันการออกจากระบบ
    ├── places/                # detail.html, list.html, map.html, favorites.html, add.html, edit.html
    ├── auth/                  # login.html, register.html, forgot_password.html, reset_password.html
    └── admin/                 # dashboard.html
    </div>

    <!-- 3.8 Haversine Formula -->
    <h2 class="section-title">3.8 อัลกอริทึมการคำนวณระยะทางบนพิกัดทรงกลม (Haversine Formula)</h2>
    <p>
        ระบบใช้อัลกอริทึม <strong>Haversine Formula</strong> ในการคำนวณระยะห่างระหว่างพิกัดละติจูดและลองจิจูดของผู้ใช้งาน (User GPS) กับสถานที่ท่องเที่ยวแต่ละแห่ง โดยคำนวณตามความโค้งของผิวโลกจริง ซึ่งให้ผลลัพธ์ที่มีความแม่นยำสูง:
    </p>

    <div class="formula-card">
        <strong>สูตรคำนวณคณิตศาสตร์ (Mathematical Formula):</strong><br><br>
        \( a = \sin^2\left(\frac{\Delta\phi}{2}\right) + \cos(\phi_1) \cdot \cos(\phi_2) \cdot \sin^2\left(\frac{\Delta\lambda}{2}\right) \)<br><br>
        \( c = 2 \cdot \operatorname{atan2}\left(\sqrt{a}, \sqrt{1-a}\right) \)<br><br>
        \( d = R \cdot c \) &nbsp;&nbsp;&nbsp; <em>(โดยที่ \( R = 6,371 \) กิโลเมตร คือรัศมีเฉลี่ยของโลก)</em>
    </div>

    <div class="code-box">
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # รัศมีโลกเฉลี่ย (กิโลเมตร)
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * \
        math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c
    </div>

    <br>
    <hr style="border: 0; border-top: 1px solid #e2e8f0; margin-top: 30px;">
    <p class="no-indent" style="text-align: center; color: #6b7280; font-size: 11pt;">
        — จบบทที่ 3 การวิเคราะห์และออกแบบระบบ (System Analysis and Design) —
    </p>

</body>
</html>
"""

# Output Paths
output_dir = os.path.dirname(os.path.abspath(__file__))
html_file_path = os.path.join(output_dir, "บทที่_3_การวิเคราะห์และออกแบบระบบ.html")
pdf_file_path = os.path.join(output_dir, "บทที่_3_การวิเคราะห์และออกแบบระบบ.pdf")

# 1. Save HTML
with open(html_file_path, "w", encoding="utf-8") as f:
    f.write(html_content)
print(f"✅ สร้างไฟล์ HTML เรียบร้อยแล้ว: {html_file_path}")

# 2. Convert to PDF using Microsoft Edge headless
edge_paths = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Users\%USERNAME%\AppData\Local\Microsoft\Edge\Application\msedge.exe"
]

edge_exe = None
for p in edge_paths:
    expanded = os.path.expandvars(p)
    if os.path.exists(expanded):
        edge_exe = expanded
        break

pdf_generated = False
if edge_exe:
    cmd = [
        edge_exe,
        "--headless",
        "--disable-gpu",
        f"--print-to-pdf={pdf_file_path}",
        "--no-pdf-header-footer",
        html_file_path
    ]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if os.path.exists(pdf_file_path) and os.path.getsize(pdf_file_path) > 0:
            print(f"🎉 สร้างไฟล์ PDF เรียบร้อยแล้ว: {pdf_file_path} (ขนาด {os.path.getsize(pdf_file_path):,} ไบต์)")
            pdf_generated = True
        else:
            print("Edge conversion returned but PDF not created.")
    except Exception as e:
        print(f"Error converting with Edge: {e}")

if not pdf_generated:
    print("⚠️ คุณสามารถเปิดไฟล์ HTML ใน Browser และกด Ctrl + P -> บันทึกเป็น PDF ได้ทันทีครับ")
