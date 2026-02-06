import streamlit as st
import os

# --- 1. Database (หน่วยกิตเป๊ะ 100%) ---
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
    "วิชาเลือก 1": [3, "1", "A", "เลือกเสรี 1", "ELECTIVE"], "วิชาเลือก 2": [3, "1", "B", "เลือกเสรี 2", "ELECTIVE"]
}

st.set_page_config(page_title="Ultimate Law GPA & Planner", layout="wide")

# --- 2. State Management (หัวใจสำคัญ) ---
if "study_plan" not in st.session_state:
    st.session_state.study_plan = {f"Y{y}T{t}": {s: "-" for s in ["1A","1B","2A","2B","3A","3B","4A","4B"]} 
                                  for y in range(1, 5) for t in ["1", "2", "S"]}

# --- 3. CSS (ดำชัดเจน ทะลุทุกโหมด) ---
st.markdown("""
    <style>
    header {visibility: hidden;}
    .overall-table { width: 100%; border-collapse: collapse; background-color: #ffffff; }
    .overall-table th, .overall-table td { border: 2px solid #000; padding: 6px; color: #000 !important; vertical-align: top; }
    .overall-table th { background-color: #1e3a8a; color: #fff !important; }
    .sub-tag { background: #e0f2fe; padding: 2px 4px; border-radius: 4px; display: block; margin-bottom: 2px; border-left: 3px solid #0369a1; font-size: 11px; color: #000 !important; font-weight: bold; }
    .credit-alert { color: #fff !important; font-weight: bold; background: #d32f2f; padding: 10px; border-radius: 5px; margin-bottom: 10px; }
    .stMetric label, .stMetric [data-testid="stMetricValue"] { color: #000 !important; font-weight: bold !important; }
    p, span, label { color: #000 !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. Logic Functions ---
def update_slot(tk, sn, val):
    st.session_state.study_plan[tk][sn] = val

def clear_all():
    for tk in st.session_state.study_plan:
        for sn in st.session_state.study_plan[tk]:
            st.session_state.study_plan[tk][sn] = "-"

st.title("⚖️ ระบบวางแผนเรียนนิติศาสตร์ (V.เสถียร)")
tab1, tab2 = st.tabs(["📊 GPA สะสม", "📅 วางแผนลงทะเบียน"])

with tab1:
    st.write("ส่วนคำนวณเกรด (GPA)...") # ใส่โค้ดเดิมได้เลยครับ

with tab2:
    # เลือกเทอม
    c1, c2, c3 = st.columns(3)
    yr = c1.selectbox("ปีการศึกษา", [1, 2, 3, 4], key="sel_yr")
    tm = c2.selectbox("เทอม", ["1", "2", "S"], key="sel_tm")
    grad = c3.toggle("🎓 ขอจบ (ลงได้ 30/12 นก.)")
    curr_tk = f"Y{yr}T{tm}"
    
    # 1. คำนวณหน่วยกิตเทอมปัจจุบันแบบ Real-time
    curr_c = 0
    for val in st.session_state.study_plan[curr_tk].values():
        if val != "-":
            code = val.split(" | ")[0]
            curr_c += all_courses_db.get(code, [0])[0]

    limit = (12 if tm == "S" else 30) if grad else (9 if tm == "S" else 22)
    
    if curr_c > limit:
        st.markdown(f'<div class="credit-alert">⚠️ ลงเกิน! เทอม {tm} ลงได้สูงสุด {limit} นก. (ตอนนี้ลงไป {curr_c})</div>', unsafe_allow_html=True)
    else:
        st.metric(f"หน่วยกิตเทอม {tm}", f"{curr_c} / {limit}")

    st.divider()
    
    # 2. วิชาที่ลงไปแล้วในเทอม "อื่น" (เพื่อกันลงซ้ำ)
    used = [v.split(" | ")[0] for tk, s in st.session_state.study_plan.items() if tk != curr_tk for v in s.values() if v != "-"]

    slots = ["1A", "1B", "2A", "2B", "3A", "3B", "4A", "4B"]
    rows = st.columns(4)
    
    # 3. วนลูปสร้างสล็อต 8 ช่อง
    for i, sn in enumerate(slots):
        with rows[i % 4]:
            st.markdown(f"**📌 คาบ {sn}**")
            
            # ตัวเลือกวิชาที่สอบตรงคาบ และยังไม่เคยลงเทอมอื่น
            valid = ["-"] + [f"{c} | {all_courses_db[c][3]}" for c in all_courses_db if all_courses_db[c][1] == sn[0] and all_courses_db[c][2] == sn[1] and c not in used]
            
            # ดึงค่าเดิมที่เคยเลือกไว้กลับมาโชว์ (สำคัญมาก! กันวิชาหาย)
            saved_val = st.session_state.study_plan[curr_tk][sn]
            if saved_val not in valid: saved_val = "-"
            
            # เมื่อเลือกวิชา ให้ใช้ on_change เพื่อบังคับให้คำนวณใหม่ทันที
            choice = st.selectbox(f"S_{sn}", options=valid, index=valid.index(saved_val), 
                                  key=f"widget_{curr_tk}_{sn}", 
                                  label_visibility="collapsed")
            
            # บันทึกค่าลง State ทุกครั้งที่เปลี่ยน
            st.session_state.study_plan[curr_tk][sn] = choice

    # --- 4. ตารางสรุปภาพรวม 4 ปี (เห็นทุกอย่างในหน้าเดียว) ---
    st.divider()
    st.markdown("### 🗓️ สรุปแผนการเรียน 4 ปี (วิชาจะไม่หายเมื่อสลับหน้า)")
    
    
    
    html = "<table class='overall-table'><tr><th>ปี</th><th>เทอม 1</th><th>เทอม 2</th><th>เทอม S</th></tr>"
    for y in range(1, 5):
        html += f"<tr><td><b>ปี {y}</b></td>"
        for t in ["1", "2", "S"]:
            tk = f"Y{y}T{t}"; cell, tc = "", 0
            for sn, val in st.session_state.study_plan[tk].items():
                if val != "-":
                    c = val.split(" | ")[0]; u_c = all_courses_db.get(c, [0])[0]
                    cell += f"<span class='sub-tag'>{sn}: {val} ({u_c} นก.)</span>"
                    tc += u_c
            html += f"<td>{cell}<b style='color:#000'>รวม {tc} นก.</b></td>"
        html += "</tr>"
    st.markdown(html + "</table>", unsafe_allow_html=True)
    
    if st.button("♻️ ล้างแผนทั้งหมด", on_click=clear_all):
        st.rerun()
