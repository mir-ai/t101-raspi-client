#!/usr/local/bin/python3
# coding: utf-8

import os
import subprocess
from subprocess import check_call
import socket
import time
import re
import struct
try:
    from uuid import getnode as get_mac
except ModuleNotFoundError:
    pass

# log_code 4400

# 下位ライブラリ
# ラズパイでの各種処理
class PlatformRaspi:

    def _get_device_cpu_id_raspi(interface : str = 'eth0') -> str:
        '''
        ラズパイ用のハードウェア（macアドレス）
        '''
        # get_mac() 202481594620491 48bit整数
        # hex(get_mac()) '0xb827eb855a4b'
        # str(hex(get_mac())) '0xb827eb855a4b'
        # str(hex(get_mac()))[2:] 'b827eb855a4b'
        mac_addr = ''
        for i in range(0, 16):
            try:
                with open('/sys/class/net/%s/address' % interface) as f:
                    mac_addr = f.read()
                break
            except:
                mac_addr = "00:00:00:00:00:00"
            
            # ネット断状態から回復した際に、LANケーブルのmac_addressをとりたい。
            time.sleep(1)

        mac_addr = mac_addr[0:17]
        mac_addr = mac_addr.replace(':', '')

        return mac_addr

    def _get_device_ip_addr_raspi() -> str:
        ''' Get ip address of raspi'''

        cmd = f"/usr/bin/hostname -I"
        ret = PlatformRaspi.run_cmd(cmd)
        ret = ret.strip()
        return ret

    def _get_record_device_raspi():
        cmd = "/usr/bin/arecord -l"

        ret = PlatformRaspi.run_cmd(cmd)
        ret = ret.strip()

        if 'card 1:' in ret:
            return 'plughw:1,0'
        
        return 'plughw:0,0'

    # 録音用のデバイス名を返す（ラズパイ用）
    def _get_record_device_name_raspi() -> str:
        # USBデバイスの一覧を取得
        stdout = PlatformRaspi.run_cmd('/usr/bin/arecord -L')

        record_device = ''

        plughws = []
        for line in stdout.splitlines():
            if line.startswith('plughw:'):
                plughws.append(line)
        
        # もしUSBマイクが使用されていたら、USBマイクを使いたい
        #
        # plughw:CARD=sndrpigooglevoi,DEV=0
        # plughw:CARD=Device,DEV=0
        #    ↓
        # plughw:CARD=Device,DEV=0
        # plughw:CARD=sndrpigooglevoi,DEV=0
        plughws.sort()

        if len(plughws):
            record_device = plughws[0]

        return record_device
    
    def _get_record_command_list_raspi(record_wav_file_path: str, record_sec: int, device_name : str, rate: int = '22050', bit: str = '48k') -> list:

        commands = [
            '/usr/bin/arecord',
            '--device',
            device_name,
            '--channels',
            '1',
            '--format',
            'S16_LE',
            '--rate',
            str('22050'),
            '-d',
            str(record_sec),
            record_wav_file_path            
        ]

        return commands
    
    def reboot_raspi():
        check_call(['sudo', '/usr/sbin/reboot'])
        return
    
    # ラズパイのマイク感度を設定する (alsamixer相当)
    # gain 0 - 100
    def set_mic_gain_raspi(gain : int) -> bool:
        
        if gain < 0:
            gain = 0

        if gain > 100:
            gain = 100

        cmd = f"/usr/bin/amixer sset Capture {gain}%"
        stdout = PlatformRaspi.run_cmd(
            cmd=cmd,
            abort=True,
            ret='stdout'
        )
        is_success = f" [{gain}%] " in stdout

        if not is_success:
            raise ValueError(f"1981|set_mic_gain Failed cmd={cmd} stdout={stdout}")

        return True
    
    # ラズパイのマイク感度を取得する (alsamixer相当)
    # gain 0 - 100
    def get_mic_gain_raspi() -> int:
        cmd = f"/usr/bin/amixer sget Capture"
        stdout = PlatformRaspi.run_cmd(
            cmd=cmd,
            abort=True,
            ret='stdout'
        )

        val = -1
        # Mono: Capture 30480 [47%] [on]
        # から 47 をとる
        m = re.search(r'\[(\d+)\%\]', stdout)
        if m:
            val = m.group(1)

        return int(val)

    # マスター音量を設定する (alsamixer相当)
    # volume 0 - 100
    def set_master_volume_raspi(volume : int) -> str:
        if volume < 0:
            volume = 0

        if volume > 100:
            volume = 100

        cmd = f"/usr/bin/amixer sset Master {volume}%"
        stdout = PlatformRaspi.run_cmd(
            cmd=cmd,
            abort=True,
            ret='stdout'
        )
        is_success = f" [{volume}%] " in stdout

        if not is_success:
            raise ValueError(f"1982|set_master_volume Failed cmd={cmd} stdout={stdout}")

        return True

    # ラズパイのマスター音量を取得する (alsamixer相当)
    # playback 0 - 100
    def get_master_volume_raspi() -> int:

        cmd = f"/usr/bin/amixer sget Master"
        stdout = PlatformRaspi.run_cmd(
            cmd=cmd,
            abort=True,
            ret='stdout'
        )

        val = -1
        #   Front Left: Playback 62259 [95%] [on]
        # から 95 をとる
        m = re.search(r'\[(\d+)\%\]', stdout)
        if m:
            val = m.group(1)

        return int(val)

    # コマンドを実行する。
    def run_cmd(cmd, abort = True, ret = 'stdout'):
        res = subprocess.run(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if abort and res.returncode != 0:
            raise ValueError(f"1951|exec {cmd} failed: {res.stderr}")

        if ret == 'retcode':
            return res.returncode

        return res.stdout
    
    # USBマウントディレクトリを取得する。末尾の / はナシ
    def make_usb_drive_path_cmd() -> str:
        # /dev/sda1       30210144  609024  29601120   3% /media/pi/KIOXIA
        return "/usr/bin/df | /usr/bin/grep '/dev/sda1' | tail -1 | awk '{print $6}'"

    # USBマウントディレクトリの空き容量を取得する。末尾の / はナシ
    def get_usb_drive_usage_cmd() -> str:
        # /dev/sda1       30210144  609024  29601120   3% /media/pi/KIOXIA
        return "/usr/bin/df | /usr/bin/grep '/dev/sda1' | tail -1 | awk '{print $5}'"

    # overlayroot を解除する
    def disable_overlay_root():

        # overlayroot を解除する
        cmd = f"sudo /usr/bin/raspi-config nonint disable_overlayfs"
        stdout = PlatformRaspi.run_cmd(
            cmd=cmd,
            abort=True,
            ret='stdout'
        )

        if stdout:
            raise ValueError(f"1983|disable_overlay_root Failed cmd={cmd} stdout={stdout}")
        
        return

    # ネットワーク読み込みをし直す
    def reload_network_config():
        
        # ネットワークを一時遮断する
        cmd = f"sudo /usr/sbin/ifdown eth0"
        stdout = PlatformRaspi.run_cmd(
            cmd=cmd,
            abort=False,
            ret='stdout'
        )

        # ネットワークを復帰する
        cmd = f"sudo /usr/sbin/ifup eth0"
        stdout = PlatformRaspi.run_cmd(
            cmd=cmd,
            abort=False,
            ret='stdout'
        )

        return
    
    def get_uptime() -> float:
        with open('/proc/uptime', 'r') as f:
            # 11290.53 40841.10
            uptime_seconds = float(f.readline().split()[0])

        return uptime_seconds        

if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=False)
