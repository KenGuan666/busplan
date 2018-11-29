import heapq

class MaxHeap:

    def __init__(self, initial=[], key=lambda x: x):
        self.key = lambda x: -key(x)
        self.data = [(self.key(d), d) for d in initial]
        heapq.heapify(self.data)

        self.pure = [d for d in initial]

    def push(self, item):
        if item in self.pure:
            self.remove(item)
        else:
            self.pure.append(item)
        heapq.heappush(self.data, (self.key(item), item))

    def remove(self, item):
        self.data = list(filter(lambda x : not x[1] == item, self.data))
        heapq.heapify(self.data)

    def insert(self, lst):
        for item in lst:
            self.push(item)

    def pop(self):
        return heapq.heappop(self.data)[1]

    def size(self):
        return len(self.data)

    def popAndPrint(self):
        while self.size() > 0:
            print(self.pop())


class MinHeap:

    def __init__(self, initial=[], key=lambda x: x):
        self.maxHeap = MaxHeap(initial, lambda x: -key(x))

    def push(self, item):
        self.maxHeap.push(item)

    def remove(self, item):
        self.maxHeap.remove(item)

    def insert(self, lst):
        self.maxHeap.insert(lst)

    def pop(self):
        return self.maxHeap.pop()

    def size(self):
        return self.maxHeap.size()

    def popAndPrint(self):
        self.maxHeap.popAndPrint()
