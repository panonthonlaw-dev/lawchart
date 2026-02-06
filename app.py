import streamlit as st
import os

# --- 1. ข้อมูลวิชา (Database เดียวกัน) ---
all_courses_db = {
    "RAM1101": [3, "4", "A", "ภาษาไทย", "RAM"], "RAM1111": [3, "4", "B", "อังกฤษ 1", "RAM"],
    "RAM1112": [3, "3", "B", "อังกฤษ 2", "RAM"], "RAM1132": [3, "3", "A", "การใช้ห้องสมุด", "RAM"],
    "RAM1141": [3, "2", "A", "สุขภาพและบุคลิกภาพ", "RAM"], "RAM1204": [3, "3", "B", "ทักษะการคิด", "RAM"],
    "RAM1213": [3, "3", "A", "วิชา RAM", "RAM"], "RAM1301": [3, "4", "B", "คุณธรรม", "RAM"],
    "RAM1303": [3, "2", "B", "วิทยาศาสตร์", "RAM"], "RAM1312": [3, "4", "B", "วิชา RAM", "RAM"],
    "LAW1101": [2, "2", "A", "กฎหมายมหาชน", "LAW"], "LAW1102": [2, "4", "A", "กฎหมายเอกชน", "LAW"],
    "LAW1103": [3, "2", "A", "นิติกรรม", "LAW"], "LAW2101": [3, "2", "B", "ทรัพย์", "LAW"],
    "LAW2102": [3, "3", "A", "หนี้", "LAW"], "LAW2104": [3, "2", "B", "รัฐธรรมนูญ", "LAW"],
    "LAW2105": [3, "4", "A", "ซื้อขาย", "LAW"], "LAW2106": [3, "4", "A", "อาญา 1", "LAW"],
    "LAW2107": [3, "1", "B", "อาญา 2", "LAW"], "LAW2109": [3, "3", "B", "ยืม ฝาก", "LAW"],
    "LAW2110": [2, "1", "B", "ค้ำ จำนำ", "LAW"], "LAW2111": [2, "3", "A", "ตัวแทน", "LAW"],
    "LAW2112": [2, "4", "B", "ประกัน", "LAW"], "LAW2113": [3, "2", "A", "ตั๋วเงิน", "LAW"],
    "LAW2108": [2, "1", "A", "เช่า จ้าง", "LAW"], "LAW3101": [2, "1", "A", "อาญา 3", "LAW"],
    "LAW3102": [3, "4", "B", "หุ้นส่วน", "LAW"], "LAW3103": [3, "1", "B", "ครอบครัว", "LAW"],
    "LAW3104": [2, "3", "A", "ธรรมนูญศาล", "LAW"], "LAW3105": [3, "1", "B", "วิ.แพ่ง 1", "LAW"],
    "LAW3106": [3, "4", "B", "วิอาญา 1", "LAW"], "LAW3109": [3, "3", "B", "มรดก", "LAW"],
    "LAW3110": [2, "1", "A", "ล้มละลาย", "LAW"], "LAW3111": [3, "2", "A", "พยาน", "LAW"],
    "LAW3112": [3, "1", "B", "กฎหมายปกครอง", "LAW"], "LAW3117": [2, "1", "A", "ป.วิมหาชน", "LAW"],
    "LAW4101": [2, "1", "A", "ภาษี", "LAW"], "LAW4102": [3, "2", "B", "ว่าความ", "LAW"],
    "LAW4103": [3, "4", "A", "คดีเมือง", "LAW"], "LAW4104": [2, "2", "B", "แรงงาน", "LAW"],
    "LAW4105": [2, "2", "A", "วิชาชีพทนาย", "LAW"], "LAW4106": [2, "3", "A", "สิทธิมนุษยชน", "LAW"],
    "LAW4107": [2, "2", "B", "ปรัชญา", "LAW"], "LAW4108": [3, "2", "B", "ที่ดิน", "LAW"],
    "LAW4109": [3, "4", "A", "ทรัพย์สินทางปัญญา", "LAW"], "LAW4110": [2, "1", "A", "ค้าระหว่างประเทศ", "LAW"],
    "LAW3133": [3, "3", "B", "อาชญากร", "ELECTIVE"], "LAW3138": [2, "1", "B", "เด็ก", "ELECTIVE"],
    "LAW4134": [2, "1", "B", "ทะเล", "ELECTIVE"], "LAW4156": [2, "2", "A", "อิ้งกฎหมาย", "ELECTIVE"],
    "วิชาเลือก 1": [3, "0", "0", "เลือกเสรี 1", "ELECTIVE"], "วิชาเลือก 2": [3, "0", "0", "เลือกเสรี 2", "ELECTIVE"]
}

