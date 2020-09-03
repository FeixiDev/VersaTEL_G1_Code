import pytest
import datetime
import HAAP as haap
import time
import os
try:
    import configparser as cp
except Exception:
    import ConfigParser as cp


cfg = cp.ConfigParser(allow_no_value=True)
cfg.read('config.ini')
ip = str(cfg.get('Engines', 'engine0'))
t_port = cfg.getint('EngineSetting', 'telnet_port')
passwd = str(cfg.get('EngineSetting', 'password'))
ftp_port = cfg.getint('EngineSetting', 'ftp_port')
time_now = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
cfgfname = '%s/%s' % ('CFGBackup', time_now)
tracefname = '%s/%s' % ('Trace', time_now)
pcfname = 'PC_%s_Engine_%s.log' % (time_now, ip)
level = 3


@pytest.mark.bc
def test_backup_config_all():
    assert haap.backup_config_all() == None


@pytest.mark.bc
def test_backup_config():
    assert haap.backup_config(ip) == None


@pytest.mark.fw
def test_change_firmware():
    pwd = os.getcwd()
    ls = os.listdir(pwd)
    if 'FW_15.9.8.2_OR.bin' and 'FW_15.9.8.4_OR.bin' not in ls:
        return
    status = haap.Status(ip, t_port, passwd, ftp_port)
    fw_version = status.get_version()
    if fw_version == None:
        print("Can't get firmware version.")
        return
    elif fw_version == 'V15.9.8.4':
        haap.change_firmware(ip, 'FW_15.9.8.2_OR.bin')
    else:
        haap.change_firmware(ip, 'FW_15.9.8.4_OR.bin')
    time.sleep(60)
    try:
        status = haap.Status(ip, t_port, passwd, ftp_port)
        fw_version_new = status.get_version()
    except:
        fw_version_new = None
    if fw_version_new:
        if fw_version == 'V15.9.8.4':
            assert fw_version_new == 'V15.9.8.2'
        else:
            assert fw_version_new == 'V15.9.8.4'
    else:
        print("Can't get firmware version.")


@pytest.mark.gt
def test_get_trace_all():
    assert haap.get_trace_all(level)


@pytest.mark.gt
def test_get_trace():
    assert haap.get_trace(ip, level)


# def test_analyse_trace_all():
#     assert haap.analyse_trace_all(level) == None


# def test_analyse_trace():
#     assert haap.analyse_trace(ip, level) == None


@pytest.mark.ec
def test_execute_multi_commands():
    with open('cmd.txt', 'w') as f:
            f.write("vpd\nvaai\nport\n")
            f.close()
    assert haap.execute_multi_commands(ip, 'cmd.txt') == None
    os.remove('cmd.txt')


@pytest.mark.sts
def test_print_description():
    assert haap._print_description() == None


@pytest.mark.sts
def test_print_status_in_line():
    lStatus = haap.Status(ip, t_port, passwd, ftp_port).status_to_show()
    assert haap._print_status_in_line(lStatus) == None


@pytest.mark.sts
def test_show_stauts_all():
    assert haap.show_stauts_all() == None


@pytest.mark.sts
def test_show_stauts():
    assert haap.show_stauts(ip) == None


@pytest.mark.st
def test_set_time_all():
    assert haap.set_time_all() == None


@pytest.mark.st
def test_set_time():
    assert haap.set_time(ip) == None


@pytest.mark.stm
def test_show_time_all():
    assert haap.show_time_all() == None


@pytest.mark.stm
def test_show_time():
    assert haap.show_time(ip) == None


@pytest.mark.pc
def test_periodically_check_all():
    assert haap.periodically_check_all() == None


@pytest.mark.pc
def test_periodically_check():
    assert haap.periodically_check(ip) == None


@pytest.mark.mnt
def test_origin():
    lStatus = haap.Status(ip, t_port, passwd, ftp_port)
    assert haap.origin('engine0', lStatus)


@pytest.mark.mnt
def test_info():
    lStatus = haap.Status(ip, t_port, passwd, ftp_port)
    assert haap.info('engine0', lStatus)


@pytest.mark.mnt
def test_data_for_db():
    data = haap.data_for_db()
    assert data[0].keys() == ['engine0']
    assert data[1].keys() == ['engine0']


