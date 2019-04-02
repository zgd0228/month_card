from django.shortcuts import redirect,render,HttpResponse
from web.form import game
from web.models import Game
from rbac.service.url import memory


def game_list(request):
    '''

    :param request:
    :return:
    '''
    games = Game.objects.all()
    return render(request,'game_list.html',locals())

def game_add(request):
    '''

    :param request:
    :return:
    '''
    if request.method == "GET":
        form = game.GameAddModelForm()
        return render(request,'change.html',locals())
    form = game.GameAddModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(memory(request,'game_list'))
    return render(request,'change.html',locals())