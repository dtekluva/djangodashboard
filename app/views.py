# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.conf.urls import url
from django.http.response import JsonResponse
from app.models import Member, Transaction
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
from django.views.decorators.csrf import csrf_exempt
from scripts.dashboard_helpers import get_extra_context
import json

@login_required(login_url="/login/")
def index(request):
    
    context = {}
    context['segment'] = 'index'

    html_template = loader.get_template( 'index.html' )
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:
        url_paths     = request.path.split('/')
        load_template = url_paths[1]
        extra_context = get_extra_context(id = url_paths[-1], segment = load_template) if len(url_paths) > 2 else {}
        context['segment'] = load_template
        context.update(extra_context)
        
        html_template = loader.get_template( load_template )
        return HttpResponse(html_template.render(context, request))
        
    except SyntaxError:
    # except template.TemplateDoesNotExist:

        html_template = loader.get_template( 'page-404.html' )
        return HttpResponse(html_template.render(context, request))

    except SyntaxError:
    
        html_template = loader.get_template( 'page-500.html' )
        return HttpResponse(html_template.render(context, request))

@csrf_exempt
@login_required(login_url="/login/")
def add_member(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        if request.method == 'POST': # If the form has been submitted...
            
            data = json.loads(request.body) 

            response = Member.add_member(**data)     
            
            return JsonResponse(response, status=200)
        
    except:

        return JsonResponse(response, status=500)


@csrf_exempt
@login_required(login_url="/login/")
def fetch_members_and_balances(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        if request.method == 'GET': # If the form has been submitted...
            
            all_members = Member.get_all()

            return JsonResponse({
                                    "all_members": all_members,
                                    "status": True
                                }, 
                                status=200)
        
    except SyntaxError:

        return JsonResponse({
                                    "all_members": "",
                                    "status": False
                                }, status=500)

@csrf_exempt
@login_required(login_url="/login/")
def add_transaction(request):

    try:

        if request.method == 'POST': # If the form has been submitted...
            
            data = json.loads(request.body) 

            response = Transaction.add_transaction(**data)     
            
            return JsonResponse(response, status=200)
        
    except SyntaxError:

        return JsonResponse({
                                "all_members": "",
                                "status": False
                            }, status=500)


@csrf_exempt
@login_required(login_url="/login/")
def fetch_transactions(request, user_id = False):

    try:

        if request.method == 'GET': # If the form has been submitted...
            
            all_transactions = Transaction.get_all()

            return JsonResponse({
                                    "all_transactions": all_transactions,
                                    "status": True
                                }, 
                                status=200)
        
    except SyntaxError:

        return JsonResponse({
                                "all_transactions": "",
                                "status": False
                            }, status=500)

@csrf_exempt
@login_required(login_url="/login/")
def fetch_transactions_for_chart(request):

    try:

        if request.method == 'GET': # If the form has been submitted...
            
            
            chart_transactions = Transaction.get_graph_data()

            return JsonResponse({
                                    "chart_transactions": chart_transactions,
                                    "status": True
                                }, 
                                status=200)
        
    except SyntaxError:

        return JsonResponse({
                                "chart_transactions": "",
                                "status": False
                            }, status=500)