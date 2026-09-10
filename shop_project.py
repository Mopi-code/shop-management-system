from tkinter import*
from tkinter import ttk,messagebox,simpledialog,filedialog
from tkcalendar import DateEntry
from datetime import datetime

import ast
import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

myconnection=mysql.connector.connect(
    host=os.getenv('DB_HOST', 'localhost'),
    user=os.getenv('DB_USER', 'root'),
    password=os.getenv('DB_PASSWORD'),
    database=os.getenv('DB_NAME', 'shop')
)
mycursor=myconnection.cursor()



widget_storage={}

def update_new_field(*args) :
    try :
        if 'widget' in widget_storage and widget_storage['widget'] is not None:
            widget_storage['widget'].destroy()
            
        selected_column=column_var.get()
        if selected_column=='name' :
            widget_storage['widget']=Entry(win,font=('malgun gothic',14),width=18)
            
        elif selected_column=='price' :
            widget_storage['widget']=Entry(win,validatecommand=(vcmd,'%d','%P'),validate='key',font=('malgun gothic',14),width=18)
            
        elif selected_column=='kind' :
            widget_storage['widget']=ttk.Combobox(win,state='readonly',value=['Clothing','Food','Tool','Thing'],font=('malgun gothic',14),width=16)
            widget_storage['widget'].set('Food')
            
        elif selected_column=='amount' :
            widget_storage['widget']=Spinbox(win,relief='solid',width=17,textvariable=StringVar(value='1'),highlightbackground='#121212',borderwidth=1,state='readonly',font=('malgun gothic',14),from_=1,to_=1000)
        
        elif selected_column=='vaild_date' :
            widget_storage['widget']=DateEntry(win,font=('malgun gothic',14),state='readonly',width=16)
        
        elif selected_column=='size' :
            widget_storage['widget']=ttk.Combobox(win,state='readonly',value=['Small','Medium','Big'],font=('malgun gothic',14),width=16)
            widget_storage['widget'].set('Small')
            
        widget_storage['widget'].place(x=1035,y=270)
    
    except :
        messagebox.showerror('Error!','Error!, Please try again later!')
        lb_state.config(text='An error Aqqured!',fg='red')
    
def create_default_widget() :
    try :
        widget_storage['widget']=Entry(win,width=18,font=('malgun gothic',14))
        widget_storage['widget'].place(x=1035,y=270)
            
    except :
        messagebox.showerror('Error!','Error!, Please try again later!')
        lb_state.config(text='An error Aqqured!',fg='red')

def modify() :
    mycursor.execute('SELECT EXISTS(SELECT 1 FROM products WHERE id=%s)',(en_id.get(),))
    if en_id.get() and widget_storage.get('widget') and mycursor.fetchone()[0]:
        mycursor.execute(f'UPDATE products SET {cb_column.get()}=%s WHERE id=%s',(widget_storage['widget'].get(),en_id.get(),))
        myconnection.commit()
        show_products()            
        lb_state.config(text='Modified Product Succesfully!',fg='green')

    else :
        messagebox.showerror("Error!","Error, Vaild id or No id and changes!")
        lb_state.config(text='Modify Product Failed!',fg='red')

def expired_products() :
    try :
        today=datetime.today().date()
        mycursor.execute('SELECT * FROM products')
        product_list.delete(0,END)
        
        for x in mycursor :
            vaild_date=datetime.strptime(x[5],"%m/%d/%y").date()
            
            if vaild_date<today and x[3]=='Food' :
                product_list.insert(END,x)            
        lb_state.config(text='Showed Expired Products Succesfully!',fg='green')
            
    except :      
        messagebox.showerror('Error','An Error aqqured, Try again!')
        lb_state.config(text='Showed Expired Products Failed!',fg='red')
        
