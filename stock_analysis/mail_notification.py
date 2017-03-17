# -*- coding: UTF-8 -*-
import smtplib
from email.mime.text import MIMEText

_user = "13718715237@139.com"
_pwd = "wxj555@@"
_to = "1609799372@qq.com"

def send_mail(text):
    msg = MIMEText(text,'html','utf-8')
    msg["Subject"] = "数据监控"
    msg["From"] = _user
    msg["To"] = _to

    s = smtplib.SMTP_SSL("smtp.139.com", 465)
    s.login(_user, _pwd)
    s.sendmail(_user, _to, msg.as_string())
    s.quit()
    print("Success!")

if __name__ == "__main__":
  send_mail("""
<p>Python 邮件发送测试...</p>
<p><a href="http://www.runoob.com">这是一个链接</a></p>
""");
