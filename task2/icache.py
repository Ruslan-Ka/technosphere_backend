import heapq

class ICache:
    def __init__(self, capacity: int=10) -> None:
        '''Initializes a LRUCache object'''
        self.hash = {}
        self.heapq = []
        self.capacity = capacity
        self.priority = 1

    def check(self, heap: list, key: str):
        '''Check the key in heapq: return key pos or False'''
        for i in range(0, len(heap)):
            if key == heap[i][1]:
                return i + 1
        return False

    def get(self, key: str) -> str:
        '''Return value by key'''
        if self.hash.get(key) is None:
            return ''
        heap_check = self.check(self.heapq, key)
        self.heapq[heap_check][0] = self.priority
        self.priority += 1
        return self.hash.get(key)

    def set(self, key: str, value: str) -> None:
        '''Add or replase new cache element'''
        heap_check = self.check(self.heapq, key)
        if heap_check:
            self.hash[key] = value
            self.heapq[heap_check - 1] = [self.priority, key]
        else:
            if len(self.heapq) < self.capacity:
                self.hash[key] = value
            else:
                self.hash.pop((heapq.heappop(self.heapq))[1])   
                self.hash[key] = value
            heapq.heappush(self.heapq, [self.priority, key])
        self.priority += 1

    def delete(self, key: str) -> None:
        '''Delete cache element by key'''
        if self.hash.get(key) is None:
            raise KeyError
        self.hash.pop(key)
        heap_check = self.check(self.heapq, key)
        del self.heapq[heap_check - 1]
