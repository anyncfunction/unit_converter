
import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from units import get_categories, get_units
from converter import convert, format_result, validate_input
from history import save_history, load_history, clear_history, format_history_item


# 颜色配置
COLORS = {
    "bg": "#0d0d0d",
    "card_bg": "#1a1a1a",
    "accent": "#ff00ff",
    "accent2": "#00ffff",
    "accent3": "#ff3366",
    "text": "#ffffff",
    "text_dim": "#888888",
    "input_bg": "#252525",
    "success": "#00ff88",
    "error": "#ff3366",
}


class UnitConverterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("⚡ 单位换算器")
        self.root.geometry("1000x720")
        self.root.resizable(False, False)
        self.root.configure(bg=COLORS["bg"])

        self.current_category = tk.StringVar(value="长度")
        self.current_from_unit = tk.StringVar()
        self.current_to_unit = tk.StringVar()

        self.setup_ui()

    def setup_ui(self):
        """创建界面"""
        # 标题
        self.create_header()

        # 主内容（左右布局）
        main = tk.Frame(self.root, bg=COLORS["bg"])
        main.pack(fill=tk.BOTH, expand=True, padx=30, pady=15)

        # 左侧卡片
        left_card = self.make_card(main, "🔄 单位转换")
        self.build_converter_ui(left_card)

        # 右侧卡片
        right_card = self.make_card(main, "📜 换算历史")
        self.build_history_ui(right_card)

        # 底部版权
        self.create_footer()

        # 初始化
        self.on_category_change()
        self.refresh_history()

    def make_card(self, parent, title):
        """创建卡片"""
        card = tk.Frame(parent, bg=COLORS["card_bg"], relief=tk.FLAT)
        card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 12))

        # 顶部彩色条
        top = tk.Frame(card, bg=COLORS["card_bg"], height=3)
        top.pack(fill=tk.X)
        for c in [COLORS["accent"], COLORS["accent2"], COLORS["accent3"]]:
            tk.Frame(top, bg=c, height=3).pack(side=tk.LEFT, expand=True)

        tk.Label(card, text=title, font=("Microsoft YaHei", 14, "bold"),
                bg=COLORS["card_bg"], fg=COLORS["text"]).pack(anchor="w", padx=15, pady=12)

        content = tk.Frame(card, bg=COLORS["card_bg"])
        content.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        return content

    def build_converter_ui(self, parent):
        """构建换算界面"""
        # 类型选择
        row = tk.Frame(parent, bg=COLORS["card_bg"])
        row.pack(fill=tk.X, pady=(0, 12))
        tk.Label(row, text="类型:", font=("Microsoft YaHei", 11),
                bg=COLORS["card_bg"], fg=COLORS["text_dim"]).pack(side=tk.LEFT)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TCombobox", fieldbackground=COLORS["input_bg"],
                       foreground=COLORS["text"], background=COLORS["card_bg"])

        self.category_combo = ttk.Combobox(row, textvariable=self.current_category,
            values=get_categories(), state="readonly", font=("Microsoft YaHei", 11), width=14)
        self.category_combo.pack(side=tk.LEFT, padx=(10, 0))
        self.category_combo.bind("<<ComboboxSelected>>", lambda e: self.on_category_change())

        # 输入框背景
        box = tk.Frame(parent, bg=COLORS["input_bg"])
        box.pack(fill=tk.X, pady=5)

        # 数值输入
        r1 = tk.Frame(box, bg=COLORS["input_bg"])
        r1.pack(fill=tk.X, padx=15, pady=8)
        tk.Label(r1, text="数值:", font=("Microsoft YaHei", 11),
                bg=COLORS["input_bg"], fg=COLORS["text_dim"], width=8, anchor="e").pack(side=tk.LEFT)
        self.value_entry = tk.Entry(r1, font=("Microsoft YaHei", 14), bg=COLORS["card_bg"],
                                    fg=COLORS["accent2"], relief=tk.FLAT, insertbackground=COLORS["accent2"])
        self.value_entry.pack(side=tk.LEFT, padx=(10, 0), fill=tk.X, expand=True)

        # 原单位
        r2 = tk.Frame(box, bg=COLORS["input_bg"])
        r2.pack(fill=tk.X, padx=15, pady=8)
        tk.Label(r2, text="从:", font=("Microsoft YaHei", 11),
                bg=COLORS["input_bg"], fg=COLORS["text_dim"], width=8, anchor="e").pack(side=tk.LEFT)
        self.from_unit_combo = ttk.Combobox(r2, textvariable=self.current_from_unit,
            state="readonly", font=("Microsoft YaHei", 11), width=22)
        self.from_unit_combo.pack(side=tk.LEFT, padx=(10, 0), fill=tk.X, expand=True)

        # 目标单位
        r3 = tk.Frame(box, bg=COLORS["input_bg"])
        r3.pack(fill=tk.X, padx=15, pady=8)
        tk.Label(r3, text="到:", font=("Microsoft YaHei", 11),
                bg=COLORS["input_bg"], fg=COLORS["text_dim"], width=8, anchor="e").pack(side=tk.LEFT)
        self.to_unit_combo = ttk.Combobox(r3, textvariable=self.current_to_unit,
            state="readonly", font=("Microsoft YaHei", 11), width=22)
        self.to_unit_combo.pack(side=tk.LEFT, padx=(10, 0), fill=tk.X, expand=True)

        # 转换按钮
        tk.Button(parent, text="⚡ 开始转换", font=("Microsoft YaHei", 14, "bold"),
                 bg=COLORS["accent"], fg="white", relief=tk.FLAT, padx=30, pady=8,
                 cursor="hand2", command=self.do_convert).pack(pady=12)

        self.value_entry.bind("<Return>", lambda e: self.do_convert())

        # 结果显示
        res_box = tk.Frame(parent, bg=COLORS["input_bg"])
        res_box.pack(fill=tk.BOTH, expand=True, pady=(8, 0))

        self.result_label = tk.Label(res_box, text="输入数值\n点击转换",
                                    font=("Microsoft YaHei", 18, "bold"),
                                    bg=COLORS["input_bg"], fg=COLORS["accent2"],
                                    justify=tk.CENTER)
        self.result_label.pack(expand=True, fill=tk.BOTH)

    def build_history_ui(self, parent):
        """构建历史记录界面"""
        # 列表框区域
        list_frame = tk.Frame(parent, bg=COLORS["input_bg"])
        list_frame.pack(fill=tk.BOTH, expand=True)

        self.history_listbox = tk.Listbox(list_frame, font=("Consolas", 11),
            bg=COLORS["input_bg"], fg=COLORS["text"], selectbackground=COLORS["accent"],
            selectforeground="white", relief=tk.FLAT, borderwidth=0, highlightthickness=0)
        self.history_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        scroll = tk.Scrollbar(list_frame, bg=COLORS["input_bg"])
        scroll.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 5))
        scroll.config(command=self.history_listbox.yview)
        self.history_listbox.config(yscrollcommand=scroll.set)

        # 按钮
        btn_frame = tk.Frame(parent, bg=COLORS["card_bg"])
        btn_frame.pack(fill=tk.X, pady=(10, 0))

        for txt, cmd in [("🔄 刷新", self.refresh_history), ("🗑️ 清空", self.clear_history)]:
            tk.Button(btn_frame, text=txt, font=("Microsoft YaHei", 10),
                     bg=COLORS["card_bg"], fg=COLORS["text"], relief=tk.FLAT,
                     padx=15, pady=5, cursor="hand2", command=cmd).pack(side=tk.LEFT, padx=5)

    def create_header(self):
        """顶部标题"""
        h = tk.Frame(self.root, bg=COLORS["bg"], height=70)
        h.pack(fill=tk.X)
        h.pack_propagate(False)

        tk.Label(h, text="⚡ 单位换算器", font=("Microsoft YaHei", 28, "bold"),
                bg=COLORS["bg"], fg=COLORS["accent"]).pack(side=tk.LEFT, pady=12)

        # 装饰条
        d = tk.Frame(h, bg=COLORS["bg"])
        d.pack(side=tk.RIGHT, pady=15, padx=20)
        for c in [COLORS["accent"], COLORS["accent2"], COLORS["accent3"]]:
            tk.Frame(d, bg=c, width=4, height=30).pack(side=tk.LEFT, padx=3)

    def create_footer(self):
        """底部版权"""
        f = tk.Frame(self.root, bg=COLORS["bg"])
        f.pack(fill=tk.X, pady=12)

        # 分隔线
        line = tk.Frame(f, bg=COLORS["bg"], height=2)
        line.pack(fill=tk.X, padx=30)
        for c in [COLORS["accent"], COLORS["accent2"], COLORS["accent3"]]:
            tk.Frame(line, bg=c, height=2).pack(side=tk.LEFT, expand=True)

        # 版权文字
        tk.Label(f, text="© 2025 Made by 肥鱼不是胖猫", font=("Microsoft YaHei", 14, "bold"),
                bg=COLORS["bg"], fg=COLORS["accent"]).pack(pady=(12, 0))
        tk.Label(f, text="GitHub: @anyncfunction", font=("Microsoft YaHei", 10),
                bg=COLORS["bg"], fg=COLORS["text_dim"]).pack(pady=(2, 0))

    def on_category_change(self):
        category = self.current_category.get()
        units = get_units(category)
        self.from_unit_combo["values"] = units
        self.to_unit_combo["values"] = units
        if len(units) >= 2:
            self.from_unit_combo.current(0)
            self.to_unit_combo.current(1)
        elif units:
            self.from_unit_combo.current(0)
            self.to_unit_combo.current(0)

    def do_convert(self):
        value_str = self.value_entry.get().strip()
        from_unit = self.current_from_unit.get()
        to_unit = self.current_to_unit.get()
        category = self.current_category.get()

        if not value_str:
            self.show_result("请输入数值！", error=True)
            return

        valid, value = validate_input(value_str)
        if not valid:
            self.show_result(valid, error=True)
            return

        try:
            result = convert(value, from_unit, to_unit, category)
            result_str = format_result(result)
            self.show_result(f"{value_str} {from_unit}\n    ↓\n{result_str} {to_unit}")
            save_history(from_unit, to_unit, value_str, result_str, category)
            self.refresh_history()
        except Exception as e:
            self.show_result(str(e), error=True)

    def show_result(self, text, error=False):
        self.result_label.config(text=text, fg=COLORS["error"] if error else COLORS["success"])

    def refresh_history(self):
        self.history_listbox.delete(0, tk.END)
        history = load_history()
        if not history:
            self.history_listbox.insert(0, "  暂无换算记录")
            return
        for item in history:
            self.history_listbox.insert(tk.END, "  " + format_history_item(item))

    def clear_history(self):
        if messagebox.askyesno("确认", "确定要清空所有历史记录吗？"):
            clear_history()
            self.refresh_history()
            messagebox.showinfo("提示", "历史记录已清空")


def create_gui():
    root = tk.Tk()
    UnitConverterGUI(root)
    root.mainloop()


if __name__ == "__main__":
    create_gui()