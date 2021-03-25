# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.test import TestCase
from app.models import User, Transaction, Member

class AppTestCase(TestCase):
    def setUp(self):
        user = User(first_name = "ali", last_name = "baba", email = "ali@gmail.com")
        user.save()
        member = Member(phone_number = "00923928", user = user)
        member.save()
        transaction = Transaction(amount =-10200, date = "2021-11-01", transaction_type = "withdrawal") 
        transaction.save()

    def test_create_all_models(self):
        users = User.objects.all()
        users = User.objects.all()

        self.assertTrue(users.exists())