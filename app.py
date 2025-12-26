def draw_person(can, data, start_y):
    # บรรทัดที่ 1: เลขบัตร [cite: 19], เชื้อชาติ [cite: 25]
    can.drawString(185, start_y, to_thai_num(data['id']))
    can.drawString(490, start_y, data['race'])
    
    # บรรทัดที่ 2: สัญชาติ [cite: 23], อาชีพ [cite: 20], อายุ [cite: 26], บ้านเลขที่ [cite: 26], หมู่ [cite: 27]
    y2 = start_y - 26
    can.drawString(100, y2, data['nat'])
    can.drawString(250, y2, data['job'])
    can.drawString(455, y2, to_thai_num(data['age']))
    can.drawString(530, y2, to_thai_num(data['h_no']))
    can.drawString(575, y2, to_thai_num(data['moo']))
    
    # บรรทัดที่ 3: ถนน [cite: 24], ซอย [cite: 21], ตำบล [cite: 28], อำเภอ [cite: 29]
    y3 = y2 - 26
    can.drawString(100, y3, data['road'])
    can.drawString(250, y3, data['soi'])
    can.drawString(400, y3, data['sub_d'])
    can.drawString(520, y3, data['dist'])
    
    # บรรทัดที่ 4: จังหวัด [cite: 16], รหัสไปรษณีย์ [cite: 30], โทรศัพท์ [cite: 31]
    y4 = y3 - 26
    can.drawString(100, y4, data['prov'])
    can.drawString(380, y4, to_thai_num(data['post']))
    can.drawString(480, y4, to_thai_num(data['tel']))
