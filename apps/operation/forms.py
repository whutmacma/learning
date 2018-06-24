# _*_ coding: utf-8 _*_
import re


from django import forms


from operation.models import UserAsk


class UserAskForm(forms.ModelForm):
    class Meta:
        model = UserAsk
        fields = ['name', 'mobile', 'course_name']

    def clean_name(self):
        name = self.cleaned_data['name']
        REGEX_NAME = "^[a-zA-Z0-9_-]{4,16}$"
        p = re.compile(REGEX_NAME)
        if p.match(name):
            return name
        else:
            raise forms.ValidationError(u"用户名格式错误")


    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
        p = re.compile(REGEX_MOBILE)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError(u"手机号码非法",code = "mobile_invalide")


