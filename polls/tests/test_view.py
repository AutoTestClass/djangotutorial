from django.test import TestCase
from django.urls import reverse
from polls.tests.common import create_question, create_choice


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


class DetailTest(TestCase):
    """测试polls详情页面"""

    def setUp(self):
        self.q = create_question(1, "you love movie", 10)
        create_choice(self.q, 1, "Brave heart")
        create_choice(self.q, 2, "Harry Potter and the Wizard")

    def test_polls_page_renders_detail_template(self):
        """
        断言是否用给定的detail.html模版响应
        """
        response = self.client.get("/polls/1/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'polls/detail.html')


class VoteTest(TestCase):
    """测试polls投票动作"""

    def setUp(self):
        self.q = create_question(1, "you love movie", 10)
        create_choice(self.q, 1, "Brave heart")
        create_choice(self.q, 2, "Harry Potter and the Wizard")

    def test_polls_vote(self):
        """
        投票动作
        """
        response = self.client.post("/polls/1/vote/", data={"choice": 2})
        self.assertEqual(response.status_code, 302)

    def test_polls_vote_choice_error(self):
        """
        投票动作: 选项错误
        """
        response = self.client.post("/polls/1/vote/", data={"choice": 10})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'polls/detail.html')


class ResultTest(TestCase):
    """测试polls投票结果页"""

    def setUp(self):
        self.q = create_question(1, "you love movie", 10)
        create_choice(self.q, 1, "Brave heart")
        create_choice(self.q, 2, "Harry Potter and the Wizard")

    def test_polls_result(self):
        """
        投票结果页面
        """
        response = self.client.get("/polls/1/results/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'polls/results.html')

    def test_polls_vote_result(self):
        """
        投票结果页面： 投票动作 + 结果显示
        """
        response = self.client.post("/polls/1/vote/", data={"choice": 2})
        self.assertEqual(response.status_code, 302)

        response = self.client.get("/polls/1/results/")
        self.assertEqual(response.status_code, 200)
        # print(response.content)
        self.assertContains(response, "Harry Potter and the Wizard -- 1 vote")


