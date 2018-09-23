from django import forms
from django.core import validators

from user.help import set_password
from user.models import Reg_login


# 验证登录
class LoginModelForm(forms.ModelForm):
    class Meta:
        model = Reg_login
        fields = ['tel', 'password']

        widgets = {
            'tel': forms.TextInput(attrs={"class": "login-name", "placeholder": "请输入手机号"}),
            "password": forms.PasswordInput(attrs={"class": "login-password", "placeholder": "请输入密码"})
        }

        error_messages = {
            'tel': {'required': '请填写手机号码'},
            'password': {'required': '请填写密码'}
        }

    def clean(self):
        # 验证手机号码与密码
        cleaned_data = super().clean()
        tel = self.cleaned_data.get('tel')
        password = self.cleaned_data.get('password')
        # 验证手机号码是否存在
        user = Reg_login.objects.filter(tel=tel).first()
        if user is None:
            raise forms.ValidationError('该手机号码没有注册')
        else:
            # 手机号码存在,验证密码
            pwd_in_db = user.password
            password = set_password(password)
            if pwd_in_db != password:
                raise forms.ValidationError('密码错误!')
            else:
                # 保存用户的信息对象到 cleaned_data 中
                cleaned_data['user'] = user
            return cleaned_data


# 验证注册
class RegisterModelForm(forms.ModelForm):
    repassword = forms.CharField(max_length=16, min_length=6, error_messages={'required': '请确认密码'},
                                 widget=forms.PasswordInput(attrs={"class": "login-password",
                                                                   "placeholder": "请输入确认密码"})
                                 )

    class Meta:
        model = Reg_login
        fields = ['tel', 'password']

        widgets = {
            "tel": forms.TextInput(attrs={"class": "login-name", "placeholder": "请输入手机号码"}),
            "password": forms.PasswordInput(attrs={"class": "login-password", "placeholder": "请输入密码"}),
        }

    # 自定义错误信息
    error_messages = {
        "tel": {
            "required": "请填写手机号!"
        },
        "password": {
            "required": "请填写密码!",
            "min_length": "密码必须大于6个字符!",
            "max_length": "密码必须小于16个字符!",
        }
    }

    def __init__(self, *args, **kwargs):
        # 调用父类方法
        super().__init__(*args, **kwargs)
        # 自定义的验证 密码长度的验证 6-16 位
        self.fields['password'].validators.append(validators.MinLengthValidator(6))
        self.fields['password'].validators.append(validators.MaxLengthValidator(16))

    # 自定义验证手机号码,单个
    def clean_tel(self):
        # 验证手机号码是否被注册
        tel = self.cleaned_data.get('tel')
        # 获取数据库查询
        rs = Reg_login.objects.filter(tel=tel).exists()
        if rs:
            raise forms.ValidationError('该手机号码已经注册')
        return tel

    # 综合验证
    def clean(self):
        cleaned_data = super().clean()
        pwd1 = cleaned_data.get('password')
        pwd2 = cleaned_data.get('repassword')

        # 比较两次密码是否一致
        if pwd1 and pwd2 and pwd1 != pwd2:
            raise forms.ValidationError('两次密码不一致,请重新输入')
        else:
            if pwd1:
                cleaned_data['password'] = set_password(pwd1)
        return cleaned_data


# 个人资料验证
class InfoModelForm(forms.ModelForm):
    class Meta:
        model = Reg_login
        fields = ['nickname', 'tel', 'sex', 'school', 'hometown', 'born', 'address']

        # widgets = {
        #     'nickname': forms.TextInput(attrs={'class': 'infor-tele', 'placeholder': '默契'}),
        #     'tel': forms.TextInput(attrs={'class': 'infor-tele', 'placeholder': '13012345678'}),
        #     # 'sex': forms.TextInput(attrs={'class': 'infor-tele'}),
        #     'school': forms.TextInput(attrs={'class': 'infor-tele', 'placeholder': '就读于哪个学校'}),
        #     'hometown': forms.TextInput(attrs={'class': 'infor-tele', 'placeholder': '来自哪里'}),
        #     'born': forms.DateInput(attrs={'class': 'infor-tele', 'placeholder': '出生日期'}),
        #     'address': forms.TextInput(attrs={'class': 'infor-tele', 'placeholder': '详细地址'}),
        # }
