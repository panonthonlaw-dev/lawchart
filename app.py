import streamlit as st
import os
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pypdf import PdfReader, PdfWriter
import io
import textwrap

# --- 1. ฟังก์ชันสนับสนุน (Utility Functions) ---

def to_thai_num(text):
    """แปลงตัวเลขเป็นเลขไทย"""
    thai_digits = "๐๑๒๓๔๕๖๗๘๙"
    arabic_digits = "0123456789"
    translation_table = str.maketrans(arabic_digits, thai_digits)
    return str(text).translate(translation_table)

def draw_party_details(can, data, start_y):
    """วาดรายละเอียดที่อยู่และข้อมูลส่วนตัวแยกตามช่องใน PDF [cite: 19-32, 33-46]"""
    # บรรทัดที่ 1: เลขประจำตัวประชาชน และ เชื้อชาติ
    can.drawString(185, start_y, to_thai_num(data['id']))
    can.drawString(510, start_y, data['race'])
    
    # บรรทัดที่ 2: สัญชาติ, อาชีพ, อายุ, บ้านเลขที่, หมู่ที่
    y2 = start_y - 26
    can.drawString(100, y2, data['nat'])
    can.drawString(250, y2, data['job'])
    can.drawString(455, y2, to_thai_num(data['age']))
    can.drawString(530, y2, to_thai_num(data['h_no']))
    can.drawString(585, y2, to_thai_num(data['moo']))
    
    # บรรทัดที่ 3: ถนน, ตรอก/ซอย, ตำบล/แขวง, อำเภอ/เขต
    y3 = y2 - 26
    can.drawString(100, y3, data['road'])
    can.drawString(250, y3, data['soi'])
    can.drawString(400, y3, data['sub_d'])
    can.drawString(530, y3, data['dist'])
    
    # บรรทัดที่ 4: จังหวัด, รหัสไปรษณีย์, โทรศัพท์
    y4 = y3 - 26
    can.drawString(100, y4, data['prov'])
    can.drawString(380, y4, to_thai_num(data['post']))
    can.drawString(485, y4, to_thai_num(data['tel']))

def create_pdf_overlay(data):
    """สร้างข้อมูลเลเยอร์เพื่อวางทับแบบพิมพ์ (๔)"""
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=(595.27, 841.89))
    try:
        pdfmetrics.registerFont(TTFont('ThaiFont', 'THSarabunNew.ttf'))
        can.setFont('ThaiFont', 15)
    except:
        return None

    # วางข้อมูลส่วนหัว [cite: 2, 3, 7-10]
    can.drawString(445, 764, to_thai_num(data['black_num']))
    can.drawString(360, 706, data['court'])
    can.drawString(308, 680, to_thai_num(data['day']))
    can.drawString(365, 680, data['month'])
    can.drawString(495, 680, to_thai_num(data['year']))
    can.drawString(340, 652, data['case_type'])

    # วางข้อมูลคู่ความและทุนทรัพย์ [cite: 5, 6, 11-14]
    can.drawString(250, 595, data['plaintiff']['name'])
    can.drawString(250, 550, data['defendant']['name'])
    can.drawString(250, 518, data['charge'])
    can.drawString(250, 492, to_thai_num(data['capital_baht']))
    can.drawString(510, 492, to_thai_num(data['capital_stang']))

    # รายละเอียดโจทก์ (ข้าพเจ้า...) [cite: 15-32]
    can.drawString(245, 466, data['plaintiff']['name'])
    draw_party_details(can, data['plaintiff'], 440) 

    # รายละเอียดจำเลย (ขอยื่นฟ้อง...) [cite: 18, 33-46]
    can.drawString(245, 258, data['defendant']['name'])
    draw_party_details(can, data['defendant'], 232)

    # เนื้อหาคำฟ้อง ข้อ ๑ [cite: 48]
    text_object = can.beginText(135, 145)
    text_object.setFont('ThaiFont', 15)
    lines = textwrap.wrap(data['body'], width=80)
    for line in lines:
        text_object.textLine(to_thai_num(line))
    can.drawText(text_object)

    can.save()
    packet.seek(0)
    return packet

