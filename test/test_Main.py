import subprocess
import pytest
import os
import time
import HAAP as haap
try:
    import configparser as cp
except Exception:
    import ConfigParser as cp


cfg = cp.ConfigParser(allow_no_value=True)
cfg.read('config.ini')
swip = str(cfg.get('SANSwitches', 'switch0'))
engineip = str(cfg.get('Engines', 'engine0'))
t_port = cfg.getint('EngineSetting', 'telnet_port')
passwd = str(cfg.get('EngineSetting', 'password'))
ftp_port = cfg.getint('EngineSetting', 'ftp_port')


def output(cmd):
    cmds = 'python Main.py %s' % cmd
    return subprocess.check_output(cmds, shell=True)


def test_help():
    string1 = output('')
    assert 'Command' in string1
    string2 = output('a')
    assert 'Command' in string2


@pytest.mark.ptes
def test_ptes_help():
    string1 = output('ptes')
    assert 'Show port error' in string1
    string2 = output('ptes all 10.203.1.1')
    assert 'Show port error' in string2


@pytest.mark.ptes
def test_ptes_all():
    string = output('ptes all')
    assert 'Port error count display for SAN switch' in string


@pytest.mark.ptes
def test_ptes_ip_f():
    string = output('ptes ip')
    assert 'Please provide correct switch ip...\n' == string


@pytest.mark.ptes
def test_ptes():
    string = output('ptes %s' % swip)
    assert 'Port error count display for SAN switch' in string


@pytest.mark.ptcl
def test_ptcl_help():
    string1 = output('ptcl')
    assert 'statsclear' in string1
    string2 = output('ptcl a b c')
    assert 'statsclear' in string2


@pytest.mark.ptcl
def test_ptcl_all():
    string = output('ptcl all')
    assert 'Start clearing all error count For SAN switch' in string


@pytest.mark.ptcl
def test_ptcl_ip_f():
    string = output('ptcl ip')
    assert 'Please provide correct switch ip...\n' == string


@pytest.mark.ptcl
def test_ptcl_port_f():
    string = output('ptcl %s a' % swip)
    assert 'Please provide correct port number...\n' == string


@pytest.mark.ptcl
def test_ptcl():
    string = output('ptcl %s 1' % swip)
    assert 'Clear error count of port 1' in string


@pytest.mark.sws
def test_sws_help():
    string1 = output('sws')
    assert 'switchshow' in string1
    string2 = output('sws a b')
    assert 'switchshow' in string2


@pytest.mark.sws
def test_sws_all():
    string = output('sws all')
    assert 'switchshow for SAN switch' in string


@pytest.mark.sws
def test_sws_ip_f():
    string = output('sws ip')
    assert 'Please provide correct switch ip...\n' == string


@pytest.mark.sws
def test_sws():
    string = output('sws %s' % swip)
    assert 'switchshow for SAN switch' in string


@pytest.mark.bc
def test_bc_help():
    string1 = output('bc')
    assert 'Backup config' in string1
    string2 = output('bc a b')
    assert 'Backup config' in string2


@pytest.mark.bc
def test_bc_all():
    string = output('bc all')
    assert 'backup completely for' in string


@pytest.mark.bc
def test_bc_ip_f():
    string = output('bc ip')
    assert 'Please provide correct engine ip...\n' == string


@pytest.mark.bc
def test_bc():
    string = output('bc %s' % engineip)
    assert 'backup completely for' in string


@pytest.mark.gt
def test_gt_help():
    string1 = output('gt')
    assert 'Get trace of HA-AP' in string1
    string2 = output('gt 1 1 1')
    assert 'Get trace of HA-AP' in string2


@pytest.mark.gt
def test_gt_all():
    string1 = output('gt all')
    assert 'completed' in string1
    string2 = output('gt all 2')
    assert 'completed' in string2


@pytest.mark.gt
def test_gt_all_level_f():
    string = output('gt all 50')
    assert 'Trace level must be "1" or "2" or "3"\n' == string


@pytest.mark.gt
def test_gt():
    string = output('gt %s 2' % engineip)
    assert 'completed' in string


@pytest.mark.gt
def test_gt_ip_f():
    string = output('gt ip 2')
    assert 'Please provide correct engine ip...\n' == string


@pytest.mark.gt
def test_gt_ip_level_f():
    string = output('gt %s 50' % engineip)
    assert 'Trace level must be "1" or "2" or "3"\n' == string


@pytest.mark.at
def test_at_help():
    string1 = output('at')
    assert 'Analyse given trace of HA-AP' in string1
    string2 = output('at 1 1')
    assert 'Analyse given trace of HA-AP' in string2


@pytest.mark.at
def test_at_folder_f():
    string = output('at tracea')
    assert 'Please provide correct trace folder\n' == string


@pytest.mark.at
def test_at():
    string = output('at trace')
    assert string == ''


@pytest.mark.ec
def test_ec_help():
    string = output('ec')
    assert 'Execute commands listed' in string


@pytest.mark.ec
def test_ec_ip_f():
    with open('cmd.txt', 'w') as f:
        f.write("vpd\nvaai\nport\n")
        f.close()
    string = output('ec ip cmd.txt')
    assert 'Please provide correct engine ip...' in string
    os.remove('cmd.txt')


