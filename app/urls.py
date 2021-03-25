# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from app import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path('add_member', views.add_member, name='add_member'),
    path('populate_members', views.populate_members, name='populate_members'),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
