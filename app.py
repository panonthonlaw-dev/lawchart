import streamlit as st
import os

# --- 1. ข้อมูลวิชาและตารางสอบ (Database กลาง) ---
all_courses_db = {
    # หมวด RAM
    "RAM1101": [3, "4", "A", "ภาษาไทย", "RAM"], "RAM1111": [3, "4", "B", "อังกฤษ 1", "RAM"],
    "RAM1112": [3, "3", "B", "อังกฤษ 2", "RAM"], "RAM1132": [3, "3", "A", "การใช้ห้องสมุด", "RAM"],
    "RAM1141": [3, "2", "A", "สุขภาพและบุคลิกภาพ", "RAM"], "RAM1204": [3, "3", "B", "ทักษะการคิด", "RAM"],
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

st.set_page_config(page_title="GPA Law Pro", layout="wide")

# --- 2. Initialize Session State ---
if "study_plan" not in st.session_state:
    st.session_state.study_plan = {f"ปี {y} เทอม {t}": [] for y in range(1, 5) for t in ["1", "2", "S"]}
if "current_term" not in st.session_state:
    st.session_state.current_term = "ปี 1 เทอม 1"

# --- 3. CSS ---
st.markdown("""
    <style>
    header {visibility: hidden;}
    .stMainBlockContainer { padding-top: 1.5rem !important; }
    [data-testid="stExpander"] [data-testid="column"] { flex: 1 1 45% !important; min-width: 140px !important; }
    .summary-grid { display: flex; flex-wrap: wrap; gap: 8px; justify-content: flex-start; padding: 10px 0; }
    .result-box {
        width: 100px; padding: 8px 4px; border: 2px solid #333; border-radius: 8px;
        text-align: center; background-color: #ffffff !important; box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    .result-box span { font-size: 11px !important; display: block; color: #333 !important; }
    .result-box b { font-size: 20px !important; display: block; color: #d32f2f !important; }
    .header-style { color: #1f77b4; font-weight: bold; font-size: 1.1rem; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚖️ Law GPA & Planning Tool")

tab1, tab2 = st.tabs(["📊 คำนวณเกรด (GPA)", "📅 วางแผนลงทะเบียน"])

# --- TAB 1: คำนวณเกรด ---
with tab1:
    st.info("เปิดหมวดหมู่เพื่อติ๊กวิชาที่สอบผ่านแล้ว")
    selected_gpa = []
    cats = {"หมวด RAM": "RAM", "หมวด LAW": "LAW", "หมวดวิชาเลือก": "ELECTIVE"}
    
    for label, code_prefix in cats.items():
        with st.expander(f"📂 {label}", expanded=(code_prefix == "LAW")):
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
        st.success(f"### GPA: {gpa_score:.2f} | รวม {total_creds} หน่วยกิต")
        
        # สรุปผลแบบการ์ดสวยงาม
        sum_html = '<div class="summary-grid">'
        for d in selected_gpa:
            sum_html += f'<div class="result-box"><span>{d["name"]}</span><b>{d["grade"]}</b></div>'
        sum_html += '</div>'
        st.markdown(sum_html, unsafe_allow_html=True)

# --- TAB 2: วางแผนลงทะเบียน (Dashboard แบบจิ้มเลือก) ---
with tab2:
    st.subheader("จัดแผนการเรียน (ป้องกันลงซ้ำและสอบชน)")
    col_t1, col_t2 = st.columns([2, 1])
    
    with col_t1:
        st.session_state.current_term = st.selectbox(
            "เลือกเทอมที่จะเพิ่มวิชา:", 
            list(st.session_state.study_plan.keys())
        )
    with col_t2:
        is_grad = st.toggle("ขอจบการศึกษา (30 นก. / ซ้ำซ้อน)")

    st.divider()
    col_left, col_right = st.columns([1, 1])

    with col_left:
        st.markdown("<p class='header-style'>คลังวิชาที่เหลือ (คลิกเพื่อเพิ่ม)</p>", unsafe_allow_html=True)
        used_subs = [item for sublist in st.session_state.study_plan.values() for item in sublist]
        cat = st.radio("เลือกหมวดหมู่:", ["RAM", "LAW", "ELECTIVE"], horizontal=True)
        
        # กรองวิชาที่ยังไม่ถูกลงทะเบียน
        available_courses = {k: v for k, v in all_courses_db.items() if v[4] == cat and k not in used_subs}
        
        for code, info in available_courses.items():
            exam = f"({info[1]}{info[2]})" if info[1] != "0" else ""
            if st.button(f"ADD: {code} {info[3]} {exam}", key=f"plan_add_{code}"):
                st.session_state.study_plan[st.session_state.current_term].append(code)
                st.rerun()

    with col_right:
        st.markdown(f"<p class='header-style'>เทอมที่กำลังจัด: {st.session_state.current_term}</p>", unsafe_allow_html=True)
        current_list = st.session_state.study_plan[st.session_state.current_term]
        
        if not current_list:
            st.write("ยังไม่ได้เพิ่มวิชา จิ้มปุ่มด้านซ้ายได้เลย")
        else:
            total_c = 0
            exam_check = {}
            for sub in current_list:
                info = all_courses_db[sub]
                total_c += info[0]
                
                c_sub, c_del = st.columns([5, 1])
                c_sub.write(f"**{sub}** - {info[3]} ({info[1]}{info[2]})")
                if c_del.button("DEL", key=f"plan_del_{sub}"):
                    st.session_state.study_plan[st.session_state.current_term].remove(sub)
                    st.rerun()
                
                # ตรวจสอบสอบชน
                d_code = f"{info[1]}{info[2]}"
                if d_code != "00":
                    if d_code in exam_check:
                        if is_grad: st.warning(f"เตือน: {sub} สอบชนกับ {exam_check[d_code]}")
                        else: st.error(f"ห้ามลง: {sub} สอบชนกับ {exam_check[d_code]}!")
                    exam_check[d_code] = sub

            max_c = 30 if is_grad else (9 if "เทอม S" in st.session_state.current_term else 22)
            st.metric("หน่วยกิตรวมเทอมนี้", f"{total_c} / {max_c}")
            if total_c > max_c: st.error("หน่วยกิตเกินกำหนด!")

    st.divider()
    if st.button("ล้างแผนการเรียนทั้งหมด (Reset)"):
        st.session_state.study_plan = {f"ปี {y} เทอม {t}": [] for y in range(1, 5) for t in ["1", "2", "S"]}
        st.rerun()
