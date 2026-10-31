import tkinter as tk

CELL = 40
WALL  = '#222222'
FREE  = '#ffffff'
PATH  = '#2e86de'
START = '#10ac84'
EXIT  = '#ee5253'


class MazeApp:
    def __init__(self, matrix, find_exit):
        self.matrix = matrix
        self.find_exit = find_exit
        self.rows = len(matrix)
        self.cols = len(matrix[0])
        self.start = None
        self.path = []

        self.root = tk.Tk()
        self.root.title("Лабиринт")
        self.canvas = tk.Canvas(
            self.root,
            width=self.cols * CELL,
            height=self.rows * CELL,
            bg=FREE,
            highlightthickness=0,
        )
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self._on_click)

        self._render()

    def _render(self):
        self.canvas.delete("all")

        # сетка
        for r in range(self.rows):
            for c in range(self.cols):
                x1, y1 = c * CELL, r * CELL
                x2, y2 = x1 + CELL, y1 + CELL
                fill = WALL if self.matrix[r][c] == 1 else FREE
                self.canvas.create_rectangle(
                    x1, y1, x2, y2, fill=fill, outline="#e0e0e0"
                )

        # путь — разворачиваем, чтобы стрелки шли от старта к выходу
        if len(self.path) >= 2:
            pts = list(reversed(self.path))
            for a, b in zip(pts, pts[1:]):
                self._arrow(a, b)

        # маркеры
        if self.start is not None:
            self._marker(self.start, START, "S")
        if self.path and self.path[0] != self.start:
            self._marker(self.path[0], EXIT, "E")

    def _marker(self, point, color, letter):
        r, c = point
        x1, y1 = c * CELL, r * CELL
        self.canvas.create_rectangle(
            x1, y1, x1 + CELL, y1 + CELL, fill=color, outline=""
        )
        self.canvas.create_text(
            x1 + CELL // 2, y1 + CELL // 2,
            text=letter, fill="white", font=("Arial", 14, "bold"),
        )

    def _arrow(self, p1, p2):
        r1, c1 = p1
        r2, c2 = p2
        x1 = c1 * CELL + CELL // 2
        y1 = r1 * CELL + CELL // 2
        x2 = c2 * CELL + CELL // 2
        y2 = r2 * CELL + CELL // 2
        self.canvas.create_line(
            x1, y1, x2, y2,
            arrow="last", width=3, fill=PATH, arrowshape=(12, 14, 5),
        )

    def _on_click(self, event):
        c = event.x // CELL
        r = event.y // CELL
        if not (0 <= r < self.rows and 0 <= c < self.cols):
            return
        if self.matrix[r][c] == 1:
            return  # стена — игнорируем

        self.start = (r, c)
        self.path = self.find_exit((r, c)) or []
        self._render()

    def run(self):
        self.root.mainloop()


def draw(matrix, find_exit):
    """matrix — лабиринт, find_exit — функция (start) -> list[point] | None."""
    MazeApp(matrix, find_exit).run()