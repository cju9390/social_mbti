import sys
from flask import Flask, render_template, request, jsonify
from mbti_predict import predict_mbti, calc_social_scores, display_names
from candidate_db import init_db, get_all_candidates, add_candidate_from_result, seed_candidates
from team_recommend import recommend_team
from questions import question_map

sys.stdout.reconfigure(encoding='utf-8')

app = Flask(__name__)
init_db()

# 후보 없으면 예시 16명 자동 삽입
if not get_all_candidates():
    seed_candidates()

QUESTIONS = [question_map.get(name, name) for name in display_names]


@app.route('/')
def index():
    return render_template('index.html', questions=QUESTIONS)


@app.route('/submit', methods=['POST'])
def submit():
    """퀴즈 완료: 예측 + DB 저장"""
    data = request.get_json()
    name = data['name']
    answers = data['answers']
    result = predict_mbti(answers)
    scores = calc_social_scores(result)
    add_candidate_from_result(name, result)
    return jsonify({
        'mbti':          result['mbti'],
        'axis_pct':      result['axis_pct'],
        'social_scores': scores,
    })


@app.route('/candidates')
def candidates():
    name = request.args.get('name', '')
    result = [
        {'name': c['name'], 'mbti': c['result']['mbti'], 'axis_pct': c['result']['axis_pct']}
        for c in get_all_candidates() if c['name'] != name
    ]
    return jsonify({'candidates': result})


@app.route('/recommend', methods=['POST'])
def recommend():
    """팀 추천: seed(본인)를 제외한 DB 후보로 팀 구성"""
    data = request.get_json()
    seed_result = {
        'mbti':     data['mbti'],
        'proba':    [],
        'axis_pct': data['axis_pct'],
    }
    candidates = [c for c in get_all_candidates() if c['name'] != data['name']]
    if len(candidates) < 3:
        return jsonify({'error': '후보가 3명 미만입니다.'})

    teams = recommend_team(seed_result, candidates, top_k=3)
    output = []
    for t in teams:
        output.append({
            'members':       t['members'],
            'team_min':      float(t['team_min']),
            'team_total':    float(t['team_total']),
            'team_avg':      t['team_avg'].tolist(),
            'ability_titles': t['ability_titles'],
        })
    return jsonify({'teams': output})


if __name__ == '__main__':
    app.run(debug=True)
