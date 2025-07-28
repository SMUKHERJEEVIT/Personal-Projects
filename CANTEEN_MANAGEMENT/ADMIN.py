import mysql.connector as mys
from prettytable import PrettyTable
from prettytable import from_db_cursor
mycon=mys.connect(host="localhost",user="root",passwd="Soumyadip@15")
x=mycon.cursor()
x.execute("Create database if not exists canteendft")
x.execute("Use canteendft")
x.execute('''create table if not exists Staff(Staff_ID varchar(3) primary key, STAFF_NAME varchar(10),password varchar(15))''')
#USE PASSWORD IN THE DATABASE 
#--------------------------------------------------------SHAYAAN METHOD -----------------------------------------------------#
l=[]
x.execute('select Staff_ID from Staff')
a=x.fetchall()
for i in a:
    j=i[0]
    l.append(j)
if len(l)==0:
    x.execute('''insert into Staff values('A01','Soumyadip','Sam123')''')
    mycon.commit()
#----------------------------------------------------------------MY METHOD -------------------------------------------------------#
def create():
    n=1
    while n==1:
        x.execute ('''Create table if not exists NON_VEG(Item_no varchar(5) primary key,Item_name varchar(30),Price float)''' )
        print("Non veg table created")
        x.execute ('''Create table if not exists VEG(Item_no varchar(5) primary key,Item_name varchar(30),Price float)''' )
        print("VEG table created")
        if n==1:
            break
def update ():
    while True:
        while True:
            print('''
    FOR NON-VEG TABLE
    1. UPDATE ITEM NUMBER 
    2. UPDATE ITEM NAME
    3. UPDATE PRICE''')
        print('''FOR VEG TABLE
    4. UPDATE ITEM NUMBER 
    5. UPDATE ITEM NAME
    6. UPDATE PRICE''')
        ch3=int(input("Enter the choice:"))
        if ch3 == 1:
            print("IN NON VEG MENU")
            itemnum=input("Enter the number to be updated")#NV01
            ITem_no=input("Enter the Updated item number")#NV02
            x.execute(f'''Update NON_VEG SET Item_no="{ITem_no}" WHERE Item_no ="{itemnum}"''')
            mycon.commit()
            OPTION=input("DO YOU WANT TO CONTINUE (YES/NO)")
            if OPTION.lower() == "no":
                break
        elif ch3 == 2:
            print("IN NON VEG MENU")
            ITEM_NAME=input("Enter the name of the menu ")#CP
            ITEM_NAME1=input("Enter the name of the menu updated")#CS
            x.execute('''Update NON_VEG SET Item_no={} where Item_no == {}'''.format(ITEM_NAME,ITEM_NAME1))
            mycon.commit()
            OPTION=input("DO YOU WANT TO CONTINUE (YES/NO)")
            if OPTION.lower() == "no":
                break
        elif ch3 == 3:
            print("IN NON VEG MENU")
            ITEM_PRICE = int(input("Enter the price of the item"))
            x.execute('''Update NON_VEG SET Item_no={} '''.format(ITEM_PRICE) )
            mycon.commit()
            OPTION=input("DO YOU WANT TO CONTINUE (yes/NO)")
            if OPTION.lower() == "no":
                break
        elif ch3 == 4:
            print("IN VEG MENU")
            itemnum1=input("Enter the number to be updated")
            ITem_no1=input("Enter the Updated item number")
            x.execute(f'''Update NON_VEG SET Item_no="{itemnum1}" WHERE Item_no = "{ITem_no1}"''')
            mycon.commit()
            OPTION=input("DO YOU WANT TO CONTINUE (YES/NO)")
            if OPTION.lower() == "no":
                break
        elif ch3 == 5:
            print("IN VEG MENU")
            ITEM_NAME1=input("Enter the name of the menu ")
            x.execute('''Update VEG SET Item_no={} '''.format(ITEM_NAME1))
            mycon.commit()
            OPTION=input("DO YOU WANT TO CONTINUE (YES/NO)")
            if OPTION.lower == "no":
                break
        elif ch3 == 6:
            print("IN VEG MENU")
            ITEM_PRICE1 = int(input("Enter the price of the item"))
            x.execute('''Update VEG SET Item_no={} '''.format(ITEM_PRICE1) )
            mycon.commit()
            OPTION=input("DO YOU WANT TO CONTINUE (YES/NO)")
            if OPTION.lower == "no":
                break
        else:
            break
