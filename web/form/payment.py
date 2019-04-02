from django import forms
from web.models import Payment

class PayModelForm(forms.ModelForm):
    time = forms.CharField(max_length=32,label='消费时长/次数')
    class Meta:
        model = Payment
        fields = ['games']

    def __init__(self,*args,**kwargs):
        #统一给ModeForm生成的input添加样式
        super(PayModelForm,self).__init__(*args,**kwargs)
        for name,field in self.fields.items():
            field.widget.attrs['class']='form-control'