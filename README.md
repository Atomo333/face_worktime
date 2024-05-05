# face_worktime
カメラ内に顔がある時だけ作業時間をカウントします．
そして，15分ごとにずんだもんが作業時間を通知してくれます．

# 実行方法
mainディレクトリ内で
```
python app.py
```
終了時間を決めたい場合は以下のように実行（例：3600秒）
```
python app.py --end_time 3600
```

# 必要ライブラリ
- opencv-python==4.9.0.80
- pygame==2.5.2
- numpy==1.26.4
- plyer==2.1.0
以下でインストール
```
pip install -r requirements.txt
```

# 環境
- Windows 11
- venv
- python 3.10.6