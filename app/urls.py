# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from app import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),

    # Member related URLs
    path('add_member', views.add_member, name='add_member'),
    path('fetch_members_and_balances', views.fetch_members_and_balances, name='fetch_members_and_balances'),

    # Member related URLs
    path('add_transaction', views.add_transaction, name='add_transaction'),
    path('fetch_transactions', views.fetch_transactions, name='fetch_transactions'),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
