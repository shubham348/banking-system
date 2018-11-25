import time
from tabulate import tabulate
from datetime import datetime,date
import cx_Oracle
con=cx_Oracle.connect("system/12345@localhost/xe")
cur=con.cursor()          
######administrator
#admin account creation
#def admin_account():
#    user_id=int(input("enter user id"))
#    password=raw_input("enter password")
#    cur.execute(" insert into SHUBHAM.admin values(:1,:2)",(user_id,password))
#    cur.commit()

#closed account history
def closed_his():
    cur.execute("select * from SHUBHAM.closed order by doc")
    his=cur.fetchall()
    print tabulate(his,headers=['acc.no','date & time'])
   

        
    
         
#admin account validate
def admin_validate():
    flag=0
    for i in range(0,3):
        aid=input("enter id")    
        cur.execute('select admin_id from SHUBHAM.admin')
        row = cur.fetchone()
        if aid in row:
            paw=raw_input("enter password")
            cur.execute('select password from SHUBHAM.admin where admin_id=:1', {'1': aid})
            res = cur.fetchall()
            num2=list(sum(res,()))
            if paw not in num2:
                print "try again"
                continue
            else:
                flag=1
                break
        else:
            print "wrong input"
    if(flag==1):
        print "successful login"
        return aid
    else:
        print "cannot login"
        return "fail"
    



# input details fo new user signing up
def input_detail():
    c_id=0
    acc_no=0
    name=raw_input("Enter name:")
    sex=raw_input("Enter Gender:")
    email=raw_input("Enter email address:")
    address=raw_input("Enter address:")
    city=raw_input("Enter city name:")
    state=raw_input("Enter state name:")
    while True:
        pincode=input("pincode")
        if len(str(pincode))>=6:
            break
        else:
            print(" wrong pincode /n Please re enter your pincode")
    print("Enter password it should have min. 8 characters")
    while True:
        pasw=raw_input(" password:")
        if len(str(pasw))>=8:
            break
        else:
            print("Please re enter your pssword")
        
    print("Enter 1 to create savings account Enter 2 to create current account")
    typ=int(input())
    if typ==1:
        print("Enter balance")
        balance=raw_input()
        cur.execute("insert into SHUBHAM.customer33 values(SHUBHAM.cus_id.nextval,SHUBHAM.acc_id.nextval,:1,:2,:3,:4,:5,:6,:7,:8,:9,:10)",(name,sex,address,city,state,balance,pasw,email,typ,pincode))
        con.commit()
        print("you have a saving account")
        cur.execute('select c_id from SHUBHAM.customer33')
        row = cur.fetchall()
        num = list(sum(row, ()))
        cur.execute('select accno from SHUBHAM.customer33')
        row1 = cur.fetchall()
        num1 = list(sum(row1, ()))
        print ("your account_no:")
        print max(num1)
        print ("your login id is:")
        print max(num)
    elif typ==2:
        while True:
            print("To createcurrent account min ammount should be 5k")
            balance=raw_input("Enter Balance")
            if  balance>=5000:
                cur.execute("insert into SHUBHAM.customer33 values(SHUBHAM.cus_id.nextval,SHUBHAM.acc_id.nextval,:1,:2,:3,:4,:5,:6,:7,:8,:9,:10)",(name,sex,address,city,state,balance,pasw,email,typ,pincode))
                con.commit()
                print("you have a current account")
                cur.execute('select c_id from SHUBHAM.customer33')
                row = cur.fetchall()
                num = list(sum(row, ()))
                cur.execute('select accno from SHUBHAM.customer33')
                row1 = cur.fetchall()
                num1 = list(sum(row1, ()))
                print ("your account_no:")
                print max(num1)
                print ("your account_no:")
                print max(num1)
                print ("your login id is:")
                print max(num)
                break
            else:
                print("amount entered is less than 5k")
    else:
        print("wrong account type")
        
    
    
#end of input program
##customer  facilities

####validating acccount
def validate():
    flag=0
    for i in range(0,3):
        cid=input("enter id")    
        cur.execute('select c_id from SHUBHAM.customer33')
        row = cur.fetchall()
        num = list(sum(row, ()))
        if cid in num:
            paw=raw_input("enter password")
            cur.execute('select pwd from SHUBHAM.customer33 where c_id=:1', {'1': cid})
            res = cur.fetchall()
            num2=list(sum(res,()))
            if paw not in num2:
                print "try again"
                continue
            else:
                flag=1
                break
        else:
            print "wrong input"
    if(flag==1):
        print "successful login"
        return cid
    else:
        print "cannot login"
        return "fail"
    

