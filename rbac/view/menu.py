from django.shortcuts import render,redirect,HttpResponse
from django.forms import formset_factory
from django.conf import settings
from django.utils.module_loading import import_string
from rbac.Form.Menu import MenuModelForm,PerModelForm,PermissionModelForm,MultiAddPermissionForm,MultiEditPermissionForm
from rbac.service.routes import *
from rbac.service.url import *
from rbac.models import Menu,Permission,Role



def menu_list(request):
    '''
    菜单列表
    :param request:
    :return:
    '''

    menus = Menu.objects.all()
    row_id = request.GET.get('mid')   # 获得一级菜单的id
    sid = request.GET.get('sid')      # 获得二级菜单的id
    menu_exist = Menu.objects.filter(id=row_id).exists()
    if not menu_exist:
        sid = None
    if row_id:
        seconds = Permission.objects.filter(menus_id=row_id)
    else:
        seconds = []

    per_exist = Permission.objects.filter(id=sid).exists()
    pid = request.GET.get('pid')
    if not per_exist:
        pid = None
    if sid:
        pers = Permission.objects.filter(pid=sid)
    else:
        pers = []

    return render(request,'menu_list.html',locals())

def menu_add(request):
    '''
    添加一级菜单
    :param request:
    :return:
    '''

    if request.method == "GET":
        form = MenuModelForm()
        return  render(request,'change.html',locals())
    form = MenuModelForm(data=request.POST)

    if form.is_valid():
        form.save()
        return redirect(memory(request,'menu_list'))
    return  render(request,'change.html',locals())

