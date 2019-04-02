import re

from django.shortcuts import render,HttpResponse,redirect
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
class ValidPermission(MiddlewareMixin):

    def process_request(self,request):

        current_path = request.path_info

        # 白名单验证
        valid_list = settings.VALID_URL_LIST
        for url in valid_list:
            if re.match(url,current_path):
                return None

        # 用户登录验证
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('/login/')
        bar_list = [
            {'title':'首页','url':'#'}
        ]

        # 不用权限验证白名单index,logout
        no_permission_list = settings.NO_PERMISSION_LIST
        for url in no_permission_list:
            if re.match(url,current_path):
                request.bar_list = bar_list
                request.menu_id = 0
                return None
        # 权限验证
        flag = False

        url_dict = request.session.get('urls_dict')
        for item in url_dict.values():
            url = '^%s$'%item['url']
            if re.match(url,current_path):
                flag = True
                request.menu_id = item['pid'] or item['id']

                if not item['pid']:
                    bar_list.extend([{'title':item['title'],'url':item['url'],'class':'active'}])
                else:
                    bar_list.extend([{'title':item['p_title'],'url':item['p_url']},
                                    {'title':item['title'],'url':item['url'],'class':'active'}])
                request.bar_list = bar_list
                break
        if not flag:
            return render(request,'404.html')
