"""
历史记录模块
保存和管理换算历史
"""
import json
import os
from datetime import datetime

# 历史记录文件路径
HISTORY_FILE = "converter_history.json"
MAX_HISTORY = 50  # 最多保存50条记录


def get_history_path():
    """获取历史记录文件路径"""
    return os.path.join(os.path.dirname(__file__), HISTORY_FILE)


def save_history(from_unit, to_unit, value, result, category):
    """
    保存一条换算历史

    Args:
        from_unit: 原单位
        to_unit: 目标单位
        value: 原始数值
        result: 换算结果
        category: 换算类型
    """
    history = load_history()

    # 创建记录
    record = {
        "category": category,
        "from_unit": from_unit,
        "to_unit": to_unit,
        "value": str(value),
        "result": str(result),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    # 添加到历史记录（最新在前）
    history.insert(0, record)

    # 限制记录数量
    if len(history) > MAX_HISTORY:
        history = history[:MAX_HISTORY]

    # 写入文件
    try:
        with open(get_history_path(), "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"保存历史记录失败: {e}")


def load_history():
    """
    加载历史记录

    Returns:
        历史记录列表
    """
    path = get_history_path()

    if not os.path.exists(path):
        return []

    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"加载历史记录失败: {e}")
        return []


def clear_history():
    """清空所有历史记录"""
    path = get_history_path()

    try:
        if os.path.exists(path):
            os.remove(path)
        return True
    except Exception as e:
        print(f"清空历史记录失败: {e}")
        return False


def get_last_conversion():
    """
    获取上一次换算

    Returns:
        最近的换算记录，如果没有返回None
    """
    history = load_history()
    if history:
        return history[0]
    return None


def format_history_item(record):
    """
    格式化单条历史记录为显示字符串

    Args:
        record: 历史记录字典

    Returns:
        格式化的字符串
    """
    return f"{record['value']} {record['from_unit']} → {record['result']} {record['to_unit']}"


if __name__ == "__main__":
    # 测试
    save_history("米 (m)", "英尺 (ft)", 1, 3.281, "长度")
    save_history("千克 (kg)", "磅 (lb)", 1, 2.205, "重量")

    history = load_history()
    print(f"共 {len(history)} 条记录:")
    for item in history:
        print(format_history_item(item))

    # 测试获取上一次
    last = get_last_conversion()
    if last:
        print(f"\n上一次换算: {format_history_item(last)}")

    # 清空测试
    # clear_history()