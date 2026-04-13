"""
MBTI 질문 목록 (영문 → 한국어 매핑)
mbti_preprocess_.py 의 부작용(CSV 읽기/쓰기) 없이 질문 데이터만 분리
"""

question_eng = [
    # EI
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
    # NS
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
    # TF
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
    # JP
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

question_kor = [
    # EI (외향형 vs 내향형)
    '정기적으로 새로운 친구를 사귑니다.'
    '사교 모임에서 새로운 사람에게 자신을 소개하는 일은 드물며, 주로 이미 알고 있는 사람들과 대화합니다.'
    '흥미로워 보이는 사람에게 다가가 말을 거는 것이 편안하게 느껴집니다.'
    '단체 활동에 참여하는 것을 즐깁니다.'
    '단체 모임에서 리더 역할을 맡는 것을 피합니다.'
    '자신에게 관심이 집중되는 것을 피하는 편입니다.'
    '혼자 있는 것보다 다른 사람들과 함께 있는 것을 보통 더 선호합니다.'
    '길고 고된 한 주를 보낸 후에는 활기찬 사교 모임이 꼭 필요합니다.'
    '전화 통화하는 것을 피합니다.'
    '인간의 존재 이유나 삶의 의미에 대해 깊이 고민하는 일은 거의 없습니다.'
    '대부분의 시간을 혼자서 일하는 직업을 선호합니다.'
    '어떤 단계도 건너뛰지 않고 체계적으로 일을 완수합니다.'

    # NS (직관형 vs 감각형)
    '자유 시간의 많은 부분을 흥미를 끄는 다양한 주제를 탐구하는 데 보냅니다.'
    '다른 프로젝트를 시작하기 전에 진행 중인 일을 완전히 끝내는 것을 선호합니다.'
    '창작물에 대한 다양한 해석이나 분석을 논의하는 데 큰 관심이 없습니다.'
    '결말을 스스로 해석하게 만드는 책이나 영화를 좋아합니다.'
    '자신은 확실히 예술적인 유형의 사람이 아닙니다.'
    '기분이 매우 빠르게 변할 수 있습니다.'
    '토론이 매우 이론적으로 흐르면 지루해하거나 흥미를 잃습니다.'
    '미술관에 가는 것을 즐깁니다.'
    '자신과 매우 다른 관점을 이해하려고 노력하는 데 많은 시간을 할애하곤 합니다.'
    '자신이 감정을 조절하기보다 감정이 자신을 지배할 때가 더 많습니다.'
    '추상적인 철학적 질문을 고민하는 것은 시간 낭비라고 생각합니다.'
    '논란의 여지가 있다고 여겨지는 일들에 매우 흥미를 느낍니다.'

    # TF (사고형 vs 감정형)
    '다른 사람이 우는 것을 보면 자신도 쉽게 눈물이 날 것 같습니다.'
    '매우 감수성이 풍부하거나 감성적입니다.'
    '가슴보다는 머리(이성)를 따르는 편입니다.'
    '자신의 성취보다는 다른 사람이 무언가를 이루도록 돕는 것에서 더 큰 행복을 느낍니다.'
    '사람들이 감정에 덜 치우치고 이성에 더 의존한다면 세상이 더 나은 곳이 될 것이라고 생각합니다.'
    '자신만큼 효율적이지 못한 사람들을 보면 인내심을 잃곤 합니다.'
    '자신과 매우 다른 경험을 한 사람에게도 쉽게 공감할 수 있습니다.'
    '타인의 감정을 이해하는 데 종종 어려움을 겪습니다.'
    '사교 모임에서 주로 친구들에게 연락하고 활동을 주도하는 편입니다.'
    '완전한 상대방의 잘못이라 할지라도, 그 사람이 나쁘게 보이지 않도록 세심한 주의를 기울입니다.'
    '조용하고 오붓한 곳보다 활기차고 북적이는 분위기의 장소에 더 끌립니다.'
    '다른 누군가에게 더 필요한 기회라고 생각되면 좋은 기회를 양보할 것입니다.'
    
    #JP (판단형 vs 인식형)
    '플랜 B를 넘어 플랜 C까지 세우는 등 대비책의 대비책을 자주 세웁니다.'
    '일정표나 목록 같은 정리 도구를 사용하는 것을 좋아합니다.'
    '특정한 일과를 계획하기보다 매 순간 마음이 가는 대로 행동하는 것을 보통 더 선호합니다.'
    '관심 있는 분야가 너무 많아서 다음에 무엇을 시도할지 선택하기 어렵습니다.'
    '휴식을 취하기 전에 먼저 할 일을 끝내는 것을 선호합니다.'
    '종종 마감 직전이 되어서야 일을 처리하곤 합니다.'
    '보통 최종 결정을 가능한 한 오랫동안 미룹니다.'
    '매일 할 일 목록(To-do list)을 작성하는 것을 좋아합니다.'
    '계획에 차질이 생기면 가능한 한 빨리 원래 궤도로 돌아오는 것이 최우선 과제입니다.'
    '업무 방식은 체계적이고 꾸준한 노력보다는 즉흥적으로 에너지를 쏟아붓는 쪽에 가깝습니다.'
    '상대방이 어떤 기분인지 한눈에 알아차립니다.'
    '마감 기한을 지키는 데 어려움을 겪습니다.'
]

question_map = dict(zip(question_eng, question_kor))
