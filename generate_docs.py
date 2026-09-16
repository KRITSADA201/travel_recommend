import os
import sys

# Script to build Word document and PDF for Chapter 3
try:
    from docx import Document
    from docx.shared import Inches, Pt, RGBColor
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.enum.table import WD_TABLE_ALIGNMENT
    from docx.oxml import OxmlElement, parse_xml
    from docx.oxml.ns import nsdecls, qn
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "python-docx"])
    from docx import Document
    from docx.shared import Inches, Pt, RGBColor
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.enum.table import WD_TABLE_ALIGNMENT
    from docx.oxml import OxmlElement, parse_xml
    from docx.oxml.ns import nsdecls, qn

doc = Document()

# Set Margins (Top 1.5", Left 1.5", Bottom 1.0", Right 1.0" or Top 1", Left 1.5")
for section in doc.sections:
    section.top_margin = Inches(1.0)
    section.bottom_margin = Inches(1.0)
    section.left_margin = Inches(1.25)
    section.right_margin = Inches(1.0)

# Set Normal Style Font to TH Sarabun PSK or Sarabun
style = doc.styles['Normal']
font = style.font
font.name = 'TH Sarabun PSK'
font.size = Pt(16)
font.color.rgb = RGBColor(0, 0, 0)

def set_cell_background(cell, hex_color):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def add_heading_1(text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(text)
    run.font.name = 'TH Sarabun PSK'
    run.font.size = Pt(18)
    run.font.bold = True
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(6)
    return p

def add_heading_2(text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = p.add_run(text)
    run.font.name = 'TH Sarabun PSK'
    run.font.size = Pt(16)
    run.font.bold = True
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(4)
    return p

def add_heading_3(text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = p.add_run(text)
    run.font.name = 'TH Sarabun PSK'
    run.font.size = Pt(16)
    run.font.bold = True
    p.paragraph_format.left_indent = Inches(0.25)
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(2)
    return p

def add_body_p(text, indent=True):
    p = doc.add_paragraph()
    if indent:
        p.paragraph_format.first_line_indent = Inches(0.5)
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(4)
    run = p.add_run(text)
    run.font.name = 'TH Sarabun PSK'
    run.font.size = Pt(16)
    return p

def add_bullet(text):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.left_indent = Inches(0.5)
    p.paragraph_format.space_after = Pt(2)
    run = p.add_run(text)
    run.font.name = 'TH Sarabun PSK'
    run.font.size = Pt(16)
    return p

def add_table_custom(headers, rows, col_widths=None):
    tbl = doc.add_table(rows=len(rows)+1, cols=len(headers))
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    # Headers
    hdr_cells = tbl.rows[0].cells
    for i, title in enumerate(headers):
        hdr_cells[i].text = title
        set_cell_background(hdr_cells[i], "E2E8F0")
        set_cell_margins(hdr_cells[i], top=120, bottom=120, left=150, right=150)
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs:
            r.font.name = 'TH Sarabun PSK'
            r.font.size = Pt(15)
            r.font.bold = True
            
    # Rows
    for r_idx, row_data in enumerate(rows):
        row_cells = tbl.rows[r_idx+1].cells
        for c_idx, cell_value in enumerate(row_data):
            row_cells[c_idx].text = str(cell_value)
            set_cell_margins(row_cells[c_idx], top=100, bottom=100, left=150, right=150)
            if r_idx % 2 == 1:
                set_cell_background(row_cells[c_idx], "F8FAFC")
            p = row_cells[c_idx].paragraphs[0]
            for r in p.runs:
                r.font.name = 'TH Sarabun PSK'
                r.font.size = Pt(15)
                
    if col_widths:
        for row in tbl.rows:
            for i, w in enumerate(col_widths):
                row.cells[i].width = Inches(w)
                
    doc.add_paragraph().paragraph_format.space_after = Pt(6)
    return tbl

# --- DOCUMENT CONTENT GENERATION ---
add_heading_1("บทที่ 3")
add_heading_1("การวิเคราะห์และออกแบบระบบ")

add_body_p("การจัดทำโครงงาน \"ระบบแนะนำสถานที่ท่องเที่ยวตามความสนใจของผู้ใช้ กรณีศึกษาจังหวัดอุบลราชธานี\" เป็นการวิจัยและพัฒนาเว็บแอปพลิเคชันเพื่อช่วยในการค้นหา แนะนำ และจัดการข้อมูลสถานที่ท่องเที่ยว ที่พัก คาเฟ่ และร้านอาหารในจังหวัดอุบลราชธานี เพื่ออำนวยความสะดวกให้นักท่องเที่ยวสามารถเข้าถึงข้อมูล พิกัดแผนที่ ระบบนำทาง และรีวิวได้อย่างรวดเร็วและตรงตามความสนใจ")

add_body_p("การวิเคราะห์และออกแบบระบบในโครงงานนี้ใช้วิธีการวิเคราะห์และออกแบบระบบเชิงวัตถุ (Object-Oriented Analysis and Design: OOAD) โดยนำแผนภาพต่าง ๆ ตามมาตรฐาน Unified Modeling Language (UML) มาใช้ในการอธิบายองค์ประกอบและขั้นตอนการทำงานของระบบก่อนนำไปพัฒนาจริง โดยมีรายละเอียดดังต่อไปนี้")

add_heading_2("3.1 การวิเคราะห์ความต้องการของระบบ (Requirements Analysis)")
add_heading_3("3.1.1 ความต้องการเชิงหน้าที่ (Functional Requirements)")
add_bullet("ระบบสมาชิก: สามารถสมัครสมาชิก เข้าสู่ระบบผ่าน Username/Password หรือ Google OAuth และจัดการข้อมูลส่วนตัวได้")
add_bullet("ระบบค้นหาและแนะนำ: ค้นหาสถานที่ตามหมวดหมู่ความสนใจ (ธรรมชาติ, วัด, คาเฟ่, ที่พัก) และจัดอันดับด้วย Multi-Tier Ranking Algorithm")
add_bullet("ระบบแผนที่และนำทาง: แสดงพิกัดบน Google Maps, คำนวณระยะทางจาก GPS และเปิดระบบนำทางแบบเรียลไทม์ได้")
add_bullet("ระบบสถานที่โปรด: สมาชิกสามารถบันทึกและจัดการรายการสถานที่โปรด (Favorites) ได้")
add_bullet("ระบบรีวิวและให้คะแนน: สมาชิกสามารถให้คะแนนดาว 1-5 ดาว แสดงความคิดเห็น และตอบกลับรีวิวได้")
add_bullet("ระบบจัดการสถานที่: เพิ่ม แก้ไข ลบข้อมูลสถานที่และพิกัด พร้อมระบบแปลงรูปภาพ Google Drive อัตโนมัติ")
add_bullet("ระบบสำหรับผู้ดูแลระบบ: แดชบอร์ดสถิติ จัดการหมวดหมู่ และลบผู้ใช้งานที่ไม่เหมาะสมออกจากระบบ")

add_heading_3("3.1.2 ความต้องการที่ไม่ใช่เชิงหน้าที่ (Non-Functional Requirements)")
add_bullet("ความปลอดภัย (Security): รหัสผ่านถูกเข้ารหัสด้วย Bcrypt และมีระบบ Session Protection ป้องกันการเข้าถึงโดยไม่ได้รับอนุญาต")
add_bullet("การรองรับอุปกรณ์ (Responsiveness): รองรับการใช้งานทั้งบนคอมพิวเตอร์ แท็บเล็ต และสมาร์ทโฟน (Responsive Web Design)")
add_bullet("การเชื่อมต่อฐานข้อมูล: รองรับทั้ง SQLite สำหรับการพัฒนา และ PostgreSQL สำหรับการใช้งานจริงบนคลาวด์")

add_heading_2("3.2 แผนภาพยูสเคส (Use Case Diagram)")
add_body_p("Use Case Diagram แสดงปฏิสัมพันธ์ระหว่างผู้ใช้งานระบบ 2 กลุ่ม ได้แก่ ผู้ใช้งานทั่วไป/สมาชิก (User) และผู้ดูแลระบบ (Admin) กับฟังก์ชันการทำงานหลักของระบบ")

# Add Use Case Descriptions
add_heading_2("3.3 คำอธิบายยูสเคส (Use Case Descriptions)")

# Table 3.1
p_t1 = doc.add_paragraph()
r_t1 = p_t1.add_run("ตารางที่ 3.1 แสดงรายละเอียด Use Case: สมัครสมาชิก (Register)")
r_t1.bold = True
add_table_custom(
    ["หัวข้อ", "รายละเอียด"],
    [
        ["Use Case Name:", "สมัครสมาชิก (Register)"],
        ["Actors:", "ผู้ใช้งานทั่วไป (Guest)"],
        ["Description:", "ผู้ใช้กรอกข้อมูลส่วนตัวเพื่อสร้างบัญชีผู้ใช้งานใหม่สำหรับเข้าสู่ระบบ"],
        ["Precondition:", "ผู้ใช้ยังไม่ได้เข้าสู่ระบบ และระบบเชื่อมต่อฐานข้อมูลได้สมบูรณ์"],
        ["Postcondition:", "ระบบบันทึกข้อมูลสมาชิกใหม่ลงฐานข้อมูล และสามารถเข้าสู่ระบบได้"],
        ["Trigger:", "ผู้ใช้กดปุ่ม \"สมัครสมาชิก\" บนหน้าเว็บไซต์"],
        ["Main Flow:", "1. ผู้ใช้เข้าสู่หน้าสมัครสมาชิก\n2. กรอก Username, Email, Phone และ Password\n3. ระบบตรวจสอบความถูกต้องของข้อมูล\n4. เข้ารหัสผ่านด้วย Bcrypt และบันทึกลงฐานข้อมูล\n5. เปลี่ยนเส้นทางไปยังหน้าเข้าสู่ระบบ"],
        ["Alternative Flow:", "a. หากกรอกข้อมูลไม่ครบ ระบบแจ้งเตือนให้กรอกข้อมูลให้ครบถ้วน\nb. หากชื่อผู้ใช้หรืออีเมลซ้ำ ระบบแจ้งเตือนให้เปลี่ยนข้อมูลใหม่"],
        ["Exception:", "ไม่สามารถเชื่อมต่อฐานข้อมูลได้"],
        ["Special Requirement:", "รหัสผ่านต้องถูกเข้ารหัสด้วย Bcrypt ก่อนบันทึกเสมอ"]
    ],
    [1.8, 4.7]
)

# Table 3.2
p_t2 = doc.add_paragraph()
r_t2 = p_t2.add_run("ตารางที่ 3.2 แสดงรายละเอียด Use Case: เข้าสู่ระบบ (Login)")
r_t2.bold = True
add_table_custom(
    ["หัวข้อ", "รายละเอียด"],
    [
        ["Use Case Name:", "เข้าสู่ระบบ (Login)"],
        ["Actors:", "สมาชิก (User) / ผู้ดูแลระบบ (Admin)"],
        ["Description:", "ยืนยันตัวตนเพื่อเข้าถึงสิทธิ์การใช้งานของระบบ"],
        ["Precondition:", "ผู้ใช้มีบัญชีที่ลงทะเบียนในระบบเรียบร้อยแล้ว"],
        ["Postcondition:", "ระบบสร้าง Session สำหรับผู้ใช้งาน และนำเข้าสู่หน้าหลัก"],
        ["Trigger:", "ผู้ใช้กดปุ่ม \"เข้าสู่ระบบ\" บนหน้าเว็บไซต์"],
        ["Main Flow:", "1. เปิดหน้าเข้าสู่ระบบ\n2. กรอก Username/Email และ Password หรือเลือก Login ผ่าน Google\n3. ระบบตรวจสอบความถูกต้องกับฐานข้อมูล\n4. สร้าง Session และเปลี่ยนเส้นทางไปยังหน้าหลัก"],
        ["Alternative Flow:", "หากรหัสผ่านไม่ถูกต้อง ระบบแจ้งเตือน \"รหัสผ่านไม่ถูกต้อง\""],
        ["Exception:", "การเชื่อมต่อฐานข้อมูลขัดข้อง"],
        ["Special Requirement:", "ใช้ Flask-Login ในการรักษาความปลอดภัยของ Session"]
    ],
    [1.8, 4.7]
)

# Table 3.3
p_t3 = doc.add_paragraph()
r_t3 = p_t3.add_run("ตารางที่ 3.3 แสดงรายละเอียด Use Case: ค้นหาและแนะนำสถานที่ตามความสนใจ")
r_t3.bold = True
add_table_custom(
    ["หัวข้อ", "รายละเอียด"],
    [
        ["Use Case Name:", "ค้นหาและแนะนำสถานที่ตามความสนใจ (Search & Recommendation)"],
        ["Actors:", "ผู้ใช้ทั่วไป (Guest) / สมาชิก (User)"],
        ["Description:", "ค้นหาหรือเลือกดูสถานที่ท่องเที่ยวในจังหวัดอุบลราชธานีตามหมวดหมู่ความสนใจ"],
        ["Precondition:", "มีข้อมูลสถานที่ท่องเที่ยวและหมวดหมู่ในฐานข้อมูล"],
        ["Postcondition:", "ระบบแสดงผลรายการสถานที่ท่องเที่ยวที่ตรงตามเงื่อนไขและจัดอันดับความนิยม"],
        ["Trigger:", "ผู้ใช้พิมพ์คำค้นหา หรือคลิกเลือกหมวดหมู่ความสนใจบนหน้าเว็บ"],
        ["Main Flow:", "1. ผู้ใช้เลือกหมวดหมู่ความสนใจ (ธรรมชาติ, วัด, คาเฟ่, ที่พัก) หรือพิมพ์ค้นหา\n2. ระบบประมวลผลด้วย Multi-Tier Ranking Algorithm\n3. ระบบแสดงผลการ์ดสถานที่ท่องเที่ยวพร้อมคะแนนดาวและรูปภาพ"],
        ["Alternative Flow:", "หากไม่พบข้อมูล ระบบแสดงข้อความ \"ไม่พบสถานที่ท่องเที่ยวที่ตรงกับเงื่อนไข\""],
        ["Exception:", "ฐานข้อมูลไม่สามารถเชื่อมต่อได้"],
        ["Special Requirement:", "คำนวณคะแนนเฉลี่ยดาวแบบ Dynamic Real-time"]
    ],
    [1.8, 4.7]
)

# Table 3.4
p_t4 = doc.add_paragraph()
r_t4 = p_t4.add_run("ตารางที่ 3.4 แสดงรายละเอียด Use Case: แนะนำสถานที่ใกล้เคียงและระบบนำทาง Google Maps")
r_t4.bold = True
add_table_custom(
    ["หัวข้อ", "รายละเอียด"],
    [
        ["Use Case Name:", "แนะนำสถานที่ใกล้เคียงและระบบนำทาง (Nearby & Navigation)"],
        ["Actors:", "ผู้ใช้ทั่วไป / สมาชิก"],
        ["Description:", "แสดงแผนที่พิกัดจริง คำนวณระยะทางจาก GPS แนะนำสถานที่และที่พักใกล้เคียง และเปิดนำทาง"],
        ["Precondition:", "สถานที่ท่องเที่ยวมีข้อมูลพิกัด Latitude และ Longitude บันทึกไว้"],
        ["Postcondition:", "ระบบแสดงแผนที่ Google Maps และสามารถส่งพิกัดไปยังแอปพลิเคชันนำทางได้"],
        ["Trigger:", "ผู้ใช้เปิดดูหน้ารายละเอียดสถานที่ หรือคลิกปุ่ม \"เปิดนำทาง\""],
        ["Main Flow:", "1. ระบบดึงพิกัด GPS ผู้ใช้และคำนวณระยะทางด้วย Haversine Formula\n2. แสดงแผนที่ Google Maps Official Embed และการ์ดสถานที่ใกล้เคียง\n3. เมื่อกดปุ่ม \"เปิดนำทาง\" ระบบจะเปิดแอป Google Maps นำทางทันที"],
        ["Alternative Flow:", "หากไม่มี GPS ระบบจะใช้พิกัดของสถานที่นั้นเป็นจุดอ้างอิงอัตโนมัติ (Fallback)"],
        ["Exception:", "ไม่พบพิกัดละติจูดหรือลองจิจูดของสถานที่"],
        ["Special Requirement:", "ใช้ Google Maps Official Embed แสดงผลแผนที่แบบเรียลไทม์"]
    ],
    [1.8, 4.7]
)

# Table 3.5
p_t5 = doc.add_paragraph()
r_t5 = p_t5.add_run("ตารางที่ 3.5 แสดงรายละเอียด Use Case: เขียนรีวิวและให้คะแนนดาว (Review & Rating)")
r_t5.bold = True
add_table_custom(
    ["หัวข้อ", "รายละเอียด"],
    [
        ["Use Case Name:", "เขียนรีวิวและให้คะแนนดาว (Review & Rating)"],
        ["Actors:", "สมาชิก (User) / ผู้ดูแลระบบ (Admin)"],
        ["Description:", "สมาชิกสามารถแสดงความคิดเห็น ให้คะแนน 1-5 ดาว และตอบกลับรีวิวได้"],
        ["Precondition:", "ผู้ใช้ต้องเข้าสู่ระบบเรียบร้อยแล้ว"],
        ["Postcondition:", "ระบบบันทึกรีวิว และคำนวณคะแนนดาวเฉลี่ยของสถานที่ใหม่ทันที"],
        ["Trigger:", "ผู้ใช้เลือกคะแนนดาว พิมพ์ข้อความ แล้วกดปุ่ม \"ส่งรีวิว\""],
        ["Main Flow:", "1. ผู้ใช้เข้าสู่หน้ารายละเอียดสถานที่\n2. เลือกคะแนนดาว (1-5 ดาว) และพิมพ์ความคิดเห็น\n3. กดปุ่ม \"ส่งรีวิว\"\n4. ระบบบันทึกข้อมูลและอัปเดตคะแนนเฉลี่ยดาวทันที"],
        ["Alternative Flow:", "ผู้ใช้และ Admin สามารถกดปุ่ม \"ตอบกลับ\" ใต้รีวิวเพื่อตอบโต้ได้"],
        ["Exception:", "ไม่ได้เลือกคะแนนดาว ระบบจะแจ้งเตือนให้ระบุคะแนนก่อนส่ง"],
        ["Special Requirement:", "คะแนนรีวิวมีผลต่อการจัดอันดับความนิยมในหน้าแรกโดยตรง"]
    ],
    [1.8, 4.7]
)

# Table 3.6
p_t6 = doc.add_paragraph()
r_t6 = p_t6.add_run("ตารางที่ 3.6 แสดงรายละเอียด Use Case: จัดการระบบสำหรับผู้ดูแลระบบ (Admin Dashboard)")
r_t6.bold = True
add_table_custom(
    ["หัวข้อ", "รายละเอียด"],
    [
        ["Use Case Name:", "จัดการระบบสำหรับผู้ดูแลระบบ (Admin Dashboard & User Deletion)"],
        ["Actors:", "ผู้ดูแลระบบ (Admin)"],
        ["Description:", "ดูสถิติภาพรวม จัดการหมวดหมู่ และลบผู้ใช้งานที่ไม่เหมาะสมออกจากระบบ"],
        ["Precondition:", "ผู้ใช้เข้าสู่ระบบด้วยสิทธิ์ผู้ดูแลระบบ (is_admin = True)"],
        ["Postcondition:", "ข้อมูลหมวดหมู่หรือผู้ใช้งานถูกปรับปรุงในฐานข้อมูล"],
        ["Trigger:", "ผู้ดูแลระบบเข้าสู่หน้า \"Admin Dashboard\" (/admin)"],
        ["Main Flow:", "1. แอดมินเข้าสู่หน้า Dashboard ดูจำนวนผู้ใช้ สถานที่ และหมวดหมู่\n2. เพิ่ม/ลบ หมวดหมู่ความสนใจ\n3. คลิกปุ่ม \"ลบ\" ผู้ใช้ที่ทำผิดกฎ พร้อมยืนยันผ่าน Modal\n4. ระบบลบรีวิว/รายการโปรด และโอนย้ายสถานที่ของ User นั้นให้ Admin"],
        ["Alternative Flow:", "ระบบไม่อนุญาตให้แอดมินลบบัญชีของตนเองเพื่อความปลอดภัย"],
        ["Exception:", "ผู้ใช้ทั่วไปพยายามเข้าถึง ระบบจะแจ้ง 403 Forbidden"],
        ["Special Requirement:", "Role-Based Access Control ตรวจสอบสิทธิ์ทุกคำขอ"]
    ],
    [1.8, 4.7]
)

# Data Dictionary
add_heading_2("3.4 พจนานุกรมข้อมูล (Data Dictionary)")
add_body_p("ฐานข้อมูลของระบบพัฒนาด้วยสถาปัตยกรรมเชิงสัมพันธ์ (Relational Database) ประกอบด้วย 7 ตารางหลัก ดังนี้")

# User Table
p_d1 = doc.add_paragraph()
r_d1 = p_d1.add_run("ตารางที่ 3.7 พจนานุกรมข้อมูล: ตารางผู้ใช้งาน (User)")
r_d1.bold = True
add_table_custom(
    ["ชื่อคอลัมน์", "ชนิดข้อมูล", "ขนาด", "คีย์", "คุณสมบัติ", "รายละเอียด"],
    [
        ["id", "Integer", "-", "PK", "Not Null, Auto Inc", "รหัสประจำตัวผู้ใช้งาน"],
        ["username", "String", "100", "Unique", "Not Null", "ชื่อผู้ใช้งานสำหรับเข้าสู่ระบบ"],
        ["password", "String", "200", "-", "Not Null", "รหัสผ่านที่เข้ารหัสแฮชด้วย Bcrypt"],
        ["email", "String", "200", "Unique", "Nullable", "ที่อยู่อีเมลของผู้ใช้งาน"],
        ["phone", "String", "20", "Unique", "Nullable", "เบอร์โทรศัพท์ติดต่อ"],
        ["is_admin", "Boolean", "-", "-", "Default = False", "สถานะแอดมิน (True/False)"]
    ],
    [1.1, 1.0, 0.7, 0.6, 1.4, 1.7]
)

# Category Table
p_d2 = doc.add_paragraph()
r_d2 = p_d2.add_run("ตารางที่ 3.8 พจนานุกรมข้อมูล: ตารางหมวดหมู่ความสนใจ (Category)")
r_d2.bold = True
add_table_custom(
    ["ชื่อคอลัมน์", "ชนิดข้อมูล", "ขนาด", "คีย์", "คุณสมบัติ", "รายละเอียด"],
    [
        ["id", "Integer", "-", "PK", "Not Null, Auto Inc", "รหัสหมวดหมู่ความสนใจ"],
        ["name", "String", "100", "-", "Not Null", "ชื่อหมวดหมู่ (ธรรมชาติ, วัด, คาเฟ่, ที่พัก)"]
    ],
    [1.5, 1.2, 0.8, 0.8, 1.0, 1.2]
)

# Place Table
p_d3 = doc.add_paragraph()
r_d3 = p_d3.add_run("ตารางที่ 3.9 พจนานุกรมข้อมูล: ตารางสถานที่ท่องเที่ยว (Place)")
r_d3.bold = True
add_table_custom(
    ["ชื่อคอลัมน์", "ชนิดข้อมูล", "ขนาด", "คีย์", "คุณสมบัติ", "รายละเอียด"],
    [
        ["id", "Integer", "-", "PK", "Not Null, Auto Inc", "รหัสสถานที่ท่องเที่ยว"],
        ["name", "String", "200", "-", "Not Null", "ชื่อสถานที่ท่องเที่ยว/ที่พัก"],
        ["detail", "Text", "-", "-", "Not Null", "รายละเอียดและจุดเด่นของสถานที่"],
        ["location", "String", "200", "-", "Not Null", "ที่ตั้ง / อำเภอ / จังหวัดอุบลราชธานี"],
        ["latitude", "Float", "-", "-", "Nullable", "พิกัดละติจูด (Google Maps)"],
        ["longitude", "Float", "-", "-", "Nullable", "พิกัดลองจิจูด (Google Maps)"],
        ["user_id", "Integer", "-", "FK", "Nullable", "รหัสผู้สร้าง (อ้างอิง user.id)"],
        ["category_id", "Integer", "-", "FK", "Nullable", "รหัสหมวดหมู่ (อ้างอิง category.id)"]
    ],
    [1.1, 1.0, 0.7, 0.6, 1.4, 1.7]
)

# PlaceImage Table
p_d4 = doc.add_paragraph()
r_d4 = p_d4.add_run("ตารางที่ 3.10 พจนานุกรมข้อมูล: ตารางรูปภาพสถานที่ (PlaceImage)")
r_d4.bold = True
add_table_custom(
    ["ชื่อคอลัมน์", "ชนิดข้อมูล", "ขนาด", "คีย์", "คุณสมบัติ", "รายละเอียด"],
    [
        ["id", "Integer", "-", "PK", "Not Null, Auto Inc", "รหัสรูปภาพ"],
        ["url", "String", "500", "-", "Not Null", "URL รูปภาพ หรือ Google Drive"],
        ["caption", "String", "200", "-", "Nullable", "คำบรรยายภาพ"],
        ["order", "Integer", "-", "-", "Default = 0", "ลำดับการแสดงผลของรูปภาพ"],
        ["place_id", "Integer", "-", "FK", "Not Null", "รหัสสถานที่ (อ้างอิง place.id)"]
    ],
    [1.1, 1.0, 0.7, 0.6, 1.4, 1.7]
)

# Review Table
p_d5 = doc.add_paragraph()
r_d5 = p_d5.add_run("ตารางที่ 3.11 พจนานุกรมข้อมูล: ตารางรีวิวและคะแนนดาว (Review)")
r_d5.bold = True
add_table_custom(
    ["ชื่อคอลัมน์", "ชนิดข้อมูล", "ขนาด", "คีย์", "คุณสมบัติ", "รายละเอียด"],
    [
        ["id", "Integer", "-", "PK", "Not Null, Auto Inc", "รหัสรีวิว"],
        ["comment", "Text", "-", "-", "Not Null", "ข้อความความคิดเห็น"],
        ["rating", "Integer", "-", "-", "Not Null", "คะแนนดาว (1-5 ดาว)"],
        ["user_id", "Integer", "-", "FK", "Not Null", "รหัสผู้รีวิว (อ้างอิง user.id)"],
        ["place_id", "Integer", "-", "FK", "Not Null", "รหัสสถานที่ (อ้างอิง place.id)"]
    ],
    [1.1, 1.0, 0.7, 0.6, 1.4, 1.7]
)

# ReviewReply Table
p_d6 = doc.add_paragraph()
r_d6 = p_d6.add_run("ตารางที่ 3.12 พจนานุกรมข้อมูล: ตารางตอบกลับรีวิว (ReviewReply)")
r_d6.bold = True
add_table_custom(
    ["ชื่อคอลัมน์", "ชนิดข้อมูล", "ขนาด", "คีย์", "คุณสมบัติ", "รายละเอียด"],
    [
        ["id", "Integer", "-", "PK", "Not Null, Auto Inc", "รหัสการตอบกลับความคิดเห็น"],
        ["content", "Text", "-", "-", "Not Null", "ข้อความตอบกลับรีวิว"],
        ["review_id", "Integer", "-", "FK", "Not Null", "รหัสรีวิวหลัก (อ้างอิง review.id)"],
        ["user_id", "Integer", "-", "FK", "Not Null", "รหัสผู้ตอบกลับ (อ้างอิง user.id)"]
    ],
    [1.1, 1.0, 0.7, 0.6, 1.4, 1.7]
)

# Favorite Table
p_d7 = doc.add_paragraph()
r_d7 = p_d7.add_run("ตารางที่ 3.13 พจนานุกรมข้อมูล: ตารางสถานที่โปรด (Favorite)")
r_d7.bold = True
add_table_custom(
    ["ชื่อคอลัมน์", "ชนิดข้อมูล", "ขนาด", "คีย์", "คุณสมบัติ", "รายละเอียด"],
    [
        ["id", "Integer", "-", "PK", "Not Null, Auto Inc", "รหัสรายการโปรด"],
        ["user_id", "Integer", "-", "FK", "Not Null", "รหัสผู้ใช้งาน (อ้างอิง user.id)"],
        ["place_id", "Integer", "-", "FK", "Not Null", "รหัสสถานที่ (อ้างอิง place.id)"]
    ],
    [1.1, 1.0, 0.7, 0.6, 1.4, 1.7]
)

output_docx = r"c:\Users\KRITSADA\Downloads\Pro 1\travel_recommend\บทที่_3_การวิเคราะห์และออกแบบระบบ_อุบลราชธานี.docx"
doc.save(output_docx)
print(f"DOCX created at: {output_docx}")
