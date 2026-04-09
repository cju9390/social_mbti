"""
팀 구성 추천 시스템
- seed(본인) 의 사회적 능력치 약점을 보완하는 3명을 후보 리스트에서 추천
- 팀 점수 = 4명 능력치 평균, 최소 능력치 최대화(밸런스) + 총합 가중 정렬
"""

import sys
import itertools
import numpy as np
from mbti_predict import predict_mbti, calc_social_scores, get_social_abilities
from candidate_db import init_db, get_all_candidates, seed_candidates

sys.stdout.reconfigure(encoding='utf-8')


# ─────────────────────────────────────────────
# 핵심 함수
# ─────────────────────────────────────────────

def scores_to_vector(scores: list[dict]) -> np.ndarray:
    """calc_social_scores 결과 → numpy 벡터"""
    return np.array([s['score'] for s in scores])


def team_score_stats(member_vectors: list[np.ndarray]) -> dict:
    """
    member_vectors: 각 팀원의 능력치 벡터 리스트
    반환: 능력치별 평균, 최솟값, 총합
    """
    mat = np.stack(member_vectors)          # (n_members, 6)
    avg = mat.mean(axis=0)
    return {
        'avg':    avg,
        'min':    avg.min(),
        'total':  avg.sum(),
    }


def recommend_team(
    seed_result: dict,
    candidates: list[dict],
    top_k: int = 3,
    max_candidates: int = 200,
) -> list[dict]:
    """
    seed_result  : predict_mbti() 결과 (seed 본인)
    candidates   : [{"name": str, "result": predict_mbti(answers)}]
    top_k        : 반환할 추천 조합 수 (기본 3개 조합)
    max_candidates: 후보 수 상한 (조합 폭발 방지)

    반환: 상위 top_k 개 팀 조합 리스트
      [
        {
          "members":    [{"name": ..., "mbti": ..., "scores": [...]}],
          "team_avg":   [능력치별 팀 평균 벡터],
          "team_min":   float,   # 가장 낮은 평균 능력치
          "team_total": float,   # 전체 평균 합
        },
        ...
      ]
    """
    if len(candidates) > max_candidates:
        candidates = candidates[:max_candidates]

    ability_titles = [a['title'] for a in get_social_abilities()]
    seed_vec = scores_to_vector(calc_social_scores(seed_result))

    # 후보별 벡터 계산
    cand_vecs = []
    for c in candidates:
        vec = scores_to_vector(calc_social_scores(c['result']))
        cand_vecs.append(vec)

    # 3명 조합 탐색
    n = len(candidates)
    results = []

    for combo in itertools.combinations(range(n), 3):
        members_vecs = [seed_vec] + [cand_vecs[i] for i in combo]
        stats = team_score_stats(members_vecs)
        results.append((combo, stats))

    # 정렬: 최솟값 내림차순 → 총합 내림차순 (동점 처리)
    results.sort(key=lambda x: (x[1]['min'], x[1]['total']), reverse=True)

    # 상위 top_k 조합 정리
    output = []
    for combo, stats in results[:top_k]:
        members = []
        for i in combo:
            c = candidates[i]
            scores = calc_social_scores(c['result'])
            members.append({
                'name':   c['name'],
                'mbti':   c['result']['mbti'],
                'scores': scores,
            })
        output.append({
            'members':    members,
            'team_avg':   stats['avg'],
            'team_min':   stats['min'],
            'team_total': stats['total'],
            'ability_titles': ability_titles,
        })

    return output


# ─────────────────────────────────────────────
# 출력 함수
# ─────────────────────────────────────────────

def print_seed(seed_result: dict, seed_name: str = "나(seed)"):
    scores = calc_social_scores(seed_result)
    print("\n" + "=" * 55)
    print(f"  [SEED] {seed_name}  ({seed_result['mbti']})")
    print("=" * 55)
    bar_len = 15
    for s in scores:
        filled = round(s['score'] / 10 * bar_len)
        bar    = '█' * filled + '░' * (bar_len - filled)
        print(f"  {s['title']:<8} [{bar}] {s['score']:4.1f}")


def print_team(rank: int, team: dict, seed_name: str = "나(seed)", seed_result: dict = None):
    titles = team['ability_titles']
    print(f"\n{'─'*55}")
    print(f"  추천 #{rank}  │  팀 최소 능력치: {team['team_min']:.2f}  │  총합: {team['team_total']:.2f}")
    print(f"{'─'*55}")

    # 팀원 목록
    all_members = []
    if seed_result:
        all_members.append({"name": seed_name, "mbti": seed_result['mbti'],
                            "scores": calc_social_scores(seed_result)})
    all_members.extend(team['members'])

    for m in all_members:
        tag = " ← seed" if m['name'] == seed_name else ""
        print(f"  {m['name']:<12} ({m['mbti']}){tag}")

    # 팀 평균 능력치 바
    print()
    bar_len = 15
    for title, avg in zip(titles, team['team_avg']):
        filled = round(avg / 10 * bar_len)
        bar    = '█' * filled + '░' * (bar_len - filled)
        print(f"  {title:<8} [{bar}] {avg:4.2f}")


def recommend_and_print(seed_result: dict, candidates: list[dict],
                        seed_name: str = "나(seed)", top_k: int = 3):
    print_seed(seed_result, seed_name)

    print(f"\n  후보 {len(candidates)}명 중 3명 추천 (팀 밸런스 최적화)")

    teams = recommend_team(seed_result, candidates, top_k=top_k)

    if not teams:
        print("  후보가 3명 미만이어서 추천이 불가합니다.")
        return

    for i, team in enumerate(teams, 1):
        print_team(i, team, seed_name=seed_name, seed_result=seed_result)

    print()


# ─────────────────────────────────────────────
# 예시 실행
# ─────────────────────────────────────────────
if __name__ == '__main__':
    init_db()

    # seed 본인 (ENFP 성향)
    seed_answers = [
        2,  2, -2, -2,
        2,  2, -2, -2,
        3,  3, -3, -3,
        2,  1, -2, -1,
        1,  2, -1, -2,
    ]
    seed_result = predict_mbti(seed_answers)

    # DB에서 후보 불러오기 (없으면 예시 16명 자동 삽입)
    candidates = get_all_candidates()
    if not candidates:
        seed_candidates()
        candidates = get_all_candidates()

    recommend_and_print(seed_result, candidates, seed_name="나(ENFP)", top_k=3)
