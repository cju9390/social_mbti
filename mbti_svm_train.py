"""
XGBoost 모델 학습 및 저장 — 4개 독립 이진 분류기
- Optuna 하이퍼파라미터 튜닝 적용
- 축별 독립 이진 XGBoost: EI / NS / TF / JP
- 저장 파일: svm_model.pkl
"""

import random
import warnings
import pandas as pd
import numpy as np
import joblib
import optuna
from sklearn.model_selection import train_test_split, cross_val_score
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, f1_score
from sklearn.preprocessing import LabelEncoder

warnings.filterwarnings('ignore')
optuna.logging.set_verbosity(optuna.logging.WARNING)

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

TRAIT_META = {
    'EI': {'pos': 0, 'pos_label': 'E'},
    'NS': {'pos': 1, 'pos_label': 'N'},
    'TF': {'pos': 2, 'pos_label': 'T'},
    'JP': {'pos': 3, 'pos_label': 'J'},
}

# ─────────────────────────────────────────────
# 2. 축별 랜덤 8개 선택 (seed=42 고정)
# ─────────────────────────────────────────────
SEED = 42
random.seed(SEED)
np.random.seed(SEED)

selected_indices = {}
all_col_positions = []

for trait, indices in TRAIT_INDICES.items():
    chosen = sorted(random.sample(indices, 8))
    selected_indices[trait] = chosen
    all_col_positions.extend(chosen)

selected_col_names = [df.columns[i] for i in all_col_positions]

TRAITS   = list(TRAIT_INDICES.keys())
N_PER    = 8
N_TRAITS = len(TRAITS)

display_order  = [t * N_PER + r for r in range(N_PER) for t in range(N_TRAITS)]
display_traits = [TRAITS[t] for _ in range(N_PER) for t in range(N_TRAITS)]
display_names  = [selected_col_names[i] for i in display_order]

print("선택된 32개 질문 (EI→NS→TF→JP 반복):")
for i, (trait, name) in enumerate(zip(display_traits, display_names), 1):
    print(f"  Q{i:02d} [{trait}]: {name[:60]}")

# ─────────────────────────────────────────────
# 3. 전체 X 행렬
# ─────────────────────────────────────────────
X_all = df.iloc[:, all_col_positions].values

# ─────────────────────────────────────────────
# 4. Optuna 튜닝 + 학습
# ─────────────────────────────────────────────
N_TRIALS = 50  # 트라이얼 수 (늘릴수록 정확하지만 오래 걸림)

models     = {}
accuracies = {}
f1_scores  = {}
best_params_all = {}

print()
for trait, meta in TRAIT_META.items():
    y = (df['Personality'].str[meta['pos']] == meta['pos_label']).astype(int).values
    X_tr, X_te, y_tr, y_te = train_test_split(
        X_all, y, test_size=0.2, random_state=SEED, stratify=y
    )

    def objective(trial):
        clf = XGBClassifier(
            n_estimators      = trial.suggest_int('n_estimators', 100, 600),
            max_depth         = trial.suggest_int('max_depth', 3, 7),
            learning_rate     = trial.suggest_float('learning_rate', 0.01, 0.3, log=True),
            subsample         = trial.suggest_float('subsample', 0.6, 1.0),
            colsample_bytree  = trial.suggest_float('colsample_bytree', 0.6, 1.0),
            min_child_weight  = trial.suggest_int('min_child_weight', 1, 7),
            gamma             = trial.suggest_float('gamma', 0.0, 0.5),
            eval_metric       = 'logloss',
            random_state      = SEED,
            n_jobs            = -1,
        )
        return cross_val_score(clf, X_tr, y_tr, cv=3, scoring='accuracy', n_jobs=-1).mean()

    study = optuna.create_study(direction='maximize', sampler=optuna.samplers.TPESampler(seed=SEED))
    study.optimize(objective, n_trials=N_TRIALS, show_progress_bar=False)

    best = study.best_params
    best_params_all[trait] = best

    clf = XGBClassifier(**best, eval_metric='logloss', random_state=SEED, n_jobs=-1)
    clf.fit(X_tr, y_tr)

    y_pred = clf.predict(X_te)
    acc = accuracy_score(y_te, y_pred)
    f1  = f1_score(y_te, y_pred, average='weighted')

    models[trait]     = clf
    accuracies[trait] = acc
    f1_scores[trait]  = f1

    print(f"[{trait}]  Accuracy: {acc:.4f}  F1: {f1:.4f}  best_params: {best}")

# ─────────────────────────────────────────────
# 5. 모델 + 메타데이터 저장
# ─────────────────────────────────────────────
le = LabelEncoder()
le.fit(df['Personality'].values)

save_data = {
    'models':                    models,
    'label_encoder':             le,
    'selected_col_positions':    all_col_positions,
    'selected_col_names':        selected_col_names,
    'selected_indices_by_trait': selected_indices,
    'trait_meta':                TRAIT_META,
    'classes':                   list(le.classes_),
    'seed':                      SEED,
    'accuracies':                accuracies,
    'f1_scores':                 f1_scores,
    'best_params':               best_params_all,
}

joblib.dump(save_data, 'svm_model.pkl')
print()
print("svm_model.pkl 저장 완료")
print(f"  EI acc={accuracies['EI']:.4f}  NS acc={accuracies['NS']:.4f}  "
      f"TF acc={accuracies['TF']:.4f}  JP acc={accuracies['JP']:.4f}")
avg = sum(accuracies.values()) / len(accuracies)
print(f"  평균 정확도: {avg:.4f}")
