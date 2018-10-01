from sopel import module
from datetime import datetime
from pymysql import connect, cursors
from configparser import ConfigParser

@module.rule('.*')
@module.event('JOIN')
def join(bot, trigger):
    __log(trigger.nick, trigger.host, trigger.raw, 'join')

@module.rule('.*')
@module.event('PART')
def quit(bot, trigger):
    __log(trigger.nick, trigger.host, trigger.raw, 'part')

def __log(nick, host, raw, event):
    now = datetime.now()
    config = ConfigParser()
    config.read('config.ini')
    mysql = config['mysql']
    connection = connect(host=mysql['host'],
                   user=mysql['user'],
                   password=mysql['password'],
                   db=mysql['db'])
    sql = 'INSERT INTO events(nick, host, raw, event, created) VALUES(%s, %s, %s, %s, STR_TO_DATE(%s, %s))'
    sql_datetime_format = "%Y-%m-%d %H:%i:%s"
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql, (nick, host, raw, event, now.strftime("%Y-%m-%d %H:%M:%S"), sql_datetime_format))

        connection.commit()
    finally:
        connection.close()