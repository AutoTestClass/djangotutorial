# djangotutorial

> django 官方示例

https://docs.djangoproject.com/zh-hans/5.1/intro/


## 运行应用

```shell
python manage.py runserver
```


## 运行测试

运行所有用例：

```shell
python3 manage.py test
```

运行polls应用下的所有用例：

```shell
python3 manage.py test polls
```


运行polls应用下的tests.py文件用例：

```shell
python3 manage.py test polls.tests
```


运行polls应用下的tests.py文件中的 QuestionModelTests 测试类：

```shell
python3 manage.py test polls.tests.QuestionModelTests
```
