class RList:
    def __init__(self, data, next_node=None):
        self.data = data
        self.next = next_node

    def add_head(self, data):
        self.next = RList(self.data, self.next)
        self.data = data

    def add_before(self, target, data):
        if self.data == target:
            self.add_head(data)
            return True
        if self.next is None:
            return False
        if self.next.data == target:
            self.next = RList(data, self.next)
            return True
        return self.next.add_before(target, data)

    def remove_first(self, target):
        if self.data == target:
            if self.next:
                self.data = self.next.data
                self.next = self.next.next
                return True
            else:
                raise ValueError("Cannot remove the only element in this recursive structure")

        if self.next:
            if self.next.data == target:
                self.next = self.next.next
                return True
            return self.next.remove_first(target)
        return False

    def remove_even_pos(self):
        if self.next:
            self.next = self.next.next
            if self.next:
                self.next.remove_even_pos()

    def print_odd_values(self):
        curr = self
        result = []
        while curr:
            if isinstance(curr.data, (int, float)) and curr.data % 2 != 0:
                result.append(str(curr.data))
            curr = curr.next
        print("Odd values: " + ", ".join(result))

    def contains(self, target):
        if self.data == target:
            return True
        if self.next is None:
            return False
        return self.next.contains(target)

    @property
    def Second(self):
        if self.next is None:
            raise IndexError("Second element does not exist")
        return self.next.data

    @Second.setter
    def Second(self, value):
        if self.next is None:
            self.next = RList(value)
        else:
            self.next.data = value

    def __str__(self):
        if self.next is None:
            return str(self.data)
        return str(self.data) + " -> " + str(self.next)


def main():
    # 1. Конструктор з одним та двома параметрами
    node2 = RList(20)
    r = RList(10, node2)
    print(f"Початковий список: {r}")

    # 2. Метод додавання першим
    r.add_head(5)
    print(f"Після add_head(5): {r}")

    # 3. Додавання перед значенням
    r.add_before(20, 15)
    print(f"Після add_before(20, 15): {r}")

    # 4. Пошук елемента
    print(f"Містить 15? {r.contains(15)}")
    print(f"Містить 100? {r.contains(100)}")

    # 5. Властивість Second
    print(f"Поточне значення Second: {r.Second}")
    r.Second = 99
    print(f"Після r.Second = 99: {r}")

    # 6. Видалення всіх парних по індексу
    r.remove_even_pos()
    print(f"Після remove_even_pos: {r}")

    # 7. Друк непарних значень
    r.add_head(3)
    r.add_head(8)
    print(f"Список перед друком непарних: {r}")
    r.print_odd_values()

    # 8. Видалення заданого значення
    r.remove_first(3)
    print(f"Після remove_first(3): {r}")


if __name__ == "__main__":
    main()
