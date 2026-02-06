import streamlit as st
from fpdf import FPDF
import os

# --- ข้อมูลวิชาทั้งหมด (อัปเดตตามที่คุณส่งมาล่าสุด) ---
all_courses = {
    "หมวดวิชา RAM": {
        "RAM1103": 3, "RAM1111": 3, "RAM1112": 3, "RAM1132": 3, 
        "RAM1141": 3, "RAM1204": 3, "RAM1213": 3, "RAM1301": 3, 
        "RAM1302": 3, "RAM1312": 3
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

st.set_page_config(page_title="GPA Law Calculator", layout="centered")
st.title("⚖️ ระบบคำนวณเกรดนิติศาสตร์")
st.write("ติ๊กเลือกวิชาที่สอบผ่านแล้วเพื่อคำนวณเกรด")

if "selected" not in st.session_state:
    st.session_state.selected = {}

# --- แสดงรายการวิชาให้เลือก ---
for cat, courses in all_courses.items():
    with st.expander(f"📂 {cat}"):
        cols = st.columns(3)
        for i, (name, credit) in enumerate(courses.items()):
            with cols[i % 3]:
                if st.checkbox(f"{name} ({credit})", key=f"chk_{name}"):
                    st.session_state.selected[name] = credit
                else:
                    st.session_state.selected.pop(name, None)

# --- ส่วนคำนวณผล ---
if st.session_state.selected:
    st.divider()
    st.subheader("📝 ระบุเกรด")
    
    total_creds = 0
    total_score = 0
    pdf_list = []

    # เรียงลำดับวิชาตามชื่อเพื่อให้ดูง่าย
    sorted_selected = dict(sorted(st.session_state.selected.items()))

    for name, credit in sorted_selected.items():
        c1, c2 = st.columns([3, 1])
        c1.write(f"**{name}** ({credit} หน่วยกิต)")
        g_letter = c2.selectbox("เลือกเกรด", list(grade_map.keys()), key=f"grd_{name}")
        
        total_creds += credit
        total_score += grade_map[g_letter] * credit
        pdf_list.append([name, str(credit), g_letter])

    if total_creds > 0:
        gpa = total_score / total_creds
        st.success(f"### GPA ของคุณคือ: {gpa:.2f}")
        st.info(f"จำนวนหน่วยกิตที่คำนวณ: {total_creds} หน่วยกิต")

        # --- ส่วน Export PDF ---
        if st.button("🖨️ พิมพ์ใบสรุปผล (PDF)"):
            font_path = "THSarabunNew.ttf"
            if os.path.exists(font_path):
                pdf = FPDF()
                pdf.add_page()
                pdf.add_font("THSarabun", "", font_path)
                pdf.set_font("THSarabun", "", 24)
                pdf.cell(0, 15, "สรุปผลการเรียนวิชากฎหมาย", ln=True, align='C')
                
                pdf.set_font("THSarabun", "", 16)
                pdf.ln(5)
                # หัวตาราง PDF
                pdf.cell(80, 10, "รหัสวิชา", border=1, align='C')
                pdf.cell(50, 10, "หน่วยกิต", border=1, align='C')
                pdf.cell(50, 10, "เกรด", border=1, align='C', ln=True)

                for item in pdf_list:
                    pdf.cell(80, 10, f" {item[0]}", border=1)
                    pdf.cell(50, 10, f"{item[1]}", border=1, align='C')
                    pdf.cell(50, 10, f"{item[2]}", border=1, align='C', ln=True)
                
                pdf.ln(10)
                pdf.set_font("THSarabun", "", 20)
                pdf.cell(0, 10, f"หน่วยกิตสะสมรวม: {total_creds}", ln=True)
                pdf.cell(0, 10, f"เกรดเฉลี่ย (GPA): {gpa:.2f}", ln=True)
                
                pdf_bytes = pdf.output()
                st.download_button("📥 ดาวน์โหลดไฟล์ PDF", data=pdf_bytes, file_name="GPA_Report.pdf", mime="application/pdf")
            else:
                st.error("กรุณาอัปโหลดไฟล์ THSarabunNew.ttf ไว้ใน Repo เพื่อพิมพ์ภาษาไทย")
else:
    st.info("เริ่มต้นโดยการเลือกวิชาจากเมนูด้านบน")
