# mixed-bed-toolkit-kmutnb-powerplant

เครื่องมือช่วยคำนวณสำหรับระบบผลิตน้ำบริสุทธิ์ Reverse Osmosis (RO) และ Mixed Bed

## ความสามารถ

- คำนวณสมดุลการไหลของระบบ RO (Permeate/Concentrate)
- คำนวณ Salt Rejection, Salt Passage และค่าการนำไฟฟ้าฝั่ง Permeate โดยประมาณ
- คำนวณปริมาณ TDS ที่ต้องกำจัดในระบบ Mixed Bed
- ประมาณปริมาตรเรซินที่ต้องใช้จากอัตราการไหล, เวลาเดินระบบ และสมรรถนะเรซิน

## การใช้งาน

### 1) Reverse Osmosis

```bash
python calculator.py ro \
  --feed-flow-m3h 10 \
  --recovery-percent 75 \
  --feed-conductivity-us-cm 500 \
  --salt-rejection-percent 98
```

### 2) Mixed Bed

```bash
python calculator.py mixed-bed \
  --flow-m3h 5 \
  --runtime-hours 8 \
  --influent-conductivity-us-cm 30 \
  --effluent-conductivity-us-cm 1 \
  --resin-capacity-kg-tds-per-l 0.08
```

## ทดสอบ

```bash
python -m unittest
```
