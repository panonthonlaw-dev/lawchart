from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm

def draw_court_form_4(can, data):
    # --- 1. วาดส่วนหัว (Header) ---
    can.setFont('ThaiFont', 14)
    can.drawString(50, 780, "(๔)") # เลขแบบพิมพ์ 
    can.drawCentredString(300, 780, "คำฟ้อง") # 
    
    # วาดตราครุฑ (สมมติว่ามีไฟล์ garuda.png)
    # can.drawImage("garuda.png", 275, 790, width=50, height=50) # 
    
    can.setFont('ThaiFont', 15)
    can.drawString(400, 750, f"คดีหมายเลขดำที่ ........................ / ๒๕..........") # [cite: 2, 3]
    can.drawString(330, 710, f"ศาล {data['court']}") # [cite: 7]
    can.drawString(300, 685, f"วันที่ {to_thai_num(data['day'])} เดือน {data['month']} พุทธศักราช ๒๕ {to_thai_num(data['year'])}") # [cite: 8, 9]
    can.drawString(330, 660, f"ความ {data['case_type']}") # [cite: 10]

    # --- 2. วาดส่วนคู่ความ (Parties) ---
    can.drawString(50, 600, "ระหว่าง") # [cite: 4]
    can.line(150, 615, 550, 615) # เส้นบรรทัดโจทก์
    can.drawString(560, 610, "โจทก์") # [cite: 11]
    can.line(150, 570, 550, 570) # เส้นบรรทัดจำเลย
    can.drawString(560, 565, "จำเลย") # [cite: 12]

    # --- 3. วาดส่วนทุนทรัพย์ ---
    can.drawString(70, 530, f"ข้อหาหรือฐานความผิด .........................................................................................................")
    can.drawString(70, 505, f"จำนวนทุนทรัพย์ {to_thai_num(data['capital_baht'])} บาท {to_thai_num(data['capital_stang'])} สตางค์") # [cite: 13, 14]

    # --- 4. วาดส่วนรายละเอียด (ข้าพเจ้า...) ---
    can.drawString(130, 475, f"ข้าพเจ้า {data['plaintiff']['name']}") # [cite: 11, 15]
    # วาดเส้นและข้อมูลที่อยู่แยกตามฟิลด์ [cite: 19-32]
    # (ใช้ Logic เดียวกันกับจำเลย [cite: 33-46])
    
    # --- 5. วาดเส้นบรรทัดสำหรับเนื้อหาฟ้อง ---
    y = 150 # จุดเริ่ม ข้อ ๑ 
    can.drawString(130, y, "ข้อ ๑. ") # 
    # วาดเส้นประรอรับข้อมูล
    for i in range(10):
        can.line(70, y - (i*25) - 5, 550, y - (i*25) - 5)
