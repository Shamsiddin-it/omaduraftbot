import psycopg2
from secret import *
import telebot

def open_connection():
    conn = psycopg2.connect(database = 'omaduraft',
                            user = 'postgres',
                            host = 'localhost',
                            password = passw,
                             port = 5432 )
    return conn
def close_connection(conn,cur):
    conn.close()
    cur.close()

bot = telebot.TeleBot(API_KEY)

def create_db_user():
    conn = open_connection()
    cur = conn.cursor()
    cur.execute(f"""create table if not exists students(
                id serial primary key,
                full_name varchar(100),
                course varchar(20),
                phone_number varchar(13));""")
    conn.commit()
    close_connection(conn,cur)

def create_db_come():
    conn = open_connection()
    cur = conn.cursor()
    cur.execute(f"""create table if not exists come(
                user_id int references students(id),
                st_name varchar(100),
                status varchar(10),
                c_time date default current_date);""")
    conn.commit()
    close_connection(conn,cur)

    