def purchases_list() :
    try :
        new_win=Toplevel(win)
        new_win.geometry('700x460')
        new_win.title('Purchases list')
        new_win.resizable(False,False)
        
        
        def show_purchases() :
            mycursor.execute('SELECT * FROM purchases')
            
            purchases.delete(0,END)
            for x in mycursor :
                purchases.insert(END,x)
                
            myconnection.commit()
        
        def search_purchases() :
            name_or_id=simpledialog.askstring('Search in Purchases','Type the Name or ID of the Purchase!')
            if name_or_id:
                if name_or_id.isdigit() :
                    mycursor.execute('SELECT * FROM purchases WHERE id=%s',(name_or_id,))
                    
                    purchases.delete(0,END)
                    for x in mycursor :
                        purchases.insert(END,x)
                else :
                    mycursor.execute('SELECT * FROM purchases WHERE name LIKE %s',('%'+name_or_id+'%',))

                    purchases.delete(0,END)
                    for i in mycursor :
                        purchases.insert(END,i)
                
                myconnection.commit()
                
        def delete_purchase() :
            id=simpledialog.askinteger('Delete Purchase','Type the ID of Purchase you wanna Delete')
            if id :
                try :
                    mycursor.execute('DELETE FROM purchases WHERE id=%s',(id,))
                    myconnection.commit()
                    show_purchases()
        
                except :
                    messagebox.showerror('Error!','Error!, Vaild id or Somethinge else, Try Again Later!')
        
        purchases=Listbox(new_win,bd=0,highlightthickness=0,font=('malgun gothic',14),width=65,height=15)
        purchases.place(x=23,y=20)
        
        bt_delete=Button(new_win,command=delete_purchase,text='Delete Purchase',font=('malgun gothic',14),fg='white',bg='red',width=19)
        bt_delete.place(x=23,y=390)
        
        bt_search_purchases=Button(new_win,command=search_purchases,text='Search in Purchases',font=('malgun gothic',14),fg='white',bg='green',width=19)
        bt_search_purchases.place(x=240,y=390)
        
        bt_show_purchases=Button(new_win,command=show_purchases,text='Show Purchases',font=('malgun gothic',14),bg='blue',fg='white',width=19)
        bt_show_purchases.place(x=457,y=390)            
        lb_state.config(text='Opened Purchases Succesfully!',fg='green')
        
        if win.cget('bg')=='#121212' :
            new_win.config(bg='#121212')
            purchases.configure(fg='white',bg='#212121')
            
    except :      
        messagebox.showerror('Error','An Error aqqured, Try again!')
        lb_state.config(text='Openning Purchases Failed!',fg='red')
    
def buy_product() :
    try :
        product_id=simpledialog.askinteger('Buy Product','ID of Product You wanna buy',parent=win)
        if product_id :
            product_value=simpledialog.askinteger('Buy Product','Amount of the Product',parent=win)
        
        if product_id and product_value :
            mycursor.execute('SELECT value FROM my_variables WHERE id=1')
            my_value=mycursor.fetchone()
            mycursor.execute('SELECT value FROM my_variables WHERE id=2')
            my_value2=mycursor.fetchone()
            mycursor.execute('SELECT* FROM products WHERE id=%s',(product_id,))
            item=mycursor.fetchone()

            if int(item[4])-product_value<0 :
                messagebox.showerror('Buy Prodcut Failed!','We dont have the Amount of Product You want!')
            elif int(item[4])-product_value>=0 :
                mycursor.execute('UPDATE products SET amount=%s where id=%s',(int(item[4])-product_value,product_id,))
                mycursor.execute('UPDATE my_variables SET value=%s where id=1',(int(my_value[0])+product_value,))
                mycursor.execute('UPDATE my_variables SET value=%s where id=2',(int(item[2])*product_value+int(my_value2[0]),))
                
                messagebox.showinfo('Purchased!',f'{product_value} items were sold!')

            data=list(item)[1:]
            data[3]=product_value
            data[6]=datetime.now().strftime('%m/%d/%y')
            mycursor.execute('INSERT INTO purchases(name,price,kind,amount,vaild_date,size,purchased_date) VALUES(%s,%s,%s,%s,%s,%s,%s)',tuple(data))
            myconnection.commit()
            show_products()            
            lb_state.config(text='Bought Product Succesfully!',fg='green')
            
    except :
        messagebox.showerror('Buy Product Failed!','An error Aqqured! Vaild id or no Amount left!')
        lb_state.config(text='Buying Product Failed!',fg='red')

