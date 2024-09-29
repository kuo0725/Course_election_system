import pyodbc as odbc #pip install pypyodbc

DRIVER_NAME = 'SQL Server'
SERVER_NAME = 'DESKTOP-6AEUSNG'
DATABASE_NAME = 'Master'

#uid=<username>;
#pwd=<password>;
connection_string = f"""
    DRIVER={{{DRIVER_NAME}}};
    SERVER={SERVER_NAME};
    DATABASE={DATABASE_NAME};
    Trust_Connection=yes;
    """
conn = odbc.connect(connection_string)
b=False

def Check_Sid(Sid): #檢查課程是否存在於員工表中之副程式
  SQLcmd="select * from 課程資料表 where 課程代碼='{}'".format(Sid)  
  cursor=conn.execute(SQLcmd)
  return cursor.fetchone()  #若無記錄則傳回None
def choose_class(): #選課
  global b
  Sid=input("課程代碼：")
  if Check_Sid(Sid)==None:
    print("查無此課程:{}".format(Sid))
    Main_Menu()
  else:
    if b is not True:
      try:
        SQLcmd="create table 選課紀錄(課程名稱 TEXT ,課程代碼 CHAR(6),班級 TEXT,授課教師 NVARCHAR(10)Not Null,必選修 CHAR(4),學分 INT,上課時間 NVARCHAR(20)Not Null,上下學期 CHAR(4)) " 
        conn.execute(SQLcmd)
      except:
        SQLcmd="drop table 選課紀錄 " 
        conn.execute(SQLcmd)
        SQLcmd="create table 選課紀錄(課程名稱 TEXT ,課程代碼 CHAR(6),班級 TEXT,授課教師 NVARCHAR(10)Not Null,必選修 CHAR(4),學分 INT,上課時間 NVARCHAR(20)Not Null,上下學期 CHAR(4)) " 
        conn.execute(SQLcmd)
      b=True
    SQLcmd="select * from 選課紀錄"
    Record=conn.execute(SQLcmd)
    listStaff=list(Record.fetchall())
    choosed=[]
    for i in listStaff:
      choosed.append(i[1])
    Record.close()
    if Sid in choosed:
      print("該課程已選")
      Main_Menu()
    SQLcmd="select * from 課程資料表 where 課程代碼='{}'".format(Sid)
    course=[]
    Record=conn.execute(SQLcmd)
    listStaff=list(Record.fetchall())
    for row in listStaff:
      for col in row:
          course.append(col)
    SQLcmd="INSERT INTO 選課紀錄 VALUES ('{}','{}','{}','{}','{}','{}','{}','{}')".format(course[0],course[1],course[2],course[3],course[4],course[5],course[6],course[7])
    Record.close()
    conn.execute(SQLcmd)
    conn.commit()
    print("新增課程記錄！")
    Main_Menu() #返回系統主畫面

def Delete_class(): #刪除選課記錄
 Sid=input("課程代號：")
 if Check_Sid(Sid)==None:
    print("查無此課程:{}".format(Sid))
    return
 SQLcmd="select * from 選課紀錄"
 Record=conn.execute(SQLcmd)
 listStaff=list(Record.fetchall())
 choosed=[]
 for i in listStaff:
  choosed.append(i[1])
 Record.close()
 if Sid not in choosed:
  print("沒選擇此課程選")
  Main_Menu()
 SQLcmd="Delete From 選課紀錄 WHERE 課程代碼='{}'".format(Sid)
 conn.execute(SQLcmd)
 conn.commit()
 print("刪除課程成功！")
 Main_Menu()  #返回到選課系統之主畫面


def search_class():  #查詢課程
 SQLcmd="select * from 課程資料表"
 Record=conn.execute(SQLcmd)
 listStaff=list(Record.fetchall())
 print("課程名稱                       課程代碼   班級     授課教師 必選修 學分    上課時間      上下學期")
 for row in listStaff:
     for col in row:
         print(col, end="   ")
     print()
 Record.close()
 Main_Menu()  #返回到選課系統之主畫面
 

def searched_class():  #查詢選課記錄
 try:
  SQLcmd="select * from 選課紀錄"
  Record=conn.execute(SQLcmd)
  listStaff=list(Record.fetchall())
  print("課程名稱                       課程代碼   班級     授課教師 必選修 學分    上課時間      上下學期")
  for row in listStaff:
     for col in row:
         print(col, end="   ")
     print()
  Record.close()
  Main_Menu()  #返回到選課系統之主畫面 
 except:
   print("尚未建立選課清單")
   Main_Menu()

def Main_Menu():  
  print("===資工系選課系統===")
  print("1.查詢課程")
  print("2.選課")
  print("3.選課紀錄")
  print("4.刪除選課")
  print("5.回主畫面")
  n=input("請選擇「資工系選課系統」功能清單：")
  if n=="1":
    search_class()
  elif n=="2":
    choose_class()
  elif n=="3":
    searched_class()  
  elif n=="4":
    Delete_class()
  elif n=="5":
    Main_Menu()
  else:
    print("無效指令")
    Main_Menu()

while True:
  Main_Menu()  #呼叫主選單畫面
conn.close()
