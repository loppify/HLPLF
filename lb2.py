from collections import deque
import time


def remove(lst, value):
    for i in range(len(lst)):
        if lst[i] == value:
            del lst[i]
            return
    raise ValueError("list.remove(x): x not in list")


def items(d):
    return [(k, d[k]) for k in d]


def intersection(s1, s2):
    res = set()
    for x in s1:
        if x in s2:
            res.add(x)
    return res


def index(s, sub):
    n, m = len(s), len(sub)
    for i in range(n - m + 1):
        if s[i:i + m] == sub:
            return i
    raise ValueError("substring not found")


def copy(dq):
    new_dq = deque()
    for item in dq:
        new_dq.append(item)
    return new_dq


def benchmark():
    # 1. List Remove (O(n))
    size = 10 ** 7 * 2
    data_list = list(range(size))
    target = size - 1

    start = time.perf_counter()
    data_list.remove(target)
    t_std = time.perf_counter() - start

    data_list = list(range(size))
    start = time.perf_counter()
    remove(data_list, target)
    t_custom = time.perf_counter() - start
    print(f"List remove: Std={t_std:.4f}s, Custom={t_custom:.4f}s")

    # 2. Set Intersection (O(min(len(s1), len(s2))))
    s1 = set(range(10 ** 7))
    s2 = set(range(5 * 10 ** 6, int(1.5 * 10 ** 7)))

    start = time.perf_counter()
    _ = s1.intersection(s2)
    t_std = time.perf_counter() - start

    start = time.perf_counter()
    _ = intersection(s1, s2)
    t_custom = time.perf_counter() - start
    print(f"Set intersection: Std={t_std:.4f}s, Custom={t_custom:.4f}s")

    # 3. String Index (O(n*m))
    text = "a" * 10 ** 7 * 3 + "b"
    sub = "a" * 100 + "b"

    start = time.perf_counter()
    _ = text.index(sub)
    t_std = time.perf_counter() - start

    start = time.perf_counter()
    _ = index(text, sub)
    t_custom = time.perf_counter() - start
    print(f"String index: Std={t_std:.4f}s, Custom={t_custom:.4f}s")


def run_tests():
    print("--- ТЕСТУВАННЯ ФУНКЦІЙ ---")

    # remove
    l1 = [1, 2, 3, 4, 5, 2]
    remove(l1, 2)
    print(f"remove: {l1}")
    l2 = ['a', 'b', 'c']
    remove(l2, 'a')
    print(f"remove: {l2}")
    l3 = [True, False]
    remove(l3, False)
    print(f"remove: {l3}")
    l4 = [[1], [2]]
    remove(l4, [1])
    print(f"remove: {l4}")
    l5 = [10.5, 20.1]
    remove(l5, 10.5)
    print(f"remove: {l5}")

    # items
    print(f"items: {items({'a': 1, 'b': 2})}")
    print(f"items: {items({1: 'x', 2: 'y'})}")
    print(f"items: {items({})}")
    print(f"items: {items({(1, 2): 'tuple'})}")
    print(f"items: {items({'test': [1, 2, 3]})}")

    # intersection
    print(f"intersection: {intersection({1, 2, 3}, {2, 3, 4})}")
    print(f"intersection: {intersection(set(), {1})}")
    print(f"intersection: {intersection({10}, {20})}")
    print(f"intersection: {intersection({'a', 'b'}, {'b', 'c'})}")
    print(f"intersection: {intersection({True}, {1})}")

    # index
    print(f"index: {index('hello world', 'world')}")
    print(f"index: {index('python', 'p')}")
    print(f"index: {index('aaaaa', 'aa')}")
    print(f"index: {index('12345', '34')}")
    print(f"index: {index('complex test case', 'test')}")

    # copy
    d1 = deque([1, 2, 3])
    d2 = copy(d1)
    print(f"copy: {d2}, is same object: {d1 is d2}")
    print(f"copy empty: {copy(deque())}")
    print(f"copy strings: {copy(deque(['a', 'b']))}")
    print(f"copy nested: {copy(deque([[1], [2]]))}")
    print(f"copy mixed: {copy(deque([1, 'a', 3.14]))}")
    print("\n")


if __name__ == "__main__":
    run_tests()
    benchmark()