def theme(theme_mode) :
    try :
        if theme_mode=='dark' :
            win.config(bg='#121212')
            lb_amount.configure(bg='#121212',fg='white')
            lb_to.configure(bg='#121212',fg='white')
            lb_column.configure(bg='#121212',fg='white')
            lb_data.configure(bg='#121212',fg='white')
            lb_kind.configure(bg='#121212',fg='white')
            lb_line.configure(bg='#121212',fg='white')
            lb_line2.configure(bg='#121212',fg='white')
            lb_modify.configure(bg='#121212',fg='white')
            lb_price.configure(bg='#121212',fg='white')
            lb_name.configure(bg='#121212',fg='white')
            lb_search.configure(bg='#121212',fg='white')
            lb_size.configure(bg='#121212',fg='white')
            lb_state.configure(bg='#121212',fg='white')
            en_modify_id.configure(bg='#121212',fg='white')
            en_amount.configure(bg='#121212',foreground='white',fg='white',highlightbackground='#121212',highlightcolor='#121212')
            r1.configure(bg='#121212',fg='white')
            r2.configure(bg='#121212',fg='white')
            r3.configure(bg='#121212',fg='white')
            product_list.configure(bg='#212121',fg='white')
            

        elif theme_mode=='light' :
            win.config(bg=win_bg)  
            lb_amount.configure(bg=win_bg,fg='black')
            lb_to.configure(bg=win_bg,fg='black')
            lb_column.configure(bg=win_bg,fg='black')
            lb_data.configure(bg=win_bg,fg='black')
            lb_kind.configure(bg=win_bg,fg='black')
            lb_line.configure(bg=win_bg,fg='black')
            lb_line2.configure(bg=win_bg,fg='black')
            lb_modify.configure(bg=win_bg,fg='black')
            lb_price.configure(bg=win_bg,fg='black')
            lb_name.configure(bg=win_bg,fg='black')
            lb_search.configure(bg=win_bg,fg='black')
            lb_size.configure(bg=win_bg,fg='black')
            lb_state.configure(bg=win_bg,fg='black')
            en_modify_id.configure(bg=win_bg,fg='black')
            en_amount.configure(bg=win_bg,fg='black',highlightbackground=win_bg,highlightcolor=win_bg)
            r1.configure(bg=win_bg,fg='black')
            r2.configure(bg=win_bg,fg='black')
            r3.configure(bg=win_bg,fg='black')
            product_list.configure(bg=list_bg,fg='black')      
                
        lb_state.config(text='Theme Changed Succesfully!',fg='green')
            
    except :      
        messagebox.showerror('Error','An Error aqqured, Try again!')
        lb_state.config(text='Theme Change error!',fg='red')

def flipped() :
    try :
        show_products()
        list=product_list.get(0,END)[::-1]
        product_list.delete(0,END)
        for item in list :
            product_list.insert(END,item)            
        lb_state.config(text='Flipped List Succesfully!',fg='green')
            
    except :      
        messagebox.showerror('Error','An Error aqqured, Try again!')
        lb_state.config(text='Filpping list Failed!',fg='red')
 
def sort_by(item) :
    try :
        product_list.delete(0,END)
        mycursor.execute(f'SELECT * FROM products ORDER BY {item}')
        rows=mycursor.fetchall()
        
        for row in rows :
            product_list.insert(END,row)            
        lb_state.config(text=f'Sorted Products by {item} Succesfully!',fg='green')
            
    except :      
        messagebox.showerror('Error','Sort Products Error!, Try again!')
        lb_state.config(text='Sort Products Failed!',fg='red')

def search() :
    try :
        mycursor.execute(f'SELECT * FROM products WHERE {cb_search.get()} LIKE %s',('%'+en_search.get()+'%',))
        product_list.delete(0,END)
        
        for item in mycursor :
            product_list.insert(END,item)
            
        product_list.after(3000,search)            
            
    except :      
        messagebox.showerror('Error','Search Product Failed!, Try again!')
        lb_state.config(text='Search Product Failed!',fg='red')

def total_money() :
    try :
        mycursor.execute("SELECT value FROM my_variables WHERE name='total_money'")
        messagebox.showinfo('Sales Money',f'The total amount of money from sales is {mycursor.fetchone()[0]}')

    except :      
        messagebox.showerror('Error','An Error aqqured, Try again!')
        lb_state.config(text='An Error Aqqured!',fg='red')
        
def sold_products() :
    try :
        mycursor.execute("SELECT value FROM my_variables WHERE name='total_sales'")
        messagebox.showinfo('Sold Products',f'The total amount of sold products is {mycursor.fetchone()[0]}')

    except :      
        messagebox.showerror('Error','An Error aqqured, Try again!')
        lb_state.config(text='An error Aqqured!',fg='red')
        
