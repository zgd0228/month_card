from django import forms
from django.core.exceptions import ValidationError
from web.models import CardInfo

class CardAddModelForm(forms.ModelForm):
    confirm_pwd = forms.CharField(label='确认密码')
    class Meta:
        model = CardInfo
        fields = ['number','pay','pwd','confirm_pwd']

    def __init__(self,*args,**kwargs):
        #统一给ModeForm生成的input添加样式
        super(CardAddModelForm,self).__init__(*args,**kwargs)
        for name,field in self.fields.items():
            field.widget.attrs['class']='form-control'

    def clean_confirm_pwd(self):
        user = self.cleaned_data['number']
        if len(user) != 11:
            raise ValidationError('电话格式不正确')
        pwd = self.cleaned_data['pwd']
        confirm_pwd = self.cleaned_data['confirm_pwd']
        if pwd != confirm_pwd:
            raise ValidationError('两次输入的密码不一致')
        return confirm_pwd




class CardModelForm(forms.ModelForm):

    class Meta:
        model = CardInfo
        fields = ['number','pwd','pay']

    def __init__(self,*args,**kwargs):
        #统一给ModeForm生成的input添加样式
        super(CardModelForm,self).__init__(*args,**kwargs)
        for name,field in self.fields.items():
            field.widget.attrs['class']='form-control'

    def clean_confirm_pwd(self):
        user = self.cleaned_data['number']
        if len(user) != 11:
            raise ValidationError('电话格式不正确')
        pwd = self.cleaned_data['pwd']
        confirm_pwd = self.cleaned_data['confirm_pwd']
        if pwd != confirm_pwd:
            raise ValidationError('两次输入的密码不一致')
        return confirm_pwd


class ResetPwdCardModelForm(forms.ModelForm):
    confirm_pwd = forms.CharField(label='确认密码')
    class Meta:
        model = CardInfo
        fields = ['pwd','confirm_pwd']

    def __init__(self,*args,**kwargs):
        #统一给ModeForm生成的input添加样式
        super(ResetPwdCardModelForm,self).__init__(*args,**kwargs)
        for name,field in self.fields.items():
            field.widget.attrs['class']='form-control'

    def clean_confirm_pwd(self):
        pwd = self.cleaned_data['pwd']
        confirm_pwd = self.cleaned_data['confirm_pwd']
        if pwd != confirm_pwd:
            raise ValidationError('两次输入的密码不一致')
        return confirm_pwd


