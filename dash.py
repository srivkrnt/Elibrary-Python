from Tkinter import *
import sqlite3
from tkMessageBox import *

con = sqlite3.Connection('DB')
cur = con.cursor()

global generate_books
def create():
    cur.execute("create table if not exists login(username varchar(20) PRIMARY KEY, password varchar(20), name varchar(50))")
    cur.execute("create table if not exists books (book_id varchar(10) PRIMARY KEY, book_name varchar(20), link varchar(50),username varchar(20))")
    con.commit()


def create_admin():
    cur.execute("select * from login where username='admin'")
    status = cur.fetchall()
    if (len(status))==0:
        cur.execute("insert into login values ('admin', 'admin', 'Administrator')")
    else:
        flag=0

def sign_in(index_ui,username, password):
    try:
        cur.execute("select count(*) from login where username=? and password=?", (username, password))
    except:
        showerror('ERROR', 'SIGNIN FAILED')


    status = cur.fetchall()

    if status[0][0]==1:
        index_ui.destroy()
        dashboard(username)
    else:
        showerror('ERROR', 'SIGNING FAILED')


def details_ui(option,username):
    global generate_books
    generate_books()
    details_ui = Toplevel()
    details_ui.geometry("600x600+490+100")
    details_ui.resizable(0,0)
    bg = PhotoImage(file="images/windows_bg.gif")
    Label(details_ui, image=bg).place(x=0,y=0)
    
    Label(details_ui, text='Book ID: ', font='Helvetica 11 bold',bg='#34383C',fg='white', borderwidth=0).place(x=140, y=80)
    book_id = Entry(details_ui, font='Helvetica 11 bold', fg='#373E44')
    book_id.place(x=320, y=80)


    Label(details_ui, text='Book Name: ', font='Helvetica 11 bold',bg='#34383C',fg='white').place(x=140, y=110)
    book_name = Entry(details_ui, font='Helvetica 11 bold', fg='#373E44')
    book_name.place(x=320, y=110)

    Label(details_ui, text='Link: ', font='Helvetica 11 bold',bg='#34383C',fg='white').place(x=140, y=140)
    link = Entry(details_ui, font='Helvetica 11 bold', fg='#373E44')
    link.place(x=320, y=140)

    def insert_sql():
        try:
            cur.execute("insert into books values (?,?,?,?)",(book_id.get(), book_name.get(), link.get(),username))
            showinfo('Inserted', 'Values are inserted')
        except:
            showerror('ERROR', 'Insertion failed')
        con.commit()

    if(option=='insert'):
        Label(details_ui, text='Enter the Details ', borderwidth=0, bg='white',font=(12)).place(x=360, y=10)
        Button(details_ui, text='Insert', font='Helvetica 14 bold',bg='#373E44',fg='white',borderwidth=0, command=insert_sql).place(x=460, y=520)

    def update():
        try:
            cur.execute("update books set book_id=?, book_name=?, link=?",(book_id.get(), book_name.get(), link.get()))
            details_ui.destroy()
            showinfo('UPDATED', 'DATA UPDATED')
        except:
            showerror('ERROR', 'Failed to Update')
        con.commit()

    if(option=='update'):
        Label(details_ui, text='Enter Book ID to update', borderwidth=0, bg='white', font=(12)).place(x=324, y=10)
        Button(details_ui, text='Update', font='Helvetica 14 bold',bg='#373E44',fg='white',borderwidth=0, command=update).place(x=460, y=520)
        
    def view_sql(book_id,book_name,link):
        try:
            cur.execute("select * from books where book_id=?", [book_id.get()])
            details = cur.fetchall()[0]

            if(len(book_id.get())!=0):
               book_id.delete(0,END)
            book_id.insert(0, details[0])
            
            if(len(book_name.get())!=0):
                book_name.delete(0,END)
            book_name.insert(0,details[1])
            
            if(len(link.get())!=0):
                link.delete(0,END)
            link.insert(0,details[2])
            
        except:
            showerror('ERROR', 'Book record is not available for this ID')
    def download(link):
        link = link.get()
        import os
        os.system('start ' + link)
            
            
    if (option=='view'):
        Button(details_ui, text='VIEW', font='Helvetica 11 bold',bg='#373E44',fg='white',borderwidth=0, command=lambda:view_sql(book_id,book_name,link)).place(x=460 , y=520)
        Label(details_ui, text='Enter Book id only', borderwidth=0, bg='white',font=(12)).place(x=360, y=10)
        Button(details_ui, text="DOWNLOAD", font="Helvetica 11 bold", bg='#373E44', fg='white', borderwidth=0, command=lambda:download(link)).place(x=360,y=520)
    generate_books()
    details_ui.mainloop()

