"""
SVM (RBF) 모델 학습 및 저장
- trait별 랜덤 5개 * 4 = 20개 질문으로 학습
- 저장 파일: svm_model.pkl (모델 + 메타데이터 포함)
"""

import random
import warnings
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, f1_score, classification_report
from sklearn.preprocessing import LabelEncoder

warnings.filterwarnings('ignore')

# ─────────────────────────────────────────────
# 1. 데이터 로드
# ─────────────────────────────────────────────
try:
    df = pd.read_csv('social_mbti_preprocess.csv', encoding='utf-8-sig')
except Exception:
    df = pd.read_csv('social_mbti_preprocess.csv', encoding='utf-8')

TRAIT_INDICES = {
    'EI': [1,  6, 11, 16, 21, 26, 31, 36, 41, 46, 51, 56],
    'NS': [2,  7, 12, 17, 22, 27, 32, 37, 42, 47, 52, 57],
    'TF': [3,  8, 13, 18, 23, 28, 33, 38, 43, 48, 53, 58],
    'JP': [4,  9, 14, 19, 24, 29, 34, 39, 44, 49, 54, 59],
}

# ─────────────────────────────────────────────
# 2. trait별 랜덤 5개 선택 (seed=42 고정)
# ─────────────────────────────────────────────
SEED = 42
random.seed(SEED)
np.random.seed(SEED)

selected_indices = {}
all_col_positions = []

for trait, indices in TRAIT_INDICES.items():
    chosen = sorted(random.sample(indices, 5))
    selected_indices[trait] = chosen
    all_col_positions.extend(chosen)

# 선택된 컬럼명 목록
selected_col_names = [df.columns[i] for i in all_col_positions]

# EI→NS→TF→JP 교차 순서로 출력
TRAITS   = list(TRAIT_INDICES.keys())
N_PER    = 5
N_TRAITS = len(TRAITS)

display_order  = [t * N_PER + r for r in range(N_PER) for t in range(N_TRAITS)]
display_traits = [TRAITS[t] for _ in range(N_PER) for t in range(N_TRAITS)]
display_names  = [selected_col_names[i] for i in display_order]

print("선택된 20개 질문 (EI→NS→TF→JP 반복):")
for i, (trait, name) in enumerate(zip(display_traits, display_names), 1):
    print(f"  Q{i:02d} [{trait}]: {name[:50]}")

# ─────────────────────────────────────────────
# 3. Feature / Target 분리
# ─────────────────────────────────────────────
X = df.iloc[:, all_col_positions].values
y_raw = df['Personality'].values

le = LabelEncoder()
y = le.fit_transform(y_raw)

# ─────────────────────────────────────────────
# 4. 80 / 20 분할
# ─────────────────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=SEED, stratify=y
)
print(f"\nTrain: {X_train.shape[0]}  /  Test: {X_test.shape[0]}")

# ─────────────────────────────────────────────
# 5. SVM (RBF) 학습
# ─────────────────────────────────────────────
print("\nSVM 학습 중...")
svm = SVC(kernel='rbf', random_state=SEED, probability=True)
svm.fit(X_train, y_train)

y_pred = svm.predict(X_test)
acc = accuracy_score(y_test, y_pred)
f1  = f1_score(y_test, y_pred, average='weighted')

print(f"\n[Test 결과]")
print(f"  Accuracy     : {acc:.4f}")
print(f"  F1 (weighted): {f1:.4f}")
print()
print(classification_report(y_test, y_pred, target_names=le.classes_))

# ─────────────────────────────────────────────
# 6. 모델 + 메타데이터 저장
# ─────────────────────────────────────────────
save_data = {
    'model': svm,
    'label_encoder': le,
    'selected_col_positions': all_col_positions,   # df 열 인덱스 (0-based)
    'selected_col_names': selected_col_names,       # 한국어 컬럼명 리스트
    'selected_indices_by_trait': selected_indices,  # trait -> [col positions]
    'classes': list(le.classes_),                   # MBTI 16개 레이블
    'seed': SEED,
    'test_accuracy': acc,
    'test_f1_weighted': f1,
}

joblib.dump(save_data, 'svm_model.pkl')
print("svm_model.pkl 저장 완료")
print(f"  - 모델      : SVC(kernel='rbf', probability=True)")
print(f"  - 특성 수   : {len(all_col_positions)}개")
print(f"  - 클래스 수 : {len(le.classes_)}개")
print(f"  - Accuracy  : {acc:.4f}")
