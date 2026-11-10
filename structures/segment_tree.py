class SegmentTree:
    def __init__(self, a):
        self.n = len(a)
        self.a = list(a)
        self.tree = [0] * (4 * self.n)
        if self.n > 0:
            self._build(1, 0, self.n - 1)

    def _build(self, v, tl, tr):
        if tl == tr:
            self.tree[v] = self.a[tl]
            return
        tm = (tl + tr) // 2
        self._build(2 * v, tl, tm)
        self._build(2 * v + 1, tm + 1, tr)
        self.tree[v] = self.tree[2 * v] + self.tree[2 * v + 1]

    def query(self, l, r):
        if self.n == 0:
            return 0
        if not (0 <= l <= r < self.n):
            raise IndexError(f"Некорректный диапазон [{l}, {r}] для длины {self.n}")
        return self._query(1, 0, self.n - 1, l, r)

    def _query(self, v, tl, tr, l, r):
        if r < tl or tr < l:
            return 0
        if l <= tl and tr <= r:
            return self.tree[v]
        tm = (tl + tr) // 2
        return (self._query(2 * v, tl, tm, l, r)
                + self._query(2 * v + 1, tm + 1, tr, l, r))

    def update(self, pos, value):
        if not (0 <= pos < self.n):
            raise IndexError(f"Позиция {pos} вне массива длины {self.n}")
        self.a[pos] = value
        self._update(1, 0, self.n - 1, pos, value)

    def _update(self, v, tl, tr, pos, value):
        if tl == tr:
            self.tree[v] = value
            return
        tm = (tl + tr) // 2
        if pos <= tm:
            self._update(2 * v, tl, tm, pos, value)
        else:
            self._update(2 * v + 1, tm + 1, tr, pos, value)
        self.tree[v] = self.tree[2 * v] + self.tree[2 * v + 1]
