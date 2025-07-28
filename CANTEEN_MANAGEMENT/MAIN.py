import mysql.connector as mys
from prettytable import PrettyTable
from prettytable import from_db_cursor
mycon=mys.connect(host="localhost",user="root",passwd="Soumyadip@15",database="Canteen")
x=mycon.cursor()  
print("================================================================================================")
print("                         WELCOME TO OUR CANTEEN MANAGEMENT SYSTEM                               ")
print("=================================================================================================")
print("1. ADMIN ACCESS")
print("2. User access")
print("3. Exit")
choice=int(input("Enter the desired option"))
if choice == 1:
    import ADMIN
elif choice == 2:
    import USER
