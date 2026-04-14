# 수정 기록 (Change Log)

| 2026-04-14 16:10:47 | `Write` | `c:\dev\workspace_python\social_mbti\.claude\agents\domain-agent.md` | `--- name: social-mbti-developer description: "social_mbti 프로젝트 도메인...` |
| 2026-04-14 16:11:02 | `Write` | `c:\dev\workspace_python\social_mbti\.claude\agents\auditor-agent.md` | `--- name: code-review-auditor description: "social_mbti 코드 감사관. Flask/...` |
| 2026-04-14 16:11:19 | `Write` | `c:\dev\workspace_python\social_mbti\.claude\skills\ch03-mbti-ml.md` | `# MBTI 예측 / SVM 모델 스킬  > 트리거: `mbti`, `예측`, `svm`, `모델...` |
| 2026-04-14 16:11:30 | `Write` | `c:\dev\workspace_python\social_mbti\.claude\skills\ch04-flask-db.md` | `# Flask 라우트 / SQLite DB 스킬  > 트리거: `flask`, `라우트`, `route`...` |
| 2026-04-14 16:11:37 | `Write` | `c:\dev\workspace_python\social_mbti\.claude\skills\ch05-team-recommend.md` | `# 팀 추천 스킬  > 트리거: `팀`, `team`, `추천`, `recommend`, `구성`...` |
| 2026-04-14 16:11:53 | `Write` | `c:\dev\workspace_python\social_mbti\.claude\skills\INDEX.md` | `# 스킬 매뉴얼 목차  > 필요한 챕터만 Read 도구로 로드하세요....` |
| 2026-04-14 16:12:00 | `Edit` | `c:\dev\workspace_python\social_mbti\.claude\hooks\user-prompt-submit.sh` | `SHARED_DIR=".claude/shared" SKILLS_DIR=".claude/skills" SPEC_FILE="docs/PROJECT_...` |
| 2026-04-14 16:12:12 | `Edit` | `c:\dev\workspace_python\social_mbti\.claude\hooks\user-prompt-submit.sh` | `# --- social_mbti 도메인 챕터 매칭 --- echo "$MSG_LOWER" | grep -qiE 'mbt...` |
| 2026-04-14 16:12:21 | `Edit` | `c:\dev\workspace_python\social_mbti\.claude\hooks\user-prompt-submit.sh` | `        case "$fpath" in             *mbti_predict*|*mbti_svm*|*mbti_preprocess*...` |
| 2026-04-14 16:12:28 | `Edit` | `c:\dev\workspace_python\social_mbti\.claude\hooks\user-prompt-submit.sh` | `# social_mbti 에이전트 추천 if echo "$MATCHED_CHAPTERS" | grep -qE 'ch03-m...` |
| 2026-04-14 16:12:35 | `Edit` | `c:\dev\workspace_python\social_mbti\.claude\hooks\user-prompt-submit.sh` | `echo "$USER_MSG" | grep -qE 'from flask|import flask|app\.route|jsonify|render_t...` |
