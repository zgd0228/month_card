from django.contrib import admin

from django.conf.urls import url
from rbac.view import role,user,menu

urlpatterns = [
    url(r'^role/list/$',role.role_list,name='role_list'),
    url(r'^role/add/$',role.role_add,name='role_add'),
    url(r'^role/edit/(?P<rid>\d+)/$',role.role_edit,name='role_edit'),
    url(r'^role/delete/(?P<rid>\d+)/$',role.role_delete,name='role_delete'),

    url(r'^user/list/$',user.user_list,name='user_list'),
    url(r'^user/add/$',user.user_add,name='user_add'),
    url(r'^user/edit/(?P<id>\d+)/$',user.user_edit,name='user_edit'),
    url(r'^user/delete/(?P<id>\d+)/$',user.user_delete,name='user_delete'),
    url(r'^user/reset/(?P<id>\d+)/$',user.reset_pwd,name='reset_pwd'),

    url(r'^menu/list/$',menu.menu_list,name='menu_list'),
    url(r'^menu/add/$',menu.menu_add,name='menu_add'),
    url(r'^menu/edit/(?P<id>\d+)/$',menu.menu_edit,name='menu_edit'),
    url(r'^menu/delete/(?P<id>\d+)/$',menu.menu_delete,name='menu_delete'),

    url(r'^second/menu/add/(?P<menu_id>\d+)/$',menu.second_menu_add,name='second_menu_add'),
    url(r'^second/menu/edit/(?P<id>\d+)/$',menu.second_menu_edit,name='second_menu_edit'),
    url(r'^second/menu/delete/(?P<id>\d+)/$',menu.second_menu_delete,name='second_menu_delete'),

    url(r'^permission/add/(?P<sid>\d+)/$',menu.permission_menu_add,name='permission_menu_add'),
    url(r'^permission/edit/(?P<id>\d+)/$',menu.permission_menu_edit,name='permission_menu_edit'),
    url(r'^permission/delete/(?P<id>\d+)/$',menu.permission_menu_delete,name='permission_menu_delete'),

    url(r'^multi/list/$',menu.multi,name='multi_list'),
    url(r'^multi/delete/(?P<id>\d+)/$',menu.multi_delete,name='multi_delete'),

    url(r'^desc/list/$',menu.desc_per,name='desc_list'),
]