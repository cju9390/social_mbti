import pandas as pd

try:
    df = pd.read_csv('16P.csv', encoding='utf-8')
except UnicodeDecodeError:
    df = pd.read_csv('16P.csv', encoding='cp1252')

TRAIT_INDICES = {
    'EI': [1,  6, 11, 16, 21, 26, 31, 36, 41, 46, 51, 56],
    'NS': [2,  7, 12, 17, 22, 27, 32, 37, 42, 47, 52, 57],
    'TF': [3,  8, 13, 18, 23, 28, 33, 38, 43, 48, 53, 58],
    'JP': [4,  9, 14, 19, 24, 29, 34, 39, 44, 49, 54, 59],
    'AT': [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60],
}

TRAIT_LABEL_KO = {
    'EI': '외향_내향',
    'NS': '직관_감각',
    'TF': '사고_감정',
    'JP': '판단_인식',
}

# 영어 질문 목록
question_eng = [
    # EI (외향/내향)
    'You regularly make new friends.',
    'At social events, you rarely try to introduce yourself to new people and mostly talk to the ones you already know',
    'You feel comfortable just walking up to someone you find interesting and striking up a conversation.',
    'You enjoy participating in group activities.',
    'You avoid leadership roles in group settings.',
    'You tend to avoid drawing attention to yourself.',
    'You usually prefer to be around others rather than on your own.',
    'After a long and exhausting week, a lively social event is just what you need.',
    'You avoid making phone calls.',
    'You rarely contemplate the reasons for human existence or the meaning of life.',
    'You would love a job that requires you to work alone most of the time.',
    'You complete things methodically without skipping over any steps.',

    # NS (직관/감각)
    'You spend a lot of your free time exploring various random topics that pique your interest',
    'You prefer to completely finish one project before starting another.',
    'You are not too interested in discussing various interpretations and analyses of creative works.',
    'You like books and movies that make you come up with your own interpretation of the ending.',
    'You are definitely not an artistic type of person.',
    'Your mood can change very quickly.',
    'You become bored or lose interest when the discussion gets highly theoretical.',
    'You enjoy going to art museums.',
    'You often spend a lot of time trying to understand views that are very different from your own.',
    'Your emotions control you more than you control them.',
    'You believe that pondering abstract philosophical questions is a waste of time.',
    'You are very intrigued by things labeled as controversial.',

    # TF (사고/감정)
    'Seeing other people cry can easily make you feel like you want to cry too',
    'You are very sentimental.',
    'You are more inclined to follow your head than your heart.',
    'Your happiness comes more from helping others accomplish things than your own accomplishments.',
    'You think the world would be a better place if people relied more on rationality and less on their feelings.',
    'You lose patience with people who are not as efficient as you.',
    'You find it easy to empathize with a person whose experiences are very different from yours.',
    'You often have a hard time understanding other people\u2019s feelings.',
    'In your social circle, you are often the one who contacts your friends and initiates activities.',
    'You take great care not to make people look bad, even when it is completely their fault.',
    'You feel more drawn to places with busy, bustling atmospheres than quiet, intimate places.',
    'You would pass along a good opportunity if you thought someone else needed it more.',

    # JP (판단/인식)
    'You often make a backup plan for a backup plan.',
    'You like to use organizing tools like schedules and lists.',
    'You usually prefer just doing what you feel like at any given moment instead of planning a particular daily routine.',
    'You are interested in so many things that you find it difficult to choose what to try next.',
    'You prefer to do your chores before allowing yourself to relax.',
    'You often end up doing things at the last possible moment.',
    'You usually postpone finalizing decisions for as long as possible.',
    'You like to have a to-do list for each day.',
    'If your plans are interrupted, your top priority is to get back on track as soon as possible.',
    'Your personal work style is closer to spontaneous bursts of energy than organized and consistent efforts.',
    'You know at first glance how someone is feeling.',
    'You struggle with deadlines.',
]

