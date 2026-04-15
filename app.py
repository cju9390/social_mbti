import sys
import logging
from flask import Flask, render_template, request, jsonify
from mbti_predict import predict_mbti, calc_social_scores, display_names
from candidate_db import init_db, get_all_candidates, add_candidate_from_result, seed_candidates
from team_recommend import recommend_team

sys.stdout.reconfigure(encoding='utf-8')
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

app = Flask(__name__)
init_db()

# 후보 없으면 예시 16명 자동 삽입
if not get_all_candidates():
    seed_candidates()

QUESTIONS = display_names


@app.route('/')
def index():
    return render_template('index.html', questions=QUESTIONS)


@app.route('/submit', methods=['POST'])
def submit():
    """퀴즈 완료: 예측 + DB 저장"""
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': '요청 본문이 없습니다.'}), 400
    name = str(data.get('name', '')).strip()
    if not name:
        return jsonify({'error': '이름을 입력해주세요.'}), 400
    answers = data.get('answers')
    if not isinstance(answers, list):
        return jsonify({'error': 'answers는 리스트여야 합니다.'}), 400
    try:
        result = predict_mbti(answers)
        scores = calc_social_scores(result)
        add_candidate_from_result(name, result)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logging.exception("submit 처리 중 오류 발생")
        return jsonify({'error': f'예측 오류: {e}'}), 500
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
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': '요청 본문이 없습니다.'}), 400
    name = str(data.get('name', '')).strip()
    mbti = data.get('mbti', '')
    axis_pct = data.get('axis_pct')
    if not name or not mbti or not isinstance(axis_pct, dict):
        return jsonify({'error': '필수 파라미터가 누락되었습니다.'}), 400
    seed_result = {
        'mbti':     mbti,
        'proba':    [],
        'axis_pct': axis_pct,
    }
    candidates = [c for c in get_all_candidates() if c['name'] != name]
    if len(candidates) < 3:
        return jsonify({'error': '후보가 3명 미만입니다.'}), 400
    teams = recommend_team(seed_result, candidates, top_k=3)
    output = []
    for t in teams:
        output.append({
            'members':        t['members'],
            'team_min':       float(t['team_min']),
            'team_total':     float(t['team_total']),
            'team_avg':       t['team_avg'].tolist(),
            'ability_titles': t['ability_titles'],
        })
    return jsonify({'teams': output})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False, threaded=True)