def products_number() :
    try :
        mycursor.execute('select count(*) as products_number from products')
        messagebox.showinfo('Products Number',f'You have {mycursor.fetchone()[0]} Products in Your Shop!')

    except :      
        messagebox.showerror('Error','An Error aqqured, Try again!')
        lb_state.config(text='An Error Aqqured!',fg='red')
        
def import_data() :
    try :
        filepath=filedialog.askopenfilename(defaultextension='.csv',filetypes=[('CSV Files','.*csv'),('All Files','*.*')])
        if filepath :
            with open(filepath,'r') as file:
                lines=file.readlines()
                new_lines=[line.replace('\n','') for line in lines]
                new_lines=[list(ast.literal_eval(item)) for item in new_lines]
                new_lines=[new_list[1:] for new_list in new_lines]

                for product in new_lines :
                    mycursor.execute('INSERT INTO products (name,price,kind,amount,vaild_date,size,added_date) value (%s,%s,%s,%s,%s,%s,%s)',tuple(product))
                    myconnection.commit()
                    
            messagebox.showinfo('Imported','Data has been imported!')
            show_products()            
            lb_state.config(text='Data has been imported Succesfully!',fg='green')
            
    except :      
        messagebox.showerror('Error','An Error aqqured, Try again!')
        lb_state.config(text='Import Data Failed!',fg='red')

def delete_all_data() :
    try :
        confrim=messagebox.askyesno('Confrimation','Are you sure?!')
        if confrim :
            messagebox.showinfo('Deleted','All data has been Deleted!')
            
            mycursor.execute('DELETE FROM products')
            myconnection.commit()
            
            show_products()
                        
            lb_state.config(text='Deleted Data Succesfully!',fg='green')
            
    except :      
        messagebox.showerror('Error','An Error aqqured, Try again!')
        lb_state.config(text='Deleting Products Failed!',fg='red')

def export_data() :
    try :
        filepath=filedialog.asksaveasfilename(defaultextension='.csv',filetypes=[('CSV Files','.*csv'),('All Files','*.*')])
        
        if filepath :
            with open(filepath,'w') as file:
                show_products()
                for item in product_list.get(0,END) :
                    file.write(str(item)+'\n')
                messagebox.showinfo('Exported','Data Exported Succesfully!')
                lb_state.config(text='Exported data Succesfully!',fg='green')
            
    except :      
        messagebox.showerror('Error','Export data failed!, Try again!')
        lb_state.config(text='Export data Failed!',fg='red')
                
def delete_product() :
    try :
        id=simpledialog.askinteger('Delete Product',"Enter product's id" )
        
        mycursor.execute('SELECT EXISTS(SELECT 1 FROM products WHERE id=%s)',(id,))
        if mycursor.fetchone()[0] :
            mycursor.execute('DELETE FROM products WHERE id=%s',(id,))
            myconnection.commit()
            show_products()
            lb_state.config(text='Deleted product Succesfully!',fg='green')
        else :
            messagebox.showerror('Error','Delete product failed, Try again!')
            lb_state.config(text='Delete Product Failed!',fg='red')
            
    except :      
        messagebox.showerror('Error','Delete product failed, Try again!')
        lb_state.config(text='Delete Product Failed!',fg='red')
    
def show_products() :
    try :
        mycursor.execute('SELECT* FROM products')
        
        product_list.delete(0,END)
        for x in mycursor :
            product_list.insert(END,x)
            
        lb_state.config(text='Showed Products Succesfully!',fg='green')
            
    except :      
        messagebox.showerror('Error','An Error aqqured, Try again!')
        lb_state.config(text='Showed Products Failed!',fg='red')

def clear_entries() :
    try :
        en_name.delete(0,END)
        en_price.delete(0,END)
        en_kind.set('Food')
        en_amount.set(1)
        en_vaild_date.set_date(datetime.now().strftime('%m/%d/%y'))
        var.set(0)
        
        win.update()
        
    except :
        messagebox.showerror('Error!','Error!, Please try again later!')
        lb_state.config(text='An error Aqqured!',fg='red')

