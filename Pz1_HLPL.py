# Рівень 1:
# 3.	Створіть програму, яка приймає два числа від користувача та виводить їх суму.


def sumnum(num1, num2):
    return num1 + num2


print(float(input()) + float(input()))


# Рівень 2:
# 3.	Реалізуйте програму, яка визначає, чи є введене користувачем число простим.

# num = int(input())


def is_num_simple(num):
    if num < 2:
        return False
    for i in range(2, num // 2):
        if num % i == 0:
            return False
    return True


# print(is_num_simple(num))


# Рівень 3:
# 3.	Створіть клас "Калькулятор" з методами для додавання, віднімання, множення та ділення. Виведіть результат обчислень для певного прикладу.

class Calculator:
    def __init__(self, *args):
        if len(args) < 2:
            raise ArithmeticError
        self.nums = args

    def add(self):
        return sum(self.nums)

    def sub(self):
        return self.nums[0] - sum(self.nums[1:])

    def mul(self):
        res = 1
        for i in self.nums:
            res *= i
        return res

    def div(self):
        res = self.nums[0]
        for i in self.nums[1:]:
            if i == 0:
                raise ZeroDivisionError
            res /= i
        return res


# Рівень 4:
# 3.	Створіть клас "Книготека" з можливістю додавання та видалення книг, а також виведення списку усіх книг.

class Bookstore:
    def __init__(self):
        self.books = {}

    def __add__(self, other):
        if other in self.books:
            self.books[other] += 1
            return self
        self.books[other] = 1
        return self

    def __sub__(self, other):
        if other in self.books and self.books[other] > 1:
            self.books[other] -= 1
            return self
        self.books.pop(other)
        return self

    def view_all_books(self):
        for i in self.books:
            print(f"{i}: {self.books[i]} pcs")

# bookshelf = Bookstore()
# bookshelf + "1984" + "Dune" + "Clean code" + "Harry Potter" + "Dune" + "Dune"
# bookshelf.view_all_books()
