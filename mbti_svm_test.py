"""
저장된 SVM 모델로 예측 테스트
- svm_model.pkl 로드 후 샘플 예측 및 성능 검증
- 질문 표시 순서: EI→NS→TF→JP 반복 (5라운드 × 4트레이트 = 20개)
"""

import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, classification_report

# ─────────────────────────────────────────────
# 1. 저장된 모델 로드
# ─────────────────────────────────────────────
data = joblib.load('svm_model.pkl')

svm           = data['model']
le            = data['label_encoder']
col_positions = data['selected_col_positions']
col_names     = data['selected_col_names']

print("svm_model.pkl 로드 완료")
print(f"  특성 수  : {len(col_positions)}개")
print(f"  학습시 Accuracy: {data['test_accuracy']:.4f}")

# ─────────────────────────────────────────────
# 2. 인터리브 순서 정의
#    모델 피처 저장 순서: [EI×5, NS×5, TF×5, JP×5]
#    표시/입력 순서    : EI,NS,TF,JP, EI,NS,TF,JP, ... (5라운드)
# ─────────────────────────────────────────────
TRAITS   = ['EI', 'NS', 'TF', 'JP']
N_PER    = 5   # trait당 질문 수
N_TRAITS = 4

# display_order[i] = 모델 피처 인덱스
# 예) i=0 → EI[0]=0, i=1 → NS[0]=5, i=2 → TF[0]=10, i=3 → JP[0]=15
#     i=4 → EI[1]=1, i=5 → NS[1]=6, ...
display_order = [
    t * N_PER + r
    for r in range(N_PER)
    for t in range(N_TRAITS)
]
display_traits = [TRAITS[t] for _ in range(N_PER) for t in range(N_TRAITS)]
display_names  = [col_names[i] for i in display_order]

# ─────────────────────────────────────────────
# 3. 데이터 로드 후 Test set 재현
# ─────────────────────────────────────────────
SEED = data['seed']

try:
    df = pd.read_csv('social_mbti_preprocess.csv', encoding='utf-8-sig')
except Exception:
    df = pd.read_csv('social_mbti_preprocess.csv', encoding='utf-8')

X_all = df.iloc[:, col_positions].values
y_all = le.transform(df['Personality'].values)

_, X_test, _, y_test = train_test_split(
    X_all, y_all, test_size=0.2, random_state=SEED, stratify=y_all
)

# ─────────────────────────────────────────────
# 4. 전체 Test set 성능 검증
# ─────────────────────────────────────────────
y_pred = svm.predict(X_test)
acc = accuracy_score(y_test, y_pred)
f1  = f1_score(y_test, y_pred, average='weighted')

print(f"\n[Test set 검증 결과] ({len(X_test)}건)")
print(f"  Accuracy     : {acc:.4f}")
print(f"  F1 (weighted): {f1:.4f}")
print()
print(classification_report(y_test, y_pred, target_names=le.classes_))

# ─────────────────────────────────────────────
# 5. 개별 샘플 예측 예시 (Test set 첫 5건)
# ─────────────────────────────────────────────
print("=" * 55)
print("  개별 샘플 예측 예시 (첫 5건)")
print("=" * 55)
proba = svm.predict_proba(X_test[:5])

for i in range(5):
    actual    = le.inverse_transform([y_test[i]])[0]
    predicted = le.inverse_transform([y_pred[i]])[0]
    top_prob  = proba[i].max()
    match     = "O" if actual == predicted else "X"
    print(f"  [{match}] 실제: {actual:<6}  예측: {predicted:<6}  확률: {top_prob:.2%}")

# ─────────────────────────────────────────────
# 6. 예측 함수 (EI→NS→TF→JP 교차 순서로 입력)
# ─────────────────────────────────────────────
def predict_mbti(interleaved_answers: list) -> str:
    """
    interleaved_answers: 20개 응답값
      입력 순서: EI,NS,TF,JP, EI,NS,TF,JP, ... (5라운드)
      값 범위 : -3 ~ 3
    """
    if len(interleaved_answers) != 20:
        raise ValueError("응답은 정확히 20개여야 합니다.")

    # 인터리브 순서 → 모델 피처 순서로 재정렬
    model_answers = [0] * 20
    for display_pos, model_pos in enumerate(display_order):
        model_answers[model_pos] = interleaved_answers[display_pos]

    x = np.array(model_answers).reshape(1, -1)
    pred_label = svm.predict(x)[0]
    pred_mbti  = le.inverse_transform([pred_label])[0]
    proba      = svm.predict_proba(x)[0]

    top3_idx = np.argsort(proba)[::-1][:3]
    print(f"\n예측 결과: {pred_mbti}")
    print("상위 3개 후보:")
    for idx in top3_idx:
        print(f"  {le.classes_[idx]}: {proba[idx]:.2%}")
    return pred_mbti

# ─────────────────────────────────────────────
# 7. 질문 목록 출력 (EI→NS→TF→JP 교차 순서)
# ─────────────────────────────────────────────
print("\n" + "=" * 55)
print("  질문 목록 (EI→NS→TF→JP 반복)")
print("=" * 55)
for i, (trait, name) in enumerate(zip(display_traits, display_names), 1):
    print(f"  Q{i:02d} [{trait}]: {name[:45]}")

# ─────────────────────────────────────────────
# 8. 더미 응답으로 예측 예시
# ─────────────────────────────────────────────
np.random.seed(0)
dummy_answers = np.random.randint(-3, 4, size=20).tolist()
predict_mbti(dummy_answers)