@pytest.mark.ec
def test_ec_folder_f():
    string = output('ec %s cmd.txt' % engineip)
    assert 'File not exists. please provide correct file...' in string


@pytest.mark.ec
def test_ec():
    with open('cmd.txt', 'w') as f:
        f.write("vpd\nvaai\nport\n")
        f.close()
    string = output('ec %s cmd.txt' % engineip)
    assert string != None
    os.remove('cmd.txt')


@pytest.mark.fw
def test_fw_help():
    string = output('fw')
    assert 'Change firmware for given engine using' in string


@pytest.mark.fw
def test_fw_ip_f():
    string = output('fw ip FW_15.9.8.2_OR.bin')
    assert 'Please provide correct engine ip...' in string


@pytest.mark.fw
def test_fw_folder_f():
    string = output('fw %s FW_15.bin' % engineip)
    assert 'File not exists. please provide correct file...' in string


@pytest.mark.fw
def test_fw():
    status = haap.Status(engineip, t_port, passwd, ftp_port)
    fw_version = status.get_version()
    assert fw_version != None
    if fw_version == 'V15.9.8.4':
        output('fw %s FW_15.9.8.2_OR.bin' % engineip)
    else:
        output('fw %s FW_15.9.8.4_OR.bin' % engineip)
    time.sleep(60)
    try:
        status = haap.Status(engineip, t_port, passwd, ftp_port)
        fw_version_new = status.get_version()
    except:
        fw_version_new = None
    if fw_version_new:
        if fw_version == 'V15.9.8.4':
            assert fw_version_new == 'V15.9.8.2'
        else:
            assert fw_version_new == 'V15.9.8.4'


@pytest.mark.sts
def test_sts_help():
    string = output('sts')
    assert 'sts <HAAP_IP>' in string


@pytest.mark.sts
def test_sts_all():
    string = output('sts all')
    assert 'Engine' in string


@pytest.mark.sts
def test_sts_ip_f():
    string = output('sts ip')
    assert 'Please provide correct engine ip...\n' == string


@pytest.mark.sts
def test_sts():
    string = output('sts %s' % engineip)
    assert 'Engine' in string


@pytest.mark.st
def test_st_help():
    string = output('st')
    assert 'st <HAAP_IP>' in string


@pytest.mark.st
def test_st_all():
    string = output('st all')
    assert 'Setting time for engine' in string


@pytest.mark.st
def test_st_ip_f():
    string = output('st ip')
    assert 'Please provide correct engine ip...\n' == string


@pytest.mark.st
def test_st():
    string = output('st %s' % engineip)
    assert 'Setting time for engine' in string


@pytest.mark.stm
def test_stm_help():
    string = output('stm')
    assert 'stm <HAAP_IP>' in string


@pytest.mark.stm
def test_stm_all():
    string = output('stm all')
    assert 'Current calibration' in string


@pytest.mark.stm
def test_stm_ip_f():
    string = output('stm ip')
    assert 'Please provide correct engine ip...\n' == string


@pytest.mark.stm
def test_stm():
    string = output('stm %s' % engineip)
    assert 'Current calibration' in string


@pytest.mark.pc
def test_pc_help():
    string1 = output('pc')
    assert 'Periodically check for HA-AP' in string1
    string2 = output('pc haa')
    assert 'Periodically check for HA-AP' in string2


@pytest.mark.pc
def test_pc_all():
    string = output('pc all')
    assert 'CLI>' in string
    assert 'Switch Name' in string


@pytest.mark.pc
def test_pc_haap():
    string = output('pc haap')
    assert 'CLI>' in string


@pytest.mark.pc
def test_pc_haap_ip():
    string = output('pc haap %s' % engineip)
    assert 'CLI>' in string


@pytest.mark.pc
def test_pc_haap_ip_f():
    string = output('pc haap ip')
    assert string == 'Please provide correct engine ip...\n'


@pytest.mark.pc
def test_pc_sw():
    string = output('pc sw')
    assert 'Switch Name' in string


@pytest.mark.pc
def test_pc_sw_ip():
    string = output('pc sw %s' % swip)
    assert 'Switch Name' in string


@pytest.mark.pc
def test_pc_sw_ip_f():
    string = output('pc sw ip')
    assert string == 'Please provide correct SAN switch ip...\n'


@pytest.mark.mnt
def test_mnt_help():
    string = output('mnt')
    assert 'Show status through web page' in string


@pytest.mark.mnt
def test_mnt_rt():
    pass
    # string = output('mnt rt')
    # assert '' in string


@pytest.mark.mnt
def test_mnt_db():
    pass
    # string = output('mnt db')
    # assert '' in string


@pytest.mark.mnt
def test_mnt_f():
    string = output('mnt f')
    assert 'rt(realtime) or db(datarase)\n' == string


def test_version():
    string = output('v')
    assert 'VersaTEL G1' in string


if __name__ == '__main__':
    pytest.main(['-k', 'test_version', 'test/test_Main.py'])
