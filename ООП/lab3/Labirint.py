import copy
from render import draw, edit

class Labirint:
    wrongExit = (-1, -1)

    def __init__(self, matrix : list[list[int]]):
        self.matrix = matrix

    @staticmethod
    def _getChildrens(mat : list[list[int]], parents : dict[tuple[int, int], tuple[int, int]], point: tuple[int, int]):
        points: list[tuple[int, int]] = []

        if(point[0]>0 and mat[point[0]-1][point[1]]==0):
            points.append((point[0]-1, point[1]))
        if(point[1]>0 and mat[point[0]][point[1]-1]==0):
            points.append((point[0], point[1]-1))
        if(point[0]+1<len(mat) and mat[point[0]+1][point[1]]==0):
            points.append((point[0]+1, point[1]))
        if(point[1]+1<len(mat[0]) and mat[point[0]][point[1]+1]==0):
            points.append((point[0], point[1]+1))

        for i in points: 
            parents[i] = point
            mat[i[0]][i[1]] = 1

        return points

    @staticmethod
    def _getParents(parents : dict[tuple[int, int], tuple[int, int]], point: tuple[int, int]):
        result = [point]

        while point in parents: 
            point = parents[point]
            result.append(point)

        return result

    @staticmethod
    def FromFile(filename: str) -> "Labirint":
        with open(filename, encoding="utf-8") as f:
            matrix = [[int(x) for x in line.split()]
            for line in f if line.strip()]
        return Labirint(matrix)

    def Draw(self, points=None):
        mat = copy.deepcopy(self.matrix)
        for r, c in (points or []):
            mat[r][c] = 2
        for i in mat:
            print(''.join('##' if c == 1 else '00' if c == 2 else '  ' for c in i))

    def _isExit(self, point: tuple[int, int]): return point[0]==0 or point[1]==0 or point[0]==len(self.matrix)-1 or point[1]==len(self.matrix[0])-1

    def _isPointValide(self, point):
        if not (0 <= point[0] < len(self.matrix) and 0 <= point[1] < len(self.matrix[0])):
            print(f"Точка {point} вне матрицы") 
            return False
        if self.matrix[startPoint[0]][startPoint[1]] != 0:
            print("Точка {point} занята")
            return False
        
        return True

    def FindExit(self, startPoint : tuple[int, int]):
        if not self._isPointValide(startPoint): return None
        if(self._isExit(startPoint)): return [startPoint]

        mat = copy.deepcopy(self.matrix)
        parents : dict[tuple[int, int], tuple[int, int]] = {}
        points = [startPoint]
        mat[startPoint[0]][startPoint[1]] = 1

        for point in points:
            childrens = self._getChildrens(mat, parents, point)

            for child in childrens:
                if(self._isExit(child)): return self._getParents(parents, child)

            points += childrens

        print("Выход из лабиринта не найден")
        return None

startPoint = (3, 2)

l = Labirint.FromFile("maze.txt")
l.Draw(l.FindExit(startPoint))
draw(l.matrix)
