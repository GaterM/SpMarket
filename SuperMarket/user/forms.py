from django import forms

# 验证登录
from user.models import Res_login


class Reg_logModelForm(forms.ModelForm):
    class Meta:
        model = Res_login
        fields = ['tel', 'password']

        # def error_messages = {
        #     'tel': {'required':''}
        # }

    def clean_tel(self):
        tel = self.cleaned_data.get('tel')
        tel2 = Res_login.objects.filter(tel=tel)
        if not tel2:
            raise forms.ValidationError('手机号码不存在')
        else:
            return tel
