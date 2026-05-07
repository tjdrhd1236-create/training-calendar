"""
PROJECT 36:30 - 훈련 일정 → ICS 자동 변환기

사용법:
  1. sessions.json 파일에 세션 정의 (아래 스키마 참고)
  2. python3 build_ics.py
  3. project_3630.ics 생성됨
  4. GitHub raw URL 또는 Dropbox 등에 업로드
  5. Google Calendar에서 "URL로 추가" → 12시간마다 자동 동기화

JSON 스키마 (sessions.json):
{
  "calendar_name": "PROJECT 36:30 훈련",
  "sessions": [
    {
      "uid": "고유ID-한번정하면-바꾸지말것",
      "date": "2026-05-07",
      "time": "06:00",
      "duration": 60,
      "title": "🏃 세션 제목",
      "location": "전주",
      "description": "상세 내용",
      "alarms_min": [60, 10]   // 옵션, 기본 [60, 10]
    }
  ]
}

⚠️ UID 규칙: 한 번 발행한 UID는 절대 바꾸지 말 것.
   같은 UID로 내용을 수정하면 캘린더가 "수정"으로 인식해서 갱신됨.
   UID를 바꾸면 새 이벤트가 추가되고 기존 것은 그대로 남음.
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

try:
    from icalendar import Calendar, Event, Alarm
    import pytz
except ImportError:
    print("필요 라이브러리 설치: pip install icalendar pytz")
    sys.exit(1)

KST = pytz.timezone('Asia/Seoul')


def build_ics(sessions_data: dict, output_path: str) -> None:
    """JSON 세션 데이터를 ICS로 변환"""
    cal = Calendar()
    cal.add('prodid', '-//PROJECT 36:30//Training//KO')
    cal.add('version', '2.0')
    cal.add('x-wr-calname', sessions_data.get('calendar_name', 'PROJECT 36:30'))
    cal.add('x-wr-timezone', 'Asia/Seoul')
    cal.add('method', 'PUBLISH')
    cal.add('refresh-interval;value=duration', 'PT6H')
    cal.add('x-published-ttl', 'PT6H')

    now = datetime.now(KST)
    
    for s in sessions_data['sessions']:
        event = Event()
        event.add('uid', f"{s['uid']}@project3630.training")
        event.add('summary', s['title'])
        event.add('description', s.get('description', ''))
        event.add('location', s.get('location', ''))
        
        start = KST.localize(
            datetime.strptime(f"{s['date']} {s['time']}", "%Y-%m-%d %H:%M")
        )
        end = start + timedelta(minutes=s['duration'])
        
        event.add('dtstart', start)
        event.add('dtend', end)
        event.add('dtstamp', now)
        event.add('last-modified', now)
        event.add('status', 'CONFIRMED')
        event.add('sequence', s.get('sequence', 0))
        
        for mins in s.get('alarms_min', [60, 10]):
            alarm = Alarm()
            alarm.add('action', 'DISPLAY')
            alarm.add('description', s['title'])
            alarm.add('trigger', timedelta(minutes=-mins))
            event.add_component(alarm)
        
        cal.add_component(event)
    
    Path(output_path).write_bytes(cal.to_ical())
    print(f"✅ {output_path}")
    print(f"   {len(sessions_data['sessions'])}개 이벤트")


if __name__ == '__main__':
    json_path = sys.argv[1] if len(sys.argv) > 1 else 'sessions.json'
    out_path = sys.argv[2] if len(sys.argv) > 2 else 'project_3630.ics'
    
    with open(json_path, encoding='utf-8') as f:
        data = json.load(f)
    
    build_ics(data, out_path)
