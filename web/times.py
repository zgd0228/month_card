import calendar
import datetime


def month_day():
    '''
    获取当月的天数
    :return:
    '''
    now = datetime.datetime.today()
    days = calendar.monthrange(now.year,now.month)[1]
    end = datetime.datetime.now()+datetime.timedelta(days)

    return end



