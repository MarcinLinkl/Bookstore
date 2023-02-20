from tkinter import messagebox
import sqlite3
from tkinter import filedialog as fd
import pandas as pd

def read_Data_Img(IMG_Bool,*args):
	conn = sqlite3.connect('books.db')
	c = conn.cursor()

	sql_q="SELECT " +", ".join(args) +f" from books where IMG!={IMG_Bool}"
	
	rec =c.execute(sql_q).fetchall()
	conn.commit()
	conn.close()
	print(len(rec))
	return rec


def readData_by_rowId(id):
	conn = sqlite3.connect('books.db')
	c = conn.cursor()
	sql_q=f"SELECT * from books where rowid = {id}"
	rec =c.execute(sql_q).fetchall()
	conn.commit()
	conn.close()

	return rec
def readData(boolCheck=None,*args):
	conn = sqlite3.connect('books.db')
	c = conn.cursor()
	if len(args)==0 and boolCheck is not None :
		sql_q=f"SELECT * from books where Bool = {boolCheck}"
	elif len(args)==0:
		sql_q="SELECT * from books"
	elif boolCheck is not None:
		sql_q="SELECT " +", ".join(args) +f" from books where Bool={boolCheck}"
	else:
		sql_q="SELECT " +", ".join(args)+" from books"
	rec =c.execute(sql_q).fetchall()
	conn.commit()
	conn.close()
	print(len(rec))
	return rec

def updateData_IMG(data):
	try:
		conn = sqlite3.connect('books.db')
		# CREATE CURSOR
		c = conn.cursor()
		c.execute("UPDATE books SET IMG=? where Autor=? AND Tytuł=?", (data))
		conn.commit()
		conn.close()
	except Exception as e:
		stop_threads = True
		messagebox.showerror("Update error", f"{e}")

def updateData(data):

	try:
		conn = sqlite3.connect('books.db')
		# CREATE CURSOR
		c = conn.cursor()
		c.execute("UPDATE books SET IMG_link=?,Kategoria=?,Opis=?, Ocena=?,Głosy=?, Czytelnicy=?,Link=?,Autor_Link=?, Bool=? where Autor=? AND Tytuł=?", (data))
		conn.commit()
		conn.close()
	except Exception as e:
		stop_threads = True
		messagebox.showerror("Update error", f"{e}")



def make_new_DB():
	conn = sqlite3.connect('books.db')
	c = conn.cursor()
	c.execute("""CREATE TABLE IF NOT EXISTS
     books (
    Autor TEXT DEFAULT '',
    Tytuł TEXT DEFAULT '',
    Wydawnictwo TEXT DEFAULT '',
    Rok_wydania INTEGER DEFAULT '',
    Kategoria INTEGER DEFAULT '',
    Opis TEXT DEFAULT '',
    Czytelnicy INTEGER DEFAULT '',
    Ocena REAL DEFAULT '',
    Głosy INTEGER DEFAULT '',
    Link TEXT DEFAULT '',
    Autor_link TEXT DEFAULT '',
    Bool INTEGER DEFAULT 0,
    IMG INT DEFAULT 0,
    IMG_link TEXT DEFAULT ''
    )""")
	conn.commit()
	conn.close()

def add_to_DB(df):
	conn = sqlite3.connect('books.db')
	# CREATE CURSOR
	c = conn.cursor()

	try:
		for index, row in df.iterrows():
			c.execute("INSERT OR IGNORE INTO books (Autor, Tytuł, Wydawnictwo, Rok_wydania) VALUES (?,?,?,?)",
					  (row[0], row[1],row[2],row[3]))
	except Exception as e:
		messagebox.showerror("Error", str(e))
	else:
		books=c.execute("select COUNT(*) FROM books").fetchone()[0]

		messagebox.showinfo("Info",f"Poprawnie dodano! W bazie jest {books} rekordów")
	conn.commit()
	conn.close()

def addData():
	filename = fd.askopenfilename(
		title='Select a file',
		filetypes=(('xlsx files', '*.xlsx'), ('All files', '*.*')))
	if filename:
		try:
			df = pd.read_excel(filename,header=[0])
			add_to_DB(df)
			print(df)
		except ValueError:
			messagebox.showerror("Error",'File is invalid')
		except FileNotFoundError:
			messagebox.showerror(text="File Not Found")



def drop():
	re=messagebox.askyesno("UWAGA! Usunać bazę?","Wszystko trzeba będzie wgrać na nowo?")
	if re==True:

		conn = sqlite3.connect('books.db')
		# CREATE CURSOR
		c = conn.cursor()
		try:
			c.execute("DROP TABLE IF EXISTS books")
			messagebox.showinfo("Info", "Usununięto bazę!\nUtworzę nową")
			make_new_DB()

		except Exception as e:
			messagebox.showerror("Error", str(e))
		conn.commit()
		conn.close()
	else:
		pass



	
