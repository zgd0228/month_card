from django.shortcuts import render,redirect,HttpResponse
from django.urls import reverse
from rbac.models import UserInfo
from rbac.Form.User import UserModelForm,ResetPwdUserModelForm,UpdateUserModelForm



def user_list(request):

    users = UserInfo.objects.all()

    return render(request,'user_list.html',locals())


def user_add(request):
    if request.method == "GET":
        form = UserModelForm()
        return render(request,'change.html',locals())
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(reverse('user_list'))
    else:
        return render(request,'change.html',locals())


def user_edit(request,id):
    '''
    编辑角色
    :param request:
    :param id: 角色id
    :return:
    '''
    user_obj = UserInfo.objects.filter(id=id).first()
    if not user_obj:
        return HttpResponse('404')
    if request.method == "GET":
        form = UpdateUserModelForm(instance=user_obj)
        return render(request,'change.html',locals())
    form = UpdateUserModelForm(instance=user_obj,data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(reverse('user_list'))

    return render(request,'change.html',locals())


def user_delete(request,id):
    '''
    删除角色
    :param request:
    :param id: 用户id
    :return:
    '''
    origin_url = reverse('user_list')
    user_obj = UserInfo.objects.filter(id=id).first()
    if not user_obj:
        return HttpResponse('404')
    if request.method == "GET":
        return render(request,'delete.html',{'cancel':origin_url})

    UserInfo.objects.filter(id=id).delete()
    return redirect(reverse('user_list'))


def reset_pwd(request,id):

    user_obj = UserInfo.objects.filter(id=id).first()
    if not user_obj:
        return HttpResponse('404')

    if request.method == "GET":
        form = ResetPwdUserModelForm()
        return render(request,'change.html',locals())
    form = ResetPwdUserModelForm(instance=user_obj,data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(reverse('user_list'))

    return render(request,'change.html',locals())

