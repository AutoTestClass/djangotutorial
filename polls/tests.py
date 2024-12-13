import datetime
from django.test import TestCase
from django.utils import timezone

from .models import Question


class QuestionModelTests(TestCase):
    """模型测试"""

    def setUp(self):
        Question.objects.create(id=1, question_text="Your favorite movie", pub_date=timezone.now() - datetime.timedelta(minutes=1))
        Question.objects.create(id=2, question_text="Your favorite music", pub_date=timezone.now() - datetime.timedelta(hours=1))

    def test_query_one(self):
        """查询单条数据"""
        q1 = Question.objects.get(id=1)
        self.assertEqual(q1.id, 1)
        q2 = Question.objects.get(question_text="Your favorite music")
        self.assertEqual(q2.question_text, "Your favorite music")

    def test_query_more(self):
        """查询模糊数据"""
        result = Question.objects.filter(question_text__startswith="Your favorite")
        self.assertEqual(len(result), 2)


class QuestionModelWasPublishedRecentlyTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently()
        如果查询questions的pub_date是在未来，应该返回False.(未来不是最近的）
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently()
        如果查询questions的pub_date是过去的一天+1秒。(超出了范围）

        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently()
        如果查询questions的pub_date是过去的一天少1秒。(范围内）
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)