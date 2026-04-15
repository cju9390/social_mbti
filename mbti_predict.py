"""
MBTI 예측 + 각 성향 축 퍼센트 출력
- 4개 독립 이진 SVM: EI / NS / TF / JP
- 각 축의 확률이 독립적으로 0~100% 산출됨
"""

import sys
import numpy as np
import joblib

sys.stdout.reconfigure(encoding='utf-8')

# ─────────────────────────────────────────────
# 1. 모델 로드
# ─────────────────────────────────────────────
data       = joblib.load('svm_model.pkl')
models     = data['models']        # {'EI': SVC, 'NS': SVC, 'TF': SVC, 'JP': SVC}
le         = data['label_encoder']
col_names  = data['selected_col_names']
TRAIT_META = data['trait_meta']    # {'EI': {'pos':0, 'pos_label':'E'}, ...}


# ─────────────────────────────────────────────
# 2. 인터리브 순서 → 모델 피처 순서 매핑
# ─────────────────────────────────────────────
TRAITS   = ['EI', 'NS', 'TF', 'JP']
N_TRAITS = 4
N_PER    = len(col_names) // N_TRAITS   # 32개면 8

display_order  = [t * N_PER + r for r in range(N_PER) for t in range(N_TRAITS)]
display_traits = [TRAITS[t] for _ in range(N_PER) for t in range(N_TRAITS)]
display_names  = [col_names[i] for i in display_order]


# ─────────────────────────────────────────────
# 3. 예측 함수
# ─────────────────────────────────────────────
def predict_mbti(interleaved_answers: list) -> dict:
    """
    interleaved_answers: 32개 응답 (EI,NS,TF,JP 교차 순서, 값 범위 -3~3)
    반환: 예측 결과 딕셔너리
    """
    expected = N_PER * N_TRAITS
    if len(interleaved_answers) != expected:
        raise ValueError(f"응답은 정확히 {expected}개여야 합니다.")

    # 인터리브 → 모델 순서 재정렬 (axis별 N_PER개씩: [EI*N | NS*N | TF*N | JP*N])
    model_answers = [0] * expected
    for display_pos, model_pos in enumerate(display_order):
        model_answers[model_pos] = interleaved_answers[display_pos]

    # 16P.csv 인코딩: 음수=동의, 양수=비동의 (앱의 +3=동의와 반전)
    model_arr = np.array([-x for x in model_answers])

    # 각 축 이진 예측
    mbti_chars = []
    axis_pct   = {}

    for t_idx, trait in enumerate(TRAITS):
        # 32개 전체를 각 분류기에 입력 (축간 상관관계 활용)
        x_trait = model_arr.reshape(1, -1)
        proba   = models[trait].predict_proba(x_trait)[0]

        # classes_: [0, 1] → proba[0]=P(negative), proba[1]=P(positive)
        pos_label = TRAIT_META[trait]['pos_label']  # E / N / T / J
        neg_label = {'E': 'I', 'N': 'S', 'T': 'F', 'J': 'P'}[pos_label]

        p_pos = float(proba[1]) * 100   # P(E), P(N), P(T), P(J)
        p_neg = float(proba[0]) * 100   # P(I), P(S), P(F), P(P)

        axis_pct[pos_label] = round(p_pos, 1)
        axis_pct[neg_label] = round(p_neg, 1)

        mbti_chars.append(pos_label if p_pos >= p_neg else neg_label)

    pred_mbti = ''.join(mbti_chars)

    return {
        'mbti':     pred_mbti,
        'proba':    [],          # 기존 호환성 유지 (16-class proba 불필요)
        'axis_pct': axis_pct,
    }


def print_result(result: dict):
    mbti     = result['mbti']
    axis_pct = result['axis_pct']

    print("\n" + "=" * 45)
    print(f"  예측 MBTI 유형: {mbti}")
    print("=" * 45)

    axes = [('E', 'I'), ('N', 'S'), ('T', 'F'), ('J', 'P')]
    for a, b in axes:
        pct_a   = axis_pct[a]
        pct_b   = axis_pct[b]
        bar_len = 20
        filled  = round(pct_a / 100 * bar_len)
        bar     = '█' * filled + '░' * (bar_len - filled)
        print(f"  {a} {pct_a:5.1f}%  [{bar}]  {pct_b:5.1f}% {b}")


def get_social_abilities() -> list[dict]:
    """MBTI 조합 기반 사회적 능력치 목록 반환"""
    return [
        {"title": "통찰력",  "traits": ("S", "T"), "formula": "S (감각) + T (사고)"},
        {"title": "감수성",  "traits": ("N", "I"), "formula": "N (직관) + I (내향)"},
        {"title": "유대감",  "traits": ("F", "J"), "formula": "F (감정) + J (판단)"},
        {"title": "친화력",  "traits": ("P", "E"), "formula": "P (인식) + E (외향)"},
        {"title": "열정",    "traits": ("N", "E"), "formula": "N (직관) + E (외향)"},
        {"title": "책임감",  "traits": ("S", "J"), "formula": "S (감각) + J (판단)"},
    ]


def calc_social_scores(result: dict) -> list[dict]:
    """예측 결과로 사회적 능력치 점수(1~10) 계산"""
    axis_pct = result['axis_pct']
    scores = []
    for ability in get_social_abilities():
        t1, t2 = ability['traits']
        score = round((axis_pct[t1] + axis_pct[t2]) / 20, 1)
        score = max(1.0, min(10.0, score))
        scores.append({"title": ability['title'], "formula": ability['formula'], "score": score})
    return scores


def print_social_scores(result: dict):
    scores = calc_social_scores(result)
    print("\n" + "=" * 45)
    print("  사회적 능력치 (1~10)")
    print("=" * 45)
    for item in scores:
        bar_len = 20
        filled  = round(item['score'] / 10 * bar_len)
        bar     = '█' * filled + '░' * (bar_len - filled)
        print(f"  {item['title']:<8}  [{bar}]  {item['score']:4.1f}")


# ─────────────────────────────────────────────
# 4. 예시 실행
# ─────────────────────────────────────────────
if __name__ == '__main__':
    print("질문 목록 (EI→NS→TF→JP 반복):")
    for i, (trait, name) in enumerate(zip(display_traits, display_names), 1):
        print(f"  Q{i:02d} [{trait}]: {name[:60]}")

    print("\n\n[예시 1] 외향·직관·감정·인식 성향 (ENFP)")
    answers_enfp = [
          2,   2,  -2,  -2,
          2,   2,  -2,  -2,
          3,   3,  -3,  -3,
          2,   2,  -2,  -2,
          2,   1,  -2,  -1,
          1,   2,  -1,  -2,
          2,   2,  -2,  -2,
          1,   1,  -1,  -1,
    ]
    result1 = predict_mbti(answers_enfp)
    print_result(result1)
    print_social_scores(result1)

    print("\n[예시 2] 내향·감각·사고·판단 성향 (ISTJ)")
    answers_istj = [
         -2,  -2,   2,   2,
         -2,  -2,   2,   2,
         -3,  -3,   3,   3,
         -2,  -2,   2,   2,
         -2,  -1,   2,   1,
         -1,  -2,   1,   2,
         -2,  -2,   2,   2,
         -1,  -1,   1,   1,
    ]
    result2 = predict_mbti(answers_istj)
    print_result(result2)
    print_social_scores(result2)
