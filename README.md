# System_Design2

適当メモ

最初に初期位置を撮影して確定させる。
その後は最後の撮影から30分か1時間毎に撮影して初期画像と比較。
もし工具が無くなっていたら、Slack等でその工具が無くなっているかを通知。正規の手順での持ち出しを促す。

誰かが工具を借りるときは「工具を取る→QRコードをかざす」この2手順で完了。
QRコードを取った直着に画像を撮影し、初期画像と比較。どの工具が持ち出されたのかという情報と共に誰が持って行ったかを保存
返却時は「工具を定位置に返却→QRコードをかざす」の2手順で完了。
QRコードを取った直着に画像を撮影し、初期画像と比較。どの工具が返却されたのかという情報と共に誰が返却したかを保存。

持ち出し、返却は同時に行えるようにしたほうがいい。
持ち出していた工具を返す→QRコード→新しい工具の持ち出し→QRコードではなく、
持ち出していた工具を返す→新しい工具の持ち出し→QRコードという手順を可能にする。

工具を持ち出してから設定した期間工具が戻らなかったら、Slackで持って行った人に使っていない場合は戻すように通知。
まだ使用中である事を返信すれば設定した時間延長し、再び設定した時間が経過後に再通知。

QRコードをちゃんとかざせたかを判別してもらうために、読み込み完了後に音を鳴らす。

時間があれば工具の持ち出し状況を確認できるwebアプリの作成も行う。

工具の中心位置同士を比較、値がある程度近ければその座標の工具の画像の類似度？一致度？で同じ工具かどうかを判別する

工具の順番が入れ替わる、工具を持ち出す、返却時に工具の番号がリンクしない問題
これは中心座標が近い同士で類似度比較する