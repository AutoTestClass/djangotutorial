import sys
from pathlib import Path

import pyperf

polls_dir = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(polls_dir))

from polls.polls_utils.some_code import foo

runner = pyperf.Runner(processes=4)

setup = "from polls.polls_utils.some_code import foo"

runner.timeit(name="foo test",
              stmt="foo()",
              setup=setup)
