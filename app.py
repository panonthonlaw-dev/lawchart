import streamlit as st
import os

# --- 1. ข้อมูลวิชา ---
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

st.set_page_config(page_title="Ultimate Law GPA & Planner", layout="wide")

# --- 2. State Management ---
if "study_plan" not in st.session_state:
    st.session_state.study_plan = {f"Y{y}T{t}": {s: "-" for s in ["1A","1B","2A","2B","3A","3B","4A","4B"]} 
                                  for y in range(1, 5) for t in ["1", "2", "S"]}
if "slot_versions" not in st.session_state:
    st.session_state.slot_versions = {f"Y{y}T{t}_{s}": 0 for y in range(1, 5) for t in ["1", "2", "S"] for s in ["1A","1B","2A","2B","3A","3B","4A","4B"]}

# --- 3. CSS ---
st.markdown("""
    <style>
    header {visibility: hidden;}
    .overall-table { width: 100%; border-collapse: collapse; background-color: #ffffff; color: #000 !important; }
    .overall-table th, .overall-table td { border: 2px solid #000; padding: 8px; color: #000 !important; vertical-align: top; }
    .overall-table th { background-color: #1e3a8a; color: #fff !important; }
    .sub-tag { background: #e0f2fe; padding: 2px 4px; border-radius: 4px; display: block; margin-bottom: 2px; border-left: 3px solid #0369a1; font-size: 11px; color: #000 !important; font-weight: bold; }
    .result-box { width: 95px; padding: 5px; border: 2px solid #000; border-radius: 5px; text-align: center; background-color: #fff !important; color: #000 !important; }
    .result-box b { color: #d32f2f !important; font-size: 18px; }
    .credit-alert { color: #d32f2f !important; font-weight: bold; font-size: 16px; border: 2px solid #d32f2f; padding: 5px; border-radius: 5px; background: #ffebee; }
    p, span, label { color: #000 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. Functions ---
def handle_clear_slot(tk, sn):
    st.session_state.study_plan[tk][sn] = "-"
    st.session_state.slot_versions[f"{tk}_{sn}"] += 1

def handle_clear_all():
    for tk in st.session_state.study_plan:
        for sn in st.session_state.study_plan[tk]:
            st.session_state.study_plan[tk][sn] = "-"
            st.session_state.slot_versions[f"{tk}_{sn}"] += 1

@st.dialog("🧧 สนับสนุนค่าน้ำชาผู้พัฒนา")
def show_donate():
    st.write("ขอบคุณที่สนับสนุนครับ!")
    for ext in ["jpg", "jpeg", "png"]:
        if os.path.exists(f"donate.{ext}"):
            st.image(f"donate.{ext}", use_container_width=True); break
    else: st.error("ไม่พบรูป QR Code")

st.title("⚖️ ระบบวางแผนเรียน & GPA นิติศาสตร์")
tab1, tab2 = st.tabs(["📊 คำนวณเกรด (GPA)", "📅 วางแผนลงทะเบียน"])

# --- TAB 1: GPA ---
with tab1:
    selected_gpa = []
    for label, cp in {"📂 หมวด RAM": "RAM", "📂 หมวด LAW": "LAW", "📂 หมวดวิชาเลือก": "ELECTIVE"}.items():
        with st.expander(label, expanded=(cp == "LAW")):
            cat_courses = {k: v for k, v in all_courses_db.items() if v[4] == cp}
            cols = st.columns(4)
            for idx, (code, info) in enumerate(cat_courses.items()):
                with cols[idx % 4]:
                    r = st.columns([1.2, 1])
                    if r[0].checkbox(code, key=f"gpa_chk_{code}"):
                        g = r[1].selectbox("G", ["A","B+","B","C+","C","D+","D","F"], key=f"gpa_sel_{code}", label_visibility="collapsed")
                        selected_gpa.append({"name": code, "credit": info[0], "grade": g})
    if selected_gpa:
        st.divider()
        tc = sum(d['credit'] for d in selected_gpa); tp = sum(grade_map[d['grade']] * d['credit'] for d in selected_gpa)
        st.success(f"### GPA: {tp/tc:.2f} | รวม {tc} หน่วยกิต")
        h = '<div style="display:flex; flex-wrap:wrap; gap:8px;">'
        for d in selected_gpa: h += f'<div class="result-box"><span>{d["name"]}</span><br><b>{d["grade"]}</b></div>'
        st.markdown(h + '</div>', unsafe_allow_html=True)

# --- TAB 2: วางแผน ---
with tab2:
    c_y, c_t, c_g = st.columns(3)
    yr = c_y.selectbox("ปีการศึกษา", [1, 2, 3, 4]); tm = c_t.selectbox("เทอม", ["1", "2", "S"])
    grad = c_g.toggle("🎓 ขอจบ (ลงได้สูงสุด 30/12 หน่วย)")
    curr_tk = f"Y{yr}T{tm}"
    
    # คำนวณหน่วยกิตเทอมปัจจุบัน
    current_credits = sum([all_courses_db[v.split(" | ")[0]][0] for v in st.session_state.study_plan[curr_tk].values() if v != "-"])
    
    # ตั้งเกณฑ์หน่วยกิต
    max_c = 9 if tm == "S" else 22
    if grad: max_c = 12 if tm == "S" else 30 # กรณีขอจบ

    st.markdown(f"### กำลังวางแผน: ปี {yr} เทอม {tm}")
    if current_credits > max_c:
        st.markdown(f'<div class="credit-alert">⚠️ ลงเกิน! เทอม {tm} ลงได้ไม่เกิน {max_c} หน่วยกิต (ตอนนี้ {current_credits})</div>', unsafe_allow_html=True)
    else:
        st.markdown(f"**หน่วยกิตรวมเทอมนี้:** {current_credits} / {max_c}")

    st.divider()
    used = [v.split(" | ")[0] for tk, s in st.session_state.study_plan.items() if tk != curr_tk for v in s.values() if v != "-"]
    slots = ["1A", "1B", "2A", "2B", "3A", "3B", "4A", "4B"]
    rows = st.columns(4)
    for i, sn in enumerate(slots):
        with rows[i % 4]:
            st.markdown(f"**📌 คาบ {sn}**")
            valid = ["-"] + [f"{c} | {all_courses_db[c][3]}" for c in all_courses_db if all_courses_db[c][1] == sn[0] and all_courses_db[c][2] == sn[1] and c not in used]
            v_key = f"{curr_tk}_{sn}"
            ver = st.session_state.slot_versions[v_key]
            choice = st.selectbox(f"S_{sn}", options=valid, key=f"w_{v_key}_v{ver}", label_visibility="collapsed")
            st.session_state.study_plan[curr_tk][sn] = choice
            if choice != "-":
                st.button(f"🗑️ ลบ {sn}", key=f"d_{v_key}", on_click=handle_clear_slot, args=(curr_tk, sn))

    # ตารางสรุป 4 ปี
    st.divider()
    st.markdown("### 🗓️ ตารางสรุปแผนการเรียนภาพรวม 4 ปี")
    html = "<table class='overall-table'><tr><th>ปี</th><th>เทอม 1 (Max 22)</th><th>เทอม 2 (Max 22)</th><th>เทอม S (Max 9)</th></tr>"
    for y in range(1, 5):
        html += f"<tr><td><b>ปี {y}</b></td>"
        for t in ["1", "2", "S"]:
            tk = f"Y{y}T{t}"; cell, tc = "", 0
            for sn, val in st.session_state.study_plan[tk].items():
                if val != "-":
                    c = val.split(" | ")[0]; cell += f"<span class='sub-tag'>{sn}: {val}</span>"; tc += all_courses_db[c][0]
            limit = 9 if t == "S" else 22
            c_style = "color:red; font-weight:bold;" if tc > limit else "color:black;"
            html += f"<td>{cell}<span style='{c_style}'>รวม {tc} นก.</span></td>"
        html += "</tr>"
    st.markdown(html + "</table>", unsafe_allow_html=True)
    st.button("♻️ ล้างแผนทั้งหมด", on_click=handle_clear_all)

st.markdown("---")
if st.button("🧧 สนับสนุนค่าน้ำชาผู้พัฒนา", use_container_width=True): show_donate()
