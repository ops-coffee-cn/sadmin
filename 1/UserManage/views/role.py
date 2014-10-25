#!/usr/bin/env python
#-*- coding: utf-8 -*-
#update:2014-09-12 by liufeily@163.com

from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response,RequestContext
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from UserManage.models import User,RoleList,PermissionList
from UserManage.forms import AddRoleForm,EditRoleForm
from UserManage.views.permission import PermissionVerify

@login_required
@PermissionVerify()
def AddRole(request):
    if request.method == "POST":
        form = AddRoleForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/accounts/role/list')
    else:
        form = AddRoleForm()
    
    kwvars = {
        'form':form,
        'request':request,
    }

    return render_to_response('UserManage/roleadd.html',kwvars,RequestContext(request))

@login_required
@PermissionVerify()
def ListRole(request):
    rList = RoleList.objects.all()
    pList = PermissionList.objects.all()

    #处理前台页面显示权限名称（数据库里记录的是ID，要显示成名称更直观）
    rDict = {}
    for x in rList:
        nS = ''
        for y in x.permission:
            name = pList.get(id = int(y)).name
            nS = nS + ',' + name

        rDict[long(x.id)] = nS.strip(',')

    #分页功能
    paginator = Paginator(rList, 20)

    page = request.GET.get('page')
    try:
        lst = paginator.page(page)
    except PageNotAnInteger:
        lst = paginator.page(1)
    except EmptyPage:
        lst = paginator.page(paginator.num_pages)

    kwvars = {
        'rList':rList,
        'rDict':rDict,
        'lPage':lst,
        'request':request,
    }

    return render_to_response('UserManage/rolelist.html',kwvars,RequestContext(request))

@login_required
@PermissionVerify()
def EditRole(request,ID):
    iRole = RoleList.objects.get(id=ID)

    if request.method == "POST":
        form = EditRoleForm(request.POST,instance=iRole)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/accounts/role/list')
    else:
        form = EditRoleForm(instance=iRole)

    kwvars = {
        'form':form,
        'object':iRole,
        'request':request,
    }

    return render_to_response('UserManage/roleedit.html',kwvars,RequestContext(request))

@login_required
@PermissionVerify()
def DeleteRole(request,ID):
    RoleList.objects.filter(id = ID).delete()

    return HttpResponseRedirect('/accounts/role/list')
