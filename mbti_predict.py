"""
MBTI 예측 + 각 성향 축 퍼센트 출력
- svm_model.pkl 로드 후 20개 응답으로 예측
- E/I · N/S · T/F · J/P 각 축 확률 계산
"""

import numpy as np
import joblib

# ─────────────────────────────────────────────
# 1. 모델 로드
# ─────────────────────────────────────────────
data = joblib.load('svm_model.pkl')
svm        = data['model']
le         = data['label_encoder']
col_names  = data['selected_col_names']

# ─────────────────────────────────────────────
# 2. 인터리브 순서 → 모델 피처 순서 매핑
# ─────────────────────────────────────────────
TRAITS   = ['EI', 'NS', 'TF', 'JP']
N_PER    = 5
N_TRAITS = 4

display_order  = [t * N_PER + r for r in range(N_PER) for t in range(N_TRAITS)]
display_traits = [TRAITS[t] for _ in range(N_PER) for t in range(N_TRAITS)]
display_names  = [col_names[i] for i in display_order]

# 16개 클래스에서 각 축별 그룹 인덱스
# 예) E 타입: 클래스명 첫 글자가 'E'인 것들의 인덱스
AXIS_GROUPS = {
    'E': [i for i, c in enumerate(le.classes_) if c[0] == 'E'],
    'I': [i for i, c in enumerate(le.classes_) if c[0] == 'I'],
    'N': [i for i, c in enumerate(le.classes_) if c[1] == 'N'],
    'S': [i for i, c in enumerate(le.classes_) if c[1] == 'S'],
    'T': [i for i, c in enumerate(le.classes_) if c[2] == 'T'],
    'F': [i for i, c in enumerate(le.classes_) if c[2] == 'F'],
    'J': [i for i, c in enumerate(le.classes_) if c[3] == 'J'],
    'P': [i for i, c in enumerate(le.classes_) if c[3] == 'P'],
}

# ─────────────────────────────────────────────
# 3. 예측 함수
# ─────────────────────────────────────────────
def predict_mbti(interleaved_answers: list) -> dict:
    """
    interleaved_answers: 20개 응답 (EI,NS,TF,JP 교차 순서, 값 범위 -3~3)
    반환: 예측 결과 딕셔너리
    """
    if len(interleaved_answers) != 20:
        raise ValueError("응답은 정확히 20개여야 합니다.")

    # 인터리브 순서 → 모델 피처 순서로 재정렬
    model_answers = [0] * 20
    for display_pos, model_pos in enumerate(display_order):
        model_answers[model_pos] = interleaved_answers[display_pos]

    x     = np.array(model_answers).reshape(1, -1)
    proba = svm.predict_proba(x)[0]

    # 예측 MBTI
    pred_label = svm.predict(x)[0]
    pred_mbti  = le.inverse_transform([pred_label])[0]

    # 각 축 퍼센트 계산
    axis_pct = {}
    for letter, indices in AXIS_GROUPS.items():
        axis_pct[letter] = proba[indices].sum() * 100

    return {
        'mbti':     pred_mbti,
        'proba':    proba,
        'axis_pct': axis_pct,
    }

def print_result(result: dict):
    mbti     = result['mbti']
    proba    = result['proba']
    axis_pct = result['axis_pct']

    print("\n" + "=" * 45)
    print(f"  예측 MBTI 유형: {mbti}")
    print("=" * 45)

    # 축별 퍼센트 바 시각화
    axes = [('E', 'I'), ('N', 'S'), ('T', 'F'), ('J', 'P')]
    for a, b in axes:
        pct_a = axis_pct[a]
        pct_b = axis_pct[b]
        bar_len  = 20
        filled_a = round(pct_a / 100 * bar_len)
        bar = '█' * filled_a + '░' * (bar_len - filled_a)
        print(f"  {a} {pct_a:5.1f}%  [{bar}]  {pct_b:5.1f}% {b}")


def get_social_abilities() -> list[dict]:
    """MBTI 조합 기반 사회적 능력치 목록 반환
    """
    return [
        {"title": "현실 판단력",   "formula": "S (감각) + T (사고)"},   # 상황을 빠르게 읽고 논리적으로 대처하는 능력
        {"title": "깊은 공감력",   "formula": "N (직관) + I (내향)"},   # 상대의 감정을 직관적으로 이해하는 능력
        {"title": "관계 신뢰도",   "formula": "F (감정) + J (판단)"},   # 진심 어린 배려로 신뢰를 쌓는 능력
        {"title": "사교적 유연성", "formula": "P (인식) + E (외향)"},   # 다양한 사람과 자유롭게 어울리는 능력
        {"title": "카리스마",      "formula": "N (직관) + E (외향)"},   # 영감을 주고 사람을 끌어당기는 능력
        {"title": "세심한 배려",   "formula": "S (감각) + J (판단)"},   # 디테일을 포착해 꼼꼼하게 챙기는 능력
    ]


# ─────────────────────────────────────────────
# 4. 예시 실행 (더미 응답)
# ─────────────────────────────────────────────
if __name__ == '__main__':
    print("질문 목록 (EI→NS→TF→JP 반복):")
    for i, (trait, name) in enumerate(zip(display_traits, display_names), 1):
        print(f"  Q{i:02d} [{trait}]: {name[:50]}")

    # 예시 1: 외향적/직관적/감정적/인식형 성향 응답
    print("\n\n[예시 1] 외향·직관·감정·인식 성향")
    answers_enfp = [
        # EI  NS   TF   JP  (라운드 1)
          2,   2,  -2,  -2,
        # EI  NS   TF   JP  (라운드 2)
          2,   2,  -2,  -2,
        # EI  NS   TF   JP  (라운드 3)
          3,   3,  -3,  -3,
        # EI  NS   TF   JP  (라운드 4)
          2,   1,  -2,  -1,
        # EI  NS   TF   JP  (라운드 5)
          1,   2,  -1,  -2,
    ]
    result1 = predict_mbti(answers_enfp)
    print_result(result1)

    # 예시 2: 내향적/감각적/사고적/판단형 성향 응답
    print("\n[예시 2] 내향·감각·사고·판단 성향")
    answers_istj = [
        # EI  NS   TF   JP  (라운드 1)
         -2,  -2,   2,   2,
        # EI  NS   TF   JP  (라운드 2)
         -2,  -2,   2,   2,
        # EI  NS   TF   JP  (라운드 3)
         -3,  -3,   3,   3,
        # EI  NS   TF   JP  (라운드 4)
         -2,  -1,   2,   1,
        # EI  NS   TF   JP  (라운드 5)
         -1,  -2,   1,   2,
    ]
    result2 = predict_mbti(answers_istj)
    print_result(result2)

    # 예시 3: 랜덤 응답
    print("\n[예시 3] 랜덤 응답")
    np.random.seed(7)
    answers_random = np.random.randint(-3, 4, size=20).tolist()
    result3 = predict_mbti(answers_random)
    print_result(result3)
