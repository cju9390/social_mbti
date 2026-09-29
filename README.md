# 상호 보완 동료 추천 시스템 (Social MBTI)

짧은 성향 설문으로 MBTI 4개 축을 예측하고, 그 결과를 6가지 사회적 능력치로 바꿔 **내 약점을 보완하는 팀원 3명**을 후보 풀에서 추천하는 Flask 웹앱입니다.

| 항목 | 내용 |
|---|---|
| 기간 | 2026.04 |
| 형태 | 개인 프로젝트 |
| 데이터 | [60k Responses of 16 Personalities Test (Kaggle)](https://www.kaggle.com/datasets/anshulmehtakaggl/60k-responses-of-16-personalities-test-mbt) |

## 동작 방식

1. **문항 축소** — 원본 60문항 중 축(EI/NS/TF/JP)별로 일부 문항만 뽑아 설문 길이를 줄임 (seed 고정)
2. **축별 이진 분류기 4개** — 각 축의 확률을 독립적으로 0~100%로 산출 (`mbti_ml_compare.py`로 여러 모델 성능 비교 후 선정)
3. **사회적 능력치 변환** — 축별 확률을 6가지 능력치 점수로 계산
4. **팀 추천** — 본인 포함 4인 팀의 능력치 평균에서 **최솟값을 최대화**(약점 보완)하고 총합으로 정렬해 3명 추천, 팀 강점 요약 문장 생성
5. **후보 DB** — SQLite에 설문 참여자를 후보로 저장

## 해결한 문제

- numpy `float32`가 JSON 직렬화되지 않아 결과 API가 500 에러를 내던 문제 수정
- 팀 추천 결과에 AI 강점 분석 요약 추가

## 파일 구조

```
app.py               Flask 서버 (설문 제출 → 예측 → DB 저장 → 팀 추천)
mbti_predict.py      축별 확률 예측 + 사회적 능력치 계산
team_recommend.py    약점 보완형 팀 구성 추천
candidate_db.py      후보 SQLite DB 관리
mbti_ml_compare.py   분류 모델 비교 실험
mbti_svm_train.py    최종 모델 학습·저장
mbti_preprocess_.py  데이터 전처리
templates/index.html 프론트엔드
```

## 실행

```bash
pip install flask scikit-learn xgboost optuna pandas numpy joblib
python mbti_svm_train.py   # 모델 학습 → svm_model.pkl
python app.py
```

## 개발 방식

Claude Code를 에이전트·훅·스킬 구성으로 오케스트레이션해 개발했습니다(`.claude/`). AI가 만든 코드는 직접 읽고 검증한 뒤 반영했습니다.
