"""单位换算核心逻辑"""
import json
import os

# 单位数据
UNITS = {
    "长度": {"米 (m)": 1, "千米 (km)": 1000, "厘米 (cm)": 0.01, "毫米 (mm)": 0.001,
             "英里 (mi)": 1609.344, "码 (yd)": 0.9144, "英尺 (ft)": 0.3048, "英寸 (in)": 0.0254},
    "重量": {"千克 (kg)": 1, "克 (g)": 0.001, "吨 (t)": 1000, "磅 (lb)": 0.453592, "盎司 (oz)": 0.0283495, "斤": 0.5},
    "温度": ["摄氏度 (°C)", "华氏度 (°F)", "开尔文 (K)"],
    "体积": {"升 (L)": 1, "毫升 (mL)": 0.001, "立方米 (m³)": 1000, "加仑 (gal)": 3.78541, "杯": 0.236588},
    "面积": {"平方米 (m²)": 1, "平方千米 (km²)": 1e6, "公顷 (ha)": 10000, "亩": 666.667, "英亩 (acre)": 4046.86},
    "速度": {"米/秒 (m/s)": 1, "千米/时 (km/h)": 0.277778, "英里/时 (mph)": 0.44704, "节 (kn)": 0.514444},
    "时间": {"秒 (s)": 1, "毫秒 (ms)": 0.001, "分钟 (min)": 60, "小时 (h)": 3600, "天 (d)": 86400, "周": 604800, "年": 31536000}
}

HISTORY_FILE = "converter_history.json"

def convert(value, from_u, to_u, cat):
    if cat == "温度":
        c = value if from_u == "摄氏度 (°C)" else (value - 32) * 5/9 if from_u == "华氏度 (°F)" else value - 273.15
        if to_u == "摄氏度 (°C)": return round(c, 4)
        if to_u == "华氏度 (°F)": return round(c * 9/5 + 32, 4)
        return round(c + 273.15, 4)

    data = UNITS.get(cat, {})
    base = float(value) * data[from_u]
    return round(base / data[to_u], 6)

def get_categories(): return list(UNITS.keys())
def get_units(cat): return list(UNITS.get(cat, {}).keys()) if isinstance(UNITS.get(cat), dict) else UNITS.get(cat, [])

def save_history(from_u, to_u, val, res, cat):
    h = load_history()
    h.insert(0, {"cat": cat, "from": from_u, "to": to_u, "val": val, "res": res})
    with open(HISTORY_FILE, "w") as f: json.dump(h[:50], f)

def load_history():
    try:
        with open(HISTORY_FILE, "r") as f: return json.load(f)
    except: return []

def clear_history():
    try: os.remove(HISTORY_FILE)
    except: pass