from .models import Choice, Question
from django.test import TestCase
import datetime
from django.db import models
from django.utils import timezone
from django.db import connection
import json

class Questions_TestCase(TestCase):
    def test_was_published_recently(self):
        today = timezone.now()
        question = Question(question_text="Is this awesome?", pub_date=today)
        self.assertTrue(question.was_published_recently())

    def test_was_not_published_recently(self):
        long_time_ago = datetime.datetime.strptime('2020-01-01', '%Y-%m-%d').replace(tzinfo=datetime.timezone.utc)
        question = Question(question_text="Is this awesome?", pub_date=long_time_ago)
        self.assertFalse(question.was_published_recently())

    def test_the_db_a_bit(self):
        long_time_ago = datetime.datetime.strptime('2020-01-01', '%Y-%m-%d').replace(tzinfo=datetime.timezone.utc)
        question = Question(question_text="Is this awesome?", pub_date=long_time_ago)
        question.save()

        ids = [question.id]
        print(ids)
        question_list = Question.objects.filter(id__in=ids)
        self.assertEqual(question_list[0], question)

        # delete an item and check that it's actually gone
        question.delete()
        question_list = Question.objects.filter(id__in=ids)
        self.assertEqual(len(question_list), 0)

        # read the same item and then make sure it's back in the DB
        question.save()
        ids = [question.id]
        question_list = Question.objects.filter(id__in=ids)
        self.assertEqual(question_list[0], question)

        # playing with relationships
        choice_1 = Choice(choice_text="Yes", question=question)
        choice_2 = Choice(choice_text="No", question=question)
        choice_1.save()
        choice_2.save()
        choice_1.choice_text = "Maybe"
        choice_1.save()
        choices = Choice.objects.filter(choice_text="Maybe") # no index, but it's ok because this is just a test
        self.assertEqual(choices[0], choice_1)

        ql = QueryLogger()
        with connection.execute_wrapper(ql):
            # note this is really important
            # without it, django will do all sorts of funky lazy loading that you want
            # it's comparable to EF/.net's .ToList()
            choices = list(Choice.objects.prefetch_related('question').all())
            print(choices[0].choice_text)
            print("question", choices[0].question)
            print("question", choices[1].question)
        print(json.dumps(ql.queries, indent=4))

        # do a where based update
        Question.objects.filter(id=question.id).update(question_text="This is after a where update!")
        question_list = Question.objects.filter(id__in=ids)
        self.assertEqual(question_list[0].question_text, "This is after a where update!")

        print("donezo")

import time
class QueryLogger:
    def __init__(self):
        self.queries = []

    def __call__(self, execute, sql, params, many, context):
        current_query = {"sql": sql, "params": params, "many": many}
        start = time.monotonic()
        try:
            result = execute(sql, params, many, context)
        except Exception as e:
            current_query["status"] = "error"
            current_query["exception"] = e
            raise
        else:
            current_query["status"] = "ok"
            return result
        finally:
            duration = time.monotonic() - start
            current_query["duration"] = duration
            self.queries.append(current_query)

