

def init_session(request,user):
    user_dict = {}
    permission_dict = {}

    url_lists = user.roles.values('permissions__urls',
                                  'permissions__menus_id',
                                  'permissions__id',
                                  'permissions__pid_id',
                                  'permissions__pid__title',
                                  'permissions__pid__urls',
                                  'permissions__title',
                                  'permissions__name',
                                  'permissions__menus__title',
                                  'permissions__menus__icon').distinct()
    for item in url_lists:
        permission_dict[item['permissions__name']] = {'id':item['permissions__id'],
                                'title':item['permissions__title'],
                                'url':item['permissions__urls'],
                                'pid':item['permissions__pid_id'],
                                'p_title':item['permissions__pid__title'],
                                'p_url':item['permissions__pid__urls']
                                }
        menu_id = item['permissions__menus_id']
        if not menu_id:
            continue
        node = {'id':item['permissions__id'],
                'title':item['permissions__title'],
                'urls':item['permissions__urls']
                }
        if menu_id in user_dict:
            user_dict[menu_id]['children'].append(node)
        else:
            user_dict[menu_id] = {'title':item['permissions__menus__title'],
                                  'icon':item['permissions__menus__icon'],
                                  'children':[node]}
    request.session['user_dict'] = user_dict
    request.session['user_id'] = user.pk
    request.session['urls_dict'] = permission_dict
