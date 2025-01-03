import time
import pytest
import sys
from pathlib import Path

polls_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(polls_dir))

from polls.polls_utils.some_code import foo, MyClass


# def test_my_stuff(benchmark):
#     # benchmark foo
#     result = benchmark(foo)
#     assert result == 123
#
#
# def test_my_stuff_different_arg(benchmark):
#     # benchmark foo, but add some arguments
#     result = benchmark(foo, 0.001)
#     assert result == 123


@pytest.mark.benchmark(
    group="group-name",
    min_time=0.1,
    max_time=0.5,
    min_rounds=5,
    timer=time.time,
    disable_gc=True,
    warmup=False
)
def test_my_stuff(benchmark):
    @benchmark
    def result():
        # Code to be measured
        return time.sleep(0.000001)

    # Extra code, to verify that the run
    # completed correctly.
    # Note: this code is not measured.
    assert result is None


# def test_class_method(benchmark):
#     benchmark.weave(MyClass.bar, lazy=True)
#     mc = MyClass()
#     mc.bar()
#