def create_acc():
    create_win = Toplevel()
    create_win.geometry("900x600+300+100")
    create_win.resizable(0,0)

    new_user_bg = PhotoImage(file="images/other_bg.gif")
    Label(create_win, image=new_user_bg).place(x=0, y=0)
    Label(create_win, text="CREATE AN ACCOUNT", font="Helvetica 15 bold", fg='white', bg='#34383C').place(x=331, y=60)

    username = Entry(create_win, font=(13))
    Label(create_win, text='Username', fg = '#34383C', bg='white', font='Helvetica 11 bold').place(x=300, y=160)

    password = Entry(create_win, font=(13))
    Label(create_win, text='Password', fg = '#34383C', bg='white',font='Helvetica 11 bold').place(x=300, y=260)

    name = Entry(create_win, font=(13))
    Label(create_win, text='Name', fg = '#34383C', bg='white', font='Helvetica 11 bold').place(x=300, y=360)


    username.place(x=300, y=200)
    password.place(x=300, y=300)
    name.place(x=300, y=400)


    Button(create_win, text=' '*20+' SUBMIT'+' '*22, bg='#00BC90', fg='#34383C',font='Helvetica 15' ,borderwidth=0, command=lambda:submit()).place(x=270, y=490)
    def submit():
        try:
            cur.execute("insert into login values(?,?,?)", (username.get(), password.get(), name.get()))
            showinfo("CREATED", "ACCOUNT CREATED, NOW YOU CAN LOG IN TO THE APPLICATION")
            con.commit()
        except:
            showerror("ERROR", "YOUR ACCOUNT IS PROBABLY ALREADY REGISTERED , TRY LOGGING IN AND IF THE PROBLEM PERSISTS SEE HELP MENU")


    create_win.mainloop()

def remove(item,username):
    global generate_books
    remove_ui = Toplevel()
    remove_ui.geometry("900x600+300+100")
    remove_ui.resizable(0,0)
    bg = PhotoImage(file="images/other_bg.gif")
    Label(remove_ui, image=bg).place(x=0,y=0)

    if item=='user':
        Label(remove_ui, text='Remove a User',font="times 15 bold", fg='white', bg='#34383C').place(x=364, y=60)
        Label(remove_ui, text='Username', fg = '#34383C', bg='white', font='Helvetica 18').place(x=382, y=280)
        to_remove = Entry(remove_ui, font=(13))
        to_remove.place(x=338, y=330)
        def execute_remove(to_remove):
            cur.execute("select * from login where username=?", [to_remove.get()])
            response = cur.fetchall()
            if len(response)!=0 and to_remove.get()!='admin':
                cur.execute("DELETE from login where username = ?",[to_remove.get()])
                con.commit()
            else:
                if to_remove.get()=='admin':
                    showerror("ERROR", "You can't delete your account")
                else:
                    showerror("ERROR", "User doesn't exist")
                    
    elif item=='book':
        Label(remove_ui, text='Remove a Book',font="times 15 bold", fg='white', bg='#34383C').place(x=364, y=60)
        Label(remove_ui, text='Book ID', fg = '#34383C', bg='white', font='Helvetica 18').place(x=382, y=280)
        to_remove = Entry(remove_ui, font=(13))
        to_remove.place(x=338, y=330)
        def execute_remove(to_remove):
            cur.execute("select * from books where book_id=?", [to_remove.get()])
            response = cur.fetchall()
            if len(response)!=0:
                if response[0][-1]==username or username=='admin':
                    cur.execute("DELETE from books where book_id=?",[to_remove.get()])
                    showinfo("DELETED", "Book is deleted successfully")
                else:
                    showerror("ERROR", "You dont own this book")
            else:
                showerror("ERROR", "Book doesn't exist")
            con.commit()
    Button(remove_ui, text=' '*20 + 'REMOVE' + ' '*20,bg='#F85661', fg='#34383C', font='Helvetica 15',command=lambda:execute_remove(to_remove)).place(x=270, y=490)
    con.commit()
    generate_books()
    remove_ui.mainloop()

