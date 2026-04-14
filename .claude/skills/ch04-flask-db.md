# Flask 라우트 / SQLite DB 스킬

> 트리거: `flask`, `라우트`, `route`, `api`, `endpoint`, `db`, `데이터베이스`, `후보`, `candidate`, `sqlite`, `템플릿`, `jinja`

---

## Flask 앱 구조

```python
# app.py 핵심 라우트
GET  /              → index.html 렌더링 (questions=QUESTIONS)
POST /submit        → JSON 입력 → 예측 → DB 저장 → JSON 응답
GET  /candidates    → ?name=xxx 자기 제외 후보 목록
GET  /team          → 팀 추천 결과
```

## 입력 검증 패턴 (필수)

```python
@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    if not data:
        return jsonify({'error': '요청 본문이 없습니다'}), 400

    name = data.get('name', '').strip()
    if not name:
        return jsonify({'error': '이름을 입력하세요'}), 400

    answers = data.get('answers', [])
    if len(answers) != len(display_names):
        return jsonify({'error': f'답변 수가 올바르지 않습니다 (기대: {len(display_names)})'}), 400
    ...
```

## SQLite 패턴 (candidate_db.py)

```python
import sqlite3, json

DB_PATH = 'candidates.db'

def get_all_candidates():
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute('SELECT * FROM candidates').fetchall()
    return [
        {'name': r['name'], 'result': json.loads(r['result'])}
        for r in rows
    ]

def add_candidate_from_result(name: str, result: dict):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            'INSERT OR REPLACE INTO candidates (name, result) VALUES (?, ?)',
            (name, json.dumps(result, ensure_ascii=False))
        )
```

## 스키마 초기화

```python
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS candidates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                result TEXT NOT NULL
            )
        ''')
```

## 에러 응답 일관성

모든 라우트에서 에러는 JSON으로 반환:
```python
return jsonify({'error': '메시지'}), 상태코드
```
HTML 에러 페이지가 API 응답으로 나오면 안 된다.

## Jinja2 템플릿 패턴

```html
<!-- templates/index.html -->
{% for q in questions %}
  <div class="question">{{ q }}</div>
{% endfor %}
```

템플릿에서 사용자 입력을 직접 렌더링할 때 XSS 방어는 Jinja2 auto-escaping이 처리한다.
`{{ value | safe }}` 사용 시 반드시 입력 검증 선행.
