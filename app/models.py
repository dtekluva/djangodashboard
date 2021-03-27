# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from scripts.time_helpers import convert_date
from datetime import datetime
# Create your models here.
       
class Member(models.Model):
    phone_number = models.CharField(max_length=20, default="0")
    city         = models.CharField(max_length=20, default="0")
    country      = models.CharField(max_length=20, default="0")
    address      = models.CharField(max_length=100, default="0")
    user         = models.OneToOneField(User, on_delete=CASCADE, null=True, blank=True)

    class Meta:

        verbose_name_plural = "Members"
    
    def __str__(self):
        return self.user.username
    
    @property
    def full_name(self):
        return f"{self.user.last_name} {self.user.first_name}"

    def get_balance(self, start_date = False, end_date = False):
        all_transactions = self.transaction_set.all()

        if all_transactions.exists():
            total_transaction = 0

            for transaction in all_transactions:
                total_transaction += transaction.amount
            
            return total_transaction

        else:
            
            return 0
    
    def get_total_deposits(self, start_date = False, end_date = False):
        return self.transaction_set.filter(transaction_type = "deposit").aggregate(sum('amount'))
    
    def get_total_withdrawal(self, start_date = False, end_date = False):
        return self.transaction_set.filter(transaction_type = "withdrawal").aggregate(sum('amount'))

    @staticmethod
    def add_member(**details):

        first_name = details["first_name"]
        last_name = details["last_name"]
        email = details["email"]
        address = details["address"]
        city = details["city"]
        phone_number = details["phone"]
        country = details["country"]

        user = User(username = email, first_name = first_name, 
                    last_name = last_name, 
                    email = email)
        user.save()
        
        member = Member(phone_number = phone_number,
                        city = city,
                        country = country,
                        address = address,
                        user = user)
        member.save()

        return {
            "status":True
        }

    @staticmethod
    def get_all():

        all_members = Member.objects.all().order_by("-id")

        member_values = map(lambda member: dict(
                                                    id = member.id,
                                                    name = member.full_name,
                                                    email = member.user.email,
                                                    address = member.address,
                                                    city = member.city,
                                                    phone = member.phone_number,
                                                    country = member.country,
                                                    balance = member.get_balance(),
                                                    last_transaction = member.get_last_transaction()
                                                ),  all_members
                            )
        
        return dict(
                    data = list(member_values)
                    )

    def get_last_transaction(self):
        
        ordered_transaction = self.transaction_set.all().order_by("-date")

        if ordered_transaction.exists():
            last_transaction = ordered_transaction[0]

            return dict(
                amount = last_transaction.amount,
                date = last_transaction.date
            )
        else:
            return dict(
                            amount = 0,
                            date = "-"
                        )

class Transaction(models.Model):

    amount = models.FloatField(default= 0)
    member   = models.ForeignKey(Member, on_delete=CASCADE, null=True, blank=True)
    date   = models.DateField(null=True, blank=True)

    DEPOSIT = 'deposit'
    WITHDRAWAL = 'withdrawal'

    STATUS = [
       (DEPOSIT,('deposit')),
       (WITHDRAWAL,('withdrawal')),
    ]

    transaction_type = models.CharField(
        max_length=32,
        choices=STATUS,
        default=DEPOSIT,
    )
    
    def __str__(self):
        return self.member.user.username  

    def save(self, *args, **kwargs):
        if self.transaction_type == "withdrawal":
            self.amount *= -1  # make transaction amount negative
        super(Transaction, self).save(*args, **kwargs)
    
    @staticmethod
    def add_transaction(**details):

        member_id = details["member"]
        date = details["date"]
        amount = float(details["amount"])
        transaction_type = details["transaction_type"]

        member = Member.objects.get(id = member_id)
        member.save()
        
        transaction = Transaction(member = member,
                                    amount = amount,
                                    date = date,
                                    transaction_type = transaction_type,
                                )
        transaction.save()

        return {
                "status":True
                }

    @staticmethod
    def get_all():

        all_transactions = Transaction.objects.all().order_by("-date")

        transansaction_values = map(lambda transaction: dict(
                                                    id = transaction.id,
                                                    name = transaction.member.full_name,
                                                    email = transaction.member.user.email,
                                                    address = transaction.member.address,
                                                    city = transaction.member.city,
                                                    phone = transaction.member.phone_number,
                                                    country = transaction.member.country,
                                                    balance = transaction.member.get_balance(),
                                                    last_transaction = transaction.member.get_last_transaction(),
                                                    date = transaction.date,
                                                    amount = transaction.amount,
                                                    type = transaction.transaction_type,


                                                ),  all_transactions
                            )
        
        return dict(
                    data = list(transansaction_values)
                    )