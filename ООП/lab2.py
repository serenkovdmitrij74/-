class OctalNumber:
    def __init__(self, value="0"):
        if isinstance(value, OctalNumber):
            self._digits = value._digits
        elif isinstance(value, int):
            if value < 0:
                raise ValueError("Число должно быть неотрицательным")
            self._digits = self._from_decimal(value)
        elif isinstance(value, str):
            self._digits = self._validate(value)
        else:
            raise TypeError("Неподдерживаемый тип")

    @staticmethod
    def _validate(s):
        s = s.strip()
        if not s:
            raise ValueError("Пустая строка")
        if not all(c in "01234567" for c in s):
            raise ValueError(f"'{s}' не восьмеричное число")
        return s.lstrip("0") or "0"

    @staticmethod
    def _from_decimal(number):
        if number == 0:
            return "0"
        result = ""
        while number > 0:
            result = str(number % 8) + result
            number //= 8
        return result

    @property
    def digits(self):
        return self._digits

    @property
    def decimal(self):
        return int(self._digits, 8)

    def assign(self, other):
        if isinstance(other, OctalNumber):
            self._digits = other._digits
        else:
            self._digits = self._validate(str(other))
        return self

    def _coerce(self, other):
        if isinstance(other, OctalNumber):
            return other
        try:
            return OctalNumber(other)
        except Exception:
            return NotImplemented

    def __eq__(self, other):
        o = self._coerce(other)
        if o is NotImplemented:
            return NotImplemented
        return self.decimal == o.decimal

    def __ne__(self, other):
        r = self.__eq__(other)
        return r if r is NotImplemented else not r

    def __lt__(self, other):
        o = self._coerce(other)
        if o is NotImplemented:
            return NotImplemented
        return self.decimal < o.decimal

    def __le__(self, other):
        o = self._coerce(other)
        if o is NotImplemented:
            return NotImplemented
        return self.decimal <= o.decimal

    def __gt__(self, other):
        o = self._coerce(other)
        if o is NotImplemented:
            return NotImplemented
        return self.decimal > o.decimal

    def __ge__(self, other):
        o = self._coerce(other)
        if o is NotImplemented:
            return NotImplemented
        return self.decimal >= o.decimal

    def to_decimal(self):
        return self.decimal

    def __int__(self):
        return self.decimal

    def __getitem__(self, index):
        return int(self._digits[index])

    def __setitem__(self, index, value):
        if not isinstance(value, int) or value < 0 or value > 7:
            raise ValueError("Цифра от 0 до 7")
        lst = list(self._digits)
        lst[index] = str(value)
        self._digits = self._validate("".join(lst))

    def __str__(self):
        return self._digits

    def format(self, spec=""):
        if not spec:
            return self._digits
        return format(self.decimal, spec)

    def __format__(self, spec):
        return self.format(spec)



a = OctalNumber("17")
b = OctalNumber(15)
print(a, b)

print(a.digits, a.decimal)

x = OctalNumber("100")
y = OctalNumber("777")
y.assign(x)
print("x =", x, "| y =", y)

print(OctalNumber("17") == 15)
print(OctalNumber("17") < OctalNumber("20"))
print(OctalNumber("777") > 100)
print(OctalNumber("10") <= OctalNumber("7"))
print(OctalNumber("7") != OctalNumber("10"))

print(OctalNumber("17").to_decimal())


n = OctalNumber("34567")
print(n[0], n[1], n[-1])
n[0] = 7
print(n)

n = OctalNumber("755")
print(f"{n:d}")
print(f"{n:06d}")
print(f"{n:6d}")
