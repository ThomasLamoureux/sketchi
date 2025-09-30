import tkinter as tk
from tkinter import ttk, colorchooser, Menu
import os

#choose theme colors
BG0 = "#0f1117"  # page
BG1 = "#171923"  # panels
BG2 = "#1f2330"  # headers
BG3 = "#2a3042"  # borders/hover
TX0 = "#e6e8f0"
TX1 = "#aeb4c3"
BRAND = "#7aa2ff"
SUCCESS = "#29C851"

PAD = 8

# helper to load an image if available (fallback to None)
def maybe_img(path, size=None):
    try:
        if not os.path.exists(path):
            return None
        img = tk.PhotoImage(file=path)
        if size:
            w, h = img.width(), img.height()
            sx = max(1, w // size[0])
            sy = max(1, h // size[1])
            img = img.subsample(sx, sy)
        return img
    except Exception:
        return None

class SketchiApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sketchi – Desktop GUI")
        self.configure(bg=BG0)
        self.geometry("1200x720")

        #4 columns: servers | channels | main | members
        self.grid_columnconfigure(0, weight=0, minsize=72)
        self.grid_columnconfigure(1, weight=0, minsize=260)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=0, minsize=260)
        #2 rows: header | content
        self.grid_rowconfigure(0, weight=0, minsize=56)
        self.grid_rowconfigure(1, weight=1)

        self._build_servers()
        self._build_channels()
        self._build_header()
        self._build_main()
        self._build_members()

        self.artboard = None  #created on demand

    #Left: Servers rail
    def _build_servers(self):
        rail = tk.Frame(self, bg="#0b0d13", bd=0, highlightthickness=1, highlightbackground="#121420")
        rail.grid(row=0, column=0, rowspan=2, sticky="nsew")
        for label in ["S", "UX", "3D", "🖌️", "AI", "🌙"]:
            b = tk.Canvas(rail, width=48, height=48, bg=BG2, highlightthickness=0)
            b.grid(padx=12, pady=6)
            b.create_oval(2, 2, 46, 46, fill=BG2, outline="")
            b.create_text(24, 24, text=label, fill=TX1, font=("Segoe UI", 10, "bold"))
        brand = tk.Canvas(rail, width=48, height=48, highlightthickness=0)
        brand.place(x=12, y=10)
        brand.create_oval(2, 2, 46, 46, fill=BRAND, outline="")
        brand.create_text(24, 24, text="S", fill="#0b0d13", font=("Segoe UI", 10, "bold"))

    # Channels panel 
    def _build_channels(self):
        side = tk.Frame(self, bg=BG1, highlightthickness=1, highlightbackground="#202538")
        side.grid(row=0, column=1, rowspan=2, sticky="nsew")
        side.grid_rowconfigure(1, weight=1)

        head = tk.Frame(side, bg=BG2, highlightthickness=1, highlightbackground="#242a40")
        head.grid(row=0, column=0, sticky="ew")
        tk.Label(head, text="Sketchi • Studio", bg=BG2, fg=TX0, font=("Segoe UI", 10, "bold"),
                 padx=12, pady=10).pack(anchor="w")

        body = tk.Frame(side, bg=BG1); body.grid(row=1, column=0, sticky="nsew")

        def group(title, items):
            tk.Label(body, text=title.upper(), bg=BG1, fg=TX1, font=("Segoe UI", 9, "bold"),
                     padx=12, pady=6).pack(anchor="w")
            for name in items:
                btn = tk.Button(body, text=name, anchor="w",
                                bg=BG1, fg=TX1, relief="flat",
                                activebackground=BG3, activeforeground=TX0,
                                padx=12, pady=6, borderwidth=0,
                                command=lambda n=name: print("channel:", n))
                btn.pack(fill="x", padx=6, pady=2)

        group("Text Channels", ["# general", "# critique", "# commissions", "# reference-drops"])
        group("Voice Rooms", ["🔊 Lobby", "🎨 Paint Jam", "🧪 Experimental"])

    # ----- Top header -----
    def _build_header(self):
        head = tk.Frame(self, bg=BG2, highlightthickness=1, highlightbackground="#242a40")
        head.grid(row=0, column=2, columnspan=1, sticky="nsew")
        head.grid_columnconfigure(0, weight=0)
        head.grid_columnconfigure(1, weight=1)
        head.grid_columnconfigure(2, weight=0)

        crumb = tk.Frame(head, bg=BG2)
        crumb.grid(row=0, column=0, sticky="w", padx=PAD, pady=PAD)
        tk.Label(crumb, text="Sketchi / ", bg=BG2, fg=TX1, font=("Segoe UI", 10)).pack(side="left")
        tk.Label(crumb, text="#general", bg=BG2, fg=TX1, font=("Segoe UI", 10, "bold")).pack(side="left")

        btns = tk.Frame(head, bg=BG2); btns.grid(row=0, column=2, sticky="e", padx=PAD, pady=PAD)
        def make_btn(text, cmd=None, bg="#151a27", fg=TX0):
            b = tk.Button(btns, text=text, command=cmd, bg=bg, fg=fg, relief="flat",
                          activebackground="#1b2133", padx=12, pady=6)
            b.pack(side="left", padx=4)
            return b
        make_btn("Open Artboard", self.open_artboard)
        make_btn("Start Room", bg=BRAND, fg="#0b0d13")
        make_btn("Invite", bg="#173225", fg="#a9f3c7")

    # ----- Main column (call bar + messages + composer) -----
    def _build_main(self):
        main = tk.Frame(self, bg=BG0); main.grid(row=1, column=2, sticky="nsew")
        main.grid_rowconfigure(1, weight=1)

        bar = tk.Frame(main, bg="#0e121d", highlightthickness=1, highlightbackground="#1e2234")
        bar.grid(row=0, column=0, sticky="ew")
        dot = tk.Canvas(bar, width=12, height=12, bg="#0e121d", highlightthickness=0)
        dot.create_oval(2,2,10,10, fill=SUCCESS, outline=""); dot.pack(side="left", padx=10, pady=10)
        tk.Label(bar, text="In Voice: Paint Jam", bg="#0e121d", fg=TX1, font=("Segoe UI", 10, "bold")).pack(side="left")

        msgs = tk.Frame(main, bg=BG0); msgs.grid(row=1, column=0, sticky="nsew")
        sc = tk.Scrollbar(msgs); sc.pack(side="right", fill="y")
        self.msg_list = tk.Listbox(msgs, bg=BG0, fg=TX0, font=("Segoe UI", 10),
                                   selectbackground=BG3, activestyle="none", borderwidth=0,
                                   highlightthickness=0, yscrollcommand=sc.set)
        self.msg_list.pack(fill="both", expand=True, padx=8, pady=8)
        sc.config(command=self.msg_list.yview)
        self.msg_list.insert("end", "Bridget • Here’s the Sketchi layout pass…")
        self.msg_list.insert("end", "Mika • Use the Artboard pop-up for live-drawing…")

        comp = tk.Frame(main, bg=BG1, highlightthickness=1, highlightbackground="#1e2234")
        comp.grid(row=2, column=0, sticky="ew")
        entry = tk.Entry(comp, bg="#151a27", fg=TX0, insertbackground=TX0, relief="flat")
        entry.pack(side="left", fill="x", expand=True, padx=8, pady=8)
        tk.Button(comp, text="Send ➡", bg="#151a27", fg=TX0, relief="flat",
                  activebackground="#1b2133",
                  command=lambda: self.msg_list.insert("end", f"You • {entry.get()}") or entry.delete(0,"end")
                 ).pack(side="right", padx=8, pady=8)

    # ----- Right: Members panel -----
    def _build_members(self):
        mem = tk.Frame(self, bg=BG1, highlightthickness=1, highlightbackground="#202538")
        mem.grid(row=0, column=3, rowspan=2, sticky="nsew")
        tk.Frame(mem, bg=BG2, height=40).pack(fill="x")
        tk.Label(mem, text="Online • 5", bg=BG2, fg=TX0, font=("Segoe UI", 10, "bold"),
                 padx=12, pady=8).place(x=0, y=0)

        for name, color in [("thomas", SUCCESS), ("luke", SUCCESS), ("bridget","#ffc861"),
                            ("whitebeard", SUCCESS), ("copper", SUCCESS)]:
            row = tk.Frame(mem, bg=BG1); row.pack(fill="x", padx=6, pady=4)
            dot = tk.Canvas(row, width=12, height=12, bg=BG1, highlightthickness=0)
            dot.create_oval(2,2,10,10, fill=color, outline=""); dot.pack(side="left", padx=6)
            tk.Label(row, text=name, bg=BG1, fg=TX1, font=("Segoe UI", 10)).pack(side="left")

    # ===== Artboard pop-up (icons + shapes pop; bottom palette + slider) =====
    def open_artboard(self):
        if self.artboard and tk.Toplevel.winfo_exists(self.artboard):
            self.artboard.lift(); return

        win = tk.Toplevel(self)
        win.title("Sketchi Artboard • Untitled")
        win.geometry("1000x700")
        win.configure(bg=BG1)
        self.artboard = win

        # ---- Menubar ----
        menu = Menu(win); win.config(menu=menu)
        file_m = Menu(menu, tearoff=0); menu.add_cascade(label="File", menu=file_m)
        edit_m = Menu(menu, tearoff=0); menu.add_cascade(label="Edit", menu=edit_m)
        file_m.add_command(label="New", command=lambda: canvas.delete("all"))
        file_m.add_command(label="Export (EPS)", command=lambda: canvas.postscript(file="sketchi_artboard.eps"))
        file_m.add_separator()
        file_m.add_command(label="Close", command=win.destroy)
        edit_m.add_command(label="Clear", command=lambda: canvas.delete("all"))

        # ---- Root layout
        root = tk.Frame(win, bg=BG1); root.pack(fill="both", expand=True)
        work_row = tk.Frame(root, bg=BG1); work_row.pack(fill="both", expand=True)

        # ===== Left toolbar (four icons) =====
        toolbar = tk.Frame(work_row, bg=BG1, bd=1, highlightthickness=1, highlightbackground="#202538")
        toolbar.pack(side="left", fill="y", padx=8, pady=8)

        tool_var = tk.StringVar(value="pencil")
        size_var = tk.IntVar(value=8)  # slider controls this
        fg = tk.StringVar(value="#000000")
        bgc = tk.StringVar(value="#ffffff")

        icon_size = (28, 28)
        ICONS = {
            "eraser": maybe_img("/mnt/data/eraser_2567462.png", size=icon_size),
            "pencil": maybe_img("/mnt/data/pencil_383421.png", size=icon_size),
            "shapes": maybe_img("/mnt/data/c5efc079-7539-420c-9903-f9ad9699206a.png", size=icon_size),
            "bucket": maybe_img("/mnt/data/f229dd2e-ca80-4cd7-944e-9174557e4a54.png", size=icon_size),
        }

        def tb(img, fallback_text, name, cmd=None):
            if img is not None:
                b = tk.Radiobutton(toolbar, image=img, value=name, variable=tool_var,
                                   indicatoron=False, width=36, height=36,
                                   relief="flat", bg=BG1, selectcolor=BG3,
                                   command=cmd)
                b.image = img
            else:
                b = tk.Radiobutton(toolbar, text=fallback_text, value=name, variable=tool_var,
                                   indicatoron=False, width=4, padx=6, pady=6,
                                   relief="flat", bg=BG1, fg=TX0, selectcolor=BG3,
                                   command=cmd)
            b.pack(padx=6, pady=6)
            return b

        # Shapes pop-out (appears only when shapes button clicked)
        shapes_panel = tk.Frame(toolbar, bg="#101523", bd=1, relief="solid")
        shapes_panel_visible = {"on": False}
        def toggle_shapes_panel():
            if not shapes_panel_visible["on"]:
                shapes_panel.place(x=50, y=6)
                shapes_panel_visible["on"] = True
            else:
                shapes_panel.place_forget()
                shapes_panel_visible["on"] = False

        tb(ICONS["pencil"], "✏", "pencil")
        tb(ICONS["shapes"], "◯△", "shapes", cmd=toggle_shapes_panel)
        tb(ICONS["bucket"], "🪣", "fill")
        tb(ICONS["eraser"], "🩹", "eraser")

        def shape_btn(label, tool_name):
            b = tk.Button(shapes_panel, text=label, bg="#101523", fg=TX0, relief="flat",
                          command=lambda: (tool_var.set(tool_name),
                                           shapes_panel.place_forget(),
                                           shapes_panel_visible.update(on=False)))
            b.pack(fill="x", padx=4, pady=2)
        tk.Label(shapes_panel, text="Shapes", bg="#101523", fg=TX1).pack(fill="x", padx=4, pady=(4,2))
        shape_btn("Line", "line")
        shape_btn("Circle", "circle")
        shape_btn("Triangle", "triangle")

        # ===== Canvas area =====
        canvas_wrap = tk.Frame(work_row, bg=BG1); canvas_wrap.pack(side="left", fill="both", expand=True, padx=8, pady=8)
        canvas_border = tk.Frame(canvas_wrap, bg="#1b2133", bd=1, relief="sunken")
        canvas_border.pack(fill="both", expand=True)
        canvas = tk.Canvas(canvas_border, bg=bgc.get(), cursor="crosshair", highlightthickness=0)
        canvas.pack(fill="both", expand=True)

        # ===== Bottom: color palette + brush-size SLIDER + status =====
        PAL = [
            "#000000","#7f7f7f","#880015","#ed1c24","#ff7f27","#fff200","#22b14c",
            "#00a2e8","#3f48cc","#a349a4","#ffffff","#c3c3c3","#b97a57","#ffaec9",
            "#ffc90e","#efe4b0","#b5e61d","#99d9ea","#7092be","#c8bfe7", 
        ]
        bottom = tk.Frame(root, bg=BG1); bottom.pack(fill="x", padx=8, pady=(0,8))

        # palette (left)
        palette = tk.Frame(bottom, bg=BG1, bd=1, highlightthickness=1, highlightbackground="#202538")
        palette.pack(side="left", padx=(0,8), pady=0)

        sel_fg = tk.Label(palette, text="  ", bg=fg.get(), bd=2, relief="sunken", width=2)
        sel_bg = tk.Label(palette, text="  ", bg=bgc.get(), bd=2, relief="sunken", width=2)
        sel_fg.pack(side="left", padx=(8,4), pady=6)
        sel_bg.pack(side="left", padx=(0,12), pady=6)

        def pick_from_dialog(which):
            c = colorchooser.askcolor(color=(fg.get() if which=="fg" else bgc.get()))[1]
            if not c: return
            if which=="fg":
                fg.set(c); sel_fg.configure(bg=c)
            else:
                bgc.set(c); sel_bg.configure(bg=c); canvas.configure(bg=c)

        tk.Button(palette, text="FG", command=lambda: pick_from_dialog("fg"), bg="#141927", fg=TX0, relief="flat").pack(side="left", padx=(0,4))
        tk.Button(palette, text="BG", command=lambda: pick_from_dialog("bg"), bg="#141927", fg=TX0, relief="flat").pack(side="left", padx=(0,12))

        chip_row = tk.Frame(palette, bg=BG1); chip_row.pack(side="left")
        def make_chip(color):
            f = tk.Frame(chip_row, width=22, height=18, bg=color, bd=1, relief="raised")
            f.pack(side="left", padx=2, pady=4)
            def set_fg(_): fg.set(color); sel_fg.configure(bg=color)
            def set_bg(_): bgc.set(color); sel_bg.configure(bg=color); canvas.configure(bg=color)
            f.bind("<Button-1>", set_fg)   # left click = FG
            f.bind("<Button-3>", set_bg)   # right click = BG
        for c in PAL: make_chip(c)

        # brush size slider (center)
        slider_box = tk.Frame(bottom, bg=BG1)
        slider_box.pack(side="left", padx=8)
        tk.Label(slider_box, text="Brush size", bg=BG1, fg=TX1).pack(anchor="w")
        size_readout = tk.Label(slider_box, text=str(size_var.get()), bg=BG1, fg=TX0)
        size_readout.pack(anchor="w")
        def on_slider(val):
            size_var.set(int(float(val)))
            size_readout.config(text=str(size_var.get()))
            update_status()
        size_slider = ttk.Scale(slider_box, from_=1, to=100, orient="horizontal",
                                command=on_slider)
        size_slider.set(size_var.get())
        size_slider.pack(fill="x", ipadx=120)

        # status (right)
        status = tk.Label(bottom, text="Tool: pencil | Size: 8", anchor="e",
                          bg=BG2, fg=TX1)
        status.pack(side="right", fill="x", expand=True)

        def update_status(x=None, y=None):
            status.config(text=f"Tool: {tool_var.get()} | Size: {size_var.get()} | FG: {fg.get()} | BG: {bgc.get()} | Pos: {x if x is not None else '-'}, {y if y is not None else '-'}")

        # ===== Drawing logic =====
        last = {"x": None, "y": None, "preview": None}
        tri_state = {"pts": [], "lines": []}  # for 3-click triangle

        def clear_preview():
            if last["preview"] is not None:
                canvas.delete(last["preview"])
                last["preview"] = None
            for lid in tri_state["lines"]:
                canvas.delete(lid)
            tri_state["lines"].clear()

        def start(e):
            t = tool_var.get()
            update_status(e.x, e.y)

            if t == "triangle":
                tri_state["pts"].append((e.x, e.y))
                if len(tri_state["pts"]) == 2:
                    p1, p2 = tri_state["pts"]
                    tri_state["lines"].append(canvas.create_line(p1[0], p1[1], p2[0], p2[1], fill=fg.get(), width=size_var.get()))
                elif len(tri_state["pts"]) == 3:
                    p1, p2, p3 = tri_state["pts"]
                    canvas.create_polygon([*p1, *p2, *p3], outline=fg.get(), fill="", width=size_var.get(), joinstyle="round")
                    tri_state["pts"].clear(); clear_preview()
                return

            last["x"], last["y"] = e.x, e.y

            if t in ("line", "circle"):
                if t == "line":
                    last["preview"] = canvas.create_line(e.x, e.y, e.x, e.y, fill=fg.get(), width=size_var.get())
                elif t == "circle":
                    last["preview"] = canvas.create_oval(e.x, e.y, e.x, e.y, outline=fg.get(), width=size_var.get())
            elif t == "fill":
                canvas.configure(bg=fg.get())

        def move(e):
            t = tool_var.get()
            if t == "triangle":
                if len(tri_state["pts"]) == 1:
                    clear_preview()
                    p1 = tri_state["pts"][0]
                    tri_state["lines"].append(canvas.create_line(p1[0], p1[1], e.x, e.y, fill=fg.get(), width=size_var.get()))
                elif len(tri_state["pts"]) == 2:
                    clear_preview()
                    p1, p2 = tri_state["pts"]
                    tri_state["lines"].append(canvas.create_line(p1[0], p1[1], e.x, e.y, fill=fg.get(), width=size_var.get()))
                    tri_state["lines"].append(canvas.create_line(p2[0], p2[1], e.x, e.y, fill=fg.get(), width=size_var.get()))
                update_status(e.x, e.y); return

            if last["x"] is None:
                update_status(e.x, e.y); return

            if t == "pencil":
                canvas.create_line(last["x"], last["y"], e.x, e.y,
                                   fill=fg.get(), width=size_var.get(),
                                   capstyle="round", joinstyle="round")
                last["x"], last["y"] = e.x, e.y
            elif t == "eraser":
                canvas.create_line(last["x"], last["y"], e.x, e.y,
                                   fill=bgc.get(), width=size_var.get(),
                                   capstyle="round", joinstyle="round")
                last["x"], last["y"] = e.x, e.y
            elif t == "line" and last["preview"] is not None:
                canvas.coords(last["preview"], last["x"], last["y"], e.x, e.y)
            elif t == "circle" and last["preview"] is not None:
                canvas.coords(last["preview"], last["x"], last["y"], e.x, e.y)

            update_status(e.x, e.y)

        def end(e):
            t = tool_var.get()
            if t in ("line", "circle") and last["preview"] is not None:
                last["preview"] = None
            last["x"] = last["y"] = None
            update_status(e.x, e.y)

        canvas.bind("<ButtonPress-1>", start)
        canvas.bind("<B1-Motion>", move)
        canvas.bind("<ButtonRelease-1>", end)
        canvas.bind("<Motion>", lambda e: update_status(e.x, e.y))

        tool_var.trace_add("write", lambda *_: update_status())

if __name__ == "__main__":
    app = SketchiApp()
    app.mainloop() 
