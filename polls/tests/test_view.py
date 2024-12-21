import datetime
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from polls.models import Question, Choice
from polls.tests.common import create_question


class PollsPageTest(TestCase):
    """测试polls首页"""

    def test_polls_page_renders_index_template(self):
        """
        断言是否用给定的index.html模版响应
        """
        response = self.client.get('/polls/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'polls/index.html')

    def test_no_questions(self):
        """
        如果没有问题，提示：No polls are available
        """
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_past_question(self):
        """
        查询过去的问题
        """
        question = create_question(question_id=1, question_text="Past question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question],
        )

    def test_future_question(self):
        """
        查询未来的问题
        """
        create_question(question_id=1, question_text="Future question.", days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_future_question_and_past_question(self):
        """
        查询未来的问题和过去的问题
        """
        question = create_question(question_id=1, question_text="Past question.", days=30)
        create_question(question_id=2, question_text="Future question.", days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question],
        )

    def test_two_past_questions(self):
        """
        按发布日期降序排列，最新的问题应该排在前面。
        """
        question1 = create_question(question_id=1, question_text="Past question 1.", days=30)
        question2 = create_question(question_id=2, question_text="Past question 2.", days=5)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question2, question1],
            ordered=True
        )
