# 代码覆盖率

代码覆盖度表示有多少源代码被测试了。它表明了代码的哪些部分被测试用例覆盖，哪些没有。这是测试应用很重要的部分，所以强烈推荐检查测试用例的覆盖度。

## Coverage

官方文档：https://coverage.readthedocs.io/en/7.6.10/index.html

`coverage.py`是一个测量Python程序代码覆盖率的工具。它监视你的程序，注意代码的哪些部分已被执行，然后分析源代码以识别可能已执行但未执行的代码。

### 安装

1.pip安装coverage.py

```shell
pip install coverage
```

### 快速了解使用

1.编写一个简单的示例，理解覆盖率的使用。

```python
import unittest


def some_login_api(username: str = None, password:str = None):
    """
    某登录API验证逻辑
    """
    if username is None or password is None:
        return "username or password is null"
    elif isinstance(username, str) is False or isinstance(password, str) is False:
        return "username or password type error"
    elif len(username) < 6:
        return "username length error"
    elif password.startswith("abc") or password.startswith("123"):
        return "password too easy"
    else:
        return "login success"


class SomeLoginTest(unittest.TestCase):

    def test_login_null(self):
        ret = some_login_api()
        self.assertEqual(ret, "username or password is null")
```
> 根据`some_login_api()`函数的逻辑，SomeLoginTest测试类中的代码只有一条用例肯定是覆盖率不全的。

2.使用`coverage run`来运行测试套件并收集数据。无论通常如何运行你的测试套件，都可以在覆盖下使用的测试运行器。

```shell
pytest

or 

python -m unittest discover
```
> 注：pytest 可以执行unittest编写的用例。

将上面的命令替换为 `coverage run`命令。

```shell
coverage run -m pytest

or 

coverage run -m unittest discover
```

3.使用 `coverage report`去报告结果：

```shell
coverage report -m
Name                Stmts   Miss  Cover   Missing
-------------------------------------------------
__init__.py             0      0   100%
test_something.py      15      7    53%   10-17
-------------------------------------------------
TOTAL                  15      7    53%
```

4.进一步补充测试用例，提高覆盖率

```python
import unittest

def some_login_api(username: str = None, password:str = None):
    ...


class SomeLoginTest(unittest.TestCase):

    def test_login_null(self):
        ret = some_login_api()
        self.assertEqual(ret, "username or password is null")

    def test_login_type_error(self):
        ret = some_login_api("administrator", 97843580134958)
        self.assertEqual(ret, "username or password type error")

    def test_login_length_error(self):
        ret = some_login_api("admin", "admin123")
        self.assertEqual(ret, "username length error")

    def test_login_password_error(self):
        ret = some_login_api("abcxyz", "123456")
        self.assertEqual(ret, "password too easy")

    def test_login_success(self):
        ret = some_login_api("administrator", "admin123456")
        self.assertEqual(ret, "login success")
```

重新运行测试，并统计覆盖率

```shell
> coverage run -m unittest discover  # 运行测试
.....
----------------------------------------------------------------------
Ran 5 tests in 0.001s

OK


> coverage report -m   # 统计覆盖率
Name                Stmts   Miss  Cover   Missing
-------------------------------------------------
test_something.py      27      0   100%
-------------------------------------------------
TOTAL                  27      0   100%
```

### HTML报告

为了更好的展示，使用`coverage html`来获得详细说明遗漏行的带注释的html清单：

```shell
> coverage html

Wrote HTML report to htmlcov\index.html
```

![](./images/coverage_html_report.png)

## django 中使用 Coverage


要使用标准测试设置运行 Django 测试套件的覆盖率：

1.运行之前编写的django测试

```shell
coverage run manage.py test polls
Found 25 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
.....................
DevTools listening on ws://127.0.0.1:5260/devtools/browser/68bef940-a12f-46c7-a868-4e16dcadb755
[31084:13372:0105/015028.956:ERROR:edge_qqbrowser_importer_utils_win.cc(190)] QQBrowser profile preference file doesn't exist
[31084:17956:0105/015030.569:ERROR:fallback_task_provider.cc(126)] Every renderer should have at least one task provided by a primary task provider. If a "Renderer" fallback task is shown, it is a bug. If you have repro steps, please file a new bug and tag it as a dependency of crbug.com/739782.
....[05/Jan/2025 01:50:35,841] - Broken pipe from ('127.0.0.1', 5284)
[05/Jan/2025 01:50:35,841] - Broken pipe from ('127.0.0.1', 5281)
[05/Jan/2025 01:50:35,841] - Broken pipe from ('127.0.0.1', 5282)

----------------------------------------------------------------------
Ran 25 tests in 21.786s

OK
Destroying test database for alias 'default'...
```

2.生成覆盖率结果

```shell
coverage report -m
Name                               Stmts   Miss  Cover   Missing
----------------------------------------------------------------
manage.py                             11      2    82%   12-13
mysite\__init__.py                     0      0   100%
mysite\settings.py                    27      0   100%
mysite\urls.py                         5      0   100%
polls\__init__.py                      0      0   100%
polls\admin.py                         4      0   100%
polls\apps.py                          4      0   100%
polls\migrations\0001_initial.py       6      0   100%
polls\migrations\__init__.py           0      0   100%
polls\models.py                       17      2    88%   12, 28
polls\polls_utils\__init__.py          0      0   100%
polls\polls_utils\some_code.py         9      0   100%
polls\tests\__init__.py                0      0   100%
polls\tests\common.py                  8      0   100%
polls\tests\test_model.py             57      0   100%
polls\tests\test_template.py          48      0   100%
polls\tests\test_view.py              68      0   100%
polls\urls.py                          4      0   100%
polls\views.py                        37      0   100%
----------------------------------------------------------------
TOTAL                                305      4    99%
```