def person_form(label):
    """สร้างฟอร์มกรอกรายละเอียดบุคคลแบบแยกช่อง [cite: 19-32, 33-46]"""
    st.markdown(f"#### ข้อมูล{label}")
    name = st.text_input(f"ชื่อ-นามสกุล {label}")
    id_card = st.text_input(f"เลขบัตรประชาชน {label}")
    c1, c2, c3, c4 = st.columns(4)
    race, nat, job, age = c1.text_input(f"เชื้อชาติ {label}"), c2.text_input(f"สัญชาติ {label}"), c3.text_input(f"อาชีพ {label}"), c4.text_input(f"อายุ {label}")
    c5, c6, c7, c8 = st.columns(4)
    h_no, moo, road, soi = c5.text_input(f"บ้านเลขที่ {label}"), c6.text_input(f"หมู่ {label}"), c7.text_input(f"ถนน {label}"), c8.text_input(f"ซอย {label}")
    c9, c10, c11, c12 = st.columns(4)
    sub_d, dist, prov, post = c9.text_input(f"แขวง {label}"), c10.text_input(f"เขต {label}"), c11.text_input(f"จังหวัด {label}"), c12.text_input(f"ไปรษณีย์ {label}")
    tel = st.text_input(f"เบอร์โทรศัพท์ {label}")
    return {"name": name, "id": id_card, "race": race, "nat": nat, "job": job, "age": age,
            "h_no": h_no, "moo": moo, "road": road, "soi": soi, "sub_d": sub_d,
            "dist": dist, "prov": prov, "post": post, "tel": tel}

# --- 2. หน้าจอหลัก (Main Interface) ---

st.set_page_config(page_title="ระบบร่างคำฟ้อง", layout="wide")
st.title("⚖️ ระบบร่างแบบพิมพ์คำฟ้อง (๔)")

# เช็กไฟล์ที่จำเป็นก่อนเริ่ม
if not os.path.exists("template.pdf") or not os.path.exists("THSarabunNew.ttf"):
    st.error("⚠️ ไม่พบไฟล์ template.pdf หรือ THSarabunNew.ttf ในระบบ")
    st.stop()

# สร้างฟอร์มกรอกข้อมูล
with st.form("court_form"):
    st.subheader("1. หัวคดีและทุนทรัพย์")
    ca, cb, cc = st.columns(3)
    court, black_num, case_type = ca.text_input("ศาล"), cb.text_input("เลขดำ"), cc.radio("ความ", ["แพ่ง", "อาญา"], horizontal=True)
    cd, ce, cf = st.columns(3)
    day, month, year = cd.text_input("วันที่"), ce.text_input("เดือน"), cf.text_input("พ.ศ.")
    charge = st.text_input("ข้อหาหรือฐานความผิด")
    cg, ch = st.columns(2)
    c_baht, c_stang = cg.text_input("ทุนทรัพย์ (บาท)"), ch.text_input("สตางค์", value="00")
    
    st.write("---")
    p_data = person_form("โจทก์")
    st.write("---")
    d_data = person_form("จำเลย")
    st.write("---")
    body = st.text_area("บรรยายฟ้อง ข้อ ๑", height=250)
    
    # ปุ่ม Submit (ต้องอยู่ในบล็อกฟอร์ม)
    submitted = st.form_submit_button("✅ ประมวลผลข้อมูล")

# ส่วนประมวลผลและปุ่มดาวน์โหลด (ต้องอยู่นอกบล็อกฟอร์ม)
if submitted:
    all_data = {
        'black_num': black_num, 'court': court, 'case_type': case_type,
        'day': day, 'month': month, 'year': year, 'charge': charge,
        'capital_baht': c_baht, 'capital_stang': c_stang,
        'plaintiff': p_data, 'defendant': d_data, 'body': body
    }
    try:
        overlay_packet = create_pdf_overlay(all_data)
        if overlay_packet:
            existing_pdf = PdfReader(open("template.pdf", "rb"))
            output = PdfWriter()
            page = existing_pdf.pages[0]
            page.merge_page(PdfReader(overlay_packet).pages[0])
            output.add_page(page)
            
            final_pdf = io.BytesIO()
            output.write(final_pdf)
            
            st.success(f"ประมวลผลคำฟ้องของ {p_data['name']} เรียบร้อยแล้ว")
            
            # ปุ่มดาวน์โหลดอยู่นอกฟอร์มแล้ว สามารถใช้งานได้ปกติ
            st.download_button(
                label="💾 คลิกเพื่อดาวน์โหลดไฟล์ PDF",
                data=final_pdf.getvalue(),
                file_name=f"คำฟ้อง_{p_data['name']}.pdf",
                mime="application/pdf"
            )
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาดทางเทคนิค: {e}")
