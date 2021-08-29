

import datetime



class textChangeArray():

    def getURL(self,text):#テキストからURL取得(kurashiruを使うとき)
        url = text.split("\n")[1]
        return url
    
    def getDate(self,text):#テキストからdate取得
        tdate = datetime.datetime.strptime(text,"%Y/%m/%d")
        date = datetime.date(tdate.year,tdate.month,tdate.day)
        return date
    
    def getRegisterArrays(self,text):#(kurashiru使わんとき)
        array = text.split("\n")
        menuname = array[0]
        setarray = []
        for i in range(1,len(array),2):
            record = []
            record.append([array[i],array[i+1]])
        return [menuname,setarray]
        
    def separateValue(self,string):
        number = -1
        digit = ""
        for i in range(len(string)-1,0,-1):
            checks = string[:i]
            if checks.isdigit():
                number = int(checks)
                digit = string[i:]
                break
        
        if number == -1:
            return [-1,"調味料"]
        else:
            return [number,digit]
    




class arrayChangeText:

    def makeListOtherThings(self,array,listarray):
        text = "\nその他購入物\n"
        
        for i in array:
            text += i[0] + "\n"
        
        reply =  listarray + text
        return reply

    def makeIngredientList(self,array):#買い物リストの表示
        dictionaryQuantity = {}
        dictionaryDigits = {}
        setSeasoning = set()

        for record in array:
            if record[0] in dictionaryQuantity:
                if record[1] <= 0:
                    setSeasoning.add(record[0])
                else:
                    dictionaryQuantity[record[0]] +=  record[1]
            else:
                dictionaryQuantity[record[0]] = record[1]
                dictionaryDigits[record[0]] = record[2]
        

        
        setArrayIngredient = []
        for dictkeys in list(dictionaryQuantity.keys()):
            text = str(dictionaryQuantity[dictkeys]) + dictionaryDigits[dictkeys]
            setArrayIngredient.append([dictkeys,text])
        
        setArraySeasoning = list(setSeasoning)

        #以下テキスト化

        text = "購入する物\n"

        for record in setArrayIngredient:
            text += record[0] + "   " + record[1] + "\n"
        
        text += "\n調味料\n"
        for record in setArraySeasoning:
            text += record[0] + "\n"
        
        text += "\n"

        return text

    def makeItemNameList(self,Ingarray,otharray):
        setArray = []
        for record in Ingarray:
            setArray.append(record[0])

        for name in otharray:
            setArray.append(name)

        return setArray





        

        

