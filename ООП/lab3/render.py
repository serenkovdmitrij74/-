import tkinter as tk

BG        = "#F3F3F3"
CARD      = "#FFFFFF"
BORDER    = "#E2E2E2"
TEXT      = "#1A1A1A"
TEXT_MUT  = "#605E5C"
WALL      = "#3B3B3B"
EMPTY     = "#FFFFFF"
EMPTY_BRD = "#ECECEC"
PLAYER    = "#0078D4"
ACCENT    = "#0078D4"
ACCENT_H  = "#106EBE"
BTN_BG    = "#FFFFFF"
BTN_HOVER = "#F0F0F0"

PAD = 24


def _rrect(c, x1, y1, x2, y2, r, **kw):
    pts = [x1+r, y1,  x2-r, y1,  x2, y1,  x2, y1+r,
           x2, y2-r,  x2, y2,  x2-r, y2,  x1+r, y2,
           x1, y2,  x1, y2-r,  x1, y1+r,  x1, y1]
    return c.create_polygon(pts, smooth=True, **kw)


# =====================================================================
#  Просмотр
# =====================================================================

class _Viewer:
    def __init__(self, matrix, title):
        self.root = tk.Tk()
        self.root.title(title)
        self.root.configure(bg=BG)
        self.canvas = None
        self._build(matrix)

    def _build(self, matrix):
        if self.canvas:
            self.canvas.destroy()
        if not matrix or not matrix[0]:
            return

        rows, cols = len(matrix), len(matrix[0])
        n    = max(rows, cols)
        cell = max(8,  min(30, 700 // n))
        gap  = max(2,  cell // 6)
        r    = max(3,  cell // 4)

        w = PAD*2 + cols*cell + (cols-1)*gap
        h = PAD*2 + rows*cell + (rows-1)*gap

        self.canvas = tk.Canvas(self.root, width=w, height=h,
                                bg=BG, highlightthickness=0, bd=0)
        self.canvas.pack()

        _rrect(self.canvas, PAD//2, PAD//2, w - PAD//2, h - PAD//2,
               r=16, fill=CARD, outline=BORDER, width=1)

        for i, row in enumerate(matrix):
            for j, v in enumerate(row):
                x1 = PAD + j*(cell + gap)
                y1 = PAD + i*(cell + gap)
                x2, y2 = x1 + cell, y1 + cell
                if v == 1:
                    _rrect(self.canvas, x1, y1, x2, y2, r, fill=WALL, outline=WALL)
                elif v == 2:
                    _rrect(self.canvas, x1, y1, x2, y2, r, fill=PLAYER, outline=PLAYER)
                else:
                    _rrect(self.canvas, x1, y1, x2, y2, r,
                           fill=EMPTY, outline=EMPTY_BRD, width=1)

        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth()  - w) // 2
        y = (self.root.winfo_screenheight() - h) // 2
        self.root.geometry(f"+{x}+{y}")

    def render(self, matrix):
        self._build(matrix)

    def run(self):
        self.root.mainloop()


def draw(matrix, title="Labirint"):
    """Показать матрицу в отдельном окне."""
    _Viewer(matrix, title).run()


def animate(matrices, delay_ms=150, title="Labirint"):
    """Проиграть последовательность матриц."""
    if not matrices:
        return
    app = _Viewer(matrices[0], title)

    def step(i):
        if i >= len(matrices):
            return
        app.render(matrices[i])
        if i + 1 < len(matrices):
            app.root.after(delay_ms, step, i + 1)

    step(0)
    app.run()


# =====================================================================
#  Редактор
# =====================================================================

class _Editor:
    def __init__(self, filename):
        self.filename = filename
        self.result = None
        self.rows = 10
        self.cols = 10
        self.matrix = [[0]*self.cols for _ in range(self.rows)]

        self.root = tk.Tk()
        self.root.title(filename)
        self.root.configure(bg=BG)
        self.root.resizable(False, False)

        # Размер
        bar = tk.Frame(self.root, bg=BG)
        bar.pack(fill="x", padx=PAD, pady=(PAD, 12))

        tk.Label(bar, text="Строк:", bg=BG, fg=TEXT_MUT,
                 font=("Segoe UI", 10)).pack(side="left")
        self.rows_var = tk.IntVar(value=self.rows)
        tk.Spinbox(bar, from_=2, to=40, width=4, textvariable=self.rows_var,
                   font=("Segoe UI", 10)).pack(side="left", padx=(4, 12))

        tk.Label(bar, text="Столбцов:", bg=BG, fg=TEXT_MUT,
                 font=("Segoe UI", 10)).pack(side="left")
        self.cols_var = tk.IntVar(value=self.cols)
        tk.Spinbox(bar, from_=2, to=40, width=4, textvariable=self.cols_var,
                   font=("Segoe UI", 10)).pack(side="left", padx=(4, 12))

        tk.Button(bar, text="Применить", command=self._resize,
                  bg=BTN_BG, fg=TEXT, bd=0, relief="flat",
                  activebackground=BTN_HOVER, font=("Segoe UI", 10),
                  padx=12, pady=2, cursor="hand2").pack(side="left")

        # Канва
        wrap = tk.Frame(self.root, bg=BG)
        wrap.pack(padx=PAD, pady=(0, 12))
        self.canvas = tk.Canvas(wrap, bg=CARD, highlightthickness=1,
                                highlightbackground=BORDER, bd=0)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self._on_click)
        self._draw()

        # Кнопки
        bar2 = tk.Frame(self.root, bg=BG)
        bar2.pack(fill="x", padx=PAD, pady=(6, PAD))

        def mk(txt, cmd, primary=False):
            b = tk.Button(bar2, text=txt, command=cmd, bd=0, relief="flat",
                          font=("Segoe UI", 10), padx=20, pady=6, cursor="hand2")
            if primary:
                b.configure(bg=ACCENT, fg="white",
                            activebackground=ACCENT_H, activeforeground="white")
            else:
                b.configure(bg=BTN_BG, fg=TEXT, activebackground=BTN_HOVER)
            return b

        mk("Отмена", self._cancel).pack(side="right", padx=(8, 0))
        mk("Сохранить", self._save_and_close, primary=True).pack(side="right")

    def _sizes(self):
        cell = max(14, min(28, 600 // max(self.rows, self.cols)))
        gap  = max(2, cell // 6)
        return cell, gap

    def _draw(self):
        self.canvas.delete("all")
        cell, gap = self._sizes()
        r = max(3, cell // 4)

        w = self.cols*cell + (self.cols-1)*gap
        h = self.rows*cell + (self.rows-1)*gap
        self.canvas.configure(width=w, height=h)

        for i in range(self.rows):
            for j in range(self.cols):
                x1 = j*(cell+gap)
                y1 = i*(cell+gap)
                x2, y2 = x1+cell, y1+cell
                if self.matrix[i][j] == 1:
                    _rrect(self.canvas, x1, y1, x2, y2, r,
                           fill=WALL, outline=WALL)
                else:
                    _rrect(self.canvas, x1, y1, x2, y2, r,
                           fill=EMPTY, outline=EMPTY_BRD, width=1)

    def _on_click(self, e):
        cell, gap = self._sizes()
        step = cell + gap
        j = e.x // step
        i = e.y // step
        if not (0 <= i < self.rows and 0 <= j < self.cols):
            return
        if e.x - j*step >= cell or e.y - i*step >= cell:
            return
        self.matrix[i][j] = 1 - self.matrix[i][j]
        self._draw()

    def _resize(self):
        r = max(2, min(40, self.rows_var.get()))
        c = max(2, min(40, self.cols_var.get()))
        new = [[0]*c for _ in range(r)]
        for i in range(min(r, self.rows)):
            for j in range(min(c, self.cols)):
                new[i][j] = self.matrix[i][j]
        self.matrix = new
        self.rows, self.cols = r, c
        self._draw()
        self._recenter()

    def _recenter(self):
        self.root.update_idletasks()
        w = self.root.winfo_width()
        h = self.root.winfo_height()
        x = (self.root.winfo_screenwidth()  - w) // 2
        y = (self.root.winfo_screenheight() - h) // 2
        self.root.geometry(f"+{x}+{y}")

    def _save_and_close(self):
        with open(self.filename, "w", encoding="utf-8") as f:
            for row in self.matrix:
                f.write(" ".join(str(c) for c in row) + "\n")
        self.result = self.matrix
        self.root.destroy()

    def _cancel(self):
        self.root.destroy()

    def run(self):
        self._recenter()
        self.root.mainloop()


def edit(filename):
    """Открыть окно редактора. Результат сохраняется в filename."""
    editor = _Editor(filename)
    editor.run()
    return editor.result
