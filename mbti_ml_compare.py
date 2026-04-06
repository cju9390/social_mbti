import random
import time
import warnings
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
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
# 2. trait별 랜덤 5개 선택
# ─────────────────────────────────────────────
SEED = 42
random.seed(SEED)
np.random.seed(SEED)

selected_indices = {}
all_selected_col_positions = []

for trait, indices in TRAIT_INDICES.items():
    chosen = sorted(random.sample(indices, 5))
    selected_indices[trait] = chosen
    all_selected_col_positions.extend(chosen)

print(f"총 선택 질문 수: {len(all_selected_col_positions)}개")

# ─────────────────────────────────────────────
# 3. Feature / Target 분리
# ─────────────────────────────────────────────
X = df.iloc[:, all_selected_col_positions].values
y_raw = df['Personality'].values

le = LabelEncoder()
y = le.fit_transform(y_raw)

print(f"Feature shape: {X.shape}")
print(f"Target classes ({len(le.classes_)}): {list(le.classes_)}")

# ─────────────────────────────────────────────
# 4. 80 / 20 분할
# ─────────────────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=SEED, stratify=y
)
print(f"\nTrain: {X_train.shape[0]}  /  Test: {X_test.shape[0]}")

# per-trait 정확도 계산용: 실제 레이블 문자열
y_test_str  = le.inverse_transform(y_test)   # e.g. 'INTJ'
TRAIT_POS   = {'EI': 0, 'NS': 1, 'TF': 2, 'JP': 3}

def per_trait_acc(y_true_str, y_pred_str):
    """16-class 예측에서 각 이진 축(E/I, N/S, T/F, J/P) 정확도 계산"""
    result = {}
    for trait, pos in TRAIT_POS.items():
        t_true = [s[pos] for s in y_true_str]
        t_pred = [s[pos] for s in y_pred_str]
        result[trait] = np.mean(np.array(t_true) == np.array(t_pred))
    return result

# ─────────────────────────────────────────────
# 5. 모델 정의
# ─────────────────────────────────────────────
models = {
    'Logistic Regression': LogisticRegression(max_iter=1000, random_state=SEED),
    'Random Forest':       RandomForestClassifier(n_estimators=200, random_state=SEED, n_jobs=-1),
    'Gradient Boosting':   GradientBoostingClassifier(n_estimators=200, random_state=SEED),
    'SVM (RBF)':           SVC(kernel='rbf', random_state=SEED, probability=True),
    'KNN (k=7)':           KNeighborsClassifier(n_neighbors=7),
}

try:
    from xgboost import XGBClassifier
    models['XGBoost'] = XGBClassifier(
        n_estimators=200, random_state=SEED,
        eval_metric='mlogloss', verbosity=0, n_jobs=-1
    )
    print("XGBoost 사용 가능")
except ImportError:
    print("XGBoost 미설치 -> 건너뜀")

# ─────────────────────────────────────────────
# 6. 학습 / 평가
# ─────────────────────────────────────────────
print("\n" + "=" * 75)
print(f"  모델 비교 결과 (Test 20%  |  16 classes)")
print("=" * 75)
print(f"{'모델':<22} {'Acc':>7} {'F1-W':>7} {'F1-M':>7}  "
      f"{'CV(5)':>12}  {'Time':>6}")
print("-" * 75)

results = []
for name, model in models.items():
    t0 = time.time()
    model.fit(X_train, y_train)
    train_sec = time.time() - t0

    y_pred     = model.predict(X_test)
    acc        = accuracy_score(y_test, y_pred)
    f1_w       = f1_score(y_test, y_pred, average='weighted')
    f1_m       = f1_score(y_test, y_pred, average='macro')

    # 5-fold CV (학습셋만 사용, 시간 절약을 위해 3-fold로도 가능)
    cv_scores  = cross_val_score(model, X_train, y_train, cv=5,
                                 scoring='accuracy', n_jobs=-1)
    cv_str     = f"{cv_scores.mean():.4f}±{cv_scores.std():.4f}"

    # per-trait 정확도
    y_pred_str = le.inverse_transform(y_pred)
    trait_acc  = per_trait_acc(y_test_str, y_pred_str)

    results.append({
        'name': name, 'acc': acc, 'f1_w': f1_w, 'f1_m': f1_m,
        'cv_mean': cv_scores.mean(), 'cv_str': cv_str,
        'trait_acc': trait_acc, 'y_pred': y_pred,
        'time': train_sec, 'model': model,
    })
    print(f"{name:<22} {acc:>7.4f} {f1_w:>7.4f} {f1_m:>7.4f}  "
          f"{cv_str:>12}  {train_sec:>5.1f}s")

# ─────────────────────────────────────────────
# 7. per-trait 정확도 비교표
# ─────────────────────────────────────────────
print("\n" + "=" * 60)
print("  이진 축별 정확도 (E/I · N/S · T/F · J/P)")
print("=" * 60)
print(f"{'모델':<22} {'EI':>7} {'NS':>7} {'TF':>7} {'JP':>7}")
print("-" * 60)
for r in results:
    ta = r['trait_acc']
    print(f"{r['name']:<22} {ta['EI']:>7.4f} {ta['NS']:>7.4f} "
          f"{ta['TF']:>7.4f} {ta['JP']:>7.4f}")

# ─────────────────────────────────────────────
# 8. 최고 모델 상세 리포트 (Accuracy 기준)
# ─────────────────────────────────────────────
best = max(results, key=lambda r: r['acc'])

print("\n" + "=" * 60)
print(f"  최고 모델: {best['name']}")
print(f"  Accuracy : {best['acc']:.4f}  |  F1-weighted: {best['f1_w']:.4f}"
      f"  |  F1-macro: {best['f1_m']:.4f}")
print(f"  CV(5-fold): {best['cv_str']}")
print("=" * 60)
print(classification_report(y_test, best['y_pred'], target_names=le.classes_))
