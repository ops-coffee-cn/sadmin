#!/usr/bin/env python
#-*- coding: utf-8 -*-
#update:2014-09-12 by liufeily@163.com

from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response,RequestContext
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from UserManage.models import User,RoleList,PermissionList
from UserManage.forms import AddPermissionForm,EditPermissionForm

def PermissionVerify():
    '''权限认证模块,
        此模块会先判断用户是否是管理员（is_superuser为True），如果是管理员，则具有所有权限,
        如果不是管理员则获取request.user和request.path两个参数，判断两个参数是否匹配，匹配则有权限，反之则没有。
    '''
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            print '====>%s-%s' %(request.path,request.user)

            iUser = User.objects.filter(username=request.user)
            for m in iUser:
                superuser = m.is_superuser
                roleName = m.role
                if roleName:
                    iRole = RoleList.objects.get(name=roleName)
                    permission_id_list = iRole.permission
                else:
                    permission_id_list = []

            permission = PermissionList.objects.all()
            if permission:
                pId = str('error01')  #PID默认为error，下边匹配到替换
                for n in permission:
                    if request.path == n.url or request.path.rstrip('/') == n.url: #精确匹配，判断request.path是否与permission表中的某一条相符
                        pId = str(n.id)
                    elif request.path.startswith(n.url):  #判断request.path是否以permission表中的某一条url开头
                        pId = str(n.id)
            else:
                pId = str('error02')

            if not superuser:
                if permission_id_list is None or pId not in permission_id_list:
                    return HttpResponseRedirect('/accounts/permission/deny')

            return view_func(request, *args, **kwargs)
        return _wrapped_view

    return decorator

@login_required
def NoPermission(request):

    kwvars = {
        'request':request,
    }

    return render_to_response('UserManage/nopermission.html',kwvars,RequestContext(request))

@login_required
@PermissionVerify()
def AddPermission(request):
    if request.method == "POST":
        form = AddPermissionForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/accounts/permission/list')
    else:
        form = AddPermissionForm()

    kwvars = {
        'form':form,
        'request':request,
    }

    return render_to_response('UserManage/permissionadd.html',kwvars,RequestContext(request))

@login_required
@PermissionVerify()
def ListPermission(request):
    pList = PermissionList.objects.all()

    #分页功能
    paginator = Paginator(pList, 20)

    page = request.GET.get('page')
    try:
        lst = paginator.page(page)
    except PageNotAnInteger:
        lst = paginator.page(1)
    except EmptyPage:
        lst = paginator.page(paginator.num_pages)

    kwvars = {
        'pList':lst,
        'request':request,
    }

    return render_to_response('UserManage/permissionlist.html',kwvars,RequestContext(request))

@login_required
@PermissionVerify()
def EditPermission(request,ID):
    iPermission = PermissionList.objects.get(id=ID)

    if request.method == "POST":
        form = EditPermissionForm(request.POST,instance=iPermission)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/accounts/permission/list')
    else:
        form = EditPermissionForm(instance=iPermission)

    kwvars = {
        'form':form,
        'object':iPermission,
        'request':request,
    }

    return render_to_response('UserManage/permissionedit.html',kwvars,RequestContext(request))

@login_required
@PermissionVerify()
def DeletePermission(request,ID):
    PermissionList.objects.filter(id = ID).delete()

    return HttpResponseRedirect('/accounts/permission/list')
