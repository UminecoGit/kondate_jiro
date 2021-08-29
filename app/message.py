
import datetime

from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    QuickReply,QuickReplyButtom,MessageAction
)


class messages:

    def replyAtRegister():
        setArray = []
        setArray.append(QuickReplyButtom(action=MessageAction(label="クラシルから共有",text="exporter")))
        setArray.append(QuickReplyButtom(action=MessageAction(label="クラシルを使わないで追加",text="importer")))
        return TextSendMessage(text="献立の追加方法を選択してください",quick_reply=QuickReply(items=setArray))

    def replyChooseDate(times):
        if times == 1:
            text = "登録する日付を選択してください"
        else:
            text = "再度登録する場合、日付を選択してください\n※終了する場合は終了ボタンを選択してください"
        setArray = []
        day = datetime.date.today()
        setArray.append(QuickReplyButtom(action=MessageAction(label="終了",text="quit")))
        for i in range(0,30,1):
            day += datetime.timedelta(days=1)
            labeltext = str(day.month) + "月" + str(day.day) + "日"
            setArray.append(QuickReplyButtom(action=MessageAction(label=labeltext,text=day.strftime("%Y/%m/%d"))))

        return TextSendMessage(text="登録する日付を選択してください",quick_reply=QuickReply(items=setArray))


    def replyAtInput():
        return TextSendMessage(text="登録する献立を入力してください\n※quitと入力すると終了します")


    def replyAtList(text,itemlist):
        replytext = "現在の買い物リストは以下となります\n\n" + text

        setArray = []

        quitbuttom = QuickReplyButtom(action=MessageAction(label="終了",text="quit"))
        setArray.append(quitbuttom)

        for name in itemlist:
            replybuttom = QuickReplyButtom(action=MessageAction(label=name,text=name))
            setArray.append(replybuttom)
        
        return TextSendMessage(text=replytext,quick_reply=QuickReply(items=setArray))


    def replyAfterAdd():
        return TextSendMessage(text="登録が完了しました")
    
    def replyException():
        return TextSendMessage(text="日付以外の入力がされました\n登録を終了します")




        



    
    
    

            