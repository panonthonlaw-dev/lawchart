import streamlit as st
import os
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pypdf import PdfReader, PdfWriter
import io
import textwrap

def create_pdf_overlay(data):
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=(595.27, 841.89))
    pdfmetrics.registerFont(TTFont('ThaiFont', 'THSarabunNew.ttf'))
    can.setFont('ThaiFont', 15)

    # --- [ส่วนหัวคดี] อ้างอิงจากรูปภาพ image_8585e0.png ---
    can.drawString(445, 764, to_thai_num(data['black_num'])) # คดีหมายเลขดำที่ 
    can.drawString(360, 706, data['court']) # ศาล 
    can.drawString(308, 680, to_thai_num(data['day'])) # วันที่ [cite: 8]
    can.drawString(365, 680, data['month']) # เดือน [cite: 8]
    can.drawString(495, 680, to_thai_num(data['year'])) # พุทธศักราช [cite: 9]
    can.drawString(340, 652, data['case_type']) # ความ 

    # --- [ส่วนคู่ความและทุนทรัพย์] อ้างอิงจากรูปภาพ image_875abb.png ---
    can.drawString(250, 595, data['plaintiff']['name']) # ระหว่าง โจทก์ [cite: 11]
    can.drawString(250, 550, data['defendant']['name']) # จำเลย [cite: 12]
    can.drawString(250, 518, data['charge']) # ข้อหาหรือฐานความผิด 
    can.drawString(250, 492, to_thai_num(data['capital_baht'])) # จำนวนทุนทรัพย์ (บาท) [cite: 6, 13]
    can.drawString(510, 492, to_thai_num(data['capital_stang'])) # (สตางค์) [cite: 14]

    # --- [รายละเอียดบุคคล] ตามที่คุณต้องการ (แยกช่องกรอก) ---
    # โจทก์ (ข้าพเจ้า...) [cite: 15-32]
    can.drawString(245, 466, data['plaintiff']['name'])
    draw_party_details(can, data['plaintiff'], 440) # ปรับ Y ลงมาตามลำดับ

    # จำเลย (ขอยื่นฟ้อง...) [cite: 33-47]
    can.drawString(245, 258, data['defendant']['name'])
    draw_party_details(can, data['defendant'], 232)

    # --- [เนื้อหาฟ้อง ข้อ ๑] --- [cite: 48]
    # ... (ส่วนเดิม)
