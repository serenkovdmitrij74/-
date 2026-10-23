class OctalNumber:
    def __init__(self, value="0"):
        if isinstance(value, OctalNumber):
            self._digits = value._digits
        elif isinstance(value, str):
            self._digits = self._validate(value)
        else:
            raise TypeError("Неподдерживаемый тип")

    @staticmethod
    def _validate(s):
        sign = ""
        if s.startswith("-"):
            sign, s = "-", s[1:]
        if not s:
            raise ValueError("Пустая строка")
        if s.count(".") > 1 or not all(c in "01234567." for c in s):
            raise ValueError(f"'{s}' не восьмеричное число")
        if "." in s:
            cel, drob = s.split(".")
            cel = cel.lstrip("0") or "0"
            return sign + cel + ("." + drob if drob else "")
        stripped = s.lstrip("0") or "0"
        return (sign + stripped) if stripped != "0" else "0"

    @property
    def digits(self):
        return self._digits

    @property
    def decimal(self):
        s = self._digits
        sign = -1.0 if s.startswith("-") else 1.0
        s = s.lstrip("-")
        if "." in s:
            cel, drob = s.split(".")
        else:
            cel, drob = s, ""
        result = 0.0
        for c in cel:
            result = result * 8.0 + float(c)
        for i, c in enumerate(drob):
            result += float(c) / (8.0 ** (i + 1))
        return sign * result

    def assign(self, other):
        if isinstance(other, OctalNumber):
            self._digits = other._digits
        elif isinstance(other, str):
            self._digits = self._validate(other)
        else:
            raise TypeError("Неподдерживаемый тип")
        return self

    def _to_oct(self, other):
        if isinstance(other, OctalNumber):
            return other.decimal
        if isinstance(other, float):
            return other
        try:
            return OctalNumber(other).decimal
        except Exception:
            return NotImplemented

    def __eq__(self, other):
        o = self._to_oct(other)
        if o is NotImplemented:
            return NotImplemented
        return self.decimal == o

    def __ne__(self, other):
        r = self.__eq__(other)
        return r if r is NotImplemented else not r

    def __lt__(self, other):
        o = self._to_oct(other)
        if o is NotImplemented:
            return NotImplemented
        return self.decimal < o

    def __le__(self, other):
        o = self._to_oct(other)
        if o is NotImplemented:
            return NotImplemented
        return self.decimal <= o

    def __gt__(self, other):
        o = self._to_oct(other)
        if o is NotImplemented:
            return NotImplemented
        return self.decimal > o

    def __ge__(self, other):
        o = self._to_oct(other)
        if o is NotImplemented:
            return NotImplemented
        return self.decimal >= o

    def to_decimal(self):
        return self.decimal

    def __float__(self):
        return self.decimal

    def __getitem__(self, index):
        cifri = [i for i, c in enumerate(self._digits) if c not in ".-"]
        return float(self._digits[cifri[index]])

    def __setitem__(self, index, value):
        if not isinstance(value, float) or value < 0.0 or value > 7.0 or value % 1.0 != 0.0:
            raise ValueError("Цифра от 0 до 7")
        cifri = [i for i, c in enumerate(self._digits) if c not in ".-"]
        lst = list(self._digits)
        lst[cifri[index]] = str(int(value))
        self._digits = self._validate("".join(lst))

    def __str__(self):
        return self._digits

    def format(self, spec=""):
        if not spec:
            return self._digits
        return format(self.decimal, spec.replace("d", ".0f"))

    def __format__(self, spec):
        return self.format(spec)


a = OctalNumber("17")

x = OctalNumber("100")
y = OctalNumber("777")
y.assign(x)
print("x =", x, "| y =", y)

print(OctalNumber("17") == 15.0)
print(OctalNumber("17") < OctalNumber("20"))
print(OctalNumber("777") > 100.0)
print(OctalNumber("10") <= OctalNumber("7"))
print(OctalNumber("7") != OctalNumber("10"))

print(OctalNumber("17").to_decimal())

n = OctalNumber("34567")
print(n[0], n[1], n[-1])
n[0] = 7.0
print(n)

n = OctalNumber("755.212")
print(n)
print(f"{n:d}")
print(f"{n:06d}")
print(f"{n:.2f}")
