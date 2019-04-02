from django import forms
from django.core.exceptions import ValidationError
from rbac.models import UserInfo


class UserModelForm(forms.ModelForm):
    confirm_pwd = forms.CharField(label='确认密码')
    class Meta:
        model = UserInfo
        fields = ['name','pwd','confirm_pwd']

    def __init__(self,*args,**kwargs):
        #统一给ModeForm生成的input添加样式
        super(UserModelForm,self).__init__(*args,**kwargs)
        for name,field in self.fields.items():
            field.widget.attrs['class']='form-control'

    def clean_confirm_pwd(self):
        pwd = self.cleaned_data['pwd']
        confirm_pwd = self.cleaned_data['confirm_pwd']
        if pwd != confirm_pwd:
            raise ValidationError('两次输入的密码不一致')
        return confirm_pwd

class UpdateUserModelForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ['name']

    def __init__(self,*args,**kwargs):
        #统一给ModeForm生成的input添加样式
        super(UpdateUserModelForm,self).__init__(*args,**kwargs)
        for name,field in self.fields.items():
            field.widget.attrs['class']='form-control'


class ResetPwdUserModelForm(forms.ModelForm):
    confirm_pwd = forms.CharField(label='确认密码')
    class Meta:
        model = UserInfo
        fields = ['pwd','confirm_pwd']

    def __init__(self,*args,**kwargs):
        #统一给ModeForm生成的input添加样式
        super(ResetPwdUserModelForm,self).__init__(*args,**kwargs)
        for name,field in self.fields.items():
            field.widget.attrs['class']='form-control'

    def clean_confirm_pwd(self):
        pwd = self.cleaned_data['pwd']
        confirm_pwd = self.cleaned_data['confirm_pwd']
        if pwd != confirm_pwd:
            raise ValidationError('两次输入的密码不一致')
        return confirm_pwd