def delete():
    while True:
        while True:
            print()
            print('''1. DELETE DATA FROM THE GIVEN TABLE 
            2. DELETE TABLES FROM THE GIVEN DATABASE
            3. DELETING A USER DATA''')
            ch4=int(input("Enter the choice"))
            if ch4 == 1:
                while True:
                    print('''FOR NON VEG
                    1.REMOVING Item based on ITEM NUMBER
                    2.REMOVING Item based on ITEM NAME
                    3.REMOVING Item based on PRICE
                    ''')
                    print('''FOR VEG TABLE
                    4.REMOVING Item based on ITEM NUMBER
                    5.REMOVING Item based on ITEM NAME
                    6.REMOVING Item based on PRICE
                    ''')
                    c5 = int(input("Enter the number of your choice "))
                    if c5 == 1:
                        itemno=input("Enter the itemno")
                        x.execute('''DELETE FROM NON_VEG WHERE Item_no="{}"'''.format(itemno))
                        opti=input("DO YOU WANT TO CONTINUE")
                        if opti.lower() == "no":
                            break
                    elif c5 == 2:
                        itemname=input("Enter the itemname")
                        x.execute('''DELETE FROM NON_VEG WHERE Item_name="{}"'''.format(itemname))
                        if opti.lower() == "no":
                            break
                    elif c5 == 3:
                        itemprice=input("Enter the price")
                        x.execute('''DELETE FROM NON_VEG WHERE Price="{}"'''.format(itemprice))
                        if opti.lower() == "no":
                            break
                    elif c5 == 4:
                            itemno=input("Enter the itemno")
                            x.execute('''DELETE FROM VEG WHERE Item_no="{}"'''.format(itemno))
                            if opti.lower() == "no":
                                break
                    elif c5 == 5:
                        itemname=input("Enter the itemno")
                        x.execute('''DELETE FROM VEG WHERE Item_name="{}"'''.format(itemname))
                        if opti.lower() == "no":
                            break
                    elif c5 == 6:
                       itemprice=input("Enter the itemno")
                       x.execute('''DELETE FROM VEG WHERE Price="{}"'''.format(itemprice))
                       if opti.lower() == "no":
                            break
                    else:
                        break
            elif ch4 == 2:
                while True:
                    print('''1. Delete non-veg table
                    2. Delete veg table''')
                    ch6=int(input("Enter the choice"))
                    if ch6 == 1:
                        x.execute("drop table NON_VEG ")
                        print("NON VEG TABLE HAS BEEN DELETED")
                        break
                    elif ch6 == 2:
                        x.execute("drop table VEG")
                        break
                    else:
                        break
            elif ch4 == 3:
                x.execute("drop table Staff")
                break
            else:
                break
        break
def insert():
    while True:
        while True:
            print('''1. FOR NON-VEG TABLE''')
            x.execute('''INSERT INTO NON_VEG VALUES("NV01","Chickenroll","5.5") ''')
            x.execute('''INSERT INTO NON_VEG VALUES("NV02","ChickenPuff","6.5") ''')
            print('''2. FOR VEG TABLE''')
            x.execute('''INSERT INTO VEG VALUES("V01","Vegroll","4.5") ''')
            x.execute('''INSERT INTO NON_VEG VALUES("V01","Veg_Puff","5.5") ''')
            print('''3. EXIT''')
            ch6=int(input("Enter the choice:"))
            if ch6 == 1:
                IDNO=input("Enter the ITEM ID(Start with initial as NV)")
                IDNAME=input("Enter the product name")
                IDPRICE=input("Enter the price of the item")
                x.execute('''INSERT INTO NON_VEG VALUES("{}","{}","{}") '''.format(IDNO,IDNAME,IDPRICE))
                op1=input("Do you want to continue(Yes/No)")
                if op1.lower == "no":
                    break
            elif ch6 == 2:
                iDNO=input("Enter the Staff ID(Start with initial as V)")
                iDNAME=input("Enter the product name")
                iDPRICE=input("Enter the price of the item")
                x.execute('''INSERT INTO VEG VALUES("{}","{}","{}") '''.format(iDNO,iDNAME,iDPRICE))
                op2=input("Do you want to continue(Yes/No)")
                if op1.lower == "no":
                    break
            elif ch6==3:
                break
        break
def display():
    print()
    z=PrettyTable()
    while True:
        while True:
            print("""ENTER THE TABLE TO BE DISPLAYED
    1. Display the NON VEG table
    2. Display the VEG TABLE
    3. Display the login table""")
            ch7=int(input("Enter the choice"))
            if ch7 == 1:
                x.execute("SELECT * FROM NON_VEG")
                z=from_db_cursor(x)
                print(z)
            elif ch7 == 2:
                x.execute("SELECT * FROM VEG")
                z=from_db_cursor(x)
                print(z)
            elif ch7 == 3:
                x.execute("SELECT * FROM NON_VEG")
                z=from_db_cursor(x)
                print(z)
def CLEAR_ALL():
    while True:
        while True:
            print('''1. Clear data from veg table
    2. Clear data from non veg table
    3. Clear data from user table''')
            ch8=int(input("Enter the choice"))
            if ch8 == 1:
                x.execute("""truncate TABLE NON_VEG""")
                break
            elif ch8 == 2:
                x.execute("""truncate TABLE VEG""")
                break
            elif ch8 == 3:
                x.execute("truncate 
def admin():
    l=[]
    x.execute('select Staff_ID from Staff')
    a=x.fetchall()
    for i in a:
        j=i[0]
        l.append(j)
    if len(l)==0:
        x.execute('''insert into Staff values('A01','Soumyadip','Sam123')''')
        mycon.commit()
    print("=================================================================================================================")
    print("                                             WELCOME TO THE ADMIN INTERFACE                                      ")
    print("=================================================================================================================")
    iD=input("Enter the staffid")
    passwd=input("Enter the password")
    x.execute('select password from Staff where Staff_ID="{}"'.format(iD))
    a=x.fetchone()
    if passwd in a:
        while True:
            while True:
                print('''
                1.Create 
                2. Update 
                3. Insert
                4. Delete
                5. Display
                6. Clear all
                ''')
                ch1=int(input("Enter the choice:"))
                if ch1 == 1:
                    create()
                    break
                elif ch1 == 2:
                    update()
                    break
                elif ch1 == 3:
                    insert()
                    break
                elif ch1 == 4:
                    delete()
                    break
                elif ch1 == 5:
                    display()
                    break
                elif ch1 == 6:
                    CLEAR_ALL()
            choice=input("Exit from admin Site (Yes/No)")
            if choice.lower() == "yes":
                    break
admin()
