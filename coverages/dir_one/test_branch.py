import unittest


def check_number(x):
    if x > 0:
        return "Positive"
    elif x < 0:
        return "Negative"
    else:
        return "Zero"


class TestCheckNumber(unittest.TestCase):
    def test_positive(self):
        result = check_number(10)
        self.assertEqual(result, "Positive")

    def test_negative(self):
        result = check_number(-5)
        self.assertEqual(result, "Negative")

    def test_zero(self):
        result = check_number(0)
        self.assertEqual(result, "Zero")


if __name__ == '__main__':
    unittest.main()
