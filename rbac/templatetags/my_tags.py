import re
from django.template import Library
from django.urls import reverse
from django.http import QueryDict
from collections import OrderedDict
register = Library()

@register.inclusion_tag('menu.html')
def menu(request):

    user_dict = request.session.get('user_dict')
    key_list = sorted(user_dict)

    order_dict = OrderedDict()
    for key in key_list:
        val = user_dict[key]
        val['class'] = 'hide'
        for item in val['children']:
            if item['id'] == request.menu_id:
                item['class'] = 'active'
                val['class'] = ''
        order_dict[key] = val
    return {'user_dict':order_dict}

@register.inclusion_tag('bar.html')
def bar(request):

    return {'bar_list':request.bar_list}

@register.filter
def has_permission(request,name):
    '''
    filter只能有两个参数，可以直接使用if语句判断
    :param request:
    :param name:
    :return:
    '''

    if name in request.session['urls_dict']:
        return True

@register.simple_tag
def memory_url(request,name,*args,**kwargs):
    '''
    获取菜单列表中选定的url后缀参数,
    :param request:
    :param name:
    :return:
    '''

    base_url = reverse(name,args=args,kwargs=kwargs)

    if not request.GET:
        return base_url
    query_dict = QueryDict(mutable=True)
    query_dict['filter'] = request.GET.urlencode() # mid=2&age=99

    return '%s?%s'%(base_url,query_dict.urlencode())



