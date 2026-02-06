import streamlit as st
from fpdf import FPDF
import os

# --- ข้อมูลวิชาฉบับปรับปรุง (140 หน่วยกิตพอดี) ---
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
        "LAW2113": 2, "LAW3101": 2, "LAW3102": 2, "LAW3103": 2, # ปรับเหลือ 2 แล้ว
        "LAW3104": 2, "LAW3105": 3, "LAW3106": 3, "LAW3107": 2,
        "LAW3108": 2, "LAW3109": 2, "LAW3110": 2, "LAW3111": 2,
        "LAW3112": 3, "LAW3117": 2, "LAW4101": 2, "LAW4102": 2,
        "LAW4103": 3, "LAW4104": 2, "LAW4105": 2, "LAW4106": 3,
        "LAW4107": 2, "LAW4108": 2, "LAW4109": 2, "LAW4110": 2
    },
    "หมวดวิชาเลือก (18 นก.)": {
        "วิชาเลือก 1": 3, "วิชาเลือก 2": 3, "วิชาเลือกกฎหมาย 1": 3,
        "วิชาเลือกกฎหมาย 2": 3, "วิชาเลือกกฎหมาย 3": 3, "วิชาเลือกกฎหมาย 4": 3
    }
}

grade_map = {"A": 4.0, "B+": 3.5, "B": 3.0, "C+": 2.5, "C": 2.0, "D+": 1.5, "D": 1.0, "F": 0.0}

st.set_page_config(page_title="GPA Law 140", layout="centered")
st.title("⚖️ ระบบคำนวณเกรดนิติศาสตร์ (140 นก.)")

if "selected" not in st.session_state:
    st.session_state.selected = {}

# ส่วนเลือกวิชา
for cat, courses in all_courses.items():
    with st.expander(f"📂 {cat}"):
        cols = st.columns(3)
        for i, (name, credit) in enumerate(courses.items()):
            with cols[i % 3]:
                if st.checkbox(f"{name} ({credit})", key=f"chk_{name}"):
                    st.session_state.selected[name] = credit
                else:
                    st.session_state.selected.pop(name, None)

# ส่วนคำนวณ
if st.session_state.selected:
    st.divider()
    total_creds, total_score = 0, 0
    pdf_list = []
    
    sorted_items = dict(sorted(st.session_state.selected.items()))
    for name, credit in sorted_items.items():
        c1, c2 = st.columns([3, 1])
        c1.write(f"**{name}** ({credit} หน่วยกิต)")
        g_letter = c2.selectbox("เกรด", list(grade_map.keys()), key=f"grd_{name}")
        total_creds += credit
        total_score += grade_map[g_letter] * credit
        pdf_list.append([name, str(credit), g_letter])

    if total_creds > 0:
        gpa = total_score / total_creds
        st.success(f"### GPA: {gpa:.2f} (รวม {total_creds} นก.)")

        if st.button("🖨️ พิมพ์ PDF"):
            if os.path.exists("THSarabunNew.ttf"):
                pdf = FPDF()
                pdf.add_page()
                pdf.add_font("THSarabun", "", "THSarabunNew.ttf")
                pdf.set_font("THSarabun", "", 24)
                pdf.cell(0, 15, "สรุปผลการเรียนนิติศาสตร์", ln=True, align='C')
                pdf.set_font("THSarabun", "", 16)
                for item in pdf_list:
                    pdf.cell(80, 10, f" {item[0]}", border=1)
                    pdf.cell(50, 10, f"{item[1]} นก.", border=1, align='C')
                    pdf.cell(50, 10, f"เกรด {item[2]}", border=1, align='C', ln=True)
                pdf.ln(10)
                pdf.set_font("THSarabun", "", 20)
                pdf.cell(0, 10, f"หน่วยกิตรวม: {total_creds} / เกรดเฉลี่ย: {gpa:.2f}", ln=True)
                st.download_button("📥 Download PDF", data=pdf.output(), file_name="GPA_140.pdf")
            else:
                st.error("ไม่พบไฟล์ฟอนต์ THSarabunNew.ttf")
