from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import io

def generate_overlay(data):
    packet = io.BytesIO()
    # สร้าง canvas บนกระดาษ A4
    can = canvas.Canvas(packet, pagesize=(595.27, 841.89))
    
    # อย่าลืมใส่ไฟล์ฟอนต์ THSarabunNew.ttf ในโฟลเดอร์เดียวกัน
    pdfmetrics.registerFont(TTFont('ThaiFont', 'THSarabunNew.ttf'))
    can.setFont('ThaiFont', 16)

    # 1. ข้อมูลคดี
    can.drawString(435, 775, to_thai_num(data['black_case_num'])) # 
    can.drawString(360, 710, data['court_name'])                  # 
    can.drawString(315, 682, to_thai_num(data['day']))            # 
    can.drawString(370, 682, data['month'])                       # 
    can.drawString(495, 682, to_thai_num(data['year']))           # 

    # 2. ข้อมูลคู่ความ
    can.drawString(200, 615, data['plaintiff_name'])              # 
    can.drawString(200, 565, data['defendant_name'])              # 

    # 3. เนื้อหาฟ้อง (ต้องใช้คำสั่ง wrap text หากยาวเกินไป)
    text_object = can.beginText(135, 165)                         # 
    text_object.setFont('ThaiFont', 16)
    for line in data['case_body'].split('\n'):
        text_object.textLine(line)
    can.drawText(text_object)

    can.save()
    packet.seek(0)
    return packet
