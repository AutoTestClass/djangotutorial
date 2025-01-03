"""
用于测试silk分析
"""
from time import sleep


def foo(duration=0.000001):
    """
    Function that needs some serious benchmarking.
    """
    sleep(duration)
    return 123


class MyClass:
    def __init__(self, arg=0.01):
        self.arg = arg

    def bar(self) -> []:
        sleep(self.arg)
