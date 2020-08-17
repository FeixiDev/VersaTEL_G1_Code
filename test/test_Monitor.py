import Monitor as mon
import pytest

# def test_monitor_rt_1_thread():
# 	assert mon.monitor_rt_1_thread() == None

# def test_haap_interval_check():
# 	assert mon.haap_interval_check(3) == None


@pytest.mark.mnt
def test_check_all_haap():
    assert mon.check_all_haap() == None


@pytest.mark.mnt
def test_check_all_sansw():
    assert mon.check_all_sansw() == None


@pytest.mark.mnt
def test_warning_check():
    assert mon.warning_check() == None


@pytest.mark.mnt
class Testhaap_judge:

    def setup_class(self):
        self.RT = ['10.203.1.6', 'OK', 2074129, 'OK', 'OK']
        self.DB = ['10.203.1.6', 'OK', 1725956, 'OK', 'OK']
        self.alias = 'engine0'
        self.haap = mon.haap_judge(self.RT, self.DB, self.alias)

    def test_judge_AH(self):
        assert self.haap.judge_AH(self.RT[1], self.DB[1]) != True

    def test_judge_reboot(self):
        assert self.haap.judge_reboot(self.RT[2], self.DB[2]) == None

    def test_judge_Status(self):
        assert self.haap.judge_Status(self.RT[3], self.DB[3]) == None

    def test_judge_Mirror(self):
        assert self.haap.judge_Mirror(self.RT[4], self.DB[4]) == None

    def test_all_judge(self):
        assert self.haap.all_judge() == None


@pytest.mark.mnt
def test_sansw_judge():
    assert mon.sansw_judge(20, 0, '10.203.1.9', 'switch0') == None


@pytest.mark.mnt
def test_warning_message_sansw():
    assert 'Warning' in mon.warning_message_sansw(1)
    assert 'Alarm' in mon.warning_message_sansw(2)


@pytest.mark.mnt
def test_haap_info_to_show():
    assert mon.haap_info_to_show()[1] != None


@pytest.mark.mnt
def test_sansw_info_to_show():
    assert mon.sansw_info_to_show()[1] != None


@pytest.mark.mnt
def test_haap_info_for_judge():
    info = {'engine0': {'status': [
        '10.203.1.6', 'OK', '23d 23h 35m', 'M', 'OK', 'OK'], 'up_sec': 2072108, 'level': 0}}
    assert mon.haap_info_for_judge(
        info) == {'engine0': ['10.203.1.6', 'OK', 2072108, 'OK', 'OK']}


@pytest.mark.mnt
def test_get_switch_total_db():
    total = mon.get_switch_total_db('switch0')
    assert total >= 0


@pytest.mark.mnt
def test_sansw_rt_info_to_show():
    info = mon.sansw_rt_info_to_show()
    assert info[0][0] == 'switch0'


@pytest.mark.mnt
def test_haap_rt_info_to_show():
    info = mon.haap_rt_info_to_show()
    assert info[0][0] == 'engine0'
