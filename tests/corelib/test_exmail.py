from corelib.exmail import send_mail_task


class TestExmail:
    def test_send_mail(self):
        class A:
            pass
        msg = A()
        msg.send_to = {'812350401@qq.com'}
        msg.html = "haha"
        msg.subject = '你好'
        send_mail_task(msg)
