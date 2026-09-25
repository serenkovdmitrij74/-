import re
import math

#№5
def SzhatMassiv(mas, ab):
    rezult = [i for i in mas if (i>ab[0] and i<ab[1])]
    return rezult+ [0]*(len(mas)-len(rezult))

def OdnomerniiMasiviEx5(mas, ab):
    lastOtr = -1
    for i in range(len(mas)-1,-1,-1):
        if(mas[i]<0):
            lastOtr = i
            break
    
    print("Максимум ", max(mas))
    print("Сумма до первого отрицательного ", sum(mas[0:lastOtr+1])) 
    print("Третье задание ", SzhatMassiv(mas, ab))

#№6
def ColSum(mat):
    n = len(mat)
    
    col_sums = []
    for j in range(n):
        col = [mat[i][j] for i in range(n)]
        if all(x >= 0 for x in col):
            col_sums.append(sum(col))
    
    return col_sums

def MinDiagSum(mat):
    n = len(mat)
    min_sum = float('inf')

    for i in range(n):
        diag_sum = 0
        x, y = i, 0
        while x >= 0 and y < n:
            diag_sum += abs(mat[x][y])
            x -= 1
            y += 1
        if diag_sum < min_sum:
            min_sum = diag_sum

    for j in range(1, n):
        diag_sum = 0
        x, y = n-1, j
        while x >= 0 and y < n:
            diag_sum += abs(mat[x][y])
            x -= 1
            y += 1
        if diag_sum < min_sum:
            min_sum = diag_sum

    print(min_sum)

def Ex6(mat):    
    print("Суммы ", ColSum(mat))
    print("Мин диаг ", MinDiagSum(mat))

#№7
def MeniatSlova(text):
    words = re.findall(r'\S+', text)
    for i in range(0, len(words)-1, 2):
        words[i], words[i+1] = words[i+1], words[i]

    return ' '.join(words)

def Ex7(fileName):
    with open(fileName) as f:
        content = f.read()

    result = MeniatSlova(content)
    print(result)

Ex7(r'C:\Users\DmitrijSerenkov\Desktop\kodi_i_tp\Програмирование лабы\ООП\input.txt')

#№3
def Teilor(x, eps):  
    rezult = 0.0
    n = 0
    a = x
    limit = eps/2
    while abs(a) > limit:
        rezult += a
        n += 1
        a = (x ** (2 * n + 1)) / (2 * n + 1)
    
    return 2 * rezult, n


def Ex3():
    print("Вычисление ln((1+x)/(1-x)) с помощью ряда Тейлора")
    x_start = -0.8
    x_end = 0.8
    dx = 0.1
    eps = 1e-8
    
    if abs(x_start) >= 1 or abs(x_end) >= 1:
        print(f"x должна быть в интервале от -1 до 1")
        return
    
    print(f"\n{'x':>10} {'f(x)':>15} {'n':>6} {'math':>13}")
    print("-" * 56)
    
    x = x_start
    while x <= x_end + 1e-9:
        y, n = Teilor(x, eps)
        print(f"{x:10.4f} {y:15.8f} {n:6d} {math.log((1 + x) / (1 - x)):15.8f}")
        x += dx


Ex3()