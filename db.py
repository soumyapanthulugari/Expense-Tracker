import sqlite3

con=sqlite3.connect("data.db")
'''con.execute("Create table exp (amount TEXT,type Text,des TEXT,date TEXT)")
con.close()'''

def set_data(amount,type,des,date):
    con.execute("Insert into exp values(?,?,?,?)",(amount,type,des,date))
    con.commit()
    
#set_data("10000","Food","KFC Party","23/09/2020")
def get_data():
	data=con.execute("Select * from exp")
	arr=[]
	for i in  data:
		arr.append(i)
	return arr

print(get_data())
