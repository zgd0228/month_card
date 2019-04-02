from django.conf.urls import url
from web.views import customer,account,game,payment


urlpatterns = [
    url(r'^login/$',account.login,name='login'),
    url(r'^logout/$',account.logout,name='logout'),
    url(r'^index/$',account.index,name='index' ),

    url(r'^customer/list/$', customer.customer_list, name='customer_list'),
    url(r'^customer/add/$', customer.customer_add, name='customer_add'),
    url(r'^customer/delete/(?P<uid>\d+)/$', customer.customer_delete, name='customer_delete'),
    url(r'^customer/reset/(?P<uid>\d+)/$', customer.reset_pwd, name='customer_pwd'),

    url(r'^customer/info/(?P<uid>\d+)$', customer.information, name='customer_info'),

    url(r'^game/list/$', game.game_list, name='game_list'),
    url(r'^game/add/$', game.game_add, name='game_add'),
    url(r'^payment/list/(?P<id>\d+)/$', payment.payment_list, name='payment_list'),
    url(r'^payment/add/(?P<id>\d+)/$', payment.payment_add, name='payment_add'),
    url(r'^income/count/$',payment.count_days,name='income_count')


]