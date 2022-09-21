class Protected:

    def __init__(self):
        self._value = 10

    @property
    def value(self):
        return self._value


obj = Protected()

obj.value = 12
print(obj.value)
