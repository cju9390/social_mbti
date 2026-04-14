# 팀 추천 스킬

> 트리거: `팀`, `team`, `추천`, `recommend`, `구성`, `조합`, `다양성`, `mbti.*팀`, `팀.*mbti`

---

## 팀 추천 구조

```python
# team_recommend.py
def recommend_team(name: str, candidates: list, size: int = 4) -> list:
    """
    name: 본인 이름 (제외 대상)
    candidates: [{'name': ..., 'mbti': ..., 'axis_pct': ...}, ...]
    size: 추천 팀 인원 수 (본인 포함)
    Returns: [{'name': ..., 'mbti': ...}, ...]
    """
```

## 추천 알고리즘 원칙

- **MBTI 다양성 극대화**: 4개 축(EI/NS/TF/JP) 에서 다양한 유형 조합
- 본인 MBTI를 기준으로 상호보완 유형 우선 선발
- 후보자 수 < size 일 때 예외 처리 필수

## 엣지 케이스

```python
def recommend_team(name, candidates, size=4):
    others = [c for c in candidates if c['name'] != name]
    if len(others) < size - 1:
        # 후보 부족: 가능한 만큼만 반환하거나 에러 응답
        return others  # 또는 raise ValueError(f"후보 {size-1}명 필요, 현재 {len(others)}명")
```

## Flask 라우트 연동

```python
@app.route('/team')
def team():
    name = request.args.get('name', '')
    size = int(request.args.get('size', 4))
    all_candidates = get_all_candidates()
    my_result = next((c for c in all_candidates if c['name'] == name), None)
    if not my_result:
        return jsonify({'error': '후보자를 찾을 수 없습니다'}), 404

    team = recommend_team(name, all_candidates, size)
    return jsonify({'team': team})
```

## 주의사항

- `size` 파라미터는 정수 변환 실패 시 기본값(4) 사용
- 팀 추천 결과에 본인이 포함되는지 확인
- 후보자가 0명인 극단적 케이스도 처리
