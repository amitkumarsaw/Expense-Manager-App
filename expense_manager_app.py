from tkinter import *
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.ttk import Notebook, Treeview
from tkcalendar import *
import sqlite3



def main_screen():
    gui = Tk()
    gui.title('Expense and Income Manager')
    gui.geometry('700x570')
    gui.resizable(0, 0)

    # def login_window():
    #     login_screen = Tk()
    #     login_screen.title(" LOGIN WINDOW ")
    #     login_screen.geometry('200x200')
    #     login_label = Label(login_window, "Please enter your login details")


    # styling tab text
    s = ttk.Style()
    s.configure('TNotebook.Tab', font=('Comic Sans MS','10','bold'))

    # creating tabs
    tab = Notebook(gui)
    tab.pack(padx = 10, pady=10)

    # creating frames for tabs
    frame1 = Frame(tab, width=800, height=400)
    frame1.pack(fill = "both", expand = 1)
    frame2 = Frame(tab, width=800, height=400, bg="ivory3")
    frame2.pack(fill = "both", expand = 1)

    # adding frames to the tabs
    tab.add(frame1, text = " Expense ")
    tab.add(frame2, text = " Search / Edit / Delete ")

    # frames in frame 1
    f1 = Frame(frame1, width=800, height=200, bg="ivory3")
    f1.pack(fill="both", expand=1)
    f2 = Frame(frame1, width=800, height=200, bg="ivory3")
    f2.pack(fill="both", expand=1)

    # frames in frame 2
    f3 = Frame(frame2, width=800, height=200, bg="light grey")
    f3.pack(fill="both", expand=1)
    f4 = Frame(frame2, width=800, height=200, bg="light grey")
    f4.pack(fill="both", expand=1)

    # frames inside f4
    f4_1 = Frame(f4, width=800, height=200, bg="light grey")
    f4_1.grid(row=0, column=0)
    f4_2 = Frame(f4, width=800, height=200, bg="light grey")
    f4_2.grid(row=1, column=0)

    # ---------- variables -----------
    date = StringVar()
    title = StringVar()
    expense = StringVar()
    variable = StringVar()


    #------------------------------------- database stuff -----------------------------------

    # -------------- functions ----------------------
    # create table
    def create_table():
        connect = sqlite3.connect("expense.db")
        cursor = connect.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS expense_table(
                    date text,
                    title text,
                    expense real)""")
        connect.commit()

    create_table()



    # --------------------------------- tabe 1 (frame1) --------------------------------------
    def main_window1_tab1():
        # open a new window on a click to "show all" button
        def open_New_Window():
            new_Window = Toplevel(f1)
            new_Window.title("ALL THE STORED RECORDS UNTIL NOW")
            new_Window.geometry("690x540")

            # frame for the new opened window
            frame_new = Frame(new_Window, bg="light grey")
            frame_new.pack(fill="both", expand=1, padx=10, pady=10)  

            # ctreate a tree view in the new opened window
            tree_view_new = ttk.Treeview(frame_new, columns=(1, 2, 3), show="headings", height="20")
            tree_view_new.grid(row=0, column=0, padx=30, pady=10, sticky='w')

            tree_view_new.heading('#1', text="D A T E")
            tree_view_new.heading('#2', text="T I T L E")
            tree_view_new.heading('#3', text="E X P E N S E")

            # scrollbar for the tree_view_new
            scrollbar_new = ttk.Scrollbar(frame_new, orient=VERTICAL, command=tree_view_new.yview)
            tree_view_new.configure(yscrollcommand=scrollbar_new.set)
            scrollbar_new.grid(row=0, column=0, sticky=S + E + N)


            connect = sqlite3.connect("expense.db")
            cursor = connect.cursor() 
            cursor.execute("SELECT * FROM expense_table")
            rows = cursor.fetchall()     # fetching all the contents of the tabe to insert in the new window tree view
            connect.commit() 
            # inserts all the contents of the table into the tree_view_new
            for row in rows:
                print(row) # it print all records in the database
                tree_view_new.insert('', 'end', values=row)
                
                    # function to delete every record
            def delete_all():
                connect = sqlite3.connect("expense.db")
                cursor = connect.cursor()

                # warning window for delete all button 
                MsgBox = messagebox.askquestion ('DELETE EVERYTHING','Are you sure you want to delete all the contents of the table !!',icon = 'warning')
                if MsgBox == 'yes':
                    cursor.execute("DELETE FROM expense_table")     # delete the contents of the table
                    connect.commit()
                    new_Window.destroy()
                else:
                    messagebox.showinfo('Return','You will now return to the application screen')

                # delete the contents of tree_view (in the first tab)
                x = tree_view.get_children()
                for item in x:
                    tree_view.delete(item)

            # create a button to delete everything
            button_delete_all = Button(frame_new, text=' DELETE ALL ', font=(None, 12, 'bold'), border=6, command=delete_all, bg="indian red")
            button_delete_all.grid(row=1, column=0, padx=40, pady=15)


        # insert data into the table and treeview
        def insert():
            connect = sqlite3.connect("expense.db")
            cursor = connect.cursor()

            date = e_date.get()
            title = e_title.get()
            expense = e_expense.get()
            cursor.execute("INSERT INTO expense_table VALUES (?, ?, ?)", (date, title, expense))

            tree_view.insert('', 'end', values=(date, title, expense))
            connect.commit()

            e_title.delete(0, END)   # to clear the title entry box
            e_expense.delete(0, END)   # to clear the expense entry box


        # -----row 0, date entry-----
        l_date = ttk.Label(f1, text='DATE : ', font=(None, 13, 'bold'), background="ivory3")
        l_date.grid(row=0, column=0, padx=20, pady=20, sticky='w')

        e_date = DateEntry(f1, width=10, font=(None, 13, 'bold'),  textvariable=date)
        e_date.grid(row=0, column=1, padx=50, pady=20, sticky='w')

        # -----row 1, title entry-----
        l_title = ttk.Label(f1, text='TITLE : ', font=(None, 13, 'bold'), background="ivory3")
        l_title.grid(row=1, column=0, padx=20, pady=5, sticky='w')

        e_title = ttk.Entry(f1, width=20, font=(None, 13, 'bold'), textvariable=title)
        e_title.grid(row=1, column=1, padx=50, pady=5, sticky='w')

        # -----row 2, expense entry-----
        l_expense = ttk.Label(f1, text='EXPENSE : ', font=(None, 13, 'bold'), background="ivory3")
        l_expense.grid(row=2, column=0, padx=20, pady=25, sticky='w') 

        e_expense = ttk.Entry(f1, width=20, font=(None, 13, 'bold'),  textvariable=expense)
        e_expense.grid(row=2, column=1, padx=50, pady=25, sticky='w')

        # button to add the entered data into the database
        button_add = Button(f1, text='       ADD      ', font=(None, 14, 'bold'), border=6, command=insert)
        button_add.grid(row=2, column=2, padx=40, pady=15)

        # button to show all the entries in the treeView
        button_show_all = Button(f2, text='   SHOW ALL   ', font=(None, 12, 'bold'), border=6, command=open_New_Window)
        button_show_all.grid(row=1, column=0, padx=40, pady=5)


        # ------------- tree view ---------------
        tree_view = ttk.Treeview(f2, columns=(1, 2, 3), show="headings", height="10")
        tree_view.grid(row=0, column=0, padx=30, pady=25, sticky='w')

        tree_view.heading('#1', text="D A T E")
        tree_view.heading('#2', text="T I T L E")
        tree_view.heading('#3', text="E X P E N S E")

        scrollbar = ttk.Scrollbar(f2, orient=VERTICAL, command=tree_view.yview)
        tree_view.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=0, sticky=S + E + N)



    #---------------------------------------tab 2 (frame2)-----------------------------------
    def main_window2_tab2():

        # function for clear screen
        def clear_screen():
            tree_view1_records = tree_view1.get_children()
            for item in tree_view1_records:
                tree_view1.delete(item)

        # search function (in tab 2)
        def search():
            # checking for empty space
            if e_search.get() == "":
                messagebox.showinfo("WARNING !! ", "WARNING: Search Entry is empty. Check again !!")
            else:
                connect = sqlite3.connect("expense.db")
                cursor = connect.cursor()

                variable_input = variable.get()   # taking selected option from the option menu

                if variable_input == "Date :":
                    cursor.execute("SELECT * FROM expense_table WHERE date = ?", (e_search.get(),))
                    records = cursor.fetchall()
                    connect.commit()
                elif variable_input == "Title :":
                    cursor.execute("SELECT * FROM expense_table WHERE title = ?", (e_search.get(),))
                    records = cursor.fetchall()
                    connect.commit()
                else:
                    cursor.execute("SELECT * FROM expense_table WHERE expense = ?", (e_search.get(),))
                    records = cursor.fetchall()
                    connect.commit()

                for record in records:
                    tree_view1.insert('', 'end', values=record)

                e_search.delete(0, END)    # to clear the search entry


        # to delete the selected contents from the database and tree_view1
        def delete_record():
            connect = sqlite3.connect("expense.db")
            cursor = connect.cursor()
            # if else stmt to check if there is record selected or not
            if tree_view1.selection():
                # warning window for delete all button 
                MsgBox = messagebox.askquestion ('DELETE SELECTED RECORD','Are you sure you want to delete the selected records !!',icon = 'warning')
                if MsgBox == 'yes':
                        for selected_item in tree_view1.selection():
                            print(selected_item)      # it prints the selected row id
                            cursor.execute("DELETE FROM expense_table WHERE date=? AND title=? AND expense=?", (tree_view1.set(selected_item, '#1'), tree_view1.set(selected_item, '#2'), tree_view1.set(selected_item, '#3')))
                            connect.commit()
                            tree_view1.delete(selected_item)
                else:
                    messagebox.showinfo('Return','You will now return to the application screen')
            else:
                messagebox.showinfo('WARNING','There is no record selected !!')


        # to define an edit function
        def edit_record():
            # to check if there is a record selected or not
            if tree_view1.selection():
                # local variables
                edited_date = StringVar()
                edited_title = StringVar()
                edited_expense = StringVar()

                # to get the editable item from the tree_view1
                editable_item = tree_view1.selection()
                # defining update function
                def update():
                    edited_date = edit_e_date.get()
                    edited_title = edit_e_title.get()
                    edited_expense = edit_e_expense.get()
                    # connecting to sqlite database
                    connect = sqlite3.connect("expense.db")
                    cursor = connect.cursor()

                    for x in editable_item:
                        # database stuff
                        cursor.execute("UPDATE expense_table SET date=?, title=?, expense=? WHERE date=? AND title=? AND expense=?", (edited_date, edited_title, edited_expense, tree_view1.set(editable_item, '#1'), tree_view1.set(editable_item, '#2'), tree_view1.set(editable_item, '#3')))
                        connect.commit()
                        # replacing the selected row with new inputs(edit_e_date, edit_e_title, edit_e_expense)
                        tree_view1.item(x, values=(edited_date, edited_title, edited_expense))   # to edit the selected item in the tree_view1
                    
                    # to exit the edit window
                    new_edit_Window.destroy()

                # edit popup window to edit the items
                new_edit_Window = Toplevel(f3)
                new_edit_Window.title("EDIT TOOL WINDOW :")
                new_edit_Window.geometry("590x170")

                # frame for the new opened window
                edit_frame = Frame(new_edit_Window, bg="light grey")
                edit_frame.pack(fill="both", expand=1, padx=10, pady=10)

                edit_l_date = ttk.Label(edit_frame, text='DATE : ', font=(None, 13, 'bold'), background="light grey")
                edit_l_date.grid(row=0, column=0, padx=15, pady=5, sticky='w')

                edit_e_date = DateEntry(edit_frame, width=10, font=(None, 13, 'bold'),  textvariable=edited_date)
                edit_e_date.grid(row=1, column=0, padx=15, pady=5, sticky='w')

                edit_l_title = ttk.Label(edit_frame, text='TITLE : ', font=(None, 13, 'bold'), background="light grey")
                edit_l_title.grid(row=0, column=1, padx=15, pady=5, sticky='w')

                edit_e_title = ttk.Entry(edit_frame, width=20, font=(None, 13, 'bold'), textvariable=edited_title)
                edit_e_title.grid(row=1, column=1, padx=15, pady=5, sticky='w')

                edit_l_expense = ttk.Label(edit_frame, text='EXPENSE : ', font=(None, 13, 'bold'), background="light grey")
                edit_l_expense.grid(row=0, column=2, padx=15, pady=5, sticky='w') 

                edit_e_expense = ttk.Entry(edit_frame, width=20, font=(None, 13, 'bold'), textvariable=edited_expense)
                edit_e_expense.grid(row=1, column=2, padx=15, pady=5, sticky='w')

                # button to add the entered data into the database
                update_button = Button(edit_frame, text='  UPDATE  ', font=(None, 14, 'bold'), border=6, command=update)
                update_button.grid(row=2, column=2, padx=40, pady=15)
            else:
                messagebox.showinfo('WARNING','There is no record selected !!')


        # -------------------------- row 0 (search) --------------------------------
        # label for search
        l_search = ttk.Label(f3, text="Search by ", font=(None, 13, 'bold'), background="light grey")
        l_search.grid(row=0, column=0, padx=30, pady=20, sticky='w')

        # create menulist
        variable.set("Title :") # default value
        drop_down = OptionMenu(f3, variable, "Date :", "Title :", "Expense :")
        drop_down.grid(row=0, column=1, pady=20, sticky='w')
        # configure text of the menulist
        drop_down.config(font=(None, 13, 'bold'))

        # text field for search
        e_search = ttk.Entry(f3, width=20, font=(None, 13, 'bold'))
        e_search.grid(row=0, column=2, padx=30, pady=50, sticky='w')

        # button for search
        button_search = Button(f3, text='SEARCH', font=(None, 13, 'bold'), border=4, command=search)
        button_search.grid(row=0, column=3, padx=15, pady=30)

        # ------------------- row 1 (delete/update/clearscreen buttons) ---------------
        # button to delete
        button_delete = Button(f4_2, text=' DELETE RECORD ', font=(None, 13, 'bold'), border=4, command=delete_record)
        button_delete.grid(row=0, column=0, padx=10, pady=10)

        # button to update
        button_edit = Button(f4_2, text=' EDIT RECORD ', font=(None, 13, 'bold'), border=4, command=edit_record)
        button_edit.grid(row=0, column=1, padx=10, pady=20)

        # ---------------------- f4 (tree view) --------------------------
        tree_view1 = ttk.Treeview(f4_1, columns=(1, 2, 3), show="headings", height="10")
        tree_view1.grid(row=0, column=0, padx=20, pady=20, sticky='w')

        tree_view1.heading(1, text="D A T E")
        tree_view1.heading(2, text="T I T L E")
        tree_view1.heading(3, text="E X P E N S E")
        # scrollbar for tree_view1
        scrollbar = ttk.Scrollbar(f4_1, orient=VERTICAL, command=tree_view1.yview)
        tree_view1.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=0, sticky=S + E + N)

        # exit button
        button_exit = Button(f4_2, text=' EXIT ', font=(None, 13, 'bold'), border=4, command=gui.destroy)
        button_exit.grid(row=0, column=2, padx=100, pady=20)

        # button to clear the tree_view1
        button_clear_tv = Button(f3, text=' CLEAR SCREEN ', font=(None, 13, 'bold'), border=4, command=clear_screen)
        button_clear_tv.grid(row=1, column=2, padx=15, pady=10)


    main_window1_tab1()
    main_window2_tab2()

    gui.mainloop()

main_screen()