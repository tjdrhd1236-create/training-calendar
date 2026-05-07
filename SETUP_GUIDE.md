# PROJECT 36:30 — Google Calendar 구독 자동화 가이드

## 📦 받은 파일

| 파일 | 용도 |
|---|---|
| `project_3630_w19.ics` | W19 테이퍼 일정 (5/7~5/12) — 즉시 사용 가능 |
| `build_ics.py` | JSON → ICS 변환기 (재사용 가능) |
| `sessions.json` | W19 세션 정의 (편집 시 ICS 재생성) |

---

## 🚀 즉시 사용 (방법 1: 일회성 import)

가장 빠른 방법. 30초 안에 완료.

1. `project_3630_w19.ics` 다운로드
2. [calendar.google.com](https://calendar.google.com) 접속
3. 좌측 **다른 캘린더** 옆 **+** 클릭 → **가져오기**
4. `project_3630_w19.ics` 선택 → 추가할 캘린더 선택 → **가져오기** 클릭
5. 완료 — 6개 일정이 캘린더에 추가됨

**한계**: 일회성. 다음 주 일정은 다시 import 필요.

---

## ⚙️ 진짜 자동화 (방법 2: GitHub + URL 구독)

ICS 파일을 GitHub에 올리고 Google Calendar가 6~12시간마다 자동으로 fetch.
**한 번 설정하면 영구**, 수정도 GitHub push 한 번이면 캘린더 자동 갱신.

### Step 1. GitHub 저장소 생성 (5분)

```bash
# 새 저장소 생성 (public 또는 private 둘 다 OK)
# https://github.com/new

# 로컬에서 클론 후
git clone https://github.com/[당신아이디]/training-calendar.git
cd training-calendar

# 파일 복사
cp /path/to/build_ics.py .
cp /path/to/sessions.json .
cp /path/to/project_3630_w19.ics .

# 커밋 & 푸시
git add .
git commit -m "Initial training calendar"
git push
```

### Step 2. Raw URL 확보

GitHub에서 `project_3630_w19.ics` 클릭 → **Raw** 버튼 클릭 → URL 복사

형식: `https://raw.githubusercontent.com/[아이디]/training-calendar/main/project_3630_w19.ics`

### Step 3. Google Calendar에서 URL 구독

1. [calendar.google.com](https://calendar.google.com) 접속
2. 좌측 **다른 캘린더** 옆 **+** 클릭 → **URL로 만들기**
3. Step 2의 Raw URL 붙여넣기 → **캘린더 추가**
4. 완료 — 6시간마다 자동 동기화

⚠️ Google Calendar의 URL 구독은 **수정 불가** (read-only). 수정은 GitHub에서.

---

## 🔄 매주 새 일정 추가하는 흐름

매주 일요일 저녁, 다음 주 훈련 계획이 정해지면:

```bash
# 1. sessions.json 편집 (새 세션 추가 또는 기존 세션 수정)
vim sessions.json

# 2. ICS 재생성
python3 build_ics.py sessions.json project_3630_w19.ics

# 3. 푸시
git add project_3630_w19.ics sessions.json
git commit -m "Update W20 schedule"
git push

# 4. 끝. 6시간 안에 Google Calendar에 자동 반영됨
```

**또는 Claude에게 부탁**:
> "다음주(W20) 훈련 계획 sessions.json에 추가해줘. 5/13~5/19, 회복주로."

→ Claude가 sessions.json 업데이트 → 새 ICS 생성 → 다운로드 → GitHub push 한 번이면 끝.

---

## 🎯 UID 규칙 (중요)

각 세션에는 고유한 `uid`가 있습니다:

```json
"uid": "w19-thu-z2-strides"
```

**규칙**:
- ✅ 같은 UID + 다른 내용 → Google Calendar가 **수정**으로 인식 → 기존 이벤트 갱신
- ❌ UID 변경 → **새 이벤트** 추가 (기존 이벤트는 그대로 남음)
- ❌ UID 중복 (다른 날짜인데 같은 UID) → 충돌 발생

**권장 명명 규칙**: `w{주차}-{요일}-{세션종류}`
- `w19-thu-z2-strides`
- `w20-sat-tempo-8km`
- `w21-sun-long-15km`

---

## 🧬 운동생리학 룰을 sessions.json에 통합 (선택)

향후 확장 아이디어 — Polar H10 데이터 → 자동 강도 조정:

```python
# 예시: 수면 데이터 기반 자동 조정
# (별도 스크립트로 구현 가능)
def adjust_session(base_session, sleep_data):
    rmssd = sleep_data['rmssd']
    hr_under_40 = sleep_data['hr_under_40_min']
    avg_hr = sleep_data['avg_hr']
    
    # 4조건 동시 충족 → 상향
    if rmssd >= 113 and hr_under_40 >= 100 and avg_hr <= 44:
        base_session['title'] += " [상향]"
        # Z2 페이스 상단, 인터벌 +1세트 등 적용
    
    # 하향 조건
    elif rmssd < 80 or avg_hr > 50:
        base_session['title'] = base_session['title'].replace("인터벌", "회복")
    
    return base_session
```

이 부분은 5/12 TT 결과 본 다음에 같이 만들어요.

---

## 📊 요약

| 단계 | 작업 | 빈도 |
|---|---|---|
| 1회 | GitHub repo 생성 + URL 구독 등록 | 한 번만 |
| 매주 | sessions.json 편집 → ICS 재생성 → push | 5분 |
| 자동 | Google Calendar가 6시간마다 fetch | 자동 |

GitHub 계정만 있으면 영구 무료, 별도 서비스 불필요.

---

## ⚡ 다음 단계 추천

1. **지금 바로**: `project_3630_w19.ics` import (30초)
2. **5/12 TT 후**: GitHub repo 만들고 W20 일정부터 구독 방식 적용
3. **W22~**: sleep_data 자동 fetch + 룰 기반 강도 조정 통합

