from django.http import HttpResponseForbidden, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import json
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, FollowEvent, UnfollowEvent,
    TextSendMessage, ImageMessage, AudioMessage
)
import datetime
import pytz
from linebot import LineBotApi, WebhookHandler

from .models import Members

# 各クライアントライブラリのインスタンス作成
# 本当はべたがきダメだった気がする 環境変数？
line_bot_api = LineBotApi(--秘密キー--)
handler = WebhookHandler(--トークン--)

@csrf_exempt
def callback(request):


    # signatureの取得
    real_signature = request.META['HTTP_X_LINE_SIGNATURE']
    body = request.body.decode('utf-8')

    try:
        # 署名の検証を行い、成功した場合にhandleされたメソッドを呼び出す
        handler.handle(body,real_signature)
    except InvalidSignatureError:
        return HttpResponseForbidden()
    return HttpResponse('OK')

# フォローイベントの場合の処理
@handler.add(FollowEvent)
def handle_follow(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='初めまして')
    )


# メッセージイベントの場合の処理
@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    # メッセージでもテキストの場合はオウム返しする
    #line_bot_api.reply_message(event.reply_token,TextSendMessage(text=event.message.text))

    #誰から来たのか把握してmemberに情報を入れる
    try:
        member = Members.objects.get(ID=event.source.user_id)
    except:
        member = Members(ID=event.source.user_id,Active=False,when=datetime.datetime.now(pytz.utc))
        member.save()

    #最優先:アラームが鳴っているとき（設定時刻を過ぎているかつアクティブ）止める
    if member.when < datetime.datetime.now(pytz.utc) and member.Active:
        member.Active=False
        member.save()
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="起きれてえらい"))

    #改行で分割
    tex = event.message.text.split("\n")
    
    #キャンセル
    if tex[0]=="キャンセル":
        member.Active=False
        member.save()
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="アラーム設定を解除しました"))
    #設定
    elif tex[0]=="設定":
        try:
            tmp = datetime.datetime.now(pytz.utc)
            #alermhour alermminute
            ah,am = map(int,tex[1].split(":"))
            #おかしな入力じゃないかチェック
            settime = datetime.datetime(tmp.year,tmp.month,tmp.day,ah,am,0,tzinfo=pytz.utc)
            #標準時刻表記
            ah = (ah-9)%24
            settime = datetime.datetime(tmp.year,tmp.month,tmp.day,ah,am,0,tzinfo=pytz.utc)
            #今日のその時間を過ぎていたら明日のその時間にする
            if settime < datetime.datetime.now(pytz.utc):
                settime = settime+datetime.timedelta(days=1)

            member.when=settime
            member.Active=True
            member.save()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=str((ah+9)%24)+":"+str(am)+"に設定しました"))

        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="時刻は\n0:00 ~ 23:59 で入力してください\nフォーマットもこの通り"))

    #確認
    elif tex[0]=="確認":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=str(member.Active)+str((member.when.hour+9)%24)+":"+str(member.when.minute)))




#画像や音源
@handler.add(MessageEvent, message=(ImageMessage, AudioMessage))
def handle_image_audio_message(event):
    return
    # 画像と音源の場合は保存する
    content = line_bot_api.get_message_content(event.message.id)
    with open('file', 'w') as f:
        for c in content.iter_content():
            f.write(c)
        
#デバッグ用　データベースに登録されているuserIDを一覧表示
def db2(request):
    greetings = Members.objects.all()
    print("-------------------")
    return render(request, "db2.html",{"greetings": greetings})

#全消去
def alldel(request):
    Members.objects.all().delete()

#毎分チェック（GASで定期実行）して，Activeかつwhenが現在時刻より前のユーザーにメッセージを送る
def check(request):
    for member in Members.objects.all():
        if member.when < datetime.datetime.now(pytz.utc) and member.Active:
            line_bot_api.push_message(member.ID,TextSendMessage("起きて"))
    return render(request, "no.html")
