<<<<<<< HEAD
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
=======
"""
换算核心模块
处理各种单位之间的换算
"""
import math
from units import UNIT_DATA


def convert(value, from_unit, to_unit, category):
    """
    单位换算

    Args:
        value: 要转换的数值
        from_unit: 原单位
        to_unit: 目标单位
        category: 换算类型

    Returns:
        换算结果（浮点数）

    Raises:
        ValueError: 无效的单位或类型不匹配
    """
    if category not in UNIT_DATA:
        raise ValueError(f"未知的换算类型: {category}")

    # 温度需要特殊处理
    if category == "温度":
        return convert_temperature(value, from_unit, to_unit)

    units = UNIT_DATA[category]
    if not isinstance(units, dict):
        raise ValueError(f"类型 {category} 不支持换算")

    if from_unit not in units:
        raise ValueError(f"未知单位: {from_unit}")

    if to_unit not in units:
        raise ValueError(f"未知单位: {to_unit}")

    # 转换为基准值，再转换为目标单位
    base_value = float(value) * units[from_unit]
    result = base_value / units[to_unit]

    # 处理精度问题
    if abs(result) < 1e-10:
        return 0.0

    # 四舍五入到合理精度
    return round(result, 10)


def convert_temperature(value, from_unit, to_unit):
    """
    温度单位换算（特殊处理）

    Args:
        value: 温度值
        from_unit: 原单位
        to_unit: 目标单位

    Returns:
        换算结果
    """
    # 先转换为摄氏度
    celsius = 0.0
    if from_unit == "摄氏度 (°C)":
        celsius = float(value)
    elif from_unit == "华氏度 (°F)":
        celsius = (float(value) - 32) * 5 / 9
    elif from_unit == "开尔文 (K)":
        celsius = float(value) - 273.15
    else:
        raise ValueError(f"未知温度单位: {from_unit}")

    # 从摄氏度转换为目标单位
    if to_unit == "摄氏度 (°C)":
        result = celsius
    elif to_unit == "华氏度 (°F)":
        result = celsius * 9 / 5 + 32
    elif to_unit == "开尔文 (K)":
        result = celsius + 273.15
    else:
        raise ValueError(f"未知温度单位: {to_unit}")

    return round(result, 2)


def format_result(value):
    """
    格式化结果，去除不必要的精度

    Args:
        value: 数值结果

    Returns:
        格式化后的字符串
    """
    if value == 0:
        return "0"

    # 如果是整数，直接返回
    if isinstance(value, int) or (isinstance(value, float) and value.is_integer()):
        return str(int(value))

    # 否则保留合理的小数位
    if abs(value) >= 1000:
        return f"{value:.2f}"
    elif abs(value) >= 1:
        return f"{value:.4f}".rstrip('0').rstrip('.')
    else:
        return f"{value:.6f}".rstrip('0').rstrip('.')


def validate_input(value_str):
    """
    验证输入是否为有效的数字

    Args:
        value_str: 输入的字符串

    Returns:
        (是否有效, 数值 or 错误信息)
    """
    try:
        value = float(value_str)
        return True, value
    except ValueError:
        return False, "请输入有效的数字"


if __name__ == "__main__":
    # 测试
    print(convert(100, "厘米 (cm)", "米 (m)", "长度"))
    print(convert(1, "千米 (km)", "米 (m)", "长度"))
    print(convert(0, "摄氏度 (°C)", "华氏度 (°F)", "温度"))
    print(convert(100, "摄氏度 (°C)", "华氏度 (°F)", "温度"))
>>>>>>> 004a9208a5964b26d8fec900de1339cba22f2173
