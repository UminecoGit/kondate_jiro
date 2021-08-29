import psycopg2


class databaseCtrl:

    def __init__(self,accessInfo):
        self.accessInfo = accessInfo

        self.conn = psycopg2.connect(self.accessInfo)
        self.cur = self.conn.cursor()
    
    def close(self):
        self.cur.close()
        self.conn.close()
    

    def add(self,Url,scheduledDate,
        name,ingredient,ingredientQuantity,digit):
        self.cur.execute("INSERT INTO menus VALUES (%s,%s,%s,%s,%s,False,%s)",
        (Url,scheduledDate,name,ingredient,ingredientQuantity,digit))

        self.conn.commit()

    
    def getScheduledDate(self,menuName):
        self.cur.execute("SELECT scheduled_date FROM menus WHERE menu_name=%s",(menuName,))

        array = self.cur.fetchall()
        return array[0][0]
    
    def getMenuName(self,scheduleddate):
        self.cur.execute("SELECT menu_name FROM menus WHERE scheduled_date=%s",(scheduleddate,))
        array = self.cur.fetchall()
        return array
    
    def getMenu(self,startday,endday):
        self.cur.execute("SELECT scheduled_date,menu_name FROM menus WHERE %s<=scheduled_date AND scheduled_date<=%s",(startday,endday))

        array = self.cur.fetchall()
        return array

    def getIngredientsList(self,startday,endday):
        self.cur.execute("SELECT ingredient,ingredient_quantity,digit \
            FROM menus WHERE %s<=scheduled_date AND scheduled_date<=%s AND bought_flag=False",(startday,endday))
        
        array = self.cur.fetchall()
        return array


    def deleteMenu(self,scheduledDate,MenuName=None):#Noneの時は全て削除とする
        self.cur.execute("DELETE FROM menus WHERE scheduled_date=%s",(scheduledDate,))
        self.conn.commit()
    
    def swapMenus(self,scheduledDateA,scheduledDateB):
        nameB = self.getMenuName(scheduledDateB)
        self.cur.execute("UPDATE menus SET scheduled_date=%s WHERE scheduled_date=%s",(scheduledDateB,scheduledDateA))
        self.cur.execute("UPDATE menus SET scheduled_date=%s WHERE menu_name=%s",(scheduledDateA,nameB,))
        self.conn.commit()

    def checkExistance(self,scheduledDate):
        self.cur.execute("SELECT * FROM menus WHERE scheduled_date=%s",(scheduledDate,))
        length = len(self.cur.fetchall())
        if not length == 0:
            return True
        else:
            return False
    
    def changeFlagToTrue(self,ingredient,startday,endday):
        self.cur.execute("UPDATE menus SET bought_flag=True WHERE %s<=scheduled_date AND \
            scheduled_date<=enddate AND ingredient=%s",(startday,endday,ingredient))

        self.conn.commit()
        


        

    

class statusCtrl:

    def __init__(self,accessInfo):
        self.accessInfo = accessInfo

        self.conn = psycopg2.connect(self.accessInfo)
        self.cur = self.conn.cursor()

    def initStatus(self,userId):
        self.cur.execute("SELECT current_status FROM userstatus WHERE userid=%s",(userId,))
        array = self.cur.fetchall()
        if len(array)==0:
            self.cur.execute("INSERT INTO userstatus VALUES(%s,'quit',False,'2000-01-01')",(userId,))
            self.conn.commit()
        else:
            return

    
    def close(self):
        self.cur.close()
        self.conn.close()
    
    #ステータス関連
    def getStatus(self,userId):
        self.initStatus(userId)
        self.cur.execute("SELECT current_status FROM userstatus WHERE userid=%s",(userId,))
        status = self.cur.fetchall()
        return status[0][0]
    
    def setStatus(self,userId,status):
        self.cur.execute("UPDATE userstatus SET current_status=%s WHERE userid=%s",(status,userId))
        self.conn.commit()

    #フラグ関連
    def flagOn(self,userId):
        self.cur.execute("UPDATE userstatus SET set_flag=True WHERE userid=%s",(userId,))
        self.conn.commit()
    
    def flagOff(self,userId):
        self.cur.execute("UPDATE userstatus SET set_flag=False WHERE userid=%s",(userId,))
        self.conn.commit()
    
    def getflag(self,userId):
        self.cur.execute("SELECT set_flag FROM userstatus WHERE userid=%s",(userId,))
        setArray = self.cur.fetchall()
        return setArray[0][0]
    

    #日付関連
    def getDate(self,userId):
        self.cur.execute("SELECT set_date FROM userstatus WHERE userid=%s",(userId,))
        status = self.cur.fetchall()
        return status[0][0]
    
    def setDate(self,userId,setDate):
        self.cur.execute("UPDATE userstatus SET set_date=%s WHERE userid=%s",(setDate,userId))
        self.conn.commit()
    
class otherThings:

    def __init__(self,accessInfo):
        self.accessInfo = accessInfo

        self.conn = psycopg2.connect(self.accessInfo)
        self.cur = self.conn.cursor()
    
    def add(self,name,addDate):
        self.cur.execute("INSERT INTO others VALUES (%s,%s)",(name,addDate))
        self.conn.commit()

    def delete(self,name):
        self.cur.execute("DELETE FROM others WHERE item_name=%s",(name,))
        self.conn.commit()

    def getAllDays(self):
        self.cur.execute("SELECT add_date FROM others")
        array = self.cur.fetchall()

        return array

    def getAllItems(self):
        self.cur.execute("SELECT item_name FROM others")
        array = self.cur.fetchall()

        return array

class pastMenu:
    pass
