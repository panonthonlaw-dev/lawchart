import streamlit as st
import os

# --- 1. ข้อมูลวิชา (Database กลาง) ---
all_courses_db = {
    "RAM1101": [3, "4", "A", "ภาษาไทย", "RAM"], "RAM1111": [3, "4", "B", "อังกฤษ 1", "RAM"],
    "RAM1112": [3, "3", "B", "อังกฤษ 2", "RAM"], "RAM1132": [3, "3", "A", "การใช้ห้องสมุด", "RAM"],
    "RAM1141": [3, "2", "A", "บุคลิกภาพ", "RAM"], "RAM1204": [3, "3", "B", "ทักษะการคิด", "RAM"],
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

st.set_page_config(page_title="Ultimate Law Planner", layout="wide")

# --- 2. Initialize Session State ---
if "study_plan" not in st.session_state:
    st.session_state.study_plan = {f"Y{y}T{t}": {s: "-" for s in ["1A","1B","2A","2B","3A","3B","4A","4B"]} 
                                  for y in range(1, 5) for t in ["1", "2", "S"]}

# --- 3. CSS ---
st.markdown("""
    <style>
    header {visibility: hidden;}
    .overall-table { width: 100%; border-collapse: collapse; background: white; font-size: 13px; }
    .overall-table th, .overall-table td { border: 1px solid #ddd; padding: 8px; vertical-align: top; }
    .overall-table th { background-color: #1e3a8a; color: white; }
    .sub-tag { background: #e0f2fe; padding: 2px 4px; border-radius: 4px; display: block; margin-bottom: 2px; border-left: 3px solid #0369a1; font-size: 11px; }
    .slot-label { font-weight: bold; color: #1e3a8a; margin-bottom: 2px; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚖️ Law Planner & GPA System")

tab1, tab2 = st.tabs(["📊 คำนวณเกรดสะสม", "📅 วางแผนลงทะเบียน 4 ปี"])

# --- TAB 1: GPA (คงเดิม) ---
with tab1:
    st.info("ส่วนคำนวณเกรดสะสม")
    # (ใส่ Logic เดิมที่นี่)

# --- TAB 2: วางแผน 4 ปี ---
with tab2:
    col_y, col_t, col_g = st.columns(3)
    y = col_y.selectbox("ปีการศึกษา", [1, 2, 3, 4])
    t = col_t.selectbox("เทอม", ["1", "2", "S"])
    grad = col_g.toggle("🎓 ขอจบ (ลงซ้ำซ้อนได้)")

    curr_term_key = f"Y{y}T{t}"
    st.divider()
    
    # รวบรวมวิชาที่ถูกเลือกไปแล้วในเทอม "อื่นๆ"
    used_elsewhere = []
    for tk, slots in st.session_state.study_plan.items():
        if tk != curr_term_key:
            used_elsewhere.extend([v.split(" | ")[0] for v in slots.values() if v != "-"])

    # แสดงผล 8 สล็อต
    slots_list = ["1A", "1B", "2A", "2B", "3A", "3B", "4A", "4B"]
    rows = st.columns(4)
    
    for i, s_name in enumerate(slots_list):
        with rows[i % 4]:
            st.markdown(f"<div class='slot-label'>📌 คาบ {s_name}</div>", unsafe_allow_html=True)
            
            # กรองวิชา: 1. ตรงคาบสอบ 2. ยังไม่เคยถูกเลือกในเทอมอื่น
            day, period = s_name[0], s_name[1]
            valid_options = ["-"] + [
                f"{code} | {info[3]}" for code, info in all_courses_db.items() 
                if info[1] == day and info[2] == period and code not in used_elsewhere
            ]
            
            # ดึงค่าปัจจุบันจาก state
            current_val = st.session_state.study_plan[curr_term_key][s_name]
            if current_val not in valid_options: current_val = "-"

            choice = st.selectbox(f"S_{s_name}", options=valid_options, 
                                  index=valid_options.index(current_val),
                                  key=f"sel_{curr_term_key}_{s_name}", label_visibility="collapsed")
            
            # บันทึกค่าลง State ทันที
            st.session_state.study_plan[curr_term_key][s_name] = choice
            
            if choice != "-":
                if st.button(f"ลบ {s_name}", key=f"del_{curr_term_key}_{s_name}"):
                    st.session_state.study_plan[curr_term_key][s_name] = "-"
                    st.rerun()

    # --- ส่วนตารางสรุปภาพรวม 4 ปี ---
    st.divider()
    st.markdown("### 🗓️ ตารางสรุปแผนการเรียนภาพรวม 4 ปี (วิชาที่เลือกแล้วจะหายจากตัวเลือกเทอมอื่น)")
    
    html = "<table class='overall-table'><tr><th>ปีการศึกษา</th><th>เทอม 1</th><th>เทอม 2</th><th>เทอม S</th></tr>"
    for yr in range(1, 5):
        html += f"<tr><td><b>ปีที่ {yr}</b></td>"
        for tm in ["1", "2", "S"]:
            tk = f"Y{yr}T{tm}"
            cell = ""
            total_c = 0
            for sn, val in st.session_state.study_plan[tk].items():
                if val != "-":
                    code = val.split(" | ")[0]
                    cell += f"<span class='sub-tag'>{sn}: {val}</span>"
                    total_c += all_courses_db[code][0]
            html += f"<td>{cell}<b>รวม {total_c} นก.</b></td>"
        html += "</tr>"
    html += "</table>"
    st.markdown(html, unsafe_allow_html=True)

    if st.button("♻️ ล้างแผนทั้งหมดทุกปี"):
        st.session_state.study_plan = {f"Y{y}T{t}": {s: "-" for s in ["1A","1B","2A","2B","3A","3B","4A","4B"]} 
                                      for y in range(1, 5) for t in ["1", "2", "S"]}
        st.rerun()
