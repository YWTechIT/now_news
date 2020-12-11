from flask import Flask, render_template, jsonify, request
from datetime import datetime
from newsapi import NewsApiClient
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta  # 'dbsparta'라는 이름의 db를 만들거나 사용합니다.

now = datetime.now()
print("서버 날짜:", now.year, ".", now.month, ".", now.day, ".")
print("서버 업데이트 시간: ", now.hour, ":", now.minute, ":", now.second)

# Init
newsapi = NewsApiClient(api_key='e65f8f56bf7a4bdeb9a2923031113604')


# api
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/headline', methods=['GET'])
def get_headline():
    # top_headlines = newsapi.get_top_headlines(q='bitcoin',
    #                                           sources='bbc-news,the-verge',
    #                                           category='business',
    #                                           language='en',
    #                                           country='us')

    country = request.args.get('country')
    category = request.args.get('category')

    print('카테고리: ', category, ',', '국가: ', country)

    if country and category is not None:
        headline = newsapi.get_top_headlines(country=country, category=category)
    else:
        headline = newsapi.get_top_headlines(country='kr', category='general')

    # web_scrap = {
    #     'title': title,
    #     'url': url,
    #     'content': content,
    #     'urlToImage': urlToImage,
    #     'desc': description
    # }

    return jsonify({'result': 'success', 'msg': '헤드라인 뉴스를 가져옵니다.', 'headline': headline})


@app.route('/everything', methods=['GET'])
def get_everything():
    # /v2/everything
    # all_articles = newsapi.get_everything(q='bitcoin',
    #                                       sources='bbc-news,the-verge',
    #                                       domains='bbc.co.uk,techcrunch.com',
    #                                       from_param='2017-12-01',
    #                                       to='2017-12-12',
    #                                       language='en',
    #                                       sort_by='relevancy',
    #                                       page=2)

    keyword = request.args.get('q')
    sort_by = request.args.get('sort_by')

    print(keyword)
    print(sort_by)

    if keyword and sort_by is not None:
        everything = newsapi.get_everything(q=keyword, sort_by=sort_by)
    else:
        everything = newsapi.get_everything(q='속보', sort_by='publishedAt')

    return jsonify({'result': 'success', 'msg': '키워드 뉴스를 가져옵니다.', 'everything': everything})


@app.route('/scrap', methods=['POST'])
def scraped_article():
    title = request.form.get('title')
    publisher = request.form.get('publisher')
    date = request.form.get('date')
    time = request.form.get('time')
    url = request.form.get('url')
    url_image = request.form.get('url_image')
    desc = request.form.get('desc')

    print(title, publisher, date, time, url, url_image, desc)

    scrap_head_line = {
        'title': title,
        'publisher': publisher,
        'date': date,
        'time': time,
        'url': url,
        'url_image': url_image,
        'desc': desc
    }

    db.scrap_article.insert_one(scrap_head_line)
    return jsonify({'result': 'success', 'msg': '해당 기사를 스크랩합니다.'})


@app.route('/scrap', methods=['POST'])
def scrap_everything():
    title = request.form.get('title')
    date = request.form.get('date')
    time = request.form.get('time')
    url = request.form.get('url')
    url_image = request.form.get('url_image')
    desc = request.form.get('desc')

    scrap_all_article = {
        'title': title,
        'date': date,
        'time': time,
        'url': url,
        'url_image': url_image,
        'desc': desc
    }

    db.scrap_article.insert_one(scrap_all_article)
    return jsonify({'result': 'success', 'msg': '해당 기사를 스크랩합니다.'})


@app.route('/scrap', methods=['GET'])
def read_headline():
    scrap_list = list(db.scrap_article.find({}, {'_id': False}).sort("_id", -1))
    return jsonify({'result': 'success', 'msg': '스크랩한 기사들을 불러옵니다.', 'scrap_list': scrap_list})


# @app.route('/scrap', methods=['GET'])
# def read_all_article():
#     all_article_list = list(db.scrap_all_article.find({}, {'_id': False}).sort("_id", -1))
#     return jsonify({'result': 'success', 'msg': '스크랩한 기사들을 불러옵니다.', 'scrap_list': all_article_list})


# @app.route('/ip', methods=['GET'])
# def ipify():
#     ip = ''
#     api_key = 'at_TuFxvDdo4X3QkxlOw2DLHFmxS9dRY'
#     api_url = 'https://geo.ipify.org/api/v1?'
#
#     url = api_url + 'apiKey=' + api_key + '&ipAddress=' + ip
#
#     print(urlopen(url).read().decode('utf8'))
#     return jsonify({'result': 'success', 'msg': '리뷰 내용을 가져옵니다.', 'ip': url})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
