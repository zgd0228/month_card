from django import forms
from django.core.exceptions import ValidationError
from web.models import Game

class GameAddModelForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['title','type']

    def __init__(self,*args,**kwargs):
        #统一给ModeForm生成的input添加样式
        super(GameAddModelForm,self).__init__(*args,**kwargs)
        for name,field in self.fields.items():
            field.widget.attrs['class']='form-control'



class GameModelForm(forms.ModelForm):

    class Meta:
        model = Game
        fields = ['title','type']

    def __init__(self,*args,**kwargs):
        #统一给ModeForm生成的input添加样式
        super(GameModelForm,self).__init__(*args,**kwargs)
        for name,field in self.fields.items():
            field.widget.attrs['class']='form-control'



