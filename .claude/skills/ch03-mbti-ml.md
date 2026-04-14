# MBTI 예측 / SVM 모델 스킬

> 트리거: `mbti`, `예측`, `svm`, `모델`, `분류`, `train`, `학습`, `social score`, `사회적 능력`

---

## 모델 구조

- **알고리즘**: SVM (Support Vector Machine) — `svm_model.pkl` (joblib 직렬화)
- **분류 축**: E/I, N/S, T/F, J/P 각각 독립적인 이진 분류 → MBTI 16가지
- **입력**: 설문 답변 벡터 (숫자 배열, `questions.py`의 `display_names` 순서)
- **출력**: 각 축의 예측 레이블 + 확률값(axis_pct)

## 주요 함수 시그니처

```python
# mbti_predict.py
def predict_mbti(answers: list) -> dict:
    """
    Returns:
        {
          'mbti': 'ENFP',
          'axis_pct': {'EI': 72, 'NS': 58, 'TF': 61, 'JP': 45}
        }
    """

def calc_social_scores(result: dict) -> dict:
    """
    MBTI 결과 → 사회적 능력 점수 (리더십, 공감, 창의, 실행력 등)
    """
```

## 모델 재학습 패턴

```python
# mbti_svm_train.py 수정 후 실행
# 1. 전처리: mbti_preprocess_.py → social_mbti_preprocess.csv
# 2. 학습: mbti_svm_train.py → svm_model.pkl 갱신
# 3. 검증: mbti_svm_test.py 실행하여 정확도 확인
```

## 주의사항

- `svm_model.pkl`은 직접 편집하지 않는다. 재학습 스크립트를 통해 갱신.
- 입력 벡터 차원이 학습 데이터와 반드시 일치해야 한다.
- `predict_mbti(answers)` 호출 전 `len(answers) == len(display_names)` 검증 필수.
- 모델 로드 실패 시 fallback 처리:

```python
try:
    model = joblib.load('svm_model.pkl')
except FileNotFoundError:
    raise RuntimeError("svm_model.pkl을 찾을 수 없습니다. mbti_svm_train.py를 먼저 실행하세요.")
```

## social_scores 구조

`calc_social_scores`가 반환하는 dict 키:
- 리더십, 공감능력, 창의성, 실행력, 소통력, 협업력 (또는 유사 이름)
- 각 점수는 0~100 범위의 float