def save_product() :
    try :
        if en_name.get() and en_price.get() :
            size='Small' if var.get()==0 else 'Medium' if var.get()==1 else 'Big'
            data=(en_name.get(),int(en_price.get()),en_kind.get(),int(en_amount.get()),en_vaild_date.get(),size,datetime.now().strftime('%m/%d/%y'))
            mycursor.execute('INSERT INTO products (name,price,kind,amount,vaild_date,size,added_date) value (%s,%s,%s,%s,%s,%s,%s)',data)
            myconnection.commit()
                
            show_products()
            clear_entries()
            
            lb_state.configure(text='Saved product Succesfully!',fg='green')
            
        else :
            messagebox.showwarning('Error','Enter the Name and Price!')
            lb_state.config(text='Save product Failed!',fg='red')
        
    except :
        messagebox.showerror('Error','Try Again later!')
        lb_state.config(text='Save product Failed!',fg='red')
    
def velidate_number(action,value_if_allowed) :
    try :
        if action=='1' :
            return value_if_allowed.isdigit()
        return True
    
    except :
        messagebox.showerror('Error!','Error!, Please try again later!')
        lb_state.config(text='An error Aqqured!',fg='red')




win=Tk()
win.geometry('1250x600+0+0')
win.resizable(False,False)
win.title('Shop Management')

 
 
menubar=Menu(win)

file_menu=Menu(menubar,tearoff=0)
file_menu.add_command(label='Import Data',command=import_data)
file_menu.add_command(label='Export Data',command=export_data)
file_menu.add_command(label='Delete All Data',command=delete_all_data)
file_menu.add_separator()
file_menu.add_command(label='Exit',command=win.destroy)

info_menu=Menu(menubar,tearoff=0)
info_menu.add_command(label='Amount of Products',command=products_number)
info_menu.add_command(label='Sold Products',command=sold_products)
info_menu.add_command(label='Total Sales',command=total_money)
info_menu.add_separator()
info_menu.add_command(label='Purchases List',command=purchases_list)

sort_menu=Menu(menubar,tearoff=0)
sort_menu.add_command(label='Sort by ID',command=lambda : sort_by('id'))
sort_menu.add_command(label='Sort by Name',command=lambda : sort_by('name'))
sort_menu.add_command(label='Sort by Price',command=lambda : sort_by('price'))
sort_menu.add_command(label='Sort by Kind',command=lambda : sort_by('kind'))
sort_menu.add_command(label='Sort by Amount',command=lambda : sort_by('amount'))
sort_menu.add_command(label='Sort by Size',command=lambda : sort_by('size'))
sort_menu.add_command(label='Sort by Vaild date',command=lambda : sort_by('vaild_date'))
sort_menu.add_command(label='Sort by Added date',command=lambda : sort_by('added_date'))
sort_menu.add_separator()
sort_menu.add_command(label='Flipped',command=flipped)

theme_menu=Menu(win,tearoff=0)
theme_menu.add_command(label='Light',command=lambda : theme('light'))
theme_menu.add_command(label='Dark',command=lambda :theme('dark'))

menubar.add_cascade(label='File',menu=file_menu)
menubar.add_cascade(label='Sort',menu=sort_menu)
menubar.add_cascade(label='Info',menu=info_menu)
menubar.add_cascade(label='Theme',menu=theme_menu)
win.config(menu=menubar)


lb_name=Label(win,text='Name :- ',font=('Malgun gothic',14))
lb_name.place(x=20,y=20)

lb_price=Label(win,text='Price :- ',font=('malgun gothic',14))
lb_price.place(x=20,y=70)

lb_kind=Label(win,text='Kind :- ',font=('malgun gothic',14))
lb_kind.place(x=20,y=120)

lb_amount=Label(win,text='Amount :- ',font=('malgun gothic',14))
lb_amount.place(x=20,y=170)

lb_data=Label(win,text='Vaild Date :- ',font=('malgun gothic',14))
lb_data.place(x=20,y=220)

lb_size=Label(win,text='Size :- ',font=('malgun gothic',14))
lb_size.place(x=20,y=270)

en_name=ttk.Entry(win,width=20,font=('malgun gothic',14))
en_name.place(x=100,y=20)


vcmd=win.register(velidate_number)

en_price=Entry(win,validate='key',validatecommand=(vcmd,'%d','%P'),font=('malgun gothic',14))
en_price.place(x=100,y=70)

