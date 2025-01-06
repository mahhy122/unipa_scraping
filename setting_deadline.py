import googleapiclient.discovery
import google_auth_oauthlib
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os
import homework as hm
import datetime


# スコープの設定
SCOPES = ['https://www.googleapis.com/auth/calendar']
SCOPES_READ = ['https://www.googleapis.com/auth/calendar.readonly']

homework = hm.homework_list

def setting_API():
    creds = None
    # 保存されたトークンがある場合はそれを使用
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # トークンがない、または無効な場合に認証を実行
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'google_calendar_API.json', SCOPES)  # ダウンロードしたJSONファイル名
            creds = flow.run_local_server(port=0)
        # トークンを保存
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    # APIサービスを構築
    service = build('calendar', 'v3', credentials=creds)
    return service

def register_calendar(service, payload):
    # 新しいイベントを作成
    event = {
        'summary': payload[0],
        'start': {
            'dateTime': payload[1],
            'timeZone': 'Asia/Tokyo',
        },
        'end': {
            'dateTime': payload[2],
            'timeZone': 'Asia/Tokyo',
        },
    }

    # カレンダーにイベントを挿入
    event_result = service.events().insert(calendarId='primary', body=event).execute()
    print(f"作成されたイベント: {event_result.get('htmlLink')}")

def get_schedule(service):
    # 今日から半年のイベントを取得
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z'はUTC時間を表す
    one_week_later = (datetime.datetime.utcnow() + datetime.timedelta(days=185)).isoformat() + 'Z'

    print('今後半年のイベントを取得中...')
    events_result = service.events().list(
        calendarId='primary',  # 'primary'はメインカレンダーを指す
        timeMin=now,
        timeMax=one_week_later,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    events = events_result.get('items', [])
    schedule_box = []
    if not events:
        print('イベントが見つかりませんでした。')
    else:
        for event in events:
            schedule_box.append(event['summary'])
    return schedule_box


def main():
    service = setting_API()
    schedule_box = get_schedule(service)
    print("")
    print("")
    for i in homework:
        print(i)
        for j in range(1,len(i)):
            title = i[j][1]
            if title in schedule_box:
                print("記入済み")
            else:

                time = i[j][2][1]
                time = time.replace("/","-").replace(" ","")
                index = time.replace("/","-").find("(")
                deadline = time[:index] +"T" + time[index+3:]+":00+09:00"

                startd = datetime.datetime(int(time[:index-6]), int(time[index-5:index-3]), int(time[index-2:index]),int(time[index+3:index+5]),int(time[index+6:]))-datetime.timedelta(hours=5)
                start = startd.strftime('%Y-%m-%dT%H:%M:00+09:00')
                print(deadline)
                print(start)
                payload = [title, start, deadline]
                register_calendar(service,payload)


if __name__ == '__main__':
    main()
