# Import required libraries
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from time import sleep
# Create an instance of tkinter window
import threading
from google_images_download import google_images_download
from sql import *


font = ("Comic Sans MS", 30, "bold")

global thread_stop
thread_stop = False
def scraper():

    def start_img_scrape():
        b1["state"] = "disabled"
        global thread_stop
        thread_stop = False
        value_label = ttk.Label(win, text="")
        value_label.pack(side=TOP, anchor=NW)
       


        mainLabel.config(text="start")
        query_set=read_Data_Img(1,"Autor","Tytuł","Wydawnictwo","Rok_wydania")
        response = google_images_download.googleimagesdownload()
        n_record=0
        for query in query_set:
            
            print(len(query_set))
            n_record+=1
            print(n_record)
            if thread_stop: break
            sentence =' '.join(map(str,query))
                 

            arguments = {"keywords": sentence, "limit": 1,
                         "print_urls": False}
            response.download(arguments)

            val=round(n_record/len(query_set)*100,4)

            my_progress["value"]=val
            value_label.config(text=f"Current Progress: {val}%  - {n_record}/{len(query_set)}")
            data=["1",query[0],query[1]]
            updateData_IMG(data)
        # return(paths)

    def stop_img_scrape():

        global thread_stop
        thread_stop=True

        print("stop")

        mainLabel.config(text="stop")
        b1["state"] ="normal"
    def quit():
        stop_img_scrape()
        win.destroy()


    win = Toplevel()
    win.title("Img scrapper")
    # Define the geometry of the window
    win.geometry("700x600")

    frame = Frame(win, width=600, height=400)
    frame.pack()
    frame.place(anchor='center', relx=0.5, rely=0.5)

    img = ImageTk.PhotoImage(Image.open("image/bk3.jpg"))

    # Create a Label Widget to display the text or Image on frame
    label = Label(frame, image=img)
    label.pack()
    text="Pobieraj obrazy"

    mainLabel=Label(win, text=text,font=font, background='#F5EAB2')
    mainLabel.place(relx=0.5, rely=0.2, anchor=CENTER)

    
    my_progress = ttk.Progressbar(win,orient=HORIZONTAL, length=300, mode='determinate')
    my_progress.place(relx=0.5, rely=0.3, anchor=CENTER)
    my_progress["value"] =0

    b1=Button(win, text='Start',font=font, bg="olive", highlightthickness=0, width=16, height=1, bd=0, command=lambda: threading.Thread(target=start_img_scrape).start())
    b1.place(relx=0.5, rely=0.4, anchor=CENTER)
    Button(win, text='Stop',font=font, bg="olive", highlightthickness=0, width=16, height=1, bd=0, command=stop_img_scrape).place(relx=0.5, rely=0.5, anchor=CENTER)

    Button(win, text='Quit',font=font, bg="olive", highlightthickness=0, width=16, height=1, bd=0, command=quit).place(relx=0.5,rely=0.7,anchor=CENTER)

    win.mainloop()