en_kind=ttk.Combobox(win,state='readonly',font=('malgun gothic',14),value=['Clothing','Food','Tool','Thing'],width=18)
en_kind.place(x=100,y=120)
en_kind.set('Food')

en_amount=Scale(win,font=('malgun gothic',12),from_=1,to_=200,length=180,orient='horizontal',width=15)
en_amount.place(x=120,y=157)

en_vaild_date=DateEntry(win,width=14,font=('malgun gothic',14),state='readonly')
en_vaild_date.place(x=140,y=220)

var=IntVar()

r1=Radiobutton(win,text='Small',font=('malgun gothic',11),variable=var,value=0)
r1.place(x=90,y=272)

r2=Radiobutton(win,text='Medium',font=('malgun gothic',11),variable=var,value=1)
r2.place(x=160,y=272)

r3=Radiobutton(win,text='Big',font=('malgun gothic',11),variable=var,value=2)
r3.place(x=250,y=272)

bt_save=Button(win,text='Save Product',command=save_product,font=('malgun gothid',12),width=20,bg='green',fg='white')
bt_save.place(x=65,y=340)

product_list=Listbox(win,bd=0,highlightthickness=0,font=('malgun gothic',14),width=56,height=16,relief='groove',highlightbackground='#787878',borderwidth=1)
product_list.place(x=360,y=30)

bt_show__products=Button(win,text='Show Products',command=show_products,font=('malgun gothic',12),width=20,bg='blue',fg='white')
bt_show__products.place(x=360,y=430)

bt_delete_product=Button(win,text='Delete Product',command=delete_product,font=('malgun gothic',12),width=20,bg='red',fg='white')
bt_delete_product.place(x=547,y=430)

bt_expired_products=Button(win,text='Expired Products',command=expired_products,font=('malgun gothic',12),width=20,bg='orange',fg='white')
bt_expired_products.place(x=734,y=430)

lb_search=Label(win,text='Search By',font=('malgun gothic',14))
lb_search.place(x=960,y=30)

cb_search=ttk.Combobox(win,state='readonly',width=11,value=['id','name','price','kind','amount','vaild_date','size','added_date'],font=('malgun gothic',14))
cb_search.place(x=1086,y=30)
cb_search.set('id')

en_search=Entry(win,font=('malgun gothic',14),width=20)
en_search.place(x=960,y=75)

bt_search=Button(win,text='Search',command=search,width=8,font=('malgun gothic',10),background='yellow')
bt_search.place(x=1153,y=75)

lb_line=Label(win,text='_____________________________',font=('malgun gothic',14))
lb_line.place(x=969,y=110)

lb_modify=Label(win,text='Modify Product',font=('malgun gothic',14))
lb_modify.place(x=1030,y=155)

en_modify_id=Label(win,text="Product's ID",font=('malgun gothic',14))
en_modify_id.place(x=960,y=200)

en_id=Entry(win,font=('malgun gothic',14),width=11,validate='key',validatecommand=(vcmd,'%d','%P'))
en_id.place(x=1100,y=200)

lb_column=Label(win,text='Column :-',font=('malgun gothic',14))
lb_column.place(x=960,y=235)

column_var=StringVar()
column_var.trace_add("write",update_new_field)

cb_column=ttk.Combobox(win,textvariable=column_var,state='readonly',font=('malgun gothic',14),width=11,value=['name','price','kind','amount','vaild_date','size'])
cb_column.place(x=1086,y=235)
cb_column.set('name')

lb_to=Label(win,text='to :- ',font=('malgun gothic',14))
lb_to.place(x=960,y=270)

widget_storage={}

bt_modify=Button(win,text='Modify',command=modify,width=26,fg='white',bg='SpringGreen3',font=('malgun gothic',12))
bt_modify.place(x=970,y=310)

lb_line2=Label(win,text='_____________________________',font=('malgun gothic',14))
lb_line2.place(x=973,y=355)

bt_buy=Button(win,text='Buy Product',bg='turquoise',width=16,font=('malgun gothic',12),command=buy_product)
bt_buy.place(x=1015,y=400)

lb_state=Label(win,text='Ready',font=('malgun gothic',15),fg='#121212')
lb_state.place(x=20,y=550)

win_bg=lb_state.cget('bg')
list_bg=product_list.cget('bg')
create_default_widget()




mainloop()