# changing adress
def change_addr(cid):
    addr=raw_input("enter new adress")
    cur.execute('update SHUBHAM.customer33 set adrs=:1 where c_id=:2',{'2':cid,'1':addr})
    con.commit()

#money deposit
def money_deposit(cid):
    am=int(input("enter amount"))
    cur.execute('select balance from SHUBHAM.customer33 where c_id=:1',{'1':cid})
    bl=cur.fetchone()
    bal=int(bl[0])
    if am>0:
        
        new_amount=bal+am
        cur.execute('update SHUBHAM.customer33 set balance=balance+:1 where c_id=:2',{'1':am,'2':cid})
        con.commit()
        cur.execute("insert into SHUBHAM.history1 values(:1,sysdate,'credited',:2,:3)",{'1':cid,'2':am,'3':new_amount})
        con.commit()
    else:
         print(" entered amount less than zero")

#money withdrawal
def money_withdrawal(cid):
    wam=int(input("enter amount for withdrawal "))
    cur.execute('select balance from SHUBHAM.customer33 where c_id=:1',{'1':cid})
    bal=cur.fetchone()
    cur.execute('select type from SHUBHAM.customer33 where c_id=:1',{'1':cid})
    typ=cur.fetchone()
    t=int(typ[0])
    b=int(bal[0])
    if t==1:  
        if b>0:
            if wam<b:
                new_amount=b-wam
                cur.execute('update SHUBHAM.customer33 set balance=:1 where c_id=:2',{'1':new_amount,'2':cid})
                con.commit()
                cur.execute("insert into SHUBHAM.history1 values(:1,sysdate,'debited',:2,:3)",{'1':cid,'2':wam,'3':new_amount})
                con.commit()
                
            else:
                print("insufficient balance ")   
        else:
            print("insufficient balance ")
    elif 2==t:
        if wam>0 and b-wam>5000:
            new_amount1=b-wam
            cur.execute('update SHUBHAM.customer33 set balance=:1 where c_id=:2',{'1':new_amount1,'2':cid})
            con.commit()
            cur.execute("insert into SHUBHAM.history1 values(:1,sysdate,'debited',:2,:3)",{'1':cid,'2':wam,'3':new_amount1})
            con.commit()
            
        else:
                print("insufficient balance ")   
          



#money transfer

def money_transfer(cid):
    ano=int(input("enter account no in which money is to be trasfered"))
    tam=int(input("enter amount to br transfered"))
    cur.execute('select type from SHUBHAM.customer33 where c_id=:1',{'1':cid})
    typ=cur.fetchone()
    t=int(typ[0])
    if t==1:
        cur.execute('select balance from SHUBHAM.customer33 where c_id=:1',{'1':cid})
        bal=cur.fetchone()
        b=int(bal[0])
        if b-tam>=0:
            new_amount=b-tam
            new_amount1=b+tam
            cur.execute('update SHUBHAM.customer33 set balance=balance+:1 where accno=:2',{'1':tam,'2':ano})
            con.commit()
            cur.execute('update SHUBHAM.customer33 set balance=balance-:1 where c_id=:2',{'1':tam,'2':cid})
            con.commit()
            cur.execute("insert into SHUBHAM.history1 values(:1,sysdate,'debited(by transfer)',:2,:3)",{'1':cid,'2':tam,'3':new_amount})
            con.commit()
            cur.execute("insert into SHUBHAM.history1 values(:1,sysdate,'credited(by transfer)',:2,:3)",{'1':ano,'2':tam,'3':new_amount1})
            con.commit()
        else:
            print("insufficient balance")
    elif t==2:
        cur.execute('select balance from SHUBHAM.customer33 where c_id=:1',{'1':cid})
        bal=cur.fetchone()
        b=int(bal[0])
        if b-tam>5000:
            new_amount=b-tam
            new_amount1=b+tam
            cur.execute('update SHUBHAM.customer33 set balance=:1 where c_id=:2',{'1':new_amount,'2':cid})
            con.commit()
            cur.execute('update SHUBHAM.customer33 set balance=balance+:1 where accno=:2',{'1':tam,'2':ano})
            con.commit()
            cur.execute("insert into SHUBHAM.history1 values(:1,sysdate,'debited(by transfer)',:2,:3)",{'1':cid,'2':tam,'3':new_amount})
            con.commit()
            cur.execute("insert into SHUBHAM.history1 values(:1,sysdate,'credited(by transfer)',:2,:3)",{'1':ano,'2':tam,'3':new_amount1})
            con.commit()
            
        else:
            print("insufficient balance")
        
        
