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