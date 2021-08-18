# line_-alarm

## 背景
朝起きれない+  
推しに起こされたい+    
友達に「明日まじで起きなきゃやばいからLineで起こして」「起きてなさそうだったらメッセージ爆撃して」というやつ  

## できること
<img width="433" alt="目覚ましbot" src="https://user-images.githubusercontent.com/69378772/129932386-8e530fe1-e180-4f10-8c86-6968cb3a90ce.png">
こんな感じです．メッセージで設定時刻を言うとその時間にメッセージ爆撃してきます．起きたというと止まります．推しのはずのアイコンが手書きのゾロリになっていますが，これはLine開発者アカウントのところから変更できます．

## 使用方法
認識されるメッセージは4種類

- 時刻設定  
  __設定
  (時間):(分)__  
  でメッセージを送るとアラーム時刻が設定されます．既にされている場合は上書きされます
- 確認  
　__確認__  
 と送ると設定されているアラーム時刻を確認できます．
- キャンセル   
  __キャンセル__  
  と送るとアラームを解除します
- ストップ   
  __起きた__  
  アラームが鳴ってる（メッセージが立て続けに送られてきているときに）「起きた」と送ると止まります．「起きれてえらいとほめてくれます」

## 構成
pythonのプログラムを走りっぱなしにして置く環境がないので，herokuの無料枠を借ります．とある事情からheroku run main.pyの使い方（コード走りっぱなし）にはできないので，HTTPリクエストでたたくと処理を行うようにしておいてGASで定期実行させます．これによって設定された時刻にメッセージ送信を行います．  
メッセージが送られてきたら処理..はwebhockというLINE側が用意している機能というか仕組みで簡単に行えます．
![名称未設定ファイル](https://user-images.githubusercontent.com/69378772/129938401-b502c6c7-59bb-4002-a776-374a67e6f886.png)


## 今後の展望
起こすセリフやほめるセリフの変更をメッセージから「セリフ追加　～～」などで行えるようにしたいです．このキャラはこんなセリフ言わない！という解釈違いを起こさないために．  
実は展望というほど遠い話ではなくて，ちょこっと実装するだけなんですがやる気でず．結局現状自分用なのでセリフ追加はプログラム書き換えのほうが楽だし．

## 公開先
LineAPIの無料枠は1か月に1000通（恐ろしく少ない）しか送れないという縛りがあるのでとりあえず公開しません． 　

アラームとして使ったら5秒に1通だから30秒で止めたとしても6通，設定に5通くらいと考えても1日約10通．3人で使ったら止まっちゃうので．
