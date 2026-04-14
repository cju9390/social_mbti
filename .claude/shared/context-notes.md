# 맥락노트

> 왜 이렇게 결정했는지, 관련 자료가 어디 있는지 기록하는 문서.
> **새 대화 세션이 열릴 때마다 이 파일을 읽어서 맥락을 복원한다.**
> 작업 단위가 끝날 때마다 업데이트할 것.

---

## 현재 작업

오케스트레이션 세팅 완료 (2026-04-14). 다음 기능 개발로 이동 가능.

## 핵심 결정사항

### 프로젝트 개요
- Flask + SVM 기반 MBTI 예측 및 팀 추천 웹앱
- 설문 응답 → MBTI 16유형 + 사회적 능력 점수 → 팀 구성 추천
- 데이터: 16P.csv(원본), social_mbti_preprocess.csv(전처리), svm_model.pkl(학습된 모델)
- DB: SQLite candidates.db (후보자 저장, JSON result 컬럼)

### 기술 스택
- Backend: Flask (Python)
- ML: scikit-learn SVM, joblib
- DB: SQLite (sqlite3)
- Frontend: Jinja2 템플릿 + 바닐라 JS

### 오케스트레이션 결정사항 (2026-04-14)
- `.claude/shared/` 를 공유 상태 디렉토리로 통일 (hooks 경로 버그 수정)
- domain-agent: `social-mbti-developer` — Flask/SVM/SQLite/팀추천 전담
- auditor-agent: `code-review-auditor` — Flask 입력검증/SQL인젝션/모델로드 집중 감사
- 스킬 챕터 3개 추가: ch03(MBTI ML), ch04(Flask/DB), ch05(팀추천)

## 자료 위치

| 자료 | 경로 |
|------|------|
| 기획서 | `docs/PROJECT_SPEC.md` (미작성) |
| 이 맥락노트 | `.claude/shared/context-notes.md` |
| 체크리스트 | `.claude/shared/checklist.md` |
| 수정기록 | `.claude/shared/change-log.md` |
| MBTI 스킬 | `.claude/skills/ch03-mbti-ml.md` |
| Flask/DB 스킬 | `.claude/skills/ch04-flask-db.md` |
| 팀추천 스킬 | `.claude/skills/ch05-team-recommend.md` |
