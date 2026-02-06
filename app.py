import streamlit as st
from fpdf import FPDF
import os

# ข้อมูลวิชา (140 นก. เป๊ะตามที่คุยกัน)
all_courses = {
    "หมวดวิชา RAM (30 นก.)": {
        "RAM1103": 3, "RAM1111": 3, "RAM1112": 3, "RAM1132": 3, 
        "RAM1141": 3, "RAM1204": 3, "RAM1213": 3, "RAM1301": 3, 
        "RAM1302": 3, "RAM1312": 3
    },
    "หมวดวิชา LAW (92 นก.)": {
        "LAW1101": 2, "LAW1102": 2, "LAW1103": 3, "LAW1106": 3,
        "LAW2101": 3, "LAW2102": 3, "LAW2103": 2, "LAW2104": 3,
        "LAW2105": 2, "LAW2106": 3, "LAW2107": 2, "LAW2108": 2,
        "LAW2109": 2, "LAW2110": 2, "LAW2111": 2, "LAW2112": 2,
        "LAW2113": 2, "LAW3101": 2, "LAW3102": 2, "LAW3103": 2,
        "LAW3104": 2, "LAW3105": 3, "LAW3106": 3, "LAW3107": 2,
        "LAW3108": 2, "LAW3109": 2, "LAW3110": 2, "LAW3111": 2,
        "LAW3112": 3, "LAW3117": 2, "LAW4101": 2, "LAW4102": 2,
        "LAW4103": 3, "LAW4104": 2, "LAW4105": 2, "LAW4106": 3,
        "LAW4107": 2, "LAW4108": 2, "LAW4109": 2, "LAW4110": 2
    },
    "หมวดวิชาเลือก (18 นก.)": {
        "เลือก 1": 3, "เลือก 2": 3, "กม.เลือก 1": 3,
        "กม.เลือก 2": 3, "กม.เลือก 3": 3, "กม.เลือก 4": 3
    }
}

grade_map = {"A": 4.0, "B+": 3.5, "B": 3.0, "C+": 2.5, "C": 2.0, "D+": 1.5, "D": 1.0, "F": 0.0}

st.set_page_config(page_title="GPA Law Compact", layout="wide") # ใช้หน้ากว้าง
st.title("⚖️ คำนวณเกรดนิติศาสตร์ (Compact UI)")

if "selected" not in st.session_state:
    st.session_state.selected = {}

# --- ส่วนเลือกวิชา (แสดงผลแบบ Grid 4 คอลัมน์เพื่อความไว) ---
for cat, courses in all_courses.items():
    with st.expander(f"📂 {cat}", expanded=(cat=="หมวดวิชา RAM (30 นก.)")):
        cols = st.columns(4)
        for i, (name, credit) in enumerate(courses.items()):
            with cols[i % 4]:
                if st.checkbox(f"{name}", key=f"chk_{name}"):
                    st.session_state.selected[name] = credit
                else:
                    st.session_state.selected.pop(name, None)

# --- ส่วนกรอกเกรด (ปรับให้กระชับที่สุด) ---
if st.session_state.selected:
    st.markdown("---")
    st.subheader("📝 ระบุเกรดวิชาที่เลือก")
    
    selected_sorted = dict(sorted(st.session_state.selected.items()))
    items = list(selected_sorted.items())
    
    total_creds, total_score = 0, 0
    pdf_list = []

    # แสดงผล 3 ชุดต่อ 1 แถว
    rows = (len(items) + 2) // 3
    for r in range(rows):
        cols = st.columns(3) # แบ่งเป็น 3 คอลัมน์ใหญ่
        for c in range(3):
            idx = r * 3 + c
            if idx < len(items):
                name, credit = items[idx]
                with cols[c]:
                    # ในแต่ละวิชา แบ่งย่อยเป็น [ชื่อวิชา, ช่องเกรด] ให้ชิดกัน
                    c1, c2 = st.columns([2, 1])
                    c1.markdown(f"**{name}** ({credit})")
                    g_letter = c2.selectbox("Grade", list(grade_map.keys()), key=f"grd_{name}", label_visibility="collapsed")
                    
                    total_creds += credit
                    total_score += grade_map[g_letter] * credit
                    pdf_list.append([name, str(credit), g_letter])

    if total_creds > 0:
        gpa = total_score / total_creds
        st.info(f"### GPA: {gpa:.2f} | รวม {total_creds} หน่วยกิต")

        # ปุ่ม PDF
        if st.button("🖨️ พิมพ์ PDF"):
            if os.path.exists("THSarabunNew.ttf"):
                pdf = FPDF()
                pdf.add_page()
                pdf.add_font("THSarabun", "", "THSarabunNew.ttf")
                pdf.set_font("THSarabun", "", 24)
                pdf.cell(0, 15, "สรุปผลการเรียนนิติศาสตร์", ln=True, align='C')
                
                pdf.set_font("THSarabun", "", 14)
                # หัวตาราง PDF
                pdf.cell(60, 10, "รหัสวิชา", 1); pdf.cell(60, 10, "หน่วยกิต", 1); pdf.cell(60, 10, "เกรด", 1, ln=True)
                
                for item in pdf_list:
                    pdf.cell(60, 10, f" {item[0]}", 1)
                    pdf.cell(60, 10, f" {item[1]}", 1)
                    pdf.cell(60, 10, f" {item[2]}", 1, ln=True)
                
                pdf.ln(5)
                pdf.set_font("THSarabun", "", 18)
                pdf.cell(0, 10, f"หน่วยกิตรวม: {total_creds}  |  GPA: {gpa:.2f}", ln=True)
                st.download_button("📥 โหลดไฟล์ PDF", data=pdf.output(), file_name="GPA_Compact.pdf")
            else:
                st.error("ไม่พบไฟล์ฟอนต์ THSarabunNew.ttf")
