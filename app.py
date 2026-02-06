import streamlit as st
import os

# --- 1. Database (ตรวจสอบหน่วยกิตและคาบสอบเป๊ะ 100%) ---
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

grade_map = {"A": 4.0, "B+": 3.5, "B": 3.0, "C+": 2.5, "C": 2.0, "D+": 1.5, "D": 1.0, "F": 0.0}

st.set_page_config(page_title="Ultimate Law GPA & Planner", layout="wide")

# --- 2. State Management (กันวิชาหาย) ---
if "study_plan" not in st.session_state:
    st.session_state.study_plan = {f"Y{y}T{t}": {s: "-" for s in ["1A","1B","2A","2B","3A","3B","4A","4B"]} 
                                  for y in range(1, 5) for t in ["1", "2", "S"]}

# --- 3. CSS (ตัวหนังสือดำเข้ม 100%) ---
st.markdown("""
    <style>
    header {visibility: hidden;}
    .overall-table { width: 100%; border-collapse: collapse; background-color: #ffffff; }
    .overall-table th, .overall-table td { border: 2px solid #000; padding: 6px; color: #000 !important; vertical-align: top; }
    .overall-table th { background-color: #1e3a8a; color: #fff !important; }
    .sub-tag { background: #e0f2fe; padding: 2px 4px; border-radius: 4px; display: block; margin-bottom: 2px; border-left: 3px solid #0369a1; font-size: 11px; color: #000 !important; font-weight: bold; }
    .summary-grid { display: flex; flex-wrap: wrap; gap: 8px; justify-content: flex-start; padding: 10px 0; }
    .result-box { width: 95px; padding: 5px; border: 2px solid #000; border-radius: 5px; text-align: center; background-color: #fff !important; color: #000 !important; }
    .result-box b { color: #d32f2f !important; font-size: 18px; }
    .credit-alert { color: #fff !important; font-weight: bold; background: #d32f2f; padding: 8px; border-radius: 5px; }
    p, span, label, .stMetric { color: #000 !important; font-weight: bold !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. Functions ---
def clear_all_plan():
    for tk in st.session_state.study_plan:
        for sn in st.session_state.study_plan[tk]:
            st.session_state.study_plan[tk][sn] = "-"

@st.dialog("🧧 สนับสนุนค่าน้ำชาผู้พัฒนา")
def show_donate():
    st.write("ขอบคุณที่สนับสนุนครับ! กด X มุมขวาเพื่อปิด")
    for ext in ["jpg", "jpeg", "png"]:
        if os.path.exists(f"donate.{ext}"):
            st.image(f"donate.{ext}", use_container_width=True); break
    else: st.error("ไม่พบรูป QR Code")

st.title("⚖️ ระบบคำนวณ GPA & วางแผนเรียนนิติศาสตร์")
tab1, tab2 = st.tabs(["📊 คำนวณเกรดสะสม (GPA)", "📅 วางแผนลงทะเบียน 4 ปี"])

# --- TAB 1: GPA ---
with tab1:
    st.info("ติ๊กวิชาที่สอบผ่านแล้วเพื่อคำนวณ GPA")
    selected_gpa = []
    cats = {"📂 หมวด RAM": "RAM", "📂 หมวด LAW": "LAW", "📂 หมวดวิชาเลือก": "ELECTIVE"}
    for label, cp in cats.items():
        with st.expander(label, expanded=(cp == "LAW")):
            cat_courses = {k: v for k, v in all_courses_db.items() if v[4] == cp}
            gpa_cols = st.columns(4)
            for idx, (code, info) in enumerate(cat_courses.items()):
                with gpa_cols[idx % 4]:
                    r = st.columns([1.2, 1])
                    if r[0].checkbox(code, key=f"gpa_chk_{code}"):
                        g = r[1].selectbox("G", ["A","B+","B","C+","C","D+","D","F"], key=f"gpa_sel_{code}", label_visibility="collapsed")
                        selected_gpa.append({"name": code, "credit": info[0], "grade": g})
    if selected_gpa:
        st.divider()
        tc = sum(d['credit'] for d in selected_gpa); tp = sum(grade_map[d['grade']] * d['credit'] for d in selected_gpa)
        st.success(f"### GPA สะสม: {tp/tc:.2f} | รวม {tc} หน่วยกิต")
        h = '<div class="summary-grid">'
        for d in selected_gpa: h += f'<div class="result-box"><span>{d["name"]}</span><br><b>{d["grade"]}</b></div>'
        st.markdown(h + '</div>', unsafe_allow_html=True)

# --- TAB 2: วางแผน (8 Slot + วิชาไม่หาย) ---
with tab2:
    c1, c2, c3 = st.columns(3)
    yr = c1.selectbox("ปีการศึกษา", [1, 2, 3, 4]); tm = c2.selectbox("เทอม", ["1", "2", "S"])
    grad = c3.toggle("🎓 ขอจบ (ลงได้สูงสุด 30/12 นก.)")
    curr_tk = f"Y{yr}T{tm}"

    # คำนวณหน่วยกิตทันทีจาก State
    curr_c = sum([all_courses_db.get(v.split(" | ")[0], [0])[0] for v in st.session_state.study_plan[curr_tk].values() if v != "-"])
    max_c = (12 if tm == "S" else 30) if grad else (9 if tm == "S" else 22)

    st.markdown(f"### 📍 ปี {yr} เทอม {tm}")
    if curr_c > max_c:
        st.markdown(f'<div class="credit-alert">⚠️ ลงเกิน! เทอม {tm} ลงได้ไม่เกิน {max_c} นก. (ตอนนี้ {curr_c})</div>', unsafe_allow_html=True)
    else:
        st.metric("หน่วยกิตรวมเทอมนี้", f"{curr_c} / {max_c}")

    st.divider()
    # กันลงซ้ำข้ามเทอม
    used = [v.split(" | ")[0] for tk, s in st.session_state.study_plan.items() if tk != curr_tk for v in s.values() if v != "-"]

    slots = ["1A", "1B", "2A", "2B", "3A", "3B", "4A", "4B"]
    rows = st.columns(4)
    for i, sn in enumerate(slots):
        with rows[i % 4]:
            st.markdown(f"**📌 คาบ {sn}**")
            valid = ["-"] + [f"{c} | {all_courses_db[c][3]}" for c in all_courses_db if all_courses_db[c][1] == sn[0] and all_courses_db[c][2] == sn[1] and c not in used]
            
            # ดึงค่าจาก state เพื่อให้วิชาไม่หาย
            saved_val = st.session_state.study_plan[curr_tk][sn]
            if saved_val not in valid: saved_val = "-"
            
            # แสดงสล็อต (ลบวิชาได้โดยการเลือก "-")
            choice = st.selectbox(f"S_{sn}", options=valid, index=valid.index(saved_val), key=f"widget_{curr_tk}_{sn}", label_visibility="collapsed")
            st.session_state.study_plan[curr_tk][sn] = choice

    # --- ตารางสรุปภาพรวม 4 ปี ---
    st.divider()
    st.markdown("### 🗓️ ตารางสรุปแผนการเรียนภาพรวม 4 ปี")
    
    html = "<table class='overall-table'><tr><th>ชั้นปี</th><th>เทอม 1</th><th>เทอม 2</th><th>เทอม S</th></tr>"
    for y in range(1, 5):
        html += f"<tr><td><b>ปีที่ {y}</b></td>"
        for t in ["1", "2", "S"]:
            tk = f"Y{y}T{t}"; cell, tc = "", 0
            for sn, val in st.session_state.study_plan[tk].items():
                if val != "-":
                    c = val.split(" | ")[0]; u_c = all_courses_db.get(c, [0])[0]
                    cell += f"<span class='sub-tag'>{sn}: {val}</span>"; tc += u_c
            limit = 9 if t == "S" else 22
            c_style = "color:red; font-weight:bold;" if tc > limit else "color:black;"
            html += f"<td>{cell}<span style='{c_style}'>รวม {tc} นก.</span></td>"
        html += "</tr>"
    st.markdown(html + "</table>", unsafe_allow_html=True)
    st.button("♻️ ล้างแผนทั้งหมดทุกปี", on_click=clear_all_plan)

st.markdown("---")
if st.button("🧧 สนับสนุนค่าน้ำชาผู้พัฒนา", use_container_width=True): show_donate()
