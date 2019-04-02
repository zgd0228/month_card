from django.test import TestCase

# Create your tests here.
user_dict = {1:
                 {'title': '信息管理',
                  'icon': 'fa-connectdevelop',
                  'children':
                      {'title': '查看用户信息',
                       'urls': '/customer/list/'}},
             2:
                 {'title': '账户管理',
                  'icon': 'fa-code-fork',
                  'children':
                      {'title': '添加客户消费记录',
                       'urls': '/pay/add/'}}}

print(sorted(user_dict))


