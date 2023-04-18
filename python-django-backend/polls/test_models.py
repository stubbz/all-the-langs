from .models import Question
from django.test import TestCase
import datetime
from django.db import models
from django.utils import timezone

class Questions_TestCase(TestCase):
    def test_was_published_recently(self):
        today = timezone.now()
        question = Question(question_text="Is this awesome", pub_date=today)
        self.assertTrue(question.was_published_recently())

    def test_was_not_published_recently(self):
        long_time_ago = datetime.datetime.strptime('2020-01-01', '%Y-%m-%d').replace(tzinfo=datetime.timezone.utc)
        question = Question(question_text="Is this awesome", pub_date=long_time_ago)
        self.assertFalse(question.was_published_recently())