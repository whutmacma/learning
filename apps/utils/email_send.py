# _*_ encoding:utf-8 _*_

from random import Random
from django.core.mail import send_mail


from users.models import EmailVerifyRecord
from learning.settings import EMAIL_FROM

def random_str(randomlength=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str


def send_register_email(email, send_type="register"):
    email_record = EmailVerifyRecord()
    code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    email_title = ""
    email_body = ""

    if send_type == "register":
       email_title = u"TDL在线学习网注册链接"
       email_body = u"请点击下面的链接激活你的账号：http://47.94.236.221/active/{0}".format(code)

       send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
       if send_status:
         pass
    elif send_type == "forget":
       email_title = u"TDL在线学习网密码重置链接"
       email_body = u"请点击下面的链接重置密码：http://47.94.236.221/reset/{0}".format(code)

       send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
       if send_status:
         pass


def send_pin_email(email, send_type='reset_email'):
    email_record = EmailVerifyRecord()
    code = random_str(6)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()
    if send_type == "reset_email":
       email_title = u"TDL在线学习网验证码"
       email_body = u"修改邮箱的验证码：" + code

       send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
       if send_status:
         pass








