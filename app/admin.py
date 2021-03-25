# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin

from .models import Member, Transaction


class TransactionAdmin(admin.ModelAdmin):
    fields = ['member', 'amount', "date", "transaction_type"]
    list_display = ('member', 'amount', "date", "transaction_type")

admin.site.register(Transaction, TransactionAdmin)

class MemberAdmin(admin.ModelAdmin):
    fields = ['user', 'phone_number', "country", "city"]
    list_display = ('user', 'phone_number', "country", "city")

admin.site.register(Member, MemberAdmin)