@pytest.mark.bc
@pytest.mark.gt
@pytest.mark.ec
@pytest.mark.pc
@pytest.mark.fw
class TestAction:

    def setup_class(self):
        time.sleep(5)
        self.action = haap.Action(ip, t_port, passwd, ftp_port)

    def test_telnet_connect(self):
        assert self.action._TN_Conn != None
        assert self.action._TN_Connect_Status == True

    def test_executeCMD(self):
        action = haap.Action(ip, t_port, passwd, ftp_port)
        assert action._executeCMD('engine') != None
        action._TN_Connect_Status = None
        assert action._executeCMD('engine') == None

    def test_FTP_connect(self):
        assert self.action._FTP_connect() == None

    def test_ftp(self):
        assert self.action._ftp() != None

    def test_backup(self):
        assert self.action.backup(cfgfname) == None

    def test_auto_commands(self):
        with open('cmd.txt', 'w') as f:
            f.write("vpd\nvaai\nport\n")
            f.close()
        assert self.action.auto_commands('cmd.txt') == None
        os.remove('cmd.txt')

    def test_get_trace(self):
        assert self.action.get_trace(tracefname, level) == None

    def test_periodic_check(self):
        pccommand = ['vpd', 'conmgr status', 'mirror', 'group',
                     'map', 'drvstate', 'history', 'sfp', 'all']
        assert self.action.periodic_check(
            pccommand, 'PeriodicCheck', pcfname) == None

    def test_set_time(self):
        assert self.action.set_time() == None

    def test_show_time(self):
        assert self.action.show_time() == None


@pytest.mark.sts
@pytest.mark.mnt
class TestUptime:

    def setup_class(self):
        strtime = 'Uptime : 12d 23:14:23'
        self.uptime = haap.Uptime(strtime)

    def test__uptime_list(self):
        assert self.uptime.list_uptime == [12, 23, 14, 23]

    def test_uptime_list(self):
        assert self.uptime.uptime_list() != None

    def test_uptime_second(self):
        assert self.uptime.uptime_second() == 1120463

    def test_uptime_to_show(self):
        assert self.uptime.uptime_to_show() == '12d 23h 14m'


@pytest.mark.sts
@pytest.mark.mnt
class TestStatus:

    def setup_class(self):
        self.status = haap.Status(ip, t_port, passwd, ftp_port)

    def test_get_info_to_dict(self):
        assert self.status.dictInfo != None

    def test_uptime_list(self):
        assert self.status.uptime_list() != None

    def test_uptime_second(self):
        assert self.status.uptime_second() != None

    def test_uptime_to_show(self):
        assert self.status.uptime_to_show() != None

    def test__is_master(self):
        status = haap.Status(ip, t_port, passwd, ftp_port)
        assert status._is_master(None) == 0
        engine1 = "Engine  Status  Serial #  IP Addresses"
        engine2 = ">> 0 (M) Online  11340468  10.203.1.6  15.9.8.2 OR"
        assert status._is_master(engine1) == None
        assert status._is_master(engine2) == 1

    def test_is_master(self):
        assert self.status.is_master()

    def test_cluster_status(self):
        status = haap.Status(ip, t_port, passwd, ftp_port)
        status.dictInfo['engine'] = '>> 0 offline'
        assert status.cluster_status() == 1
        status.dictInfo['engine'] = '>> 0 online'
        assert status.cluster_status() == 0

    def test_get_version(self):
        status = haap.Status(ip, t_port, passwd, ftp_port)
        status.dictInfo['vpd'] = "Firmware V15.9.8.2 HA-AP"
        assert status.get_version() == 'V15.9.8.2'
        status.dictInfo['vpd'] = None
        assert status.get_version() == None

    def test_get_mirror_status(self):
        status = haap.Status(ip, t_port, passwd, ftp_port)
        status.dictInfo['mirror'] = " 33281(0x8201) Operational  67108864  2044 (OK )  2046 (OK )"
        assert status.get_mirror_status() == 0
        status.dictInfo['mirror'] = " 33281(0x8201) Operational  67108864  2044 (deg )  2046 (OK )"
        assert status.get_mirror_status() == 1
        status.dictInfo['mirror'] = None
        assert status.get_mirror_status() == None

    def test_over_all(self):
        status = haap.Status(ip, t_port, passwd, ftp_port)
        assert status.over_all()[1] == 0
        status.AHStatus = 1
        assert status.over_all()[1] == '1'
        status._TN_Connect_Status = None
        assert status.over_all()[1] == '--'

    def test_status_to_show(self):
        date = self.status.status_to_show()
        assert isinstance(date, list)

    def test_status_to_show_and_warning(self):
        date = self.status.status_to_show_and_warning()
        assert isinstance(date, list)
