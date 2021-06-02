from tkinter import *
import db
import time
import fpdf
import webbrowser
import matplotlib.pyplot as plt

expMethod=None

def get_used():
    arr=db.get_data()
    sum=0
    for i in arr:
        sum+=int(i[0])
    return sum

date=time.strftime("%d/%m/%Y")
#date="01/03/2020"
salary=100000
used=get_used()

def tkBox():
    root=Tk()
    root.geometry("650x500")
    root.configure(bg="light blue")
    root.title("TRACKING OF EXPENSES")

    sal=StringVar()
    use=StringVar()
    rem=StringVar()

    w=Label(root,text="SALARY :")
    w.grid(row=1,column=1)
    me=Entry(root,font=("courier New",12,'bold'),textvar=sal,state='readonly',width=10,bd=5,bg="light blue")
    me.grid(row=1,column=2)
    sal.set(str(salary))

    w=Label(root,text="Used :")
    w.grid(row=2,column=1)
    me=Entry(root,font=("courier New",12,'bold'),textvar=use,state='readonly',width=10,bd=5,bg="light blue")
    me.grid(row=2,column=2)
    use.set(str(used))

    w=Label(root,text="Remaining :")
    w.grid(row=3,column=1)
    me=Entry(root,font=("courier New",12,'bold'),textvar=rem,state='readonly',width=10,bd=5,bg="light blue")
    me.grid(row=3,column=2)
    rem.set(str(salary-used))

    w=Label(root,text="DATE :")
    w.grid(row=4,column=3,pady=10)
    equation3=StringVar()
    me=Entry(root,font=("courier New",12,'bold'),textvar=equation3,width=10,bd=5,bg="yellow")
    me.grid(row=5,column=3,pady=10)
    equation3.set(date)
 
    clicked=StringVar()
    clicked.set("EXPENDITURE_LIST")
    drop=OptionMenu(root,clicked,"food","travel","shoping","other",command=print_choice)
    drop.grid(row=6,column=1,pady=10)
    drop.grid()

    w=Label(root,text="DESCRIPTION :")
    w.grid(row=7,column=2,pady=10)
    w=Label(root,text="AMOUNT :")
    w.grid(row=7,column=1,pady=10)

    amount=StringVar()
    me=Entry(root,font=("courier New",12,'bold'),textvar=amount,width=20,bd=5,bg="white")
    me.grid(row=8,column=1,pady=10)
    amount.set("")

    des=StringVar()
    me=Entry(root,font=("courier New",12,'bold'),textvar=des,width=20,bd=5,bg="white")
    me.grid(row=8,column=2,pady=10)
    des.set("")
    sug=StringVar()
    addB=Button(root,text="add",bg="pink",command=lambda :add_db(des,amount,use,rem,sug,equation3))
    addB.grid(row=8,column=3,pady=10)

    w=Label(root,text="SUGGESTION:")
    w.grid(row=12,column=1,pady=10,padx=5)
    me=Entry(root,font=("courier New",12,'bold'),textvar=sug,width=40,bd=5,bg="light pink")
    me.grid(row=12,column=2,padx=5,pady=10,columnspan=4)
    sug.set("")

    graph=Button(root,text="graph",padx=10,pady=10,fg="white",bg="light green",command=lambda :show_graph())
    graph.grid(row=13,column=1,pady=10)
    pie=Button(root,text="pie",padx=10,pady=10,fg="white",bg="light green",command=lambda :show_pie())
    pie.grid(row=13,column=2,pady=10)
    pdf=Button(root,text="pdf",padx=10,pady=10,fg="white",bg="light green",command=lambda :print_pdf())
    pdf.grid(row=13,column=3,pady=10)
    root.mainloop()

def add_db(des,amount,use,rem,sug,date):
    global used
    print("adding to database")
    db.set_data(amount.get(),expMethod,des.get(),date.get())
    used+=int(str(amount.get()))
    use.set(str(used))
    rem.set(str(salary-used))
    des.set('')
    amount.set('')
    percent=(int(used)/int(salary-used))*100
    percent=int(percent)
    dict={10:'you are savings are good',20:'you savings are better',30:'your savings are sufficient ',40:'your savings are decreasing',50:'your savings are reduced by half',60:'your savings are reduced more than half',70:'please have a vision on savings',80:'please check your savings',90:'your savings are going to be exhausted',100:'your savings are exhausted'}
    percent-=(percent%10)
    sug.set(dict[percent])

def print_choice(event):
    global expMethod
    expMethod=event

def print_pdf():
    pdf=fpdf.FPDF(format='letter')
    pdf.set_font("Arial",size=14)
    pdf.add_page()
    data=db.get_data()
    pdf.cell(200,10,txt="date           type            amount            DESCRIPTION",ln=1,align="L")
    pdf.cell(200,10,txt="-"*135,ln=2,align="C")
    for line,i in enumerate(data):
        pdf.cell(200,10,txt=i[-1]+":       "+i[1]+"        "+i[0]+"        "+i[2],ln=line+2,align="L")
    pdf.output("expense.pdf")
    webbrowser.open("expense.pdf")

def show_graph():
    arr=db.get_data()
    data={}
    for i in arr:
        if i[-1] in data.keys():
            data[i[-1]]+=int(i[0])
        else:
            data[i[-1]]=int(i[0])
    names = data.keys()
    values = data.values()
    plt.figure(figsize=(9, 3))
    plt.bar(names, values)
    plt.show()

def show_pie():
    arr=db.get_data()
    data={}
    for i in arr:
        if i[1] in data.keys():
            data[i[1]]+=int(i[0])
        else:
            data[i[1]]=int(i[0])
    labels = data.keys()
    sizes = data.values()
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%',shadow=True, startangle=90)
    ax1.axis('equal')
    plt.show()


tkBox()