grade_map = {"A": 4.0, "B+": 3.5, "B": 3.0, "C+": 2.5, "C": 2.0, "D+": 1.5, "D": 1.0, "F": 0.0}

st.set_page_config(page_title="Law Overall Planner", layout="wide")

# --- 2. Initialize Session State ---
if "study_plan" not in st.session_state:
    st.session_state.study_plan = {f"ปี {y} เทอม {t}": [] for y in range(1, 5) for t in ["1", "2", "S"]}

# --- 3. CSS ---
st.markdown("""
    <style>
    header {visibility: hidden;}
    .overall-table { width: 100%; border-collapse: collapse; margin-top: 20px; font-size: 14px; }
    .overall-table th, .overall-table td { border: 1px solid #ddd; padding: 12px; text-align: left; vertical-align: top; }
    .overall-table th { background-color: #f4f4f4; color: #333; }
    .term-title { font-weight: bold; color: #1f77b4; margin-bottom: 5px; display: block; }
    .sub-item { font-size: 12px; background: #e1f5fe; padding: 2px 5px; border-radius: 4px; margin-bottom: 2px; display: block; border-left: 3px solid #0288d1; }
    .credit-tag { font-weight: bold; color: #d32f2f; font-size: 11px; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚖️ Law GPA & Planning Tool")

tab1, tab2 = st.tabs(["📊 คำนวณเกรด", "📅 วางแผนลงทะเบียน"])

with tab1:
    st.info("ส่วนคำนวณเกรด (GPA)")
    # (ใช้ Logic เดิมจากโค้ดชุดก่อนได้เลยครับ)

with tab2:
    st.subheader("Dashboard วางแผนเรียน")
    
    col_l, col_r = st.columns([1, 1.2])
    
    with col_l:
        st.markdown("### 1. เลือกวิชาเข้าแผน")
        target_term = st.selectbox("เทอมที่ต้องการจัด:", list(st.session_state.study_plan.keys()))
        is_grad = st.toggle("🎓 ขอจบการศึกษา (ลงได้ 30 นก. / ซ้ำซ้อน)")
        
        cat = st.radio("หมวดหมู่:", ["RAM", "LAW", "ELECTIVE"], horizontal=True)
        used_subs = [item for sublist in st.session_state.study_plan.values() for item in sublist]
        available = {k: v for k, v in all_courses_db.items() if v[4] == cat and k not in used_subs}
        
        for code, info in available.items():
            if st.button(f"ADD: {code} {info[3]} ({info[1]}{info[2]})", key=f"p_add_{code}"):
                st.session_state.study_plan[target_term].append(code)
                st.rerun()

    with col_r:
        st.markdown(f"### 2. วิชาใน {target_term}")
        current_list = st.session_state.study_plan[target_term]
        if not current_list:
            st.write("ยังไม่มีวิชา")
        else:
            total_c = 0
            for sub in current_list:
                info = all_courses_db[sub]
                total_c += info[0]
                c_s, c_d = st.columns([5, 1])
                c_s.write(f"**{sub}** {info[3]} ({info[1]}{info[2]})")
                if c_d.button("DEL", key=f"p_del_{sub}"):
                    st.session_state.study_plan[target_term].remove(sub)
                    st.rerun()
            st.metric("หน่วยกิตเทอมนี้", f"{total_c}")

    # --- ส่วนที่เพิ่มใหม่: ตารางสรุปภาพรวม 4 ปี ---
    st.divider()
    st.markdown("### 🗓️ ตารางสรุปแผนการเรียนภาพรวม 4 ปี")
    
    overall_html = "<table class='overall-table'><tr><th>ปีการศึกษา</th><th>เทอม 1</th><th>เทอม 2</th><th>เทอม S</th></tr>"
    
    for y in range(1, 5):
        overall_html += f"<tr><td><b>ปีที่ {y}</b></td>"
        for t in ["1", "2", "S"]:
            t_key = f"ปี {y} เทอม {t}"
            subs = st.session_state.study_plan[t_key]
            t_creds = sum(all_courses_db[s][0] for s in subs)
            
            cell_content = ""
            for s in subs:
                cell_content += f"<span class='sub-item'>{s} {all_courses_db[s][3]}</span>"
            
            overall_html += f"<td>{cell_content}<span class='credit-tag'>รวม {t_creds} นก.</span></td>"
        overall_html += "</tr>"
    
    overall_html += "</table>"
    st.markdown(overall_html, unsafe_allow_html=True)
    
    if st.button("ล้างแผนทั้งหมด"):
        st.session_state.study_plan = {f"ปี {y} เทอม {t}": [] for y in range(1, 5) for t in ["1", "2", "S"]}
        st.rerun()
