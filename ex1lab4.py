
import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters
import pymysql

updater = Updater('759057057:AAFdDmr2PEbO6QSkvfhMf5KKqcIyPBrj0g8')
dispatcher = updater.dispatcher




def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="This is the Task_bot: commands supported are\n/showTasks\n/newTask <task to add>\n/removeTask <task to remove>\n/removeAllTasks <substring to use to remove all the tasks that contain it>")


def showTasks(bot, update):
    sql = "SELECT  todo  FROM task_1 order by todo"
    conn = pymysql.connect(user='root', password='MarcoVinai97', host='localhost', database='tasks')
    cursor = conn.cursor()
    cursor.execute(sql)
    res = cursor.fetchall()
    if res.__len__() == 0:
        bot.send_message(chat_id=update.message.chat_id, text="nothing to do here!")
    else:
        for elem in res:
            bot.send_message(chat_id=update.message.chat_id, text=elem[0])
    cursor.close()
    conn.commit()
    conn.close()


def newTask(bot, update, args):
    task = ' '.join(args)
    sql = "INSERT INTO task_1 (id_task, todo) values (%s, %s)"
    sql2 = "SELECT COUNT(*) from task_1"
    conn = pymysql.connect(user='root', password='MarcoVinai97', host='localhost', database='tasks')
    cursor = conn.cursor()
    cursor.execute(sql2)
    n = cursor.fetchone()
    cursor. execute(sql, (n[0], task))
    bot.send_message(chat_id=update.message.chat_id, text="new task added!")
    cursor.close()
    conn.commit()
    conn.close()


def removeTask(bot, update, args):
    task = ' '.join(args)
    sql1 = "SELECT * FROM task_1 WHERE todo = %s"
    sql2 = "DELETE FROM task_1 WHERE todo = %s and id_task = %s"
    conn = pymysql.connect(user='root', password='MarcoVinai97', host='localhost', database='tasks')
    cursor = conn.cursor()
    cursor.execute(sql1, ("task",))
    a = cursor.fetchone()
    if a == "none":
        bot.send_message(chat_id=update.message.chat_id, text="task not found!")
    else:
        cursor.execute(sql2, (task,a[0]))
        bot.send_message(chat_id=update.message.chat_id, text="task correctly deleted!")
    cursor.close()
    conn.commit()
    conn.close()


def removeAllTasks(bot, update, args):
    t = ' '.join(args)
    t = "%" + t + "%"
    sql1 = "SELECT * FROM task_1 WHERE todo LIKE %s"
    sql2 = "DELETE FROM task_1 WHERE todo LIKE %s "
    conn = pymysql.connect(user='root', password='MarcoVinai97', host='localhost', database='tasks')
    cursor = conn.cursor()
    cursor2 = conn.cursor()
    cursor.execute(sql1, (t,))
    a = cursor.fetchall()
    if a == "none":
        bot.send_message(chat_id=update.message.chat_id, text="task not found!")
    else:
        cursor2.execute(sql2, (t,))
    for elem in a:
        testo = "deleted " + elem[1]
        bot.send_message(chat_id=update.message.chat_id, text=testo)
    cursor.close()
    cursor2.close()
    conn.commit()
    conn.close()


def echo(bot, update):
    receivedText = update.message.text
    textToSend = "I'm sorry, I can't do that"
    bot.sendMessage(chat_id=update.message.chat_id, text=textToSend)

dispatcher.add_handler(CommandHandler('start', start))

showTask_handler = dispatcher.add_handler(CommandHandler('showTasks', showTasks))
dispatcher.add_handler(showTask_handler)

newTask_handler = dispatcher.add_handler(CommandHandler('newTask', newTask, pass_args=True))
dispatcher.add_handler(newTask_handler)

removeTask_handler = dispatcher.add_handler(CommandHandler('removeTask', removeTask, pass_args=True))
dispatcher.add_handler(removeTask_handler)

removeAllTask_handler = dispatcher.add_handler(CommandHandler('removeAllTasks', removeAllTasks, pass_args=True))
dispatcher.add_handler(removeAllTask_handler)

dispatcher.add_handler(MessageHandler(Filters.text, echo))

updater.start_polling()
updater.idle()

