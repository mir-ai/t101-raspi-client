#!/usr/bin/python3
# coding: utf-8

import sqlite3
import time
import threading
import sys

# log_code 3600
# Sqlite という軽量のSQLサーバを使用して
# 音源再生の状態を管理する

class SqliteDb:

    sqlite_lock = threading.Lock()
    dbname = ''
    conn = None

    # sqlite 接続
    def connect():

        # 再入防止
        if SqliteDb.dbname:
            # 既にsqliteへの接続があったら、
            if SqliteDb.conn:
                # 現状のコネクションを返す
                return SqliteDb.conn

        SqliteDb.dbname = f"/tmp/sql_t101_raspi_client.sqlite3"

        with SqliteDb.sqlite_lock:
            # このあたりは職人芸で調整
            # 複数スレッドからの同時アクセス時に競合しないように調整
            SqliteDb.conn = sqlite3.connect(
                SqliteDb.dbname,
                isolation_level=None, # Auto Commit
                # autocommit=True, # Auto Commit
                check_same_thread=False, # 操作毎に直列ロックするので、マルチスレッドでの実行を許容する。
                timeout=7.0
            )
            SqliteDb.conn.row_factory = sqlite3.Row

            return SqliteDb.conn

    # テーブルを削除する。テーブル構造が変更になった場合に備えて起動時に毎回呼び出す
    def drop_table():

        with SqliteDb.sqlite_lock:
            cur = SqliteDb.conn.cursor()

            # playlists テーブル　削除
            cur.execute(
                (
                    'DROP TABLE IF EXISTS playlists'
                )
            )

            cur.close()

    # テーブルを作成する。
    def create_table():

        with SqliteDb.sqlite_lock:

            cur = SqliteDb.conn.cursor()

            # playlists テーブル　作成
            cur.execute(
                (
                    'CREATE TABLE IF NOT EXISTS playlists ('

                    # 配信システム側でのメッセージID
                    '    message_id INTEGER PRIMARY KEY '

                    # 放送音源のパス
                    '    , audio_path TEXT NOT NULL'

                    # 放送ステータス。
                    # ['0' => '未処理', '70' => '再生開始', '100' => '再生完了']
                    '    , play_status INTEGER DEFAULT 0'

                    ')'
                )
            )

            cur.close()

    # ローカルプレイリストの追加・更新
    # プレイリストで毎回上書きされるので、ステータスは更新しない
    def playlist_upsert(
        message_id: int,
        audio_path: str,
    ):

        with SqliteDb.sqlite_lock:
            cur = SqliteDb.conn.cursor()

            cur.execute(
                '''
                INSERT INTO playlists (
                    message_id
                    , play_status
                    , audio_path
                ) VALUES (
                    :message_id
                    , 0
                    , :audio_path
                ) ON CONFLICT (message_id) DO UPDATE SET
                    message_id = :message_id
                    , audio_path = :audio_path
                ''',
                {
                    "message_id": message_id
                    , "audio_path": audio_path
                }
            )
            
            cur.close()

    # プレイリスト処理開始
    def playlist_update_process_new(message_id: int):

        with SqliteDb.sqlite_lock:
            cur = SqliteDb.conn.cursor()

            cur.execute(
                '''
                UPDATE
                    playlists
                SET
                    play_status = 10
                WHERE
                    message_id = :message_id
                ''',
                {
                    "message_id": message_id
                }
            )

            cur.close()

        return

    # プレイリスト再生開始
    def playlist_play_start(message_id: int):

        with SqliteDb.sqlite_lock:
            cur = SqliteDb.conn.cursor()

            cur.execute(
                '''
                UPDATE
                    playlists
                SET
                    play_status = 70
                WHERE
                    message_id = :message_id
                ''',
                {
                    "message_id": message_id
                }
            )

            cur.close()

        return

    # プレイリスト再生完了
    def playlist_play_complete(message_id: int):

        with SqliteDb.sqlite_lock:
            cur = SqliteDb.conn.cursor()

            cur.execute(
                '''
                UPDATE
                    playlists
                SET
                    play_status = 100
                WHERE
                    message_id = :message_id
                ''',
                {
                    "message_id": message_id
                }
            )

            cur.close()

        return

    # プレイリストエラー
    def playlist_error(message_id: int):

        with SqliteDb.sqlite_lock:
            cur = SqliteDb.conn.cursor()

            cur.execute(
                '''
                UPDATE
                    playlists
                SET
                    play_status = 999
                WHERE
                    message_id = :message_id
                    and play_status < 999
                ''',
                {
                    "message_id": int(message_id)
                }
            )

            cur.close()

        return
        
    # 指定したステータスのプレイリストを選択する。
    def playlists_select_by_status(play_status: int) -> list:

        with SqliteDb.sqlite_lock:

            cur = SqliteDb.conn.cursor()
            cur_unixtime = int(time.time())
            
            res = cur.execute(
                '''
                SELECT
                    *
                FROM
                    playlists
                WHERE
                    play_status = :play_status
                ''',
                {
                    "play_status": play_status
                }
            )

            playlists = res.fetchall()

            cur.close()

        return playlists
        
    # メッセージを１件取得する。
    def playlist_select_by_message_id(message_id: int) -> list:

        with SqliteDb.sqlite_lock:

            cur = SqliteDb.conn.cursor()

            res = cur.execute(
                '''
                SELECT
                    *
                FROM
                    playlists
                WHERE
                    message_id = :message_id
                ''',
                {
                    "message_id": message_id
                }
            )

            playlist = res.fetchone()

            cur.close()

        return playlist
                
    # プレイリストを取得する
    def playlists_select():

        with SqliteDb.sqlite_lock:

            cur = SqliteDb.conn.cursor()

            res = cur.execute(
                '''
                SELECT
                    *
                FROM
                    playlists
                ORDER BY
                    message_id
                '''
            )

            playlists = res.fetchall()

            cur.close()

        return playlists

def main(argv):
    db_conn = SqliteDb.connect()
    SqliteDb.drop_table()
    SqliteDb.create_table()
    SqliteDb.playlist_upsert(1, 'good_morning.mp3')
    SqliteDb.playlist_upsert(2, 'good_afternoon.mp3')
    SqliteDb.playlist_upsert(3, 'good_night.mp3')

    SqliteDb.playlist_play_start(1)
    SqliteDb.playlist_play_complete(2)
    SqliteDb.playlist_error(3)

    print (f"Sqllite playlist table'")


    playlists = SqliteDb.playlists_select()
    for playlist in playlists:
        message_id = playlist['message_id']
        audio_path = playlist['audio_path']
        play_status = playlist['play_status']

        print (f"message_id={message_id}, audio_path='{audio_path}', play_status='{play_status}'")

if __name__ == "__main__":
    main(sys.argv[1:])
