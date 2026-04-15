# 체크리스트

> 작업 추적. 하나 끝낼 때마다 [x]로 체크. 다음 할 일을 항상 정리해둘 것.

---

## Phase 0: 오케스트레이션 세팅

- [x] `.claude` 훅 경로 버그 수정 (SHARED_DIR)
- [x] domain-agent 프로젝트 전용 재작성
- [x] auditor-agent 프로젝트 전용 재작성
- [x] 도메인 스킬 챕터 작성 (ch03, ch04, ch05)
- [x] user-prompt-submit.sh 키워드 매핑 추가
- [x] post-tool-use.sh Flask/SQLite 체크 추가

## Phase 1: 기능 개발 (다음 할 일)

- [x] questions.py 콤마 누락 버그 수정 + question_eng 텍스트 불일치 수정 (2026-04-15)
- [x] MBTI 모델 재설계: 16-class → 4개 독립 이진 분류기 (LinearSVC, 2026-04-15)
- [x] 16P.csv 부호 인코딩 버그 수정: 음수=동의 → 앱 입력 부호 반전 (2026-04-15)
- [x] XGBoost + 32문항으로 모델 교체 → 평균 84.78% (EI 86.4 / NS 84.8 / TF 83.8 / JP 84.1, 2026-04-15)
- [x] 입력 검증 강화 (app.py `/submit`, `/recommend` 라우트, 2026-04-15)
- [x] team_recommend.py 안쓰는 함수 제거 (print_seed, print_team, recommend_and_print, __main__, 2026-04-15)
- [ ] 팀 추천 엣지케이스 처리 (team_recommend.py)
- [ ] 에러 응답 JSON 일관성 정비
- [ ] docs/PROJECT_SPEC.md 작성
- [ ] 테스트 코드 추가
