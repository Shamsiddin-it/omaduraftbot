import telebot
from telebot import types
from telebot.types import ReplyKeyboardMarkup
from context import *
from datetime import datetime

create_db_user()
create_db_come()

@bot.message_handler(commands = ['start'])
def handler(message):
    btn1 = types.InlineKeyboardButton("add_student")
    btn2 = types.InlineKeyboardButton("come")
    btn3 = types.InlineKeyboardButton("left")
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.row(btn1)
    markup.row(btn2,btn3)
    bot.send_message(message.chat.id, "Salom xush omaded ba attendence bot!",reply_markup=markup)
    bot.register_next_step_handler(message,m_handler)


@bot.message_handler()
def m_handler(message):
    if message.text == "add_student":
        bot.send_message(message.chat.id,"Enter full name of student: ")
        bot.register_next_step_handler(message,name)
    elif message.text == "come":
        bot.send_message(message.chat.id,"Enter student id to regist his come!")
        bot.register_next_step_handler(message,comer)
    elif message.text == "left":
        bot.send_message(message.chat.id, "Enter students id to reg his left!")
        bot.register_next_step_handler(message,lefter)


@bot.message_handler()
def lefter(message):
    id1 = message.text
    today = datetime.now().date()
    conn = open_connection()
    cur = conn.cursor()
    cur.execute(f"select user_id from come where user_id = {id1} and c_time = '{today}' and status = 'left'")
    a = cur.fetchone()
    if a!=None:
        bot.send_message(message.chat.id, "This student is already left!")
        bot.register_next_step_handler(message,m_handler)
    else:
        cur.execute(f"""insert into come(user_id,st_name,status) values(
                    (select id from students where id={id1}),
                    (select full_name from students where id={id1}),
                    'left')""")
        conn.commit()
        bot.send_message(message.chat.id, "Student's left registered!")
    close_connection(conn,cur)
    bot.register_next_step_handler(message,m_handler)


@bot.message_handler()
def comer(message):
    id1 = message.text
    today = datetime.now().date()
    conn = open_connection()
    cur = conn.cursor()
    cur.execute(f"select user_id from come where user_id = {id1} and c_time = '{today}' and status = 'come'")
    a = cur.fetchone()
    if a!=None:
        bot.send_message(message.chat.id, "This student is already here!")
        bot.register_next_step_handler(message,m_handler)
    else:
        cur.execute(f"""insert into come(user_id,st_name,status) values(
                    (select id from students where id={id1}),
                    (select full_name from students where id={id1}),
                    'come')""")
        conn.commit()
        bot.send_message(message.chat.id, "Student's come registered!")
    close_connection(conn,cur)
    bot.register_next_step_handler(message,m_handler)

def name(message):
    global f_name
    f_name = message.text
    bot.send_message(message.chat.id, "Enter course that student wanna study!")
    bot.register_next_step_handler(message,course)

def course(message):
    global course_n
    course_n = message.text
    bot.send_message(message.chat.id,"Enter student phone number")
    bot.register_next_step_handler(message,adder)

@bot.message_handler()
def adder(message):
    phone = message.text
    conn = open_connection()
    cur = conn.cursor()
    cur.execute("insert into students(full_name,course,phone_number) values(%s,%s,%s)", (f_name,course_n,phone))
    conn.commit()
    close_connection(conn,cur)
    bot.send_message(message.chat.id,"Student added successfuly!")
    bot.register_next_step_handler(message,m_handler)

bot.infinity_polling()