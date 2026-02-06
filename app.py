import streamlit as st
from fpdf import FPDF
import os

# --- ข้อมูลวิชาที่คุณให้มา ---
all_courses = {
    "หมวดวิชา RAM": {
        "RAM1111": 3, "RAM1131": 3, "RAM1141": 3, "RAM1201": 3, 
        "RAM1112": 3, "RAM1301": 3, "RAM1302": 3, "RAM1311": 3
    },
    "หมวดวิชา LAW": {
        "LAW1101": 2, "LAW1102": 2, "LAW1103": 3, "LAW1106": 3,
        "LAW2101": 3, "LAW2102": 3, "LAW2103": 2, "LAW2104": 3,
        "LAW2105": 2, "LAW2106": 3, "LAW2107": 2, "LAW2108": 2,
        "LAW2109": 2, "LAW2110": 2, "LAW2111": 2, "LAW2112": 2,
        "LAW2113": 2, "LAW3101": 2, "LAW3102": 2, "LAW3103": 3,
        "LAW3104": 2, "LAW3105": 3, "LAW3106": 3, "LAW3112": 3,
        "LAW3107": 2, "LAW3108": 2, "LAW3109": 2, "LAW3110": 2,
        "LAW3111": 2, "LAW3117": 2, "LAW4101": 2, "LAW4102": 2,
        "LAW4103": 3, "LAW4104": 2, "LAW4105": 2, "LAW4106": 3,
        "LAW4107": 2, "LAW4108": 2, "LAW4109": 2, "LAW4110": 2
    },
    "หมวดวิชาเลือก": {
        "วิชาเลือก 1": 3, "วิชาเลือก 2": 3, "วิชาเลือกกฎหมาย 1": 3,
        "วิชาเลือกกฎหมาย 2": 3, "วิชาเลือกกฎหมาย 3": 3, "วิชาเลือกกฎหมาย 4": 3
    }
}

grade_map = {"A": 4.0, "B+": 3.5, "B": 3.0, "C+": 2.5, "C": 2.0, "D+": 1.5, "D": 1.0, "F": 0.0}

st.set_page_config(page_title="GPA Calculator", layout="centered")
st.title("⚖️ เครื่องมือคำนวณเกรดนิติศาสตร์")

if "selected" not in st.session_state:
    st.session_state.selected = {}

# ส่วนเลือกวิชา
for cat, courses in all_courses.items():
    with st.expander(cat):
        cols = st.columns(3)
        for i, (name, credit) in enumerate(courses.items()):
            with cols[i % 3]:
                if st.checkbox(f"{name} ({credit})", key=f"chk_{name}"):
                    st.session_state.selected[name] = credit
                else:
                    st.session_state.selected.pop(name, None)

# ส่วนกรอกเกรดและคำนวณ
if st.session_state.selected:
    st.header("📝 กรอกเกรดวิชาที่เลือก")
    total_creds = 0
    total_score = 0
    pdf_data = []

    for name, credit in st.session_state.selected.items():
        c1, c2 = st.columns([3, 1])
        c1.write(f"**{name}** ({credit} หน่วยกิต)")
        g_letter = c2.selectbox("เกรด", list(grade_map.keys()), key=f"grd_{name}")
        
        total_creds += credit
        total_score += grade_map[g_letter] * credit
        pdf_data.append([name, str(credit), g_letter])

    gpa = total_score / total_creds if total_creds > 0 else 0
    st.success(f"### GPA ของคุณคือ: {gpa:.2f}")

    # ปุ่มพิมพ์ PDF
    if st.button("🖨️ พิมพ์เป็น PDF"):
        font_path = "THSarabunNew.ttf"
        if os.path.exists(font_path):
            pdf = FPDF()
            pdf.add_page()
            pdf.add_font("THSarabun", "", font_path)
            pdf.set_font("THSarabun", "", 24)
            pdf.cell(0, 15, "รายงานผลการเรียน", ln=True, align='C')
            
            pdf.set_font("THSarabun", "", 16)
            for row in pdf_data:
                pdf.cell(100, 10, f"วิชา: {row[0]}")
                pdf.cell(40, 10, f"หน่วยกิต: {row[1]}")
                pdf.cell(40, 10, f"เกรด: {row[2]}", ln=True)
            
            pdf.ln(10)
            pdf.set_font("THSarabun", "", 20)
            pdf.cell(0, 10, f"เกรดเฉลี่ยสะสม: {gpa:.2f}", ln=True)
            
            pdf_bytes = pdf.output()
            st.download_button("📥 ดาวน์โหลดไฟล์ PDF", data=pdf_bytes, file_name="GPA.pdf", mime="application/pdf")
        else:
            st.error("ไม่พบไฟล์ THSarabunNew.ttf ใน Repo กรุณาอัปโหลดไฟล์ฟอนต์ก่อนครับ")
