import cv2
import time
import numpy as np
import pygame
import math
import threading
import argparse

# カメラを初期化
cap = cv2.VideoCapture(0)

# 顔検出のための分類器をロード
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# 作業時間の初期化
work_time = 0
start_time = time.time()
last_announcement_time = start_time

# pygameの初期化
pygame.init()

hours_list = [i for i in range(11)]
minutes_list = [0, 15, 30, 45]
# 音声ファイルのロード
sound_intro = pygame.mixer.Sound("sounds/intro.wav") # 作業時間が
sound_hour = [pygame.mixer.Sound(f"sounds/hours/{i}hours.wav") for i in range(11)] # ◯時間
sound_minute = [pygame.mixer.Sound(f"sounds/minutes/{i}minutes.wav") for i in minutes_list] # ◯分
sound_exceeded = pygame.mixer.Sound("sounds/exceeded.wav") # を超えました
sound_work_end = pygame.mixer.Sound("sounds/work_end.wav") # 作業終了

Flag = False
end_Flag = False

window_name = "Work time tracker"

parser = argparse.ArgumentParser(description='作業時間トラッカー')
parser.add_argument('--end_time', type=int, default=36000, help='作業終了時間（秒）')
args = parser.parse_args()

if args.end_time > 36000:
    end_time = 36000
else:
    end_time = args.end_time

def play_announcement(work_time):
    hours = int(work_time // 3600)
    minutes = int((work_time % 3600) // 60)

    sound_intro.play()
    pygame.time.wait(int(sound_intro.get_length() * 1000))

    if hours > 0:
        sound_hour[hours].play()
        pygame.time.wait(int(sound_hour[hours].get_length() * 1000))

    if minutes > 0:
        sound_minute[minutes // 15].play()
        pygame.time.wait(int(sound_minute[minutes // 15].get_length() * 1000))

    sound_exceeded.play()
    pygame.time.wait(int(sound_exceeded.get_length() * 1000))

while True:
    # カメラからフレームを取得
    ret, frame = cap.read()

    # グレースケールに変換
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 顔検出を実行（画面の前にいればいいので閾値を甘めに設定）
    faces = face_cascade.detectMultiScale(gray, 1.05, 2)

    # 顔が検出された場合
    if len(faces) > 0:
        # 作業時間を更新
        work_time += time.time() - start_time

        # 15分ごとにアナウンスを流す
        if int(work_time) != 0 and int(work_time) % 900 == 0 and not Flag:
            announcement_thread = threading.Thread(target=play_announcement, args=(work_time,))
            announcement_thread.start()
            Flag = True
        
        if int(work_time) % 900 != 0 and Flag:
            Flag = False

        if int(work_time) > end_time:
            sound_work_end.play()
            end_Flag = True
    

    # 現在の時刻を更新
    start_time = time.time()

    # 作業時間を表示
    cv2.putText(frame, f"Work Time: {int(work_time)} seconds", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    # 結果を表示
    cv2.imshow(window_name, frame)

    # 'q'キーが押されたらループを終了
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    if end_Flag:
        pygame.time.wait(int(sound_work_end.get_length() * 1000))
        break
    # ウィンドウの×ボタンが押されたらループを終了
    if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
        break


end_hours = int(work_time // 3600)
end_minutes = int((work_time % 3600) // 60)
end_seconds = int(work_time % 60)
print(f"作業時間： {end_hours} 時間 {end_minutes} 分 {end_seconds} 秒")
# リソースを解放
cap.release()
cv2.destroyAllWindows()

# pygameの終了
pygame.quit()