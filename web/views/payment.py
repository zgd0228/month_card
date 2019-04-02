import datetime,time
from django.shortcuts import render,redirect
from django.http import JsonResponse
from web.models import Payment,Game,CardInfo,Time
from web.form import payment
from web import times

def payment_list(request,id):
    '''
    用户消费明细
    [game:[user_id,pay_time,game,time]]
    :param request:
    :return:
    '''

    payment_obj = Payment.objects.filter(user_id=id)


    return render(request,'payment_list.html',locals())

def count_days(request):
    '''
    统计收入
    :param request:
    :return:
    '''
    customers = CardInfo.objects.all()
    date_now = str(datetime.datetime.now().strftime('%Y-%m-%d'))
    month = str(datetime.datetime.now().strftime('%Y-%m'))
    start_time = customers.values('start_time')
    count_day = 0
    count_month = 0
    for item in start_time:
        start_date = str(item['start_time'])
        start_month = str(time.strftime('%Y-%m',item['start_time'].timetuple()))
        if date_now == start_date:
            count_day += customers.filter(start_time=item['start_time']).first().pay
        if start_month == month:
            count_month += customers.filter(start_time=item['start_time']).first().pay
    return render(request,'count.html',locals())

def payment_add(request,id):
    '''
    用户充值
    :param request:
    :return:
    '''
    response = {'user':None,'msg':None}
    date_now = datetime.datetime.now().strftime('%Y-%m-%d')
    customer = CardInfo.objects.filter(id=id).first()
    if request.is_ajax():
        pay = request.POST.get('pay')
        if int(pay) == 60:
            response['user'] = id
            end_time = times.month_day()
            CardInfo.objects.filter(id=id).update(pay=int(pay),start_time = date_now,end_time = end_time)
            Time.objects.filter(user_id=id,title='dk').update(tm=10)
            Time.objects.filter(user_id=id,title='zm').update(tm=10)
            Time.objects.filter(user_id=id,title='htc').update(tm=30)
        else:
            response['msg'] = '您的充值金额不正确，请重新输入'
        return JsonResponse(response)
    return render(request,'payment_add.html',locals())


