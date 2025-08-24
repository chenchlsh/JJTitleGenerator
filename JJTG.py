import tkinter as tk
from tkinter import messagebox

# ===================== 数据：四列词汇 =====================
COL1 = [
    "进入娱乐圈后",
    "嫁进豪门后",
    "穿越后",
    "失忆后",
    "重生后",
    "C位出道后",
    "获得金手指后",
    "抑制剂失效后",
    "逃婚后",
    "分手后",
]

COL2 = [
    "被虐得体无完肤的我",
    "当替身的我",
    "想当绿茶的我",
    "遍地仇家的我",
    "被迫营业的我",
    "拒绝恋爱脑沉迷赚钱的我",
    "只想当咸鱼的我",
    "觉醒精神体的我",
    "带球跑的我",
    "变成美强惨的我",
]

COL3 = [
    "和死对头",
    "和渣攻",
    "和最强战力",
    "和白月光",
    "和反派BOSS",
    "和超人气主播",
    "和前男友",
    "和暗恋对象",
    "和影帝",
    "和男神",
]

COL4 = [
    "崩人设了",
    "HE了",
    "一起种田了",
    "通关了逃生游戏",
    "双向攻略了",
    "改写了原作剧情",
    "被系统绑定了",
    "联手复仇了",
    "称霸末世了",
    "成为了双人机甲驾驶员",
]

COLUMNS = [COL1, COL2, COL3, COL4]

# ===================== 应用 =====================
class JJTitleGenerator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("晋江文热榜标题生成器")
        self.configure(bg="white")

        # 顶部标题（始终保留）
        self.title_label = tk.Label(
            self,
            text="晋江文热榜标题生成器",
            bg="white",
            fg="black",
            font=("PingFang SC", 24, "bold"),
        )
        self.title_label.pack(pady=(20, 10))

        # 可变内容区域（提交后会清空重建）
        self.content_frame = tk.Frame(self, bg="white")
        self.content_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        # 底部签名
        self.signature = tk.Label(
            self,
            text="Design by LS",
            bg="white",
            fg="black",
            font=("PingFang SC", 10, "italic"),
            anchor="e"
        )
        self.signature.pack(side="bottom", anchor="se", padx=10, pady=5)

        self.build_input_ui()

    def build_input_ui(self):
        # 输入行：输入框 + 提交按钮
        input_row = tk.Frame(self.content_frame, bg="white")
        input_row.pack(pady=(10, 6))

        self.entry = tk.Entry(
            input_row,
            width=20,
            font=("PingFang SC", 16),
            fg="black",
            bg="white",
            relief=tk.SOLID,
            bd=1,
        )
        self.entry.grid(row=0, column=0, ipady=6)

        submit_btn = tk.Button(
            input_row,
            text="submit",
            command=self.on_submit,
            fg="white",
            bg="black",
            activebackground="black",
            activeforeground="white",
            bd=0,
            font=("PingFang SC", 14, "bold"),
            height=1,
            padx=16,
        )
        submit_btn.grid(row=0, column=1, padx=(10, 0), ipady=5)

        # 提示文案（居中）
        hint = tk.Label(
            self.content_frame,
            text="输入四位数字，每位数字在0-9之间",
            bg="white",
            fg="black",
            font=("PingFang SC", 12),
        )
        hint.pack()

        # 错误提示占位（初始空）
        self.err_label = tk.Label(
            self.content_frame,
            text="",
            bg="white",
            fg="red",
            font=("PingFang SC", 11),
        )
        self.err_label.pack(pady=(6, 0))

    def on_submit(self):
        s = self.entry.get().strip()
        if not (len(s) == 4 and s.isdigit()):
            self.err_label.config(text="请输入4位数字（0-9）")
            return

        digits = list(map(int, s))
        for d in digits:
            if not (0 <= d <= 9):
                self.err_label.config(text="每位数字必须在0-9之间")
                return

        # 验证通过，清空内容区域（保留顶部标题）
        for w in self.content_frame.winfo_children():
            w.destroy()

        # 构建“老虎机”四列
        self.build_slot_ui(digits)

    def build_slot_ui(self, digits):
        # 外框（白底）
        slot_frame = tk.Frame(self.content_frame, bg="white")
        slot_frame.pack(pady=20)

        # 单列标签 + 分隔符“｜”
        self.labels = []
        for i in range(4):
            lbl = tk.Label(
                slot_frame,
                text=" ",
                bg="white",
                fg="black",
                font=("PingFang SC", 18, "bold"),
                width=16,
                anchor="center",
            )
            lbl.grid(row=0, column=i*2, padx=(5,5))
            self.labels.append(lbl)
            if i < 3:
                sep = tk.Label(slot_frame, text="｜", bg="white", fg="black", font=("PingFang SC", 18, "bold"))
                sep.grid(row=0, column=i*2+1)

        targets = [
            COLUMNS[0][digits[0]],
            COLUMNS[1][digits[1]],
            COLUMNS[2][digits[2]],
            COLUMNS[3][digits[3]],
        ]

        base_durations = [1600, 2000, 2400, 2800]
        start_interval = 30
        end_interval = 120

        for i in range(4):
            self.start_spin(
                label=self.labels[i],
                words=COLUMNS[i],
                target_text=targets[i],
                total_ms=base_durations[i],
                start_interval=start_interval,
                end_interval=end_interval,
            )

    def start_spin(self, label, words, target_text, total_ms=2000, start_interval=30, end_interval=120):
        state = {
            "t": 0,
            "elapsed": 0,
            "interval": float(start_interval),
            "text_index": 0,
        }

        def tick():
            state["elapsed"] += state["interval"]
            state["text_index"] = (state["text_index"] + 1) % len(words)
            label.config(text=words[state["text_index"]])

            progress = min(1.0, state["elapsed"] / float(total_ms))
            state["interval"] = start_interval + (end_interval - start_interval) * progress

            if state["elapsed"] < total_ms:
                label.after(int(state["interval"]), tick)
            else:
                label.config(text=target_text)

        label.after(int(state["interval"]), tick)


if __name__ == "__main__":
    app = JJTitleGenerator()
    app.minsize(720, 300)
    app.mainloop()