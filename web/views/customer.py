import datetime,time
from django.shortcuts import redirect,render,HttpResponse
from django.urls import reverse
from django.http import JsonResponse
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.forms import formset_factory
from django.conf import settings

from web.models import CardInfo,Payment,Game,Time
from web.form import customer,payment
from rbac.service.url import memory

def customer_list(request):
    '''
    用户列表
    :param request:
    :return:
    '''
    response = {'user':None,'msg':None}

    customers = CardInfo.objects.all()
    paginator = Paginator(customers,10)
    page_count = paginator.count   # 客户的总数
    current_page = int(request.GET.get('page',1)) # 当前页数，如果为空则默认第一页
    per_page = paginator.num_pages  # 总页数
    if per_page >9:
        if current_page-4 < 1:
            page_range = range(1,9)
        elif current_page+4 > per_page:
            page_range = range(per_page-7,per_page+1)
        else:
            page_range = range(current_page-4,current_page+4)
    else:
        page_range = paginator.page_range
    try:
        customer_list = paginator.page(current_page)
    except EmptyPage as e:
        current_page = 1

    if request.is_ajax():
        card = request.POST.get('card')
        customers = CardInfo.objects.filter(number=card).first()
        if not customers:
            response['msg']='该用户不存在请重新输入'
        response['user']=customers.pk
        return JsonResponse(response)
    return render(request,'customer_list.html',locals())

def customer_add(request):
    '''
    添加用户
    :param request:
    :return:
    '''
    if request.method == "GET":
        form = customer.CardAddModelForm()
        return render(request,'change.html',locals())
    form = customer.CardAddModelForm(data=request.POST)
    number = request.POST.get('number')
    if form.is_valid():
        form.save()
        uid = CardInfo.objects.filter(number=number).first().pk
        time_set(request,uid)
        return redirect(memory(request,'customer_list'))

    return render(request,'change.html',locals())

def customer_delete(request,uid):
    '''
    删除用户
    :param request:
    :param uid:
    :return:
    '''

    origin_url = reverse('customer_list')

    customer_obj = CardInfo.objects.filter(id=uid).first()
    if not customer_obj:
        return render(request,'404.html')
    if request.method == "GET":
        return render(request,'delete.html',{'cancel':origin_url})

    CardInfo.objects.filter(id=uid).delete()
    return redirect(memory(request,'customer_list'))

def reset_pwd(request,uid):
    '''
    重置密码
    :param request:
    :param uid:
    :return:
    '''
    customer_obj = CardInfo.objects.filter(id=uid).first()
    if not customer_obj:
        return render(request,'404.html')
    if request.method == "GET":
        form = customer.ResetPwdCardModelForm()
        return render(request,'change.html',locals())
    form = customer.ResetPwdCardModelForm(instance=customer_obj, data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(memory(request,'customer_list'))
    return render(request,'change.html',locals())

def information(request,uid):
    '''
    用户信息以及消费信息
    :param request:
    :return:
    '''
    response = {'mes':None}
    customers = CardInfo.objects.filter(id=uid).first()
    # 将当前日期与截止日期转换成时间戳进行比较
    end_date = time.mktime(customers.end_time.timetuple())
    date_now = datetime.datetime.now().strftime('%Y-%m-%d')
    date = time.mktime(time.strptime(date_now,'%Y-%m-%d'))
    state = None
    if date>end_date:
        state = 1
        CardInfo.objects.filter(id=uid).update(pay=0) # 如果用户过期，则对余额进行清零
        Time.objects.filter(user_id=uid).update(tm=0) # 如果用户过期，则对游戏进行清零，使其游戏时长为0
        Payment.objects.filter(user_id=uid).delete()  # 如果用户过期，则对消费详情进行清空

    dk = customers.time_set.filter(title='dk').first().tm
    htc = customers.time_set.filter(title='htc').first().tm
    zm = customers.time_set.filter(title='zm').first().tm

    game_dict = {}
    obj_list = []
    if request.is_ajax():
        game_dict['zm'] = request.POST.get('zm')
        game_dict['htc'] = request.POST.get('htc')
        game_dict['dk'] = request.POST.get('dk')
        for game in game_dict:
            tms = Time.objects.filter(title=game,user_id=uid).first()

            input_game = game_dict.get(game)
            if input_game == '':  # 如果输入为空，则跳出本次循环进行下一次循环
                continue
            if tms.tm<1 and int(input_game)>0:
                response['mes'] = '%s游戏已达到上限，请选择其他的游戏'%(
                    Time.objects.filter(title=game).first().game.title)
                return JsonResponse(response)
            if int(input_game) > tms.tm:
                response['mes'] = '%s游戏额度不足，请重新选择游戏的次数或时长'%(
                    Time.objects.filter(title=game).first().game.title)
                return JsonResponse(response)
            payment_obj = Payment(user_id=uid,games_id=Time.objects.filter(title=game).first().game.pk,time=input_game)
            obj_list.append(payment_obj)
            Time.objects.filter(title=game,user_id=uid).update(tm=tms.tm - int(input_game))
        Payment.objects.bulk_create(obj_list,batch_size=100)
    return render(request,'info.html',locals())

def time_set(request,uid):
    '''
    用于解决游戏、用户与游戏时长次数的绑定
    :param request:
    :param uid: 用户id
    :return:
    '''
    game_list = []
    games = Game.objects.all()
    for game in games:
        id = game.pk
        if id == 4:
            tm = '10'
            times = Time(title='dk',user_id=uid,tm=tm,game_id=id)
        elif id == 5:
            tm = '10'
            times = Time(tm=tm,user_id=uid,game_id = id,title = 'zm')
        else:
            tm = '30'
            times = Time(tm=tm,user_id=uid,game_id = id,title = 'htc')
        game_list.append(times)

    Time.objects.bulk_create(game_list,batch_size=100)
