"""GUI版本"""
import tkinter as tk
from tkinter import ttk, messagebox
from converter import convert, get_categories, get_units, save_history, load_history, clear_history

COLORS = {"bg": "#0d0d0d", "card": "#1a1a1a", "accent": "#ff00ff", "accent2": "#00ffff", "text": "#fff", "dim": "#888", "input": "#252525"}

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("单位换算器")
        self.root.geometry("900x600")
        self.root.configure(bg=COLORS["bg"])

        self.cat = tk.StringVar(value="长度")
        self.from_u = tk.StringVar()
        self.to_u = tk.StringVar()

        self.build_ui()

    def build_ui(self):
        tk.Label(self.root, text="⚡ 单位换算器", font=("Microsoft YaHei", 24, "bold"),
                bg=COLORS["bg"], fg=COLORS["accent"]).pack(pady=15)

        main = tk.Frame(self.root, bg=COLORS["bg"])
        main.pack(fill=tk.BOTH, expand=True, padx=20)

        # 左侧
        left = tk.Frame(main, bg=COLORS["card"])
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        tk.Label(left, text="🔄 转换", font=("Microsoft YaHei", 14, "bold"),
                bg=COLORS["card"], fg=COLORS["text"]).pack(anchor="w", padx=15, pady=10)

        f = tk.Frame(left, bg=COLORS["card"])
        f.pack(fill=tk.X, padx=15)
        tk.Label(f, text="类型:", bg=COLORS["card"], fg=COLORS["dim"]).pack(side=tk.LEFT)

        self.combo_cat = ttk.Combobox(f, textvariable=self.cat, values=get_categories(),
                                       state="readonly", width=12)
        self.combo_cat.pack(side=tk.LEFT, padx=10)
        self.combo_cat.bind("<<ComboboxSelected>>", lambda e: self.update_units())

        box = tk.Frame(left, bg=COLORS["input"])
        box.pack(fill=tk.X, padx=15, pady=10)

        tk.Label(box, text="数值:", bg=COLORS["input"], fg=COLORS["dim"]).grid(row=0, column=0, pady=5)
        self.ent_val = tk.Entry(box, bg=COLORS["card"], fg=COLORS["accent2"], font=("Microsoft YaHei", 14))
        self.ent_val.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        tk.Label(box, text="从:", bg=COLORS["input"], fg=COLORS["dim"]).grid(row=1, column=0, pady=5)
        self.combo_from = ttk.Combobox(box, textvariable=self.from_u, state="readonly", width=18)
        self.combo_from.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        tk.Label(box, text="到:", bg=COLORS["input"], fg=COLORS["dim"]).grid(row=2, column=0, pady=5)
        self.combo_to = ttk.Combobox(box, textvariable=self.to_u, state="readonly", width=18)
        self.combo_to.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        box.columnconfigure(1, weight=1)

        tk.Button(left, text="⚡ 转换", font=("Microsoft YaHei", 12, "bold"),
                 bg=COLORS["accent"], fg="white", relief=tk.FLAT, padx=30, pady=8,
                 command=self.do_convert).pack(pady=10)
        self.ent_val.bind("<Return>", lambda e: self.do_convert())

        self.lbl_result = tk.Label(left, text="输入数值\n点击转换", font=("Microsoft YaHei", 18, "bold"),
                                   bg=COLORS["input"], fg=COLORS["accent2"], justify=tk.CENTER)
        self.lbl_result.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        # 右侧
        right = tk.Frame(main, bg=COLORS["card"])
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        tk.Label(right, text="📜 历史", font=("Microsoft YaHei", 14, "bold"),
                bg=COLORS["card"], fg=COLORS["text"]).pack(anchor="w", padx=15, pady=10)

        self.lst = tk.Listbox(right, font=("Consolas", 11), bg=COLORS["input"],
                             fg=COLORS["text"], selectbackground=COLORS["accent"], relief=tk.FLAT, borderwidth=0)
        self.lst.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)

        btn_f = tk.Frame(right, bg=COLORS["card"])
        btn_f.pack(pady=5)
        tk.Button(btn_f, text="🔄", bg=COLORS["card"], fg=COLORS["text"], relief=tk.FLAT,
                 command=self.refresh).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_f, text="🗑️", bg=COLORS["card"], fg=COLORS["text"], relief=tk.FLAT,
                 command=self.clear).pack(side=tk.LEFT, padx=5)

        tk.Label(self.root, text="© 2025 by 肥鱼不是胖猫", font=("Microsoft YaHei", 11),
                bg=COLORS["bg"], fg=COLORS["accent"]).pack(pady=10)

        self.update_units()
        self.refresh()

    def update_units(self):
        us = get_units(self.cat.get())
        self.combo_from["values"] = us
        self.combo_to["values"] = us
        if len(us) >= 2:
            self.combo_from.current(0)
            self.combo_to.current(1)

    def do_convert(self):
        try:
            v = float(self.ent_val.get())
            r = convert(v, self.from_u.get(), self.to_u.get(), self.cat.get())
            s = f"{v} {self.from_u.get()}\n    ↓\n{r} {self.to_u.get()}"
            self.lbl_result.config(text=s, fg=COLORS["accent2"])
            save_history(self.from_u.get(), self.to_u.get(), str(v), str(r), self.cat.get())
            self.refresh()
        except ValueError:
            self.lbl_result.config(text="请输入有效数字!", fg="#ff3366")
        except Exception as e:
            self.lbl_result.config(text=str(e), fg="#ff3366")

    def refresh(self):
        self.lst.delete(0, tk.END)
        for h in load_history():
            self.lst.insert(tk.END, f"{h['val']} {h['from']} → {h['res']} {h['to']}")

    def clear(self):
        if messagebox.askyesno("确认", "清空历史?"):
            clear_history()
            self.refresh()

if __name__ == "__main__":
    tk.Tk().withdraw()
    root = tk.Tk()
    App(root)
    root.mainloop()