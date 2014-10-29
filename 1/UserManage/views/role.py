#!/usr/bin/env python
#-*- coding: utf-8 -*-
#update:2014-09-12 by liufeily@163.com

from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response,RequestContext
from django.contrib.auth.decorators import login_required
from website.common.CommonPaginator import SelfPaginator
from UserManage.views.permission import PermissionVerify

from UserManage.forms import RoleListForm
from UserManage.models import RoleList

@login_required
@PermissionVerify()
def AddRole(request):
    if request.method == "POST":
        form = RoleListForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/accounts/role/list')
    else:
        form = RoleListForm()

    kwvars = {
        'form':form,
        'request':request,
        'title':'Role Add',
        'postUrl':'/accounts/role/add/',
    }

    return render_to_response('UserManage/roleadd.html',kwvars,RequestContext(request))

@login_required
@PermissionVerify()
def ListRole(request):
    mList = RoleList.objects.all()

    #分页功能
    lst = SelfPaginator(request,mList, 20)

    kwvars = {
        'lPage':lst,
        'request':request,
    }

    return render_to_response('UserManage/rolelist.html',kwvars,RequestContext(request))

@login_required
@PermissionVerify()
def EditRole(request,ID):
    iRole = RoleList.objects.get(id=ID)

    if request.method == "POST":
        form = RoleListForm(request.POST,instance=iRole)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/accounts/role/list')
    else:
        form = RoleListForm(instance=iRole)

    kwvars = {
        'form':form,
        'request':request,
        'title':'Role Edit',
        'postUrl':'/accounts/role/edit/%s/' %ID,
    }

    return render_to_response('UserManage/roleedit.html',kwvars,RequestContext(request))

@login_required
@PermissionVerify()
def DeleteRole(request,ID):
    RoleList.objects.filter(id = ID).delete()

    return HttpResponseRedirect('/accounts/role/list')
