# -*- coding: utf-8 -*-

"""
Author:by wlq on 2023/4/17 20:26
FileName:EmailUtil.py in CV_study
Tools:PyCharm python3.8.4
"""
import smtplib
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from tool import config


class EmailUtil:
    """"""
    stp = None

    def __init__(self):
        self.host = config.email_config['host']
        self.license = config.email_config['license']
        self.port = config.email_config['port']

    def open(self):
        self.stp = smtplib.SMTP()
        self.stp.connect(
            host=self.host,
            port=self.port
        )

    def close(self):
        # 关闭SMTP对象
        self.stp.quit()

    def sendOne(self, receiver, content, sender='linqingwang2001@163.com'):
        """单独发送邮件"""
        try:
            self.open()
            self.stp.login(sender, self.license)
            mm = MIMEMultipart('related')
            mm["From"] = f"签到系统<{sender}>"
            # mm["From"] = f"签到系统<{sender}>"
            print(f"签到系统<{sender}>")
            # 设置接受者,注意严格遵守格式,里面邮箱为接受者邮箱
            mm["To"] = f"<{receiver}>"
            # 设置邮件主题
            mm["Subject"] = Header(content['subject'], 'utf-8')
            # 构造文本,参数1：正文内容，参数2：文本格式，参数3：编码方式
            message_text = MIMEText(content['body'], "plain", "utf-8")
            # 向MIMEMultipart对象中添加文本对象
            mm.attach(message_text)
            # 发送邮件，传递参数1：发件人邮箱地址，参数2：收件人邮箱地址，参数3：把邮件内容格式改为str
            self.stp.sendmail(sender, receiver, mm.as_string())
        except Exception as e:
            print(e)
        finally:
            self.close()

    def sendMany(self, receivers, content, sender='linqingwang2001@163.com'):
        """群发邮件"""
        try:
            self.open()
            self.stp.login(sender, self.license)
            mm = MIMEMultipart('related')
            mm["From"] = f"签到系统<{sender}>"
            receivers_str = ''
            for receiver in receivers:
                receivers_str += f'<{receiver}>;'
            mm["To"] = receivers_str
            # 设置邮件主题
            mm["Subject"] = Header(content['subject'], 'utf-8')
            # 构造文本,参数1：正文内容，参数2：文本格式，参数3：编码方式
            message_text = MIMEText(content['body'], "plain", "utf-8")
            # 向MIMEMultipart对象中添加文本对象
            mm.attach(message_text)
            # 发送邮件，传递参数1：发件人邮箱地址，参数2：收件人邮箱地址，参数3：把邮件内容格式改为str
            self.stp.sendmail(sender, receivers, mm.as_string())
        except Exception as e:
            print(e)
        finally:
            self.close()
