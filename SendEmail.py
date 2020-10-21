# coding:utf8
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import GetConfig as gc
try:
    import configparser as cp
except Exception:
    import ConfigParser as cp


class Email():
    def __init__(self):
        # read configuration from config.ini/[EmailSetting]
        cfg = gc.EmailConfig()
        self._enable = cfg.email_enable()
        self._host = cfg.email_host()
        self._port = cfg.email_port()
        self._sender = cfg.email_sender()
        self._password = cfg.email_password()
        self._receiver = cfg.email_receiver()
        self._receiver_list = self._receiver.split(',')
        self._encrypt = cfg.email_encrypt()
        self._anonymous = cfg.email_anonymous()
        self._timeout = 5

    def _package_msg(self, title, content):
        msg = MIMEMultipart()
        msg['Subject'] = title
        msg['From'] = self._sender
        msg['To'] = self._receiver
        context = MIMEText(content, _subtype='html', _charset='utf-8')
        msg.attach(context)
        return msg

    def email_switch(func):
        def send(self, *args):
            if self._enable == 'yes':
                return func(self, *args)
            else:
                print("The Email swich is off.")
        return send

    def _connect_login(self):
        try:
            if self._encrypt == 'ssl':
                send_smtp = smtplib.SMTP_SSL(self._host, self._port, timeout=self._timeout)
                send_smtp.connect(self._host)
            else:
                send_smtp = smtplib.SMTP(timeout=self._timeout)
                if self._encrypt == 'tls':
                    send_smtp.connect(self._host, self._port)
                    send_smtp.ehlo()
                    send_smtp.starttls()
                else:
                    send_smtp.connect(self._host, self._port)
                    send_smtp.ehlo()
        except:
            print("Failed to connect smtp server!")
            return False
        try:
            send_smtp.login(self._sender, self._password)
        except:
            print("ID or Password is wrong")
            return False
        return send_smtp

    def _connect_login_anonymous(self):
        try:
            if self._encrypt == 'ssl':
                send_smtp = smtplib.SMTP_SSL(self._host, self._port, timeout=self._timeout)
            else:
                send_smtp = smtplib.SMTP(self._host, self._port, timeout=self._timeout)
            return send_smtp
        except:
            print("The Host unable to connect!")
            return False

    def _send_mail(self, title, content):
        if self._anonymous == 'yes':
            send_smtp = self._connect_login_anonymous()
        else:
            send_smtp = self._connect_login()
        if send_smtp:
            try:
                msg = self._package_msg(title, content)
                send_smtp.sendmail(
                    self._sender, self._receiver_list, msg.as_string())

            except:
                print("Send Fail, Please check 'receiver'.")
                return
        else:
            return
        send_smtp.close()
        print("Send success!")

    @email_switch
    def send_warning_mail(self, warninfo_email):
        data_table = ""
        for lstMsg in warninfo_email:
            line_table = """<tr>
                            <td>""" + str(lstMsg[0]) + """</td>
                            <td>""" + str(lstMsg[1]) + """</td>
                            <td>""" + str(lstMsg[2]) + """</td>
                            <td>""" + str(lstMsg[3]) + """</td>
                            <td>""" + str(lstMsg[4]) + """</td>
                        </tr>"""
            data_table = data_table + line_table
        content = """\
                <html>
                <head>
                    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
                    <title>用户未确认预警信息</title>
                </head>
                <body>
                    <div id="container">
                    <p><strong>用户未确认预警信息</strong></p>
                    </div>
                    <div id="content">
                        <table width="500" border="2" bordercolor="red" cellspacing="2">
                            <div class="container">
                                <div class="row">
                                <div class="container">
                                    <tr>
                                        <th>Time</th>
                                        <th>IP</th>
                                        <th>Device</th>
                                        <th>Level</th>
                                        <th>Message</th>
                                    </tr>
                                    """ + data_table + """
                                </div>
                                </div>  
                            </div>     
                        </table>
                    </div>
                </body>
                </html> """
        title = "ClusterIO System Status Alert"
        self._send_mail(title, content)

    @email_switch
    def send_alive_mail(self):
        title = "HA-AP Timing alarm clock"
        content = "I'm still alive"
        self._send_mail(title, content)


    @email_switch
    def send_test_mail(self):
        title = "This is a HA-AP test email"
        content = "Test"
        self._send_mail(title, content)


if __name__ == '__main__':
    email = Email()
    email.send_test_mail()
    email.send_alive_mail()
    email.send_warning_mail([['2020-04-29 16:36:42', '10.203.1.4', 'engine0', 2, 'Engine reboot 6674 secends ago']])
    # a = [['2020-04-29 16:36:42', '10.203.1.4', 'engine0', 2, 'Engine reboot 6674 secends ago']]
    # send_warnmail(a)
