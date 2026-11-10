class MyHashMap:
    MAX_LOAD_FACTOR = 0.75

    def __init__(self, capacity=8):
        self.capacity = capacity
        self.size = 0
        self.buckets = [[] for _ in range(capacity)]

    def _index(self, key):
        return hash(key) % self.capacity

    def load_factor(self):
        return self.__len__() / self.capacity

    def _resize(self):
        old_buckets = self.buckets

        self.capacity *= 2
        self.buckets = [[] for _ in range(self.capacity)]

        for bucket in old_buckets:
            for key, value in bucket:
                idx = self._index(key)
                self.buckets[idx].append([key, value])

    def put(self, key, value):
        idx = self._index(key)

        for pair in self.buckets[idx]:
            if pair[0] == key:
                pair[1] = value
                return

        if (self.size + 1) / self.capacity > self.MAX_LOAD_FACTOR:
            self._resize()
            idx = self._index(key)

        self.buckets[idx].append([key, value])
        self.size += 1

    def get(self, key):
        idx = self._index(key)

        for k, v in self.buckets[idx]:
            if k == key:
                return v

        return None

    def contains(self, key):
        idx = self._index(key)

        for k, _ in self.buckets[idx]:
            if k == key:
                return True

        return False

    def remove(self, key):
        idx = self._index(key)
        bucket = self.buckets[idx]

        for i in range(len(bucket)):
            if bucket[i][0] == key:
                bucket.pop(i)
                self.size -= 1

                return True

        return False

    def __len__(self):
        return self.size


def build_hash_index(values):
    index = MyHashMap()

    for row_id, key in enumerate(values):
        index.put(key, row_id)

    return index


def linear_search(values, target):
    for i in range(len(values)):
        if values[i] == target:
            return i
    return None
