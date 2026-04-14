# 스킬 매뉴얼 목차

> 필요한 챕터만 Read 도구로 로드하세요. 전체를 한번에 읽지 마세요.
> UserPromptSubmit 훅이 키워드를 감지하여 관련 챕터를 자동 주입합니다.

## 도메인 스킬 (social_mbti 프로젝트)

| # | 챕터 | 파일 | 트리거 키워드 |
|---|------|------|--------------|
| 03 | MBTI 예측 / SVM 모델 | `ch03-mbti-ml.md` | mbti, 예측, svm, 모델, 학습, social score |
| 04 | Flask 라우트 / SQLite DB | `ch04-flask-db.md` | flask, 라우트, api, db, 후보, candidate, sqlite |
| 05 | 팀 추천 로직 | `ch05-team-recommend.md` | 팀, team, 추천, recommend, 구성, 조합 |

## 메타 스킬 (프로세스/품질)

| 챕터 | 파일 | 용도 |
|------|------|------|
| Python 품질 | `ch01-python-quality.md` | 에러 처리, 보안, async 패턴, 코드 품질 기준 |
| 스킬 활성화 규칙 | `ch02-skill-activation.md` | 키워드·패턴·경로·코드 감지 규칙 상세 |

## 에이전트

| 에이전트 | 파일 | 용도 |
|----------|------|------|
| social-mbti-developer | `.claude/agents/domain-agent.md` | 도메인 개발 작업 전반 |
| code-review-auditor | `.claude/agents/auditor-agent.md` | 코드 품질/보안/기획 일치 검증 |

## 자동 로드 규칙
- 사용자 지시에서 키워드가 감지되면 → 해당 챕터가 Claude 컨텍스트에 자동 주입
- PostToolUse에서 보안/에러 이슈 감지 → `ch01-python-quality.md` 참고 안내
- 수동으로 읽으려면: `.claude/skills/chXX-name.md`
