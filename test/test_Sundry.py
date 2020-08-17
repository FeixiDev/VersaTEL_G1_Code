import Sundry as sun
import HAAP as haap
import pytest
import datetime
import time
import os
import shutil
import xlwt
try:
    import configparser as cp
except Exception:
    import ConfigParser as cp


cfg = cp.ConfigParser(allow_no_value=True)
cfg.read('config.ini')
ip = str(cfg.get('Engines', 'engine0'))

@pytest.mark.bc
def test_time_now_folder():
    assert sun.time_now_folder()


@pytest.mark.mnt
def test_time_now_to_show():
    assert sun.time_now_to_show()


@pytest.mark.mnt
def test_is_Warning():
    assert sun.is_Warning(500, 200) == True
    assert sun.is_Warning(500, 2000) == None
    assert sun.is_Warning(100, [200, 2000]) == 0
    assert sun.is_Warning(600, [200, 2000]) == 1
    assert sun.is_Warning(3000, [200, 2000]) == 2


@pytest.mark.gt
def test_is_trace_level():
    assert sun.is_trace_level(0) == None
    assert sun.is_trace_level(1) == True


@pytest.mark.ptes
@pytest.mark.ptcl
@pytest.mark.sws
@pytest.mark.bc
@pytest.mark.gt
@pytest.mark.ec
@pytest.mark.fw
@pytest.mark.st
@pytest.mark.stm
@pytest.mark.pc
def test_is_IP():
    assert sun.is_IP('10.203.1.1') == True
    assert sun.is_IP('6.6.6.256') == False


@pytest.mark.ec
@pytest.mark.fw
def test_is_file():
    assert sun.is_file('Sundry.py') == True
    assert sun.is_file('test_Sundry.py') == False


@pytest.mark.at
@pytest.mark.pc
def test_is_folder():
    assert sun.is_folder('test') == True
    assert sun.is_folder('pytest') == False


@pytest.mark.ptcl
def test_is_port():
    assert sun.is_port('789') == True
    assert sun.is_port(789) == True
    assert sun.is_port('a789') == False


@pytest.mark.bc
@pytest.mark.gt
@pytest.mark.ec
@pytest.mark.pc
@pytest.mark.fw
@pytest.mark.st
@pytest.mark.stm
@pytest.mark.sts
@pytest.mark.mnt
def test_ShowErr():
    assert sun.ShowErr('a', 'b', 'c', 'd', 'e') == None


@pytest.mark.bc
@pytest.mark.at
def test_GotoFolder():
    fold = sun.GotoFolder('testa')
    assert fold == True
    if fold:
        try:
            os.chdir('../')
            os.removedirs('testa')
        except:
            pass


@pytest.mark.mnt
class TestTiming:

    def setup_class(self):
        self.timing = sun.Timing()

    def a(self):
        print('a test')

    def test_add_interval(self):
        assert self.timing.add_interval(self.a, 3) == None

    def test_stt(self):
        pass
        # assert self.timing.stt() == None

    def test_stp(self):
        pass
        # assert self.timing.stp() == None


@pytest.mark.bc
@pytest.mark.gt
@pytest.mark.ec
@pytest.mark.pc
@pytest.mark.fw
@pytest.mark.st
@pytest.mark.stm
class TestTimeNow:

    def setup_class(self):
        self.time = sun.TimeNow()
        self.timenow = time.localtime()

    def test_y(self):
        assert self.time.y() == self.timenow[0]

    def test_mo(self):
        assert self.time.mo() == self.timenow[1]

    def test_d(self):
        assert self.time.d() == self.timenow[2]

    def test_h(self):
        assert self.time.h() == self.timenow[3]

    def test_mi(self):
        assert self.time.mi() == self.timenow[4]

    def test_s(self):
        assert self.time.s() == self.timenow[5]

    def test_wd(self):
        assert self.time.wd() == self.timenow[6]


@pytest.mark.at
class TestTraceAnalyse:

    def setup_class(self):
        haap.get_trace_all(3)
        os.chdir('Trace')
        pwd = os.getcwd()
        ls = os.listdir(pwd)
        self.trace = ls[-1]
        self.analyse = sun.TraceAnalyse(self.trace)

    def teardown_class(self):
        shutil.rmtree(self.trace)
        os.chdir('..')
        try:
            os.removedirs('Trace')
        except:pass

    def test_run(self):
        assert self.analyse.run() == None

    def test_get_trace_file_list(self):
        os.chdir(self.trace)
        file = self.analyse._get_trace_file_list()
        assert file[0] == 'Trace_%s_Secondary.log' % ip
        assert file[1] == 'Trace_%s_Primary.log' % ip
        assert file[2] == 'Trace_%s_Trace.log' % ip
        os.chdir('../')

    def test_analyse_file(self):
        assert self.analyse._analyse_file() == None

    def test_find_error(self):
        assert self.analyse._find_error(
            '%s/Trace_%s_Secondary.log' % (self.trace, ip)) == None

    def test_generate_excel_file_name(self):
        assert self.analyse._generate_excel_file_name(
            'Trace_%s_Secondary.log' % ip) == 'TraceAnalyze_Trace_%s_Secondary.xls' % ip

    def test_write_to_excel(self):
        objExcel = xlwt.Workbook()
        date =  [('11:11', 'P1', 'test', 'test'), ('12:12', 'P1', 'test', 'test')]
        assert self.analyse._write_to_excel(objExcel, 'test_error', date) == None
        xls_file_name = 'TraceAnalyze_Trace_Test.xls'
        objExcel.save(xls_file_name)
        os.remove(xls_file_name)
        

    def test_read_file(self):
        assert self.analyse._read_file(
            'Trace_%s_Secondary.log' % ip) == None
