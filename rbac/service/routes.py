import re
from django.utils.module_loading import import_string
from django.urls import RegexURLPattern,RegexURLResolver
from django.conf import settings
from collections import OrderedDict



def check_urls(url):
    '''
    过滤url，相当于设置白名单
    :param url:
    :return:
    '''

    for item in settings.AUTO_DISCOVER_EXCLUDE:
        if re.match(item,url):
            return True


def recursion_url(pre_namespace,pre_url,urlpatterns,order_dict):
    '''

    :param pre_namespace: 命名空间
    :param per_url: url前缀
    :param urlpatterns: 路有关系列表
    :param url_ordered_dict: 递归所有的路由
    :return:
    '''
    for item in urlpatterns:
        if isinstance(item, RegexURLPattern):  # 非路由分发，讲路由添加到url_ordered_dict
            if not item.name:
                continue

            if pre_namespace:
                name = "%s:%s" % (pre_namespace, item.name)
            else:
                name = item.name
            url = pre_url + item._regex  # /rbac/user/edit/(?P<pk>\d+)/
            url = url.replace('^', '').replace('$', '')

            if check_urls(url):
                continue

            order_dict[name] = {'name': name, 'urls': url}

        elif isinstance(item, RegexURLResolver):  # 路由分发，递归操作

            if pre_namespace:
                if item.namespace:
                    namespace = "%s:%s" % (pre_namespace, item.namespace,)
                else:
                    namespace = item.namespace
            else:
                if item.namespace:
                    namespace = item.namespace
                else:

                    namespace = None
            recursion_url(namespace, pre_url + item.regex.pattern, item.url_patterns, order_dict)

def get_all_url_dict():
    '''

    :return:
    '''
    order_dict = OrderedDict()
    md = import_string(settings.ROOT_URLCONF)
    recursion_url(None,'/',md.urlpatterns,order_dict)

    return order_dict