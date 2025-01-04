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
