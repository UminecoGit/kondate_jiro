
"""from linebot import (
    LineBotApi, WebhookHandler
)"""

import textCtrl
import getHTML as gH
import database as db
#import message

import datetime as dt

#初期化
host=""
port=""
dbname=""
user=""
passw=""

accessinfo = ''
accessinfo += 'host='+host
accessinfo += ' port='+port
accessinfo += ' dbname='+dbname
accessinfo += ' user='+user
accessinfo += ' password='+passw


textCtr = textCtrl.textChangeArray()
arrayCtr = textCtrl.arrayChangeText()
#regiDb = db.databaseCtrl(accessinfo)
#statusDb = db.statusCtrl(accessinfo)
#otherDb = db.otherThings(accessinfo)
#mess = message.messages()

#line_bot_api = LineBotApi('YOUR_CHANNEL_ACCESS_TOKEN')



class mainApp:

    def __init__(self,event):
        self.text = event.message.text
        self.userId = event.source.user_id
        self.replyToken= event.reply_token

    def registerAtK(self):
        
        
        #フラグオフ OK
        statusDb.flagOff(self.userId)

        #テキストからURLの分割 OK
        url = textCtr.getURL(self.text)

        #分割したURLを使いスクレイピング //URLは取っておく OK
        html = gH.getDishInfo(url)

        #返信
        reply = mess.replyAfterAdd()
        line_bot_api.reply_message(self.replyToken,text=reply)

        #dateを取得 OK
        date = statusDb.getDate(self.userId)
        #name取得 OK
        name = html.getDishName()
        #適性分量
        quant = html.getProperQuantity()
        #材料配列取得 OK
        ingArray = html.getIngredients(self)
        #材料配列操作
        for record in ingArray:
            ingredient = record[0]
            quantity,digit = textCtr.separateValue(record[1])
            quantity = round(quantity*2/quant)
            regiDb.add(url,date,name,ingredient,quantity,digit)#登録


    def makeBuyList(self):
        startday = dt.date.today() + dt.timedelta(days=1)
        endday = startday + dt.timedelta(days=1)

        #購入品の取得
        buyarray = regiDb.getIngredientsList(startday,endday)
        otherlist = otherDb.getAllItems()
        nameList = arrayCtr.makeItemNameList(buyarray,otherlist)

        #配列からテキストへ

        listText = arrayCtr.makeIngredientList(buyarray)
        listText = arrayCtr.makeListOtherThings(otherlist,listText)

        #line_bot_api.reply_message(self.replyToken,text=mess.replyAtList(listText,nameList))


    def rooting(self):#ルーティング用
        text = self.text

        #現在のステータス取得
        currentStatus = statusDb.getStatus(self.userId)
        currentFrag = statusDb.getflag(self.userId)

        if text == "quit":
            #返信

            #ステータス変更
            pass
        elif text == "register":
            #返信
            reply = mess.replyAtRegister()
            line_bot_api.reply_message(self.replyToken,text=reply)
            #ステータス変更Quick
            statusDb.setStatus(text)
            pass
        elif text == "exporter":
            #返信
            reply = mess.replyChooseDate(1)
            line_bot_api.reply_message(self.replyToken,text=reply)
            #ステータス変更Q
            statusDb.setStatus(self.userId,text)
            pass
        elif text == "importer":
            #返信
            #ステータス変更Q
            pass
        elif text == "list":
            #返信+リスト表示Quick            
            self.makeBuyList()
            #ステータス変更
            statusDb.setStatus(self.userId,self.text)


        else:


            #ステータスで分岐
            #exporterの場合
            if currentStatus=="exporter":

                if currentFrag==False:
                    #テキストを日付型にできるかどうかで例外処理
                    try:
                        date = dt.datetime.strptime(text,"%Y/%m/%d %H:%M:%S")
                        tdate = dt.date(year=date.year,month=date.month,day=date.day)
                    except ValueError :
                        line_bot_api.reply_message(self.replyToken,text=mess.replyException())
                        statusDb.setStatus(self.userId,"quit")
                        statusDb.flagOff(self.userId)
                        return
                    
                    statusDb.flagOn(self.userId)
                    line_bot_api.reply_message(self.replyToken,text=mess.replyAtImporter())
                
                else:

                    try:
                        self.registerAtK()
                    except:
                        line_bot_api.reply_message(self.replyToken,text=mess.replyException())
                        statusDb.setStatus(self.userId,"quit")
                        statusDb.flagOff(self.userId)
                        return

                    statusDb.flagOff(self.userId)
                    line_bot_api.reply_message(self.replyToken,text=mess.replyChooseDate(2))
                    

            elif currentStatus=="list":

                startday = dt.datetime.today() + dt.timedelta(days=1)
                endday = startday + dt.timedelta(days=1)

                #入力された商品名のレコードを削除もしくはflagを切替
                regiDb.changeFlagToTrue(self.text,startday,endday)
                otherDb.delete(self.text)
                #返信+リスト表示Quick            
                self.makeBuyList()













host = "ec2-52-22-161-59.compute-1.amazonaws.com"
name = "dcr0gm4fmurj28"
pasw = "9e85c7f22d1f66c9abae208c1992839a08bd096b71e3be7c0b792c011fe2dfb8"
port = "5432"
url = "postgres://nhgyavmxoajgzn:9e85c7f22d1f66c9abae208c1992839a08bd096b71e3be7c0b792c011fe2dfb8@ec2-52-22-161-59.compute-1.amazonaws.com:5432/dcr0gm4fmurj28"
user = "nhgyavmxoajgzn"

def makeKey(host,port,dbname,user,passw):
    accessinfo = ''
    accessinfo += 'host='+host
    accessinfo += ' port='+port
    accessinfo += ' dbname='+dbname
    accessinfo += ' user='+user
    accessinfo += ' password='+passw
    return accessinfo


access = makeKey(host,port,name,user,pasw)

regiDb = db.databaseCtrl(access)
statusDb = db.statusCtrl(access)
otherDb = db.otherThings(access)

