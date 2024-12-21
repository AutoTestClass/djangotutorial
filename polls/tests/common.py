import datetime
from django.utils import timezone

from polls.models import Question, Choice


def create_question(question_id: int, question_text: str, days: int):
    """
    封装: 创建问题
    """
    time = timezone.now() - datetime.timedelta(days=days)
    return Question.objects.create(id=question_id, question_text=question_text, pub_date=time)


def create_choice(question, choice_id: int, choice_text: str, votes: int = 0):
    """
    封装问题选项的创建
    """
    return Choice.objects.create(question=question, id=choice_id, choice_text=choice_text, votes=votes)