#print statement
def print_statement(cid):
    date_from=raw_input("enter date from")
    date_to=raw_input("enter date to")
    date_from1=time.strptime(date_from,"%d/%m/%Y")
    date_to2=time.strptime(date_to,"%d/%m/%Y")
    if date_from1<date_to2:                  
        cur.execute('''select * from SHUBHAM.history1 where c_id=:1 and time between to_date(:2,'dd/mm/yyyy')
        and to_date(:3,'dd/mm/yyyy') order by time''',{'1':cid,'2':date_from,'3':date_to})
        table=cur.fetchall()
        print tabulate(table,headers=['c_id','date & time','operation','amount','cur_bal'],tablefmt="pipe")
        
    else:
        print ("date_from can't be greater tha date_to")


#acount closure
def close(cid):
    cur.execute("insert into SHUBHAM.closed values(:1,sysdate)",(cid))
    con.commit()
    cur.execute('insert into SHUBHAM.cl33 (select * from SHUBHAM.customer33 where c_id=:1)',(cid))
    cur.execute('delete from  SHUBHAM.customer33 where c_id=:1',{'1':cid})
    con.commit()


def restore(ccid):
    cur.execute('delete from SHUBHAM.admin where a_id=:1',{'1':ccid})
    cur.execute('insert into SHUBHAM.customer33 (select * from SHUBHAM.cl33 where accno=:1)',(ccid))
    cur.execute('delete from  SHUBHAM.cl33 where c_id=:1',{'1':ccid})
    con.commit()
    
    
#############        
        
        
         
            
    
    

    
##main
ch1="Y"
ch2="Y"
ch3="Y"
while(ch1=="Y" or ch1=="y"):
    print "MAIN MENU"
    print("1.Sign Up(New account)")
    print("2.Sign In(Existing Account)")
    print("3.Admin")
    print("4.Quit")
    choice=int(input("Please enter you choice")) 
    if choice==1:
        input_detail() 
    elif choice==2:
        print "Signing In"
        cid=validate()
        cid=str(cid)
        if cid.isdigit():
            while(ch2=="Y" or ch2=="y"):
                print "1.Address change"
                print "2.Money Deposit"
                print "3.Money Withdrawl"
                print "4.Transfer Money"
                print "5.print statement"
                print "6.Account Closure"
                print "7.Customer Logout"
                c2=input("Enter your choice")
                if c2==1:
                    change_addr(cid)
                elif c2==2:
                    money_deposit(cid)
                elif c2==3:
                    money_withdrawal(cid)
                elif c2==4:
                    money_transfer(cid)
                elif c2==5:
                    print_statement(cid)
                elif c2==6:
                    close(cid)
                    break
                elif c2==7:
                    break
                else:
                    print("wrong choise")  
                ch2=raw_input("enter Y to continue ")    
        elif cid=="fail":
            print "not allowed to sign in"
    elif choice==3:
        print "Signing In as Admin"
        aid=admin_validate()
        aid=str(aid)
        if aid.isdigit():
            #print "1.To Create a New Administrator Account"
            print "1.Print closed account history"
            print"2. to restore account"
            print "3.Quit"
            while(ch3=="Y" or ch3=="y"):
                ch4=input("Enter your choice")
                if ch4==1:
                    print "closed accounts"
                    closed_his()
                elif ch4==2:
                    ccid=raw_input("enter account no.")
                    restore(ccid)
                elif ch==3:
                    break
                else:
                    print ("wrong choise")
                ch3=raw_input("enter Y to continue")
        elif aid=="fail":
            print "not allowed to sign in"
    elif choice==4:
        break
    else:
        print("wrong choise")
        continue
    print "do u want to continue if yes press Y"
    ch1=raw_input()
