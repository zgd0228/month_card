from django.db import models
from web import times


# Create your models here.


class CardInfo(models.Model):

    number = models.CharField(verbose_name='客户卡号',max_length=11,unique=True)
    pwd = models.CharField(verbose_name='客户密码',max_length=32)
    start_time = models.DateField(verbose_name='开卡日期',auto_now_add=True)
    end_time = models.DateField(verbose_name='截止日期',default=times.month_day())

    pay = models.IntegerField(verbose_name='充值')

    def __str__(self):
        return self.number


class Game(models.Model):

    title = models.CharField(verbose_name='游戏名称',max_length=32,unique=True)
    type = models.CharField(verbose_name='游戏消费类型',max_length=32)

    def __str__(self):
        return self.title


class Payment(models.Model):

    time = models.CharField(verbose_name='消费时长',max_length=32)
    pay_time = models.DateTimeField(verbose_name='消费时间',auto_now_add=True,)
    games = models.ForeignKey(to='Game',verbose_name='消费游戏名称')
    user = models.ForeignKey(to='CardInfo',verbose_name='消费用户')

    def __str__(self):
        return self.games

class Time(models.Model):

    title = models.CharField(max_length=32,verbose_name='游戏简称')
    tm = models.IntegerField()
    game = models.ForeignKey(to='Game')
    user = models.ForeignKey(to='CardInfo')

    def __str__(self):
        return self.title

