import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

import img_scraper
from img_scraper import *
from view import view

ua = UserAgent()

font = ("Comic Sans MS", 60, "bold")

def update_window():
	def _dow_rest(link,headers):
		page = requests.get(link, headers)
		soup = BeautifulSoup(page.content, 'html.parser')
		_img = soup.find('img', class_='img-fluid')
		_kat = soup.find('a', class_='book__category d-sm-block d-none')
		_des = soup.find('div', class_='collapse-content')
		img=_img["src"]
		kat=_kat.get_text().strip()
		des=_des.get_text().strip().replace("\n\n"," ")
		print(img,kat,des)
		return img,kat,des
		
	def stop():
		global stop_threads
		stop_threads = True
		print("Stop Thread")
		headingLabel.config(text="STOP")
	
	def on_start_update():

		global stop_threads
		stop_threads=False

		nr_of_record = 0
		records = readData(False, "Autor", "Tytuł")
		text_label = ""
		def check_dziela_tom_nr(word):
				if word in ["Dzieła","Tom"]:
					return True
				elif len(word.lstrip("XVI"))==0:
					return True
				else:
					return False



		for record in records:
			if len(records)==0: 
				headingLabel.config(text="Wszystko jest pobrane")
				break

			nr_of_record += 1
			if stop_threads: break

			headingLabel.config(text=f"START {nr_of_record}/{len(records)}")

			new_query = "https://lubimyczytac.pl/szukaj/ksiazki?phrase="

			for word in record[1].split():
				if check_dziela_tom_nr(word)==False: 
					new_query+=f"%20{word}"
					
			

			print(new_query)
			headers = {"user-agent": ua.random}
			page = requests.get(new_query, headers)

			if page.status_code == 200:
				try:
					soup = BeautifulSoup(page.content, 'html.parser')
					subsoup=soup.find('div', class_ = 'authorAllBooks__single')
					_title= subsoup.find_all('a', class_ = 'authorAllBooks__singleTextTitle float-left')
					title=_title[0].get_text().strip("\n")
					title_link="https://lubimyczytac.pl"+_title[0]["href"]
					_autor = subsoup.find_all('div', class_ = 'authorAllBooks__singleTextAuthor authorAllBooks__singleTextAuthor--bottomMore')
					autor = _autor[0].get_text()
					autor_link = _autor[0].find("a",href=True)["href"]
					_stars = subsoup.find('span', class_ = 'listLibrary__ratingStarsNumber')
					stars=_stars.get_text().strip()
					_allRating = subsoup.find_all('div', class_ = 'listLibrary__ratingAll')
					allRating=_allRating[0].get_text().strip("\n ocen")
					_readers = subsoup.find_all('span', class_ = "ml-2 small grey")
					readers=_readers[0].get_text().strip("\nOpinie: ")
					print(title,title_link,autor,autor_link,stars,allRating,readers)
					img, kat, desc = _dow_rest(title_link, headers)
					data = [img, kat, desc,stars,allRating, readers,title_link,autor_link, 1,record[0], record[1]]
					text_label+=f"szukamy: "+", ".join({record[0], record[1]})+f" ocena: {stars} glosy: {allRating} czytelnicy: {readers} \n"
					updateData(data)
				except Exception as e:
					print("błąd ",record[:2], e)

					text_label+="Brak: "+", ".join({record[0], record[1]})+"\n"

					updateData(("","","", "", "", "", "", "", 1, record[0], record[1]))




			else:
				messagebox.showerror(f"Brak odpowiedzi ze strony! Spróbuj s...\n{page.status_code}")
				print(page.status_code)
			headingLabel2.config(text=text_label)

			my_progress["value"]=((nr_of_record/len(records)) *100)



	
	root = Tk()
	root.title("Library")
	root.geometry("600x500")
	headingLabel = Label(root, text='aktualizuj', fg='black', font = ('Courier',11))
	headingLabel.place(relx=0,rely=0,relwidth=1,relheight=0.1)
	headingLabel2 = Label(root, text='Ksiażki', fg='black', font = ('Courier',11))
	headingLabel2.place(relx=0,rely=0.1,relwidth=1,relheight=0.9)
	my_progress = ttk.Progressbar(root,orient=HORIZONTAL, length=400, mode='determinate')
	my_progress.pack(pady=170)
	my_progress["value"] =0
	b=Button(root, text='Start', command=lambda: threading.Thread(target=on_start_update).start())
	b.pack(padx=10)
	Button(root, text="Stop", command=stop).pack(padx=10)


	root.mainloop()

def	main():
	make_new_DB()
	root = Tk()
	root.title('Biblioteka')
	root.geometry('1100x800')
	bg = ImageTk.PhotoImage(Image.open("image/bk3.jpg"))
	canvas = Canvas(root)
	canvas.pack(fill='both', expand = True)
	canvas.create_image(
		0,
		0,
		image=bg,
		anchor = "nw"
	)

	canvas.create_text(
		250,
		150,
		text = 'Biblioteka',
		font=font
	)

	btn = Button(
		root,
		text = 'DODAJ KSIAŻKI Z PLIKU',
		command=addData,
		width=20,
		height=2,
		relief=SOLID,
		font=('arial', 18)
	)
	btn0 = Button(
		root,
		text = 'POKAŻ KSIĄŻKI',
		command=view,
		width=20,
		height=2,
		relief=SOLID,
		font=('arial', 18)
	)
	btn1 = Button(
		root,
		text = 'USUŃ BAZĘ DANYCH',
		command=drop,
		width=20,
		height=2,
		relief=SOLID,
		font=('arial', 18)
	)
	btn2 = Button(
		root,
		text = 'AKTUALIZUJ \n z lubimyczytać.pl',
		command=update_window,
		width=20,
		height=2,
		relief=SOLID,
		font=('arial', 18)
	)
	btn3 = Button(
		root,
		text = 'DODAJ OKŁADKI\n Z Google',
		command=img_scraper.scraper,
		width=20,
		height=3,
		relief=SOLID,
		font=('arial', 18)
	)
	btn_canvas = canvas.create_window(100,200,anchor = "nw",window = btn)
	btn_canvas = canvas.create_window(100,300,anchor = "nw",window = btn0)
	btn_canvas = canvas.create_window(100,400,anchor = "nw",window = btn1)
	btn_canvas = canvas.create_window(100,500,anchor = "nw",window = btn2)
	btn_canvas = canvas.create_window(100,600,anchor = "nw",window = btn3)


	root.mainloop()

if __name__ == '__main__':
	main()