def dashboard(username):
    global generate_books
    if username!="admin":
        dash_ui = Tk()
        dash_ui.geometry("900x600+300+100")
        dash_ui.resizable(0,0)
        bg = PhotoImage(file="images/dashboard_bg.gif")
        Label(dash_ui, relief="flat",image=bg).grid(row=0, column=0, rowspan=20, columnspan=20)

        user_bg = PhotoImage(file="images/user.gif")
        Label(dash_ui, image=user_bg,borderwidth=0).place(x=800 , y=6.5)

        logout = Button(dash_ui,bg='#16202C', borderwidth=0, command=lambda:dash_ui.destroy())
        logout_bg = PhotoImage(file="images/logout.gif")
        logout.config(image=logout_bg)
        logout.place(x=850, y=4)
        Label(dash_ui, text='DASHBOARD',fg='white',bg='#34383C', font='Helvetica 18 bold').place(x=420, y=10)
        Label(dash_ui, text='WELCOME '+username.upper() , bg='#34383C', fg='#0B8FCC', font = 'Helvetica 10 bold').place(x=45, y=50)

        add_bg = PhotoImage(file="images/plus.gif")
        Label(dash_ui, bg='#16202C', borderwidth=0, image=add_bg).place(x=10, y=105)
        Button(dash_ui, text='ADD BOOK', bg='#34383C', fg='#0B8FCC', font='4', borderwidth=0, command=lambda:details_ui('insert',username)).place(x=80, y=105)

        minus_bg = PhotoImage(file="images/minus.gif")
        Label(dash_ui, bg='#16202C', borderwidth=0,image=minus_bg).place(x=8.4,y=155)
        Button(dash_ui, text='REMOVE BOOK', bg='#34383C', fg='#0B8FCC', font='4', borderwidth=0, command=lambda:remove('book',username)).place(x=60, y=156)

        update_bg = PhotoImage(file="images/update.gif")
        Label(dash_ui, bg='#16202C', borderwidth=0,image=update_bg).place(x=8.4,y=205)
        Button(dash_ui, text='UPDATE BOOK', bg='#34383C', fg='#0B8FCC', font='4', borderwidth=0, command=lambda:details_ui('update',username)).place(x=60, y=207)

        view_bg = PhotoImage(file="images/view.gif")
        Label(dash_ui, bg='#16202C', borderwidth=0,image=view_bg).place(x=9.6,y=255)
        Button(dash_ui, text='VIEW BOOK', bg='#34383C', fg='#0B8FCC', font='4', borderwidth=0, command=lambda:details_ui('view',username)).place(x=72, y=258)
        
    else:
        dash_ui = Tk()
        dash_ui.geometry("900x600+300+100")
        dash_ui.resizable(0,0)
        bg = PhotoImage(file="images/dashboard_bg.gif")
        Label(dash_ui, relief="flat",image=bg).grid(row=0, column=0, rowspan=20, columnspan=20)

        user_bg = PhotoImage(file="images/user.gif")
        Label(dash_ui, image=user_bg,borderwidth=0).place(x=800 , y=6.5)

        logout = Button(dash_ui,bg='#16202C', borderwidth=0, command=lambda:dash_ui.destroy())
        logout_bg = PhotoImage(file="images/logout.gif")
        logout.config(image=logout_bg)
        logout.place(x=850, y=4)
        Label(dash_ui, text='DASHBOARD - ADMIN',fg='white',bg='#34383C', font='Helvetica 18 bold').place(x=390, y=10)
        Label(dash_ui, text='WELCOME '+username.upper() , bg='#34383C', fg='#0B8FCC', font = 'Helvetica 10 bold').place(x=45, y=50)

        add_bg = PhotoImage(file="images/plus.gif")
        Label(dash_ui, bg='#16202C', borderwidth=0, image=add_bg).place(x=10, y=105)
        Button(dash_ui, text='ADD BOOK', bg='#34383C', fg='#0B8FCC', font='4', borderwidth=0, command=lambda:details_ui('insert',username)).place(x=80, y=105)

        minus_bg = PhotoImage(file="images/minus.gif")
        Label(dash_ui, bg='#16202C', borderwidth=0,image=minus_bg).place(x=8.4,y=155)
        Button(dash_ui, text='REMOVE BOOK', bg='#34383C', fg='#0B8FCC', font='4', borderwidth=0, command=lambda:remove('book',username)).place(x=60, y=156)

        update_bg = PhotoImage(file="images/update.gif")
        Label(dash_ui, bg='#16202C', borderwidth=0,image=update_bg).place(x=8.4,y=205)
        Button(dash_ui, text='UPDATE BOOK', bg='#34383C', fg='#0B8FCC', font='4', borderwidth=0, command=lambda:details_ui('update',username)).place(x=60, y=207)

        view_bg = PhotoImage(file="images/view.gif")
        Label(dash_ui, bg='#16202C', borderwidth=0,image=view_bg).place(x=9.6,y=255)
        Button(dash_ui, text='VIEW BOOK', bg='#34383C', fg='#0B8FCC', font='4', borderwidth=0, command=lambda:details_ui('view',username)).place(x=72, y=258)
        
        Label(dash_ui, bg='#16202C', borderwidth=0,image=minus_bg).place(x=8.4,y=305)
        Button(dash_ui, text='REMOVE USER', bg='#34383C', fg='#0B8FCC', font='4', borderwidth=0, command=lambda:remove('user',username)).place(x=60, y=309)

        add_user = Button(dash_ui,borderwidth=0,bg='#16202C', command=create_acc)
        add_user_bg = PhotoImage(file="images/add_user.gif")
        add_user.config(image=add_user_bg)
        add_user.place(x=20, y=480)

    def generate_books():
        clean_bg = PhotoImage(file="images/clean_bg.gif")
        Label(dash_ui,bg='#ffffff',borderwidth=0,image=clean_bg).place(x=201,y=80)
        cur.execute("select * from books")
        all_books = cur.fetchall()
        Label(dash_ui,text='Book ID', font='Helvetica 15', bg='#ffffff').place(x=300,y=80)
        Label(dash_ui,text='Book Name', font='Helvetica 15', bg='#ffffff').place(x=450,y=80)
        Label(dash_ui,text='_'*90,font='Helvetica 15',bg='#ffffff').place(x=201,y=120)
        
        y_diff = 30
        x_diff = 190

        basex = 300
        basey = 130
        
        for book in all_books:
            basey = basey+y_diff
            Label(dash_ui, text=book[0], font='Helvetica 13', bg='#ffffff').place(x=basex,y=basey)
            Label(dash_ui, text=book[1], font='Helvetica 13', bg='#ffffff').place(x=basex+x_diff,y=basey)
    generate_books()
    dash_ui.mainloop()
