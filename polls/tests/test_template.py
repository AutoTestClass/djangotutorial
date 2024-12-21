import datetime
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.webdriver import WebDriver
from polls.models import Question, Choice
from django.utils import timezone
from polls.tests.common import create_question, create_choice


class MySeleniumTests(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(2)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def setUp(self):
        self.question = create_question(question_id=1, question_text="Your favorite movie", days=1)
        create_choice(question=self.question, choice_id=1, choice_text="Brave heart")
        create_choice(question=self.question, choice_id=2, choice_text="Harry Potter and the Philosopher's Stone")
        # # 先创建 Question 对象
        # self.question = Question.objects.create(
        #     id=1,
        #     question_text="Your favorite movie",
        #     pub_date=timezone.now() - datetime.timedelta(minutes=1)
        # )
        # # 创建 Choice 对象时正确设置 question 字段
        # Choice.objects.create(
        #     id=1,
        #     choice_text="Brave heart",
        #     question=self.question
        # )
        # Choice.objects.create(
        #     id=2,
        #     choice_text="Harry Potter and the Philosopher's Stone",
        #     question=self.question
        # )

    def test_index(self):
        self.selenium.get(f"{self.live_server_url}/polls/")
        q_title = self.selenium.find_element(By.TAG_NAME, "a")
        self.assertQuerySetEqual(q_title.text, "Your favorite movie")

    def test_detail(self):
        """测试详情页面"""
        self.selenium.get(f"{self.live_server_url}/polls/")
        self.selenium.find_element(By.TAG_NAME, "a").click()
        # 获取选项断言
        choices = self.selenium.find_elements(By.TAG_NAME, "label")
        self.assertEqual(choices[0].text, "Brave heart")
        self.assertEqual(choices[1].text, "Harry Potter and the Philosopher's Stone")

    def test_vote(self):
        """测试投票功能"""
        # 点击选项，进入结果页，检查结果
        self.selenium.get(f"{self.live_server_url}/polls/1/")
        # 选择第一个选项
        self.selenium.find_element(By.CSS_SELECTOR, "input[type='radio'][value='1']").click()
        # 点击投票按钮
        self.selenium.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
        
        # 检查结果页面
        results = self.selenium.find_elements(By.TAG_NAME, "li")
        self.assertIn("Brave heart", results[0].text)
        self.assertIn("1 vote", results[0].text)

    def test_vote_again(self):
        """测试投票功能，再次投票，检查结果"""
        # 第一次投票
        self.selenium.get(f"{self.live_server_url}/polls/1/")
        self.selenium.find_element(By.CSS_SELECTOR, "input[type='radio'][value='1']").click()
        self.selenium.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
        
        # 点击"Vote again?"链接返回投票页
        self.selenium.find_element(By.LINK_TEXT, "Vote again?").click()
        
        # 第二次投票，选择第二个选项
        self.selenium.find_element(By.CSS_SELECTOR, "input[type='radio'][value='2']").click()
        self.selenium.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
        
        # 检查结果页面
        results = self.selenium.find_elements(By.TAG_NAME, "li")
        # 第一个选项应该有1票
        self.assertIn("Brave heart", results[0].text)
        self.assertIn("1 vote", results[0].text)
        # 第二个选项应该有1票
        self.assertIn("Harry Potter and the Philosopher's Stone", results[1].text)
        self.assertIn("1 vote", results[1].text)
