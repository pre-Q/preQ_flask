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

    for w in sorted_dict:
        if w[0] in passion:
            p_cnt += 1
        if w[0] in collaboration:
            c_cnt += 1
        if w[0] in challenge:
            ch_cnt += 1
        if w[0] in problem:
            ps_cnt += 1
        if w[0] in common:
            p_cnt += 1
            c_cnt += 1
            ch_cnt += 1
            ps_cnt += 1

    ## 전체 합계
    total = p_cnt + c_cnt + ch_cnt + ps_cnt

    ## 수치 계산
    p_val = round(p_cnt / total * 100, 2)
    c_val = round(c_cnt / total * 100, 2)
    ch_val = round(ch_cnt / total * 100, 2)
    ps_val = round(ps_cnt / total * 100, 2)

    return top_5, [p_val, c_val, ch_val, ps_val]