# 한국어 번역 목록 (question_eng 와 순서 일치)
question_kor = [
    # EI (외향/내향)
    '일상 속에서, 나는 정기적으로 새로운 친구를 사귄다.',
    '처음 보는 사람들이 많은 모임에서, 나는 아는 사람과만 주로 이야기한다.',
    '흥미로운 사람을 마주쳤을 때, 나는 먼저 다가가 대화를 거는 것이 편하다.',
    '활동을 선택할 기회가 생겼을 때, 나는 단체 활동에 참여하는 것을 즐긴다.',
    '팀 프로젝트나 모임이 시작될 때, 나는 리더 역할을 피하는 편이다.',
    '여럿이 함께하는 자리에서, 나는 남의 이목을 끄는 것을 피하는 편이다.',
    '자유 시간이 생겼을 때, 나는 혼자 있는 것보다 다른 사람들과 함께 있는 것을 선호한다.',
    '힘들고 지친 한 주를 보낸 후, 나는 활기찬 사교 행사에서 에너지를 충전한다.',
    '누군가와 연락을 취해야 할 때, 나는 전화 통화를 피하는 편이다.',
    '평소에, 나는 인간 존재의 이유나 삶의 의미에 대해 깊이 생각하는 편이 아니다.',
    '미래 진로를 상상할 때, 나는 대부분 혼자 일하는 직업을 원한다.',
    '복잡한 일을 처리할 때, 나는 단계를 건너뛰지 않고 체계적으로 완료한다.',

    # NS (직관/감각)
    '특별한 계획이 없는 날, 나는 다양한 주제를 탐색하는 데 많은 시간을 쓴다.',
    '여러 프로젝트가 쌓여 있을 때, 나는 새것을 시작하기 전에 현재 것을 완전히 끝내는 것을 선호한다.',
    '영화나 책을 함께 본 후 대화할 때, 나는 다양한 해석을 논의하는 데 별로 관심이 없다.',
    '콘텐츠를 고를 때, 나는 결말을 스스로 해석해야 하는 책이나 영화를 좋아한다.',
    '내 취향이나 성격을 떠올릴 때, 나는 예술적인 유형의 사람이 절대 아니다.',
    '하루를 보내다 보면, 나의 기분은 매우 빠르게 변한다.',
    '토론이나 대화가 길어질 때, 지나치게 이론적으로 흐르면 나는 흥미를 잃는다.',
    '문화생활을 즐길 때, 나는 미술관에 가는 것을 즐긴다.',
    '내 생각과 전혀 다른 의견을 접했을 때, 나는 그 관점을 이해하려고 많은 시간을 쏟는다.',
    '일상에서, 나는 감정을 스스로 다스리기보다 감정에 이끌리는 편이다.',
    '철학적인 주제가 화제에 오르면, 나는 그런 질문을 고민하는 것은 시간 낭비라고 생각한다.',
    '사회적으로 논란이 되는 사안을 접했을 때, 나는 매우 흥미를 느낀다.',

    # TF (사고/감정)
    '슬픈 장면이나 이야기를 접했을 때, 나는 다른 사람이 우는 것을 보면 쉽게 눈물이 난다.',
    '스스로를 표현한다면, 나는 매우 감성적인 편이다.',
    '갈등 상황에 놓였을 때, 나는 감정보다 이성에 따르는 편이다.',
    '성취감을 느끼는 순간을 떠올릴 때, 나는 내 성과보다 남을 도와 무언가를 이루게 했을 때 더 행복하다.',
    '사회 문제를 생각할 때, 나는 사람들이 감정보다 이성에 더 의존한다면 세상이 더 나아질 것이라 생각한다.',
    '함께 일하는 상황에서, 나만큼 효율적이지 않은 사람에게 나는 쉽게 인내심을 잃는다.',
    '나와 매우 다른 삶을 살아온 사람의 이야기를 들을 때, 나는 쉽게 공감할 수 있다.',
    '대화 중 상대가 감정적이 될 때, 나는 종종 그 감정을 이해하기 어렵다.',
    '오랫동안 연락이 없던 친구가 생각날 때, 나는 먼저 연락하고 만남을 제안하는 편이다.',
    '누군가와 다툰 후 상황을 정리할 때, 나는 완전히 상대방 잘못이더라도 상대를 나쁘게 보이지 않으려 조심한다.',
    '어떤 공간에서 더 편안함을 느끼냐고 묻는다면, 나는 조용한 곳보다 활기차고 북적이는 분위기에 더 끌린다.',
    '좋은 기회가 생겼을 때, 다른 사람이 더 필요하다고 생각되면 나는 그 기회를 양보할 것이다.',

    # JP (판단/인식)
    '중요한 일을 앞두고 있을 때, 나는 대비책의 대비책까지 자주 만든다.',
    '일상을 관리할 때, 나는 일정표나 할 일 목록 같은 정리 도구를 즐겨 사용한다.',
    '하루 일과를 보낼 때, 나는 정해진 루틴보다 그 순간의 기분대로 행동하는 것을 선호한다.',
    '새로운 취미나 활동을 찾을 때, 나는 관심사가 너무 많아 다음에 뭘 해볼지 고르기 어렵다.',
    '해야 할 일과 쉬고 싶은 마음이 충돌할 때, 나는 쉬기 전에 할 일을 먼저 마치는 것을 선호한다.',
    '마감이 있는 일을 맡았을 때, 나는 종종 마지막 순간에야 처리하게 된다.',
    '여러 선택지 앞에 놓였을 때, 나는 최종 결정을 가능한 한 미루는 편이다.',
    '하루를 시작할 때, 나는 매일 할 일 목록을 만드는 것을 좋아한다.',
    '예상치 못한 변수로 계획이 틀어졌을 때, 나는 최대한 빨리 원래 계획대로 돌아가려 한다.',
    '내 업무 스타일을 한마디로 표현한다면, 나는 체계적인 노력보다 즉흥적인 에너지 분출에 가깝다.',
    '처음 만나는 사람과 대화할 때, 나는 한눈에 상대방의 감정 상태를 알아챈다.',
    '기한이 있는 과제나 업무를 처리할 때, 나는 마감 기한을 지키는 것이 힘들다.',
]

_question_map = dict(zip(question_eng, question_kor))

# 영어 질문 컬럼명 → 한국어로 대체 후 엑셀 저장
rename_kor = {col: _question_map.get(col, col) for col in df.columns}
df_kor = df.rename(columns=rename_kor)
df_kor.to_csv('social_mbti_preprocess.csv', index=False, encoding='utf-8-sig')

print(f"social_mbti_preprocess.csv 저장 완료: {df_kor.shape}")
