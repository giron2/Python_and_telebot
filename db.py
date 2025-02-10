import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
import json
from sqlalchemy import insert
import psycopg2
from sqlalchemy import select


conn = psycopg2.connect(database='eng', user="postgres", password="***")
Base = declarative_base()
DSN = f"postgresql://postgres:***@localhost:5432/eng"
class Pairs(Base): # Создание общего словаря
    __tablename__ = 'pairs'

    id = sq.Column(sq.Integer, primary_key=True)
    word = sq.Column(sq.String(length=60), unique=True, nullable=False)
    translat = sq.Column(sq.String(length=60), unique=True, nullable=False)

class Users(Base): # Создание таблицы пользователей
		__tablename__ = 'users'

		id = sq.Column(sq.Integer, primary_key=True)
		user_id = sq.Column(sq.String(length=60), unique=True, nullable=False)

def add_basic_data(): #Заполняем главную таблицу базовыми значениями
	with open('data.json', 'r', encoding="utf-8") as f:
		data = json.load(f)
		engine = sq.create_engine(DSN)
		Session = sessionmaker(bind=engine)
		session = Session()
		session.execute(
						insert(Pairs), data,)
		session.commit()

def create_user_table(conn, user_name): #Создание уникальной таблицы для конкретного пользователя
	cur = conn.cursor()
	cur.execute("""CREATE TABLE IF NOT EXISTS "%s"( 
	    id SERIAL  PRIMARY KEY,
	    word VARCHAR(30),
	    translat  VARCHAR(30));""", (user_name))
	conn.commit()

def add_user(conn, user_name): #Добавить пользователя в таблицу
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO users(user_id) VALUES(%s);
        """, (user_name))
    conn.commit()

def add_data_user_table(user, word, translat):#Добавляем слово
	word = tuple(word)
	translat = tuple(translat)
	cur = conn.cursor()
	cur.execute("""
	    SELECT * 
	    FROM "%s"
	    WHERE word = %s
	    ;
	    """,(user, word))
	p = cur.fetchone()
	if p==None:
		wd = tuple(word)
		cur = conn.cursor()
		cur.execute("""
		    INSERT INTO "%s"(word, translat) VALUES(%s, %s);
		    """, (user, word, translat))
		conn.commit()
	else:
		print('такое слово уже есть')
	conn.commit()

def del_data_user_table(user, word):#Удаляем слово
	word = tuple(word)
	cur = conn.cursor()
	cur.execute("""
	    SELECT * 
	    FROM "%s"
	    WHERE word = %s
	    ;
	    """,(user, word))
	p = cur.fetchone()
	if p!=None:
		wd = tuple(word)
		cur = conn.cursor()
		cur.execute("""
		    DELETE
		    FROM "%s"
		    WHERE word = %s;
		    """, (user, word))
		conn.commit()
		print(f'Слово: {list(word)} удалено')
	else:
		print('слово удалено или не существует')
	conn.commit()


def create_tables(engine):
	Base.metadata.drop_all(engine)
	Base.metadata.create_all(engine)

def create_class():
	engine = sq.create_engine(DSN)
	create_tables(engine)

	Session = sessionmaker(bind=engine)
	session = Session()

	session.close()



def check(us): #Проверяем существует ли пользователь, если нет, то создаем его
	uss = str(us)
	engine = sq.create_engine(DSN)
	Session = sessionmaker(bind=engine)
	with Session(bind=engine) as session:
		session.query(Users)
		u = session.query(Users).filter(Users.user_id == uss).all()
		if len(u) == 0:
			x = []
			x.append(us)
			add_user(conn, x)
			create_user_table(conn, x)
			print("Создался пользователь", uss)
		else:
			print("Пользователь", uss, "уже существует")
def select_user_words(user):
	cur = conn.cursor()
	cur.execute("""
			    SELECT word, translat
			    FROM "%s"
			    ;""", (user))
	conn.commit()
	a = cur.fetchall()
	return a
def select_words():
	cur = conn.cursor()
	cur.execute("""
			    SELECT word, translat
			    FROM pairs
			    ;""")
	conn.commit()
	a = cur.fetchall()
	return a


if __name__ == "__main__":
	create_class()
	add_basic_data()