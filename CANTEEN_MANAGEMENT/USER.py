import mysql.connector as mys
mycon=mys.connect(host="localhost",user="root",passwd="Soumyadip@15",database="canteen")
x=mycon.cursor()
def DIsplay_Menu():
    while True:
        while True:
            print()
            print('''1. DISPLAY VEG MENU 
            2. DISPLAY NON VEG MENU''')
            DISPLAY1=int(input("Enter the choice"))
                if DISPLAY1 == 1:
                    x.execute("Select * from VEG")
                    y= from_db_cursor(x)
                    print(y)
                elif DISPLAY1 == 2:
                    x.execute("Select * from NON_VEG")
                    y= from_db_cursor(x)
                    print(y)
                else:
                    break
            break
def Reservation():  
    while True:
        while True:
            print()
            x.execute('''CREATE TABLE RESERVATIONS(D_NO VARCHAR(6),NAME CHAR(5),ITEM_NO PRIMARY KEY VARCHAR(5),QTY INT''')
            id_name=int(input("Enter the Dno of the student"))
            itemno=int(input("Enter the item id of the order"))
            QTY=int(input("Enter the quantity "))
            x.execute('''"INSERT INTO RESERVATION VALUES({},{},{}'''.format(id_name,itemno,QTY))
            cancel=input("Enter the choice (Y/N)")
            if cancel.lower == "n":
                break
        break
def Delete_Reservation():
    while True:
        while True:
            print()
            itemno1=int(input("ENter the itemid of the order placed "))
            x.execute("DELETE FROM RESERVATIONS WHERE ITEM_NO == {} ".format(itemno1))
            mycon.commit()
            chA = input("DO YOU WANT TO DELETE MORE RECORDS(Y/N)")
            if chA.lower() == "n":
                break
        break

def USER():
    print()
    while True:
        while True:
    print('''================================================================================================================================================================
                                                                                                    WELCOME TO USER PAGE 
             ================================================================================================================================================================
    1. DIsplay Menu 
    2. Reservation
    3. Delete Reservation
    4. Exit''')
    CHOICE=int(input("Enter the choice"))
    while True:
        if CHOICE == 1:
            DIsplay_Menu() 
        elif CHOICE == 2:
            Reservation()
        elif CHOICE == 3:
            Delete_Reservation()
        else:
            break
    choice=input("Do you want to continue (Yes/No)")
    if choice.lower() == "no":
        break
USER()
