# 수정 기록 (Change Log)

| 2026-04-14 16:12:41 | `Edit` | `c:\dev\workspace_python\social_mbti\.claude\hooks\post-tool-use.sh` | `SHARED_DIR=".claude/shared" ...` |
| 2026-04-14 16:13:01 | `Edit` | `c:\dev\workspace_python\social_mbti\.claude\hooks\post-tool-use.sh` | `# ============================================================================= ...` |
| 2026-04-14 16:13:18 | `Write` | `c:\dev\workspace_python\social_mbti\.claude\shared\context-notes.md` | `# 맥락노트  > 왜 이렇게 결정했는지, 관련 자료가 어디 있는�...` |
| 2026-04-14 16:13:23 | `Write` | `c:\dev\workspace_python\social_mbti\.claude\shared\checklist.md` | `# 체크리스트  > 작업 추적. 하나 끝낼 때마다 [x]로 체크. 다�...` |
| 2026-04-15 09:42:01 | `Edit` | `c:\dev\workspace_python\social_mbti\questions.py` | `question_eng = [     # EI (외향/내향)     'You regularly make new friends.',...` |
| 2026-04-15 09:42:27 | `Edit` | `c:\dev\workspace_python\social_mbti\.claude\shared\checklist.md` | `## Phase 1: 기능 개발 (다음 할 일)  - [x] questions.py 콤마 누락 버...` |
| 2026-04-15 09:51:54 | `Write` | `c:\dev\workspace_python\social_mbti\mbti_svm_train.py` | `""" SVM (RBF) 모델 학습 및 저장 — 4개 독립 이진 분류기 - 축별...` |
| 2026-04-15 09:52:26 | `Write` | `c:\dev\workspace_python\social_mbti\mbti_predict.py` | `""" MBTI 예측 + 각 성향 축 퍼센트 출력 - 4개 독립 이진 SVM: EI /...` |
| 2026-04-15 10:19:21 | `Edit` | `c:\dev\workspace_python\social_mbti\mbti_svm_train.py` | `from sklearn.model_selection import train_test_split from sklearn.svm import Lin...` |
| 2026-04-15 10:19:26 | `Edit` | `c:\dev\workspace_python\social_mbti\mbti_svm_train.py` | `    svm_bin = CalibratedClassifierCV(         LinearSVC(random_state=SEED, max_i...` |
| 2026-04-15 10:22:15 | `Edit` | `c:\dev\workspace_python\social_mbti\mbti_svm_train.py` | `for t_idx, (trait, meta) in enumerate(TRAIT_META.items()):     # 20개 질문 �...` |
| 2026-04-15 10:22:20 | `Edit` | `c:\dev\workspace_python\social_mbti\mbti_predict.py` | `    for t_idx, trait in enumerate(TRAITS):         # 20개 전체를 각 분류�...` |
| 2026-04-15 10:26:06 | `Edit` | `c:\dev\workspace_python\social_mbti\mbti_predict.py` | `    # 인터리브 → 모델 순서 재정렬 (axis별 5개씩: [EI*5 | NS*5 | ...` |
| 2026-04-15 10:30:02 | `Edit` | `c:\dev\workspace_python\social_mbti\.claude\shared\checklist.md` | `- [x] questions.py 콤마 누락 버그 수정 + question_eng 텍스트 불일�...` |
| 2026-04-15 10:38:19 | `Edit` | `c:\dev\workspace_python\social_mbti\mbti_svm_train.py` | `""" XGBoost 모델 학습 및 저장 — 4개 독립 이진 분류기 - 축별 �...` |
| 2026-04-15 10:38:24 | `Edit` | `c:\dev\workspace_python\social_mbti\mbti_svm_train.py` | `    chosen = sorted(random.sample(indices, 8)) ...` |
| 2026-04-15 10:38:31 | `Edit` | `c:\dev\workspace_python\social_mbti\mbti_svm_train.py` | `# 인터리브 표시 순서 (UI용) TRAITS   = list(TRAIT_INDICES.keys()) N_PER...` |
| 2026-04-15 10:38:35 | `Edit` | `c:\dev\workspace_python\social_mbti\mbti_svm_train.py` | `print("선택된 32개 질문 (EI→NS→TF→JP 반복):") ...` |
| 2026-04-15 10:38:37 | `Edit` | `c:\dev\workspace_python\social_mbti\app.py` | `@app.route('/submit', methods=['POST']) def submit():     """퀴즈 완료: 예�...` |
| 2026-04-15 10:38:42 | `Edit` | `c:\dev\workspace_python\social_mbti\mbti_svm_train.py` | `    clf = XGBClassifier(         n_estimators=300,         max_depth=4, ...` |
| 2026-04-15 10:38:46 | `Edit` | `c:\dev\workspace_python\social_mbti\mbti_svm_train.py` | `print("svm_model.pkl 저장 완료 (4-binary XGBoost 구조, 32문항)") ...` |
| 2026-04-15 10:38:46 | `Edit` | `c:\dev\workspace_python\social_mbti\app.py` | `@app.route('/recommend', methods=['POST']) def recommend():     """팀 추천: s...` |
| 2026-04-15 10:38:51 | `Edit` | `c:\dev\workspace_python\social_mbti\team_recommend.py` | `import itertools import numpy as np from mbti_predict import calc_social_scores,...` |
| 2026-04-15 10:38:52 | `Edit` | `c:\dev\workspace_python\social_mbti\mbti_predict.py` | `TRAITS   = ['EI', 'NS', 'TF', 'JP'] N_TRAITS = 4 N_PER    = len(col_names) // N_...` |
| 2026-04-15 10:38:58 | `Edit` | `c:\dev\workspace_python\social_mbti\mbti_predict.py` | `    expected = N_PER * N_TRAITS     if len(interleaved_answers) != expected:    ...` |
| 2026-04-15 10:39:02 | `Edit` | `c:\dev\workspace_python\social_mbti\mbti_predict.py` | `    interleaved_answers: 32개 응답 (EI,NS,TF,JP 교차 순서, 값 범위 -3~...` |
| 2026-04-15 10:39:18 | `Edit` | `c:\dev\workspace_python\social_mbti\mbti_svm_train.py` | `    clf = XGBClassifier(         n_estimators=300,         max_depth=4, ...` |
| 2026-04-15 10:40:44 | `Edit` | `c:\dev\workspace_python\social_mbti\mbti_predict.py` | `    print("\n\n[예시 1] 외향·직관·감정·인식 성향 (ENFP)")     ans...` |
| 2026-04-15 10:40:45 | `Edit` | `c:\dev\workspace_python\social_mbti\mbti_predict.py` | `        # 32개 전체를 각 분류기에 입력 (축간 상관관계 활용) ...` |
| 2026-04-15 10:40:50 | `Edit` | `c:\dev\workspace_python\social_mbti\mbti_svm_train.py` | `# 2. 축별 랜덤 8개 선택 (seed=42 고정) ...` |
| 2026-04-15 10:40:52 | `Edit` | `c:\dev\workspace_python\social_mbti\mbti_svm_train.py` | `# 전체 X 행렬 (n × 32), 축 순서: EI[0:8] NS[8:16] TF[16:24] JP[24:32] ...` |
| 2026-04-15 10:40:53 | `Edit` | `c:\dev\workspace_python\social_mbti\mbti_svm_train.py` | `    # 32개 질문 전체를 입력 (축간 상관관계가 예측 정확도를 ...` |
| 2026-04-15 10:41:08 | `Edit` | `c:\dev\workspace_python\social_mbti\.claude\shared\checklist.md` | `- [x] XGBoost + 32문항으로 모델 교체 → 평균 84.78% (EI 86.4 / NS 84....` |
| 2026-04-15 10:46:39 | `Write` | `c:\dev\workspace_python\social_mbti\_test_mbti_predict.py` | `""" 극단적 답변으로 각 MBTI 유형 예측 테스트 - EI열: +3 = E 방�...` |
| 2026-04-15 10:47:19 | `Write` | `c:\dev\workspace_python\social_mbti\_test_mbti_predict.py` | `""" MBTI 예측 검증 1) CSV 실제 데이터 → 예측 정확도 ...` |
| 2026-04-15 10:48:24 | `Write` | `c:\dev\workspace_python\social_mbti\_test_mbti_predict.py` | `""" 각 질문의 실제 방향을 파악하고 극단 MBTI 예측 테스트 """...` |
| 2026-04-15 10:48:55 | `Write` | `c:\dev\workspace_python\social_mbti\_test_mbti_predict.py` | `""" 실제 CSV 데이터 기반 MBTI 예측 정확도 분석 """ ...` |
| 2026-04-15 10:57:39 | `Write` | `c:\dev\workspace_python\social_mbti\mbti_preprocess_.py` | `""" 16P.csv → social_mbti_preprocess.csv EI/NS/TF/JP 질문 컬럼명을 한�...` |
| 2026-04-15 10:58:07 | `Edit` | `c:\dev\workspace_python\social_mbti\app.py` | `from mbti_predict import predict_mbti, calc_social_scores, display_names from ca...` |
| 2026-04-15 11:04:22 | `Write` | `c:\dev\workspace_python\social_mbti\mbti_svm_train.py` | `""" XGBoost 모델 학습 및 저장 — 4개 독립 이진 분류기 - Optuna �...` |
| 2026-04-15 14:07:11 | `Edit` | `c:\dev\workspace_python\social_mbti\app.py` | `import sys import logging import traceback ...` |
| 2026-04-15 14:07:15 | `Edit` | `c:\dev\workspace_python\social_mbti\app.py` | `import sys import logging from flask import Flask, render_template, request, jso...` |
| 2026-04-15 14:07:22 | `Edit` | `c:\dev\workspace_python\social_mbti\app.py` | `    try:         result = predict_mbti(answers)         scores = calc_social_sco...` |
| 2026-04-15 14:08:46 | `Edit` | `c:\dev\workspace_python\social_mbti\mbti_predict.py` | `        p_pos = float(proba[1]) * 100   # P(E), P(N), P(T), P(J)         p_neg =...` |
| 2026-04-15 14:25:58 | `Edit` | `c:\dev\workspace_python\social_mbti\team_recommend.py` | `def build_reason(     seed_vec: np.ndarray,     member_vecs: list[np.ndarray], ...` |
| 2026-04-15 14:26:05 | `Edit` | `c:\dev\workspace_python\social_mbti\team_recommend.py` | `    # 상위 top_k 조합 정리     output = []     for combo, stats in results...` |
| 2026-04-15 14:26:14 | `Edit` | `c:\dev\workspace_python\social_mbti\app.py` | `        output.append({             'members':        t['members'],             ...` |
| 2026-04-15 14:26:21 | `Edit` | `c:\dev\workspace_python\social_mbti\templates\index.html` | `    .team-back {       margin-top: 8px;     } ...` |
| 2026-04-15 14:26:31 | `Edit` | `c:\dev\workspace_python\social_mbti\templates\index.html` | `  let partyAllCandidates = [];   // 전체 후보   let partyAiNames = new Set()...` |
| 2026-04-15 14:26:36 | `Edit` | `c:\dev\workspace_python\social_mbti\templates\index.html` | `    showView('team-view');     partySelected.clear();     partyAiNames.clear(); ...` |
| 2026-04-15 14:26:41 | `Edit` | `c:\dev\workspace_python\social_mbti\templates\index.html` | `      // TOP 1 멤버 사전 선택       if (recData.teams && recData.teams.len...` |
| 2026-04-15 14:26:47 | `Edit` | `c:\dev\workspace_python\social_mbti\templates\index.html` | `        ${partyAiReason ? `         <div class="team-reason">           <div cla...` |
