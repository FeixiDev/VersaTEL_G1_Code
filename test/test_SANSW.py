import pytest
import io
import sys
import datetime
import SANSW as sw
import GetConfig as gc
try:
    import configparser as cp
except Exception:
    import ConfigParser as cp


cfg = cp.ConfigParser(allow_no_value=True)
cfg.read('config.ini')
ip = str(cfg.get('SANSwitches', 'switch0'))
ssh_port = cfg.getint('SANSwitcheSetting', 'ssh_port')
user = str(cfg.get('SANSwitcheSetting', 'username'))
pw = str(cfg.get('SANSwitcheSetting', 'password'))
port = eval(cfg.get('SANSwitchePorts', 'switch0'))

sys_cfg = cp.ConfigParser(allow_no_value=True)
sys_cfg.read('sys_cfg.ini')
ssc = list(i[0] for i in sys_cfg.items('PCSANSwitchCommand'))
pcfolder = str(sys_cfg.get('FolderSetting', 'PeriodicCheck'))
time_now = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
fname = 'PC_%s_SANSwitch_%s.log' % (time_now, ip)


@pytest.mark.ptcl
def test_clear_all():
    assert sw.clear_all() == None


@pytest.mark.ptcl
def test_clear_one_port():
    assert sw.clear_one_port(ip, 1) == None


@pytest.mark.ptes
def test_print_porterror_all_formated():
    assert sw.print_porterror_all_formated() == None


@pytest.mark.ptes
def test_print_porterror_formated():
    assert sw.print_porterror_formated(ip) == None


@pytest.mark.sws
def test_print_switchshow_all():
    assert sw.print_switchshow_all() == None


@pytest.mark.sws
def test_print_switchshow():
    assert sw.print_switchshow(ip) == None


@pytest.mark.pc
def test_periodically_check_all():
    assert sw.periodically_check_all() == None


@pytest.mark.pc
def test_periodically_check():
    assert sw.periodically_check(ip) == None


@pytest.mark.mnt
def test_get_info_for_DB():
    a = []
    for i in sw.get_info_for_DB():
        a.append(i)
    assert isinstance(a[0], dict)
    assert isinstance(a[1], dict)
    assert isinstance(a[2], dict)


@pytest.mark.ptcl
@pytest.mark.sws
@pytest.mark.pc
class TestAction:

    def setup_class(self):
        self.act = sw.Action(ip, ssh_port, user, pw, [])

    def test_get_switch_info(self):
        assert self.act._get_switch_info() == True

    def test_print_porterrshow(self):
        assert self.act.print_porterrshow() == None

    def test_print_switchshow(self):
        assert self.act.print_switchshow() == None

    def test_clear_all_port(self):
        sys.stdout = io.BytesIO()
        assert self.act.clear_all_port() == None
        assert 'completed' in sys.stdout.getvalue()

    def test_clear_one_port(self):
        assert self.act.clear_one_port(1) == True

    def test_periodic_check(self):
        assert self.act.periodic_check(ssc, pcfolder, fname) == None


@pytest.mark.ptes
class TestStatus:

    def setup_class(self):
        self.st = sw.Status(ip, ssh_port, user, pw, port)

    def test_PutErrorToDict(self):
        assert self.st._dicPartPortError is not None

    def test_err_num_int(self):
        assert self.st.err_num_int('259') == 259
        assert self.st.err_num_int('2.5k') == 2500
        assert self.st.err_num_int('3.8m') == 3800000
        assert self.st.err_num_int('6.76g') == 6760000000

    def test_list_string_to_int(self):
        date = ['2.9k', '12', '3.4m', '333', '5.9g', '22k', '2']
        assert self.st.list_string_to_int(
            date) == [2900, 12, 3400000, 333, 5900000000, 22000, 2]

    def test_dict_string_to_int(self):
        assert self.st._dict_string_to_int(
            self.st._dicPartPortError) != None

    def test_sum_and_total(self):
        assert self.st.sum_and_total() != None

    # def test_sum_total_and_warning(self):
    #     assert self.st.sum_total_and_warning() == None

    def test_print_porterror_formated(self):
        assert self.st.print_porterror_formated() == None

    # def test_get_linkfail_by_port(self):
    #     assert self.st.get_linkfail_by_port(port) == None

    # def test_get_encout_by_port(self):
    #     assert self.st.get_encout_by_port(port) == None

    # def test_get_discC3_by_port(self):
    #     assert self.st.get_discC3_by_port(port) == None


@pytest.mark.mnt
class TestInfoForDB:

    def setup_class(self):
        self.infodb = sw.InfoForDB('switch0', ip, port)

    def test_get_dicOrigin(self):
        date = self.infodb.get_dicOrigin()
        assert isinstance(date, dict)

    def test_get_dicPEFormated(self):
        date = self.infodb.get_dicPEFormated()
        assert isinstance(date, dict)

    def test_get_summary_total(self):
        date = self.infodb.get_summary_total()
        PE_Sum = date['switch0']['PE_Sum']
        assert isinstance(PE_Sum, list)



if __name__ == '__main__': 
    print(port)