def menu_edit(request,id):
    '''
    编辑一级菜单
    :param request:
    :param id:
    :return:
    '''

    obj = Menu.objects.filter(id=id).first()
    if not obj:
        return HttpResponse('404')
    if request.method == "GET":
        form = MenuModelForm(instance=obj)
        return render(request,'change.html',locals())
    form = MenuModelForm(instance=obj,data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(memory(request,'menu_list'))
    return  render(request,'change.html',locals())

def menu_delete(request,id):
    '''
    删除一级菜单
    :param request:
    :param id:
    :return:
    '''

    url = memory(request,'menu_list')
    obj = Menu.objects.filter(id=id).first()
    if not obj:
        return HttpResponse('404')
    if request.method == "GET":
        return render(request,'delete.html',{'cancel':url})

    Menu.objects.filter(id=id).delete()
    return redirect(url)


def second_menu_add(request,menu_id):
    '''
    添加二级菜单
    :param request:
    :param menu_id:
    :return:
    '''

    menu_obj = Menu.objects.filter(id=menu_id).first()
    if request.method == "GET":
        form = PerModelForm(initial={'menus':menu_obj})
        return  render(request,'change.html',locals())
    form = PerModelForm(data=request.POST)

    if form.is_valid():
        form.save()
        return redirect(memory(request,'menu_list'))
    return  render(request,'change.html',locals())

def second_menu_edit(request,id):
    '''
    编辑二级菜单
    :param request:
    :param id:
    :return:
    '''
    obj = Permission.objects.filter(id=id).first()
    if not obj:
        return HttpResponse('404')
    if request.method == "GET":
        form = PerModelForm(instance=obj)
        return render(request,'change.html',locals())
    form = PerModelForm(instance=obj,data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(memory(request,'menu_list'))
    return render(request,'change.html',locals())


def second_menu_delete(request,id):
    '''
    删除二级菜单
    :param request:
    :param id:
    :return:
    '''

    url = memory(request,'menu_list')
    obj = Permission.objects.filter(id=id).first()
    if not obj:
        return HttpResponse('404')
    if request.method == "GET":
        return render(request,'delete.html',{'cancel':url})

    Permission.objects.filter(id=id).delete()
    return redirect(url)


def permission_menu_add(request,sid):
    '''
    添加三级菜单
    :param request:
    :param sid:
    :return:
    '''

    if request.method == "GET":
        form = PermissionModelForm()
        return  render(request,'change.html',locals())
    form = PermissionModelForm(data=request.POST)
    if form.is_valid():
        per_obj = Permission.objects.filter(id=sid).first()
        if not per_obj:
            return HttpResponse('404')
        form.instance.pid = per_obj
        form.save()
        return redirect(memory(request,'menu_list'))
    return  render(request,'change.html',locals())


def permission_menu_edit(request,id):
    '''
    编辑三级菜单
    :param request:
    :param id:
    :return:
    '''

    obj = Permission.objects.filter(id=id).first()
    if not obj:
        return HttpResponse('404')
    if request.method == "GET":
        form = PermissionModelForm(instance=obj)
        return render(request,'change.html',locals())
    form = PermissionModelForm(instance=obj,data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(memory(request,'menu_list'))
    return render(request,'change.html',locals())

def permission_menu_delete(request,id):
    '''
    删除三级菜单
    :param request:
    :param id:
    :return:
    '''

    url = memory(request,'menu_list')
    obj = Permission.objects.filter(id=id).first()
    if not obj:
        return HttpResponse('404')
    if request.method == "GET":
        return render(request,'delete.html',{'cancel':url})

    Permission.objects.filter(id=id).delete()
    return redirect(url)


def multi(request):
    '''
    权限的批量处理
    :param request:
    :return:
    '''

    # 更新权限，数据库与url中都有
    update_formset_class = formset_factory(MultiEditPermissionForm,extra=0)
    formset_class = formset_factory(MultiAddPermissionForm,extra=0)

    # 获取提交type
    post_type = request.GET.get('type')

    add_formset = None
    update_formset = None
    # 添加数据
    if request.method == "POST" and post_type == "add":
        formset=formset_class(data=request.POST)
        if formset.is_valid():
            obj_list = []
            has_error = False
            post_row_list = formset.cleaned_data
            for i in range(0,formset.total_form_count()):
                row_dict = post_row_list[i]
                try:
                    obj = Permission(**row_dict)
                    obj.validate_unique()
                    obj_list.append(obj)
                except Exception as e:
                    formset.errors[i].update(e)
                    add_formset = formset
                    has_error = True
            if not has_error:
                Permission.objects.bulk_create(obj_list,batch_size=100)
        else:
            add_formset = formset

    # 获取项目中所有的URL
    all_urls_dict = get_all_url_dict()
    all_urls_set = set(all_urls_dict.keys())
    # 获取数据库中所有的URL
    permission_urls = Permission.objects.all().values('id','title','urls','name','menus_id','pid_id')
    permission_dict = OrderedDict()
    permission_set = set()
    for item in permission_urls:
        permission_dict[item['name']] = item
        permission_set.add(item['name'])

    if not add_formset:
        # 添加权限 url中有，数据库中没有
        add_name_list = all_urls_set - permission_set
        add_formset = formset_class(initial = [row_dicts for names,row_dicts in all_urls_dict.items()
                                           if names in add_name_list])
    # 批量更新
    if request.method == "POST" and post_type == "update":
        formset=update_formset_class(data=request.POST)
        if formset.is_valid():
            post_row_list = formset.cleaned_data

            for i in range(0,formset.total_form_count()):
                row_dict = post_row_list[i]
                permission_id = row_dict.pop('id')
                try:
                    obj = Permission.objects.filter(id=permission_id).first()
                    for key,values in row_dict.items():
                        setattr(obj,key,values)
                    obj.validate_unique()
                    obj.save()
                except Exception as e:
                    formset.errors[i].update(e)
                    update_formset = formset

    # 删除权限  URL中没有，数据库中有
    delete_name_list = permission_set - all_urls_set
    delete_row_list = [row_dict for name,row_dict in permission_dict.items()
                       if name in delete_name_list]

    for name,value in permission_dict.items():
        route_dict = all_urls_dict.get(name)
        if not route_dict:
            continue
        if value['urls'] != route_dict['urls']:
            value['urls'] = '路由和数据库中不一致'

    if not update_formset:
        update_name_list = permission_set & all_urls_set
        update_formset = update_formset_class(initial=[row_dict for name,row_dict in permission_dict.items()
                                                if name in update_name_list])

    return render(request, 'multi_list.html', locals())

def multi_delete(request,id):
    '''
    删除批量处理页面中的菜单
    :param request:
    :param id:
    :return:
    '''

    url = memory(request,'multi_list')
    obj = Permission.objects.filter(id=id).first()
    if not obj:
        return HttpResponse('404')
    if request.method == "GET":
        return render(request,'delete.html',{'cancel':url})

    Permission.objects.filter(id=id).delete()
    return redirect(url)

def desc_per(request):
    '''
    给用户分配权限
    :param request:
    :return:
    '''
    user_id = request.GET.get('uid')
    role_id = request.GET.get('rid')

    if not user_id:
        user_id = None

    UserInfo = import_string(settings.RBAC_USER_MODEL)

    user_obj = UserInfo.objects.filter(id=user_id).first()
    role_obj = Role.objects.filter(id=role_id).first()

    roles_obj = Role.objects.all()

    if request.method == "POST" and request.POST.get('type') == 'role':
        role_list = request.POST.getlist('role')
        if not user_obj:
            return HttpResponse('请先选择用户')
        user_obj.roles.set(role_list)

    if request.method == "POST" and request.POST.get('type') == 'permission':
        permission_list = request.POST.getlist('permission')
        if not role_obj:
            return HttpResponse('请先选择角色')
        role_obj.permissions.set(permission_list)

    if user_id:
        roles = user_obj.roles.all()
    else:
        roles = []
    has_role = {item.id:None for item in roles}
    # 获取用户权限
    if user_id:
        per = user_obj.roles.filter(permissions__id__isnull=False).values('id','permissions').distinct()
    else:
        per = []
    has_per = {item['permissions']:None for item in per}

    if not role_obj:
        role_id = None
    if role_obj:
        per = role_obj.permissions.all()
        has_per = {item.id:None for item in per}
    elif user_obj:
        per = user_obj.roles.filter(permissions__id__isnull=False).values('id','permissions').distinct()
        has_per = {item['permissions']:None for item in per}
    else:
        has_per = {}


    users = UserInfo.objects.all()
    roles = Role.objects.all()
    menus = Menu.objects.all()
    menus_list = set_menu_dict()


    return render(request,'desc_list.html',locals())

def set_menu_dict():
    '''
    对权限及菜单进行处理，组合成一个字典
    :return: dict
    '''

    menus_list = Menu.objects.values('id','title')
    all_menu_dict = {}
    for item in menus_list:
        item['children'] = []

        all_menu_dict[item['id']] = item

    second_menu_list = Permission.objects.filter(menus__isnull=False).values('id','title','menus_id')
    second_menu_dict = {}

    for item in second_menu_list:
        item['children'] = []
        second_menu_dict[item['id']] = item
        menu_id = item['menus_id']
        all_menu_dict[menu_id]['children'].append(item)

    all_permission_list = Permission.objects.filter(menus__isnull=True).values('id','title','pid_id')

    for item in all_permission_list:

        if not item['pid_id']:
            continue
        second_menu_dict[item['pid_id']]['children'].append(item)

    return menus_list




