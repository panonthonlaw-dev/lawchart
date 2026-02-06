import streamlit as st
import os

# --- 1. ข้อมูลวิชา (Database กลาง) ---
all_courses_db = {
    # หมวด RAM
    "RAM1101": [3, "4", "A", "ภาษาไทย", "RAM"], "RAM1111": [3, "4", "B", "อังกฤษ 1", "RAM"],
    "RAM1112": [3, "3", "B", "อังกฤษ 2", "RAM"], "RAM1132": [3, "3", "A", "การใช้ห้องสมุด", "RAM"],
    "RAM1141": [3, "2", "A", "บุคลิกภาพ", "RAM"], "RAM1204": [3, "3", "B", "ทักษะการคิด", "RAM"],
    "RAM1213": [3, "3", "A", "วิชา RAM", "RAM"], "RAM1301": [3, "4", "B", "คุณธรรม", "RAM"],
    "RAM1303": [3, "2", "B", "วิทยาศาสตร์", "RAM"], "RAM1312": [3, "4", "B", "วิชา RAM", "RAM"],
    # หมวด LAW
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
    # หมวดเลือก
    "LAW3133": [3, "3", "B", "อาชญากร", "ELECTIVE"], "LAW3138": [2, "1", "B", "เด็ก", "ELECTIVE"],
    "LAW4134": [2, "1", "B", "ทะเล", "ELECTIVE"], "LAW4156": [2, "2", "A", "อิ้งกฎหมาย", "ELECTIVE"],
    "วิชาเลือก 1": [3, "0", "0", "เลือกเสรี 1", "ELECTIVE"], "วิชาเลือก 2": [3, "0", "0", "เลือกเสรี 2", "ELECTIVE"]
}

grade_map = {"A": 4.0, "B+": 3.5, "B": 3.0, "C+": 2.5, "C": 2.0, "D+": 1.5, "D": 1.0, "F": 0.0}
exam_slots = ["-", "1A", "1B", "2A", "2B", "3A", "3B", "4A", "4B"]

st.set_page_config(page_title="GPA & Slot Planner", layout="wide")

# --- 2. CSS ---
st.markdown("""
    <style>
    header {visibility: hidden;}
    .stMainBlockContainer { padding-top: 1.5rem !important; }
    .summary-grid { display: flex; flex-wrap: wrap; gap: 8px; justify-content: flex-start; padding: 10px 0; }
    .result-box {
        width: 100px; padding: 8px 4px; border: 2px solid #333; border-radius: 8px;
        text-align: center; background-color: #ffffff !important; box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    .result-box span { font-size: 11px !important; display: block; color: #333 !important; }
    .result-box b { font-size: 20px !important; display: block; color: #d32f2f !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚖️ Law GPA & Planning")

tab1, tab2 = st.tabs(["📊 คำนวณเกรด", "📅 วางแผนลงทะเบียน (8 Slot)"])

# --- TAB 1: คำนวณเกรด (GPA) ---
with tab1:
    st.info("เปิดหมวดหมู่เพื่อติ๊กวิชาที่สอบผ่านแล้ว")
    selected_gpa = []
    cats = {"📂 หมวด RAM": "RAM", "📂 หมวด LAW": "LAW", "📂 หมวดวิชาเลือก": "ELECTIVE"}
    
    for label, code_prefix in cats.items():
        with st.expander(label, expanded=(code_prefix == "LAW")):
            cat_courses = {k: v for k, v in all_courses_db.items() if v[4] == code_prefix}
            gpa_cols = st.columns(4)
            for idx, (code, info) in enumerate(cat_courses.items()):
                with gpa_cols[idx % 4]:
                    c_row = st.columns([1.1, 1])
                    if c_row[0].checkbox(f"{code}", key=f"gpa_{code}"):
                        g = c_row[1].selectbox("G", list(grade_map.keys()), key=f"sel_{code}", label_visibility="collapsed")
                        selected_gpa.append({"name": code, "credit": info[0], "grade": g})
    
    if selected_gpa:
        st.divider()
        total_creds = sum(d['credit'] for d in selected_gpa)
        total_points = sum(grade_map[d['grade']] * d['credit'] for d in selected_gpa)
        gpa_score = total_points / total_creds if total_creds > 0 else 0
        st.success(f"### GPA สะสม: {gpa_score:.2f} | รวม {total_creds} หน่วยกิต")
        
        # แสดงผลสรุปเป็นกล่อง
        sum_html = '<div class="summary-grid">'
        for d in selected_gpa:
            sum_html += f'<div class="result-box"><span>{d["name"]}</span><b>{d["grade"]}</b></div>'
        sum_html += '</div>'
        st.markdown(sum_html, unsafe_allow_html=True)

# --- TAB 2: วางแผนลงทะเบียน (8 Slot ตามคาบสอบ) ---
with tab2:
    col_y, col_t, col_g = st.columns([1, 1, 1])
    sel_y = col_y.selectbox("ปีการศึกษา", [1, 2, 3, 4])
    sel_t = col_t.selectbox("เทอม", ["1", "2", "S"])
    is_grad = col_g.toggle("🎓 ขอจบการศึกษา (สอบซ้ำซ้อนได้)")

    st.divider()
    st.markdown(f"### 🗓️ ตารางจัดแผน: ปี {sel_y} เทอม {sel_t}")

    term_key = f"Y{sel_y}T{sel_t}"
    total_c = 0
    exam_conflicts = []
    used_exams = {}
    course_options = ["-"] + sorted(list(all_courses_db.keys()))

    slot_cols = st.columns(4)
    for i in range(1, 9):
        with slot_cols[(i-1) % 4]:
            st.markdown(f"**แถวที่ {i}**")
            # 1. เลือกวิชา
            sub_code = st.selectbox("วิชา", course_options, key=f"slot_sub_{term_key}_{i}")
            
            if sub_code != "-":
                info = all_courses_db[sub_code]
                total_c += info[0]
                
                # 2. เลือกวันสอบ (ดึง Default จาก DB)
                def_exam = f"{info[1]}{info[2]}" if info[1] != "0" else "-"
                idx = exam_slots.index(def_exam) if def_exam in exam_slots else 0
                
                exam_time = st.selectbox("คาบสอบ", exam_slots, index=idx, key=f"slot_ex_{term_key}_{i}")
                
                if exam_time != "-":
                    if exam_time in used_exams:
                        exam_conflicts.append(f"{sub_code} ชน {used_exams[exam_time]} ({exam_time})")
                    used_exams[exam_time] = sub_code
                st.caption(f"{info[3]} ({info[0]} นก.)")
            else:
                st.selectbox("คาบสอบ", ["-"], key=f"ex_disabled_{i}", disabled=True)

    st.divider()
    max_c = 30 if is_grad else (9 if sel_t == "S" else 22)
    st.metric("หน่วยกิตรวมเทอมนี้", f"{total_c} / {max_c}")
    
    if exam_conflicts:
        if is_grad: st.warning("⚠️ มีวิชาสอบชนกัน (ใช้สิทธิ์ซ้ำซ้อน)")
        else: st.error("❌ สอบชนกัน! กรุณาจัดตารางใหม่")
        for c in exam_conflicts: st.write(f"- {c}")
    elif total_c > 0:
        st.success("✅ ตารางเรียนสมบูรณ์")

st.markdown("---")
if st.button("🧧 สนับสนุนค่าน้ำชา / โดเนท", use_container_width=True):
    for ext in ["jpg", "jpeg", "png"]:
        path = f"donate.{ext}"
        if os.path.exists(path):
            st.image(path, use_container_width=True)
