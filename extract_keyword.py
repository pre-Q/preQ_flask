from konlpy.tag import Kkma
from sklearn.feature_extraction.text import TfidfVectorizer

common = ['경험', '자신감', '노력', '정확']
passion = ['열심히', '최선', '열정', '끝까지', '충실히', '주도적', '몰입', '성실', '에너지', '활력', '몰두', '끊임없이', '포기하지 않고', '활발한', '원동력',
           '의지', '끈기', '투지', '열의', '적극']
collaboration = ['소통', '팀워크', '희생', '갈등', '리더십', '커뮤니케이션', '존중', '협력', '유대', '신뢰', '설득', '조율', '헌신', '경청', '연결',
                 '이해', '공유', '책임', '대화', '도움', '배려']
challenge = ['시도', '새로운', '도전', '혁신', '창의', '두려워하지 않고', '차별화', '도약', '목표', '변화', '실현', '시작', '용기', '시행', '탐구', '모험',
             '결단력', '실행', '기회', '호기심']
problem = ['문제', '전략', '성공', '효율', '방안', '발전', '목적', '건의', '분석', '조사', '개선', '원인', '보완', '해결', '목표', '향상', '성취',
           '성과', '기여', '달성', '접근', '완성']
leadership = ['설득', '창의성', '주도', '팀장', '임원', '조장', '회장', '갈등해결', '분위기', '제시', '리드', '리더', '솔선수범', '추진력', '책임', '피드백', '영향력', '비전']
IT = ['개발', '백엔드', '프론트엔드', '인공지능', 'AI', '증강현실', 'API', '노드', 'NodeJs', 'SpringBoot', '자바', 'Java', '스프링부트', '스프링', '자바스크립트', '안드로이드', 'iOS', 'Android', '타입스크립트', 'TypeScript', '자바스크립트', 'JavaScript', 'C++', 'C',  '데이터 분석', '모델링', '딥러닝', '머신러닝', 'C#', '파이썬', 'Python', '데이터베이스', 'DB', '서버', '웹', '앱', 'HTML', 'CSS', 'Docker', 'CICD', '스케줄링', '클라이언트', '배포', 'json', '센서', '쓰레드', 'IOT', '데이터', '장고', 'Django',
      'data', '해커톤', 'MVC', '아두이노', '라즈베리파이', 'MongoDB', 'RDS', 'PostgreSQL', 'MySQL', 'SQL', 'NoSQL', 'Git', 'AWS', 'Swagger', '스웨거', '명세서', '데이터마이닝', 'PHP', 'JSP', 'DevOps', '릴리즈', '클라우드', 'cloud', 'NFC', '메타버스', '자동화', '알고리즘', '아키텍처', 'UX', 'UI', '웹퍼블리싱', '보안', '해킹', '기계학습', '네트워크', '운영체제', 'OS', '오픈소스', 'GPT', 'Swift', 'Kotlin', '코틀린', '로드밸런싱',
      '쿠버네티스', '프레임워크', '캐시', '애자일', 'Agile', '스프린트', '스크럼', '소프트웨어', 'SW', '프로그래밍', 'SI', '빅데이터', '데이터사이언스', '블록체인', '데이터 시각화', '풀스택', 'EC2', 'Jenkins', 'Github Actions', 'React', '리액트', 'Flask', 'Vue.js', 'jQuery', '클론코딩', 'Redux', 'JPA', 'Flutter', 'Express', 'Rest API', 'BootStrap', '부트스트랩', 'Unity', '객체지향', 'R', 'Oracle', 'MariaDB', 'Linux', 'Pandas', '크롤링']


def get_keyword(application):
    data = application.split('.')
    data = list(map(lambda x: x.split('\n'), data))
    data = sum(data, [])

    kkma = Kkma()

    output = list()
    for sample in data:
        ex_pos = kkma.pos(sample)
        text_data = []
        for (text, tclass) in ex_pos:
            if tclass == 'NNG' or tclass == 'NNP' or tclass == 'VV' or tclass == 'VA':
                text_data.append(text)
        output.append(text_data)

    corpus = list(map(lambda x: ' '.join(x), output))

    tfidfv = TfidfVectorizer().fit(corpus)

    sorted_dict = sorted(tfidfv.vocabulary_.items(), key=lambda item: item[1], reverse=True)

    top_5 = sorted_dict[0:5]
    top_5 = list(map(lambda x: x[0], top_5))

    p_cnt = 0
    c_cnt = 0
    ch_cnt = 0
    ps_cnt = 0
    l_cnt = 0
    it_cnt = 0

    for w in sorted_dict:
        if w[0] in passion:
            p_cnt += 1
        if w[0] in collaboration:
            c_cnt += 1
        if w[0] in challenge:
            ch_cnt += 1
        if w[0] in problem:
            ps_cnt += 1
        if w[0] in leadership:
            l_cnt += 1
        if w[0] in IT:
            it_cnt += 1
        if w[0] in common:
            p_cnt += 1
            c_cnt += 1
            ch_cnt += 1
            ps_cnt += 1

    ## 전체 합계
    total = p_cnt + c_cnt + ch_cnt + ps_cnt + l_cnt + it_cnt

    ## 수치 계산
    p_val = round(p_cnt / total * 100, 2)
    c_val = round(c_cnt / total * 100, 2)
    ch_val = round(ch_cnt / total * 100, 2)
    ps_val = round(ps_cnt / total * 100, 2)
    l_val = round(l_cnt / total * 100, 2)
    it_val = round(it_cnt / total * 100, 2)

    return top_5, [p_val, c_val, ch_val, ps_val, l_val, it_val]
