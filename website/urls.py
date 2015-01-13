from django.conf.urls import patterns, include, url

from django.conf import settings
from website.views import Home,About,Test

#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'website.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^admin/', include(admin.site.urls)),
    url(r'^$',Home),
    url(r'^about/$',About),
    url(r'^test/$',Test),


    #static
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', { 'document_root': settings.STATIC_ROOT,}),
)

urlpatterns += patterns('UserManage.views',
    url(r'^accounts/login/$', 'user.LoginUser'),
    url(r'^accounts/logout/$', 'user.LogoutUser'),

    url(r'^accounts/user/add/$', 'user.AddUser'),
    url(r'^accounts/user/list/$', 'user.ListUser'),
    url(r'^accounts/user/edit/(?P<ID>\d+)/$', 'user.EditUser'),
    url(r'^accounts/user/delete/(?P<ID>\d+)/$', 'user.DeleteUser'),

    url(r'^accounts/user/changepwd/$', 'user.ChangePassword'),
    url(r'^accounts/user/resetpwd/(?P<ID>\d+)/$', 'user.ResetPassword'),

    url(r'^accounts/role/add/$', 'role.AddRole'),
    url(r'^accounts/role/list/$', 'role.ListRole'),
    url(r'^accounts/role/edit/(?P<ID>\d+)/$', 'role.EditRole'),
    url(r'^accounts/role/delete/(?P<ID>\d+)/$', 'role.DeleteRole'),

    url(r'^accounts/permission/deny/$', 'permission.NoPermission'),

    url(r'^accounts/permission/add/$', 'permission.AddPermission'),
    url(r'^accounts/permission/list/$', 'permission.ListPermission'),
    url(r'^accounts/permission/edit/(?P<ID>\d+)/$', 'permission.EditPermission'),
    url(r'^accounts/permission/delete/(?P<ID>\d+)/$', 'permission.DeletePermission'),

)
