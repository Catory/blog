
import smtplib
from email.mime.text import MIMEText
from threading import Thread
from Blog.settings import EMAIL_FROM,EMAIL_HOST,EMAIL_HOST_USER,EMAIL_HOST_PASSWORD

def async_send_mail(msg,mailServer,recipitents):
    mailServer.sendmail(EMAIL_FROM, recipitents, msg.as_string())
    mailServer.quit()

def send_mail(recipitents,message,**kwargs):

    msg = MIMEText(message,'html')
    msg['Subject'] = 'v2ex用户注册激活确认'
    msg['From'] = EMAIL_FROM
    mailServer = smtplib.SMTP(EMAIL_HOST, 25)
    mailServer.login(EMAIL_HOST_USER,EMAIL_HOST_PASSWORD)

    thr = Thread(target=async_send_mail,args=[msg,mailServer,recipitents])
    thr.start()
    return thr