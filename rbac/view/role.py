from django.shortcuts import render,redirect,HttpResponse
from django.urls import reverse
from rbac.models import Role
from rbac.Form.Role import RoleModelForm



def role_list(request):

    roles = Role.objects.all()

    return render(request,'role_list.html',locals())


def role_add(request):
    if request.method == "GET":
        form = RoleModelForm()
        return render(request,'change.html',locals())
    form = RoleModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(reverse('role_list'))
    else:
        return render(request,'change.html',locals())


def role_edit(request,rid):
    '''
    编辑角色
    :param request:
    :param rid: 角色id
    :return:
    '''
    role_obj = Role.objects.filter(id=rid).first()
    if not role_obj:
        return HttpResponse('404')
    if request.method == "GET":
        form = RoleModelForm(instance=role_obj)
        return render(request,'change.html',locals())
    form = RoleModelForm(instance=role_obj,data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(reverse('role_list'))
    else:
        return render(request,'change.html',locals())


def role_delete(request,rid):
    '''
    删除角色
    :param request:
    :param cid: 角色id
    :return:
    '''
    origin_url = reverse('role_list')
    role_obj = Role.objects.filter(id=rid).first()
    if not role_obj:
        return HttpResponse('404')
    if request.method == "GET":
        return render(request,'delete.html',{'cancel':origin_url})

    Role.objects.filter(id=rid).delete()
    return redirect(reverse('role_list'))


