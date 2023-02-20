import os
from tkinter import *
import sqlite3
from PIL import ImageTk,Image #PIL -> Pillow
from sql import *
from tkinter import ttk
font = ("Copperplate", 11)
font2 = ("Copperplate", 15)
font1 = ("Copperplate", 10)



def open_new_win(item):

    new_win = Toplevel()
    new_win.title("Img book")
    new_win.geometry("1220x740")
    frame_img = Frame(new_win, width=500, height= 420, bg='grey')
    frame_img.grid(rowspan=2, column=0, padx=25, pady=25)
    frame_text_t = Frame(new_win, width=500, height=90, bg='grey')
    frame_text_t.grid(row=0, column=1, padx=70, pady=25)
    frame_text_des = Frame(new_win, width=500, height=320, bg='grey')
    frame_text_des.grid(row=1, column=1, padx=70, pady=0)
    def return_img(basehight = 400):
        path=f"./downloads/{item[0]} {item[1]} {item[2]} {item[3]}/"
        # prefixed gives filenames started with certain string in catalog
        prefixed = [filename for filename in os.listdir(path) if filename.startswith(str(item[12]))]
        full_path=path+prefixed[0]
        img=Image.open(full_path)

        # determining the height ratio
        hpercent = (basehight/float(img.size[1]))
        wsize = int((float(img.size[0])*float(hpercent)))
        img = img.resize((wsize,basehight),  Image.Resampling.LANCZOS)
        # resize image
        img = ImageTk.PhotoImage(img)
        return img

    try:
        img=return_img()
        Label(frame_img,image=img ,relief=RAISED).grid(row=0, column=0, padx=10, pady=10)
   
    except Exception as e:
        print(e)  

    text=f"{item[0]}\n{item[1]}\nOcena: {item[7]}\nGlosy: {item[8]}\nCzytelnicy: {item[6]}" 
    Label(frame_text_t, text=text,font=font2,justify=LEFT).grid(row=0, column=0, padx=5, pady=5)
    
    scroll = Scrollbar(frame_text_des)
    scroll.pack(side=RIGHT, fill=Y)
    text_widget = Text(frame_text_des,font=font1, wrap=WORD,height=15,width=40, yscrollcommand=scroll.set)
    text_widget.insert(END,f"{item[5]}")
    text_widget.pack()

    # Configure the scrollbars
    scroll.config(command=text_widget.yview)
   

    text_widget.bind('<KeyPress>', lambda e: 'break')
    new_win.mainloop()



    




def view():
    root = Tk()
    root.title("Library")
    # root.minsize(width=500,height=700)
    root.geometry("1200x700")
    getHeader ="PRAGMA table_info('books');"
    con = sqlite3.connect('books.db')
    cur = con.cursor()
    headers_exe=cur.execute(getHeader)
    headers=tuple([x[1] for x in headers_exe])
    style= ttk.Style()
    style.theme_use('default')
    style.configure('Treeview',
        background='#D3D3D3',
        font=font,
        foregound='black',
        rowheight=21,
        fieldbackground='#D3D3D3')
    style.map('Treeview',
        background=[('selected',"#0C7780")])
    my_tree_frame = Frame(root)
    my_tree_frame.pack(side=BOTTOM,fill="both",expand=True)
    my_tree_scroll = Scrollbar(my_tree_frame)
    my_tree_scroll_2 = Scrollbar(my_tree_frame,orient="horizontal")
    my_tree_scroll.pack(side=RIGHT,fill=Y)
    my_tree_scroll_2.pack(side=BOTTOM,fill=X)
    my_tree=ttk.Treeview(my_tree_frame, yscrollcommand = my_tree_scroll.set,xscrollcommand = my_tree_scroll_2.set,selectmode="extended")
    my_tree.pack(fill="both",expand=True)
    my_tree_scroll.config(command=my_tree.yview)
    my_tree_scroll_2.config(command=my_tree.xview)
    my_tree['columns'] = headers
    my_tree.column("#0",width=0, stretch=NO)
    my_tree.heading("#0",text="", anchor=W)
    for x in headers:
        my_tree.column(x, anchor=W, width=170)
        my_tree.heading(x, text=x,anchor=W)
   
    my_tree.tag_configure('color', background='#AAD5FF')
    global count
    count=0
    getBooks = "select * from books"
    recs=cur.execute(getBooks)
    for rec in recs:
        my_tree.insert(parent="", index='end', iid=count,text='', values=(rec), tags=('color',))
        count+=1
        # sortownaie
    def treeview_sort_column(tv, col, reverse):
        l = [(tv.set(k, col), k) for k in tv.get_children('')]
        try:
            if reverse==False:
                l.sort(reverse=reverse, key=lambda t: float(t[0]) if t[0] else float("inf"))
            else:
                l.sort(reverse=reverse, key=lambda t: float(t[0]) if t[0] else 0 )
        except ValueError as e:
            l.sort(reverse=reverse)

        # rearrange items in sorted positions
        for index, (val, k) in enumerate(l):
            tv.move(k, '', index)
        # reverse sort next time
        tv.heading(col, command=lambda _col=col: treeview_sort_column(tv, _col, not reverse))

    for col in headers:
        my_tree.heading(col, text=col,command=lambda _col=col: treeview_sort_column(my_tree, _col, False))
    my_tree.pack()
    con.commit()
    con.close()

    def OnDoubleClick(event):
        item = my_tree.identify('item', event.x, event.y)
        print("you clicked on", item )
        open_new_win(my_tree.item(item)["values"])
        # rowid is not the same as "item" from treeview - in treeview start with 0

    my_tree.bind("<Double-1>", OnDoubleClick)


   
    root.mainloop()

