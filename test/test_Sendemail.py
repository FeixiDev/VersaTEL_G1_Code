import pytest
import SendEmail
import io
import sys


@pytest.mark.mnt
class TestEmail:

    def setup_class(self):
        self.E = SendEmail.Email()

    def test_get_msg(self):
        assert self.E.get_msg('pytest', 'test')

    def test_prepare(self):
        assert self.E.prepare()

    def test_anonymous_prepare(self):
        assert self.E.anonymous_prepare()

    def test_send_email(self):
        assert self.E.send_email('pytest', 'test') == None


@pytest.mark.mnt
def testfunc():
    return


@pytest.mark.mnt
def test_switch():
    switch = SendEmail.email_switch(testfunc())
    assert switch


@pytest.mark.mnt
def test_send_warnmail():
    info = [['2020-06-01 11:36:42', '10.203.1.4',
             'engine1', 2, 'Engine reboot 6674 secends ago']]
    sys.stdout = io.BytesIO()
    assert SendEmail.send_warnmail(info) == None
    assert sys.stdout.getvalue() == 'Send success!\n'


@pytest.mark.mnt
def test_send_test():
    sys.stdout = io.BytesIO()
    assert SendEmail.send_test() == None
    assert sys.stdout.getvalue() == 'Send success!\n'


@pytest.mark.mnt
def test_send_live():
    sys.stdout = io.BytesIO()
    assert SendEmail.send_live() == None
    assert sys.stdout.getvalue() == 'Send success!\n'
