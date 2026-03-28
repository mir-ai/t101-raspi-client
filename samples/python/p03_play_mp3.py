#!/usr/bin/python3
# coding: utf-8

import pygame
import os
import sys
import time
import traceback
from gpiozero import LED

def main(argvs):

    PIN_AUX_OUT="GPIO25"

    # スピーカーをONにする
    aux_device = LED(PIN_AUX_OUT)
    aux_device.on()

    # Pygameを使ってサウンドを再生する
    mp3_path = '../mp3/test_500hz.mp3'

    # 参考
    # Pythonで音を鳴らす(pygame)
    # https://qiita.com/week/items/ab190474eeb7c1fe9fc2

    # pygame.mixer.music
    # ストリーミング再生を操作するpygameモジュールです
    # https://westplain.sakura.ne.jp/translate/pygame/Music.cgi

    try:
        # 初期化
        pygame.mixer.init(frequency=22050,channels=1,buffer=3072)

    except pygame.error:
        # エラーの場合
        print(f"Pygame init pygame error")
        return '2031'

    except Exception as e:
        # エラーの場合
        print(f"Pygame init exception: {e}")
        return '2032'

    try:
        # MP3ファイルを読み込み
        pygame.mixer.music.load(mp3_path)

        # ボリュームをセット(0-1)
        pygame.mixer.music.set_volume(1)

        # 再生スタート
        pygame.mixer.music.play(loops = 1, start = 0.0)

        # バックグラウンドで再生される

    except pygame.error:
        # エラーの場合
        print(f"pygame.mixer.music {mp3_path} pygame error")
        return '2033'

    except Exception as e:
        # エラーの場合
        print(f"pygame.mixer.music {mp3_path} exception: {e}")
        return '2034'

    # まだ再生中かどうかを確認
    while pygame.mixer.music.get_busy():
        try:
            # 再生中。しばらく待つ。
            print ('Playing...')
            time.sleep(1)
        except Exception as e:
            # エラー発生
            print(f"Pygame is_playing exception: {e}")
            pass

    try:
        if pygame.mixer.get_init():
            # 再生終了
            pygame.mixer.music.stop()
            pygame.mixer.quit()

    except pygame.error:
        print(f"Pygame pygame.mixer.music.stop failed")
        pass

    except Exception as e:
        print(f"Pygame pygame.mixer.music.stop failed")
        pass

    # スピーカーをOFFにする
    aux_device.off()

if __name__ == "__main__":
    main(sys.argv[1:])
