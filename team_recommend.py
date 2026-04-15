"""
팀 구성 추천 시스템
- seed(본인) 의 사회적 능력치 약점을 보완하는 3명을 후보 리스트에서 추천
- 팀 점수 = 4명 능력치 평균, 최소 능력치 최대화(밸런스) + 총합 가중 정렬
"""

import itertools
import numpy as np
from mbti_predict import calc_social_scores, get_social_abilities


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
