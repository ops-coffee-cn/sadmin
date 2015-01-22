#!/usr/bin/env python
#-*- coding: utf-8 -*-
#update:2014-09-12 by liufeily@163.com

from django import forms
from django.contrib import auth
from django.contrib.auth import get_user_model
from UserManage.models import User,RoleList,PermissionList

class LoginUserForm(forms.Form):
    username = forms.CharField(label=u'账 号',error_messages={'required':u'账号不能为空'},
        widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(label=u'密 码',error_messages={'required':u'密码不能为空'},
        widget=forms.PasswordInput(attrs={'class':'form-control'}))

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None

        super(LoginUserForm, self).__init__(*args, **kwargs)

    def clean_password(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = auth.authenticate(username=username,password=password)
            if self.user_cache is None:
                raise forms.ValidationError(u'账号密码不匹配')
            elif not self.user_cache.is_active:
                raise forms.ValidationError(u'此账号已被禁用')
        return self.cleaned_data

    def get_user(self):
        return self.user_cache

class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(label=u'原始密码',error_messages={'required':'请输入原始密码'},
        widget=forms.PasswordInput(attrs={'class':'form-control'}))
    new_password1 = forms.CharField(label=u'新密码',error_messages={'required':'请输入新密码'},
        widget=forms.PasswordInput(attrs={'class':'form-control'}))
    new_password2 = forms.CharField(label=u'重复输入',error_messages={'required':'请重复新输入密码'},
        widget=forms.PasswordInput(attrs={'class':'form-control'}))

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def clean_old_password(self):
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise forms.ValidationError(u'原密码错误')
        return old_password

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if len(password1)<6:
            raise forms.ValidationError(u'密码必须大于6位')

        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(u'两次密码输入不一致')
        return password2

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data['new_password1'])
        if commit:
            self.user.save()
        return self.user

class AddUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','password','email','nickname','sex','role','is_active')
        widgets = {
            'username' : forms.TextInput(attrs={'class':'form-control'}),
            'password' : forms.PasswordInput(attrs={'class':'form-control'}),
            'email' : forms.TextInput(attrs={'class':'form-control'}),
            'nickname' : forms.TextInput(attrs={'class':'form-control'}),
            'sex' : forms.RadioSelect(choices=((u'男', u'男'),(u'女', u'女')),attrs={'class':'list-inline'}),
            'role' : forms.Select(attrs={'class':'form-control'}),
            'is_active' : forms.Select(choices=((True, u'启用'),(False, u'禁用')),attrs={'class':'form-control'}),
        }

    #username = forms.CharField(label=u'账 号',error_messages={'required':u'账号不能为空','invalid':u'失败'},
    #    widget=forms.TextInput(attrs={'class':'form-control'}))
    #password = forms.CharField(label=u'密 码',error_messages={'required':u'密码不能为空','invalid':u'失败'},
    #    widget=forms.PasswordInput(attrs={'class':'form-control'}))
    #email = forms.EmailField(label=u'邮 箱',error_messages={'required':u'邮箱不能为空','invalid':u'请输入有效邮箱'},
    #    widget=forms.TextInput(attrs={'class':'form-control'}))
    #nickname = forms.CharField(label=u'姓 名',error_messages={'required':u'姓名不能为空','invalid':u'失败'},
    #    widget=forms.TextInput(attrs={'class':'form-control'}))
    #sex = forms.ChoiceField(label=u'性 别',error_messages={'required':u'请选择性别','invalid':u'失败'},choices=((u'男', u'男'),(u'女', u'女')),
    #    widget=forms.RadioSelect(attrs={'class':'list-inline'}))
    #role = forms.ChoiceField(label=u'角 色',choices=[(x.name,x.name) for x in RoleList.objects.all()],
    #    widget=forms.Select(attrs={'class':'form-control'}))
    #is_active = forms.ChoiceField(label=u'状 态',choices=((True, u'启用'),(False, u'禁用')),
    #    widget=forms.Select(attrs={'class':'form-control'}))

    def __init__(self,*args,**kwargs):
        super(AddUserForm,self).__init__(*args,**kwargs)
        self.fields['username'].label=u'账 号'
        self.fields['username'].error_messages={'required':u'请输入账号'}
        self.fields['password'].label=u'密 码'
        self.fields['password'].error_messages={'required':u'请输入密码'}
        self.fields['email'].label=u'邮 箱'
        self.fields['email'].error_messages={'required':u'请输入邮箱','invalid':u'请输入有效邮箱'}
        self.fields['nickname'].label=u'姓 名'
        self.fields['nickname'].error_messages={'required':u'请输入姓名'}
        self.fields['sex'].label=u'性 别'
        self.fields['sex'].error_messages={'required':u'请选择性别'}
        self.fields['role'].label=u'角 色'
        self.fields['is_active'].label=u'状 态'

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 6:
            raise forms.ValidationError(u'密码必须大于6位')
        return password

class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','email','nickname','sex','role','is_active')
        widgets = {
            'username' : forms.TextInput(attrs={'class':'form-control'}),
            #'password': forms.HiddenInput,
            'email' : forms.TextInput(attrs={'class':'form-control'}),
            'nickname' : forms.TextInput(attrs={'class':'form-control'}),
            'sex' : forms.RadioSelect(choices=((u'男', u'男'),(u'女', u'女')),attrs={'class':'list-inline'}),
            'role' : forms.Select(choices=[(x.name,x.name) for x in RoleList.objects.all()],attrs={'class':'form-control'}),
            'is_active' : forms.Select(choices=((True, u'启用'),(False, u'禁用')),attrs={'class':'form-control'}),
        }

    def __init__(self,*args,**kwargs):
        super(EditUserForm,self).__init__(*args,**kwargs)
        self.fields['username'].label=u'账 号'
        self.fields['username'].error_messages={'required':u'请输入账号'}
        self.fields['email'].label=u'邮 箱'
        self.fields['email'].error_messages={'required':u'请输入邮箱','invalid':u'请输入有效邮箱'}
        self.fields['nickname'].label=u'姓 名'
        self.fields['nickname'].error_messages={'required':u'请输入姓名'}
        self.fields['sex'].label=u'性 别'
        self.fields['sex'].error_messages={'required':u'请选择性别'}
        self.fields['role'].label=u'角 色'
        self.fields['is_active'].label=u'状 态'

    def clean_password(self):
        return self.cleaned_data['password']

class PermissionListForm(forms.ModelForm):
    class Meta:
        model = PermissionList
        widgets = {
            'name' : forms.TextInput(attrs={'class':'form-control'}),
            'url' : forms.TextInput(attrs={'class':'form-control'}),
        }

    def __init__(self,*args,**kwargs):
        super(PermissionListForm,self).__init__(*args,**kwargs)
        self.fields['name'].label=u'名 称'
        self.fields['name'].error_messages={'required':u'请输入名称'}
        self.fields['url'].label=u'URL'
        self.fields['url'].error_messages={'required':u'请输入URL'}

class RoleListForm(forms.ModelForm):
    class Meta:
        model = RoleList
        widgets = {
            'name' : forms.TextInput(attrs={'class':'form-control'}),
            'permission' : forms.SelectMultiple(attrs={'class':'form-control','size':'10','multiple':'multiple'}),
            #'permission' : forms.CheckboxSelectMultiple(choices=[(x.id,x.name) for x in PermissionList.objects.all()]),
        }

    def __init__(self,*args,**kwargs):
        super(RoleListForm,self).__init__(*args,**kwargs)
        self.fields['name'].label=u'名 称'
        self.fields['name'].error_messages={'required':u'请输入名称'}
        self.fields['permission'].label=u'URL'
        self.fields['permission'].required=False

    #permission = forms.MultipleChoiceField(label=u'权 限',required=False,choices=[(x.id,x.name) for x in PermissionList.objects.all()],
    #    widget=forms.CheckboxSelectMultiple())
