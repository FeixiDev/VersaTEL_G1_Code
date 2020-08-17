import pytest
import GetConfig as gc
from collections import OrderedDict as odd


def test_read_config_file():
    readValue = gc.read_config_file()
    assert readValue


def test_read_sys_config_file():
    sys_readValue = gc.read_sys_config_file()
    assert sys_readValue


class TestEngineConfig:

    def setup_class(self):
        self.ec = gc.EngineConfig()

    def test_odd_engines(self):
        assert self.ec.oddEngines.keys() == ['engine0']
        assert self.ec.oddEngines.values() == ['10.203.1.6']

    def test_list_engines_alias(self):
        assert self.ec.list_engines_alias() == ['engine0']

    def test_list_engines_IP(self):
        assert self.ec.list_engines_IP() == ['10.203.1.6']

    def test_telnet_port(self):
        assert self.ec.telnet_port() == 23

    def test_FTP_port(self):
        assert self.ec.FTP_port() == 21

    def test_password(self):
        assert self.ec.password() == ''

    def test_trace_level(self):
        assert self.ec.trace_level() == 3


class TestDBConfig:

    def setup_class(self):
        self.dbc = gc.DBConfig()

    def test_host(self):
        assert self.dbc.host() == '127.0.0.1'

    def test_port(self):
        assert self.dbc.port() == 27017

    def test_name(self):
        assert self.dbc.name() == 'MonitorDB'


class TestSwitchConfig:

    def setup_class(self):
        self.swc = gc.SwitchConfig()

    def test_odd_switches_Alias(self):
        assert self.swc.oddSWAlias.keys() == ['switch0']
        assert self.swc.oddSWAlias.values() == ['10.203.1.9']

    def test_odd_switches_Ports(self):
        assert self.swc.oddSWPort.keys() == ['switch0', 'switch1']
        assert self.swc.oddSWPort.values() == [[1, 2, 3, 4, 5, 6], [
            1, 2, 3, 4, 5, 6]]

    def test_list_switch_alias(self):
        assert self.swc.list_switch_alias() == ['switch0']

    def test_list_switch_IP(self):
        assert self.swc.list_switch_IP() == ['10.203.1.9']

    def test_list_switch_ports(self):
        assert self.swc.list_switch_ports() == [[1, 2, 3, 4, 5, 6], [
            1, 2, 3, 4, 5, 6]]

    def test_SSH_port(self):
        assert self.swc.SSH_port() == 22

    def test_username(self):
        assert self.swc.username() == 'admin'

    def test_password(self):
        assert self.swc.password() == 'Feixi@123'

    def test_sw_enable_status(self):
        assert self.swc.sw_enable_status() == 'yes'

    def test_threshold_total(self):
        assert self.swc.threshold_total() == (200, 2000)


class TestEmailConfig:

    def setup_class(self):
        self.emc = gc.EmailConfig()

    def test_email_host(self):
        assert self.emc.email_host() == 'smtp.qq.com'

    def test_email_port(self):
        assert self.emc.email_port() == 465

    def test_email_sender(self):
        assert self.emc.email_sender() == '2134056745@qq.com'

    def test_email_password(self):
        assert self.emc.email_password() == 'qiftayumbjbtdagd'

    def test_email_receiver(self):
        assert self.emc.email_receiver() == 'paul.wen@feixitek.com'

    def test_email_enable(self):
        assert self.emc.email_enable() == 'yes'

    def test_email_encrypt(self):
        assert self.emc.email_encrypt() == 'ssl'

    def test_email_anonymous(self):
        assert self.emc.email_anonymous() == 'no'


class TestSetting:

    def setup_class(self):
        self.s = gc.Setting()

    def test_message_level(self):
        assert self.s.message_level() == 3

    def test_interval_web_refresh(self):
        assert self.s.interval_web_refresh() == 15

    def test_interval_haap_update(self):
        assert self.s.interval_haap_update() == 10

    def test_interval_sansw_update(self):
        assert self.s.interval_sansw_update() == 60

    def test_interval_warning_check(self):
        assert self.s.interval_warning_check() == 7200

    def test_cron_cycle(self):
        assert self.s.cron_cycle() == 'day'

    def test_cron_day(self):
        assert self.s.cron_day() == 2

    def test_cron_hour(self):
        assert self.s.cron_hour() == 17

    def test_cron_minutes(self):
        assert self.s.cron_minutes() == 41

    def test_folder_collection(self):
        assert self.s.folder_collection() == 'collections'

    def test_folder_swporterr(self):
        assert self.s.folder_swporterr() == 'SWPorterr'

    def test_folder_trace(self):
        assert self.s.folder_trace() == 'Trace'

    def test_folder_traceanalyse(self):
        assert self.s.folder_traceanalyse() == 'TraceAnalyse'

    def test_folder_cfgbackup(self):
        assert self.s.folder_cfgbackup() == 'CFGBackup'

    def test_folder_PeriodicCheck(self):
        assert self.s.folder_PeriodicCheck() == 'PeriodicCheck'

    def test_PCEngineCommand(self):
        assert self.s.PCEngineCommand() == [
            'vpd', 'conmgr status', 'mirror', 'group', 'map', 'drvstate', 'history', 'sfp all']

    def test_PCSANSwitchCommand(self):
        assert self.s.PCSANSwitchCommand() == [
            'switchstatusshow', 'switchshow', 'portshow', 'porterrshow', 'nsshow', 'zoneshow', 'cfgshow']

    def test_oddRegularTrace(self):
        assert self.s.oddRegularTrace()


class TestGeneral:

    def test_get_PRODUCT(self):
        g = gc.General()
        assert g.get_PRODUCT() == 'HA-AP'
