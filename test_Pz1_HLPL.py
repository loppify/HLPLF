import pytest

from Pz1_HLPL import *


@pytest.mark.parametrize("a, b, expected", [
    (1, 2, 3),
    (-1, 1, 0),
    (0.5, 0.4, 0.9),
    (0.5, 0.5, 1.0),
])
def test_sumnum(a, b, expected):
    assert sumnum(a, b) == expected


@pytest.mark.parametrize("num, expected", [
    (7, True),
    (10, False),
    (13, True),
    (1, False)
])
def test_is_num_simple(num, expected):
    assert is_num_simple(num) == expected


class TestCalculator:

    @pytest.fixture
    def basic_calc(self):
        return Calculator(10, 2, 3)

    def test_add(self, basic_calc):
        assert basic_calc.add() == 15

    def test_sub(self, basic_calc):
        assert basic_calc.sub() == 5

    def test_div_simple(self):
        calc = Calculator(100, 2, 10)
        assert calc.div() == 5

    def test_div_by_zero(self):
        calc = Calculator(10, 0)
        with pytest.raises(ZeroDivisionError):
            calc.div()

    def test_init_error(self):
        with pytest.raises(ArithmeticError):
            Calculator(5)

    @pytest.mark.parametrize("args, expected_sum", [
        ((1, 1, 1), 3),
        ((10, -5), 5),
        ((0, 0, 0, 0), 0)
    ])
    def test_add_multiple_cases(self, args, expected_sum):
        calc = Calculator(*args)
        assert calc.add() == expected_sum


class TestBookstore:
    @pytest.fixture
    def store(self):
        return Bookstore()

    def test_add_new_book(self, store):
        store + "Kobzar"
        assert "Kobzar" in store.books
        assert store.books["Kobzar"] == 1

    def test_add_existing_book(self, store):
        store + "Kobzar"
        store + "Kobzar"
        assert store.books["Kobzar"] == 2

    def test_sub_decrease_count(self, store):
        store + "Kobzar"
        store + "Kobzar"
        store - "Kobzar"
        assert store.books["Kobzar"] == 1

    def test_sub_remove_entirely(self, store):
        store + "Kobzar"
        store - "Kobzar"
        assert "Kobzar" not in store.books
