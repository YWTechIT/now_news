from flask import Flask, render_template, jsonify, request
from datetime import datetime
from newsapi import NewsApiClient
from pymongo import MongoClient

app = Flask(__name__)

now = datetime.now()
print("서버 날짜:", now.year, ".", now.month, ".", now.day, ".")
print("서버 업데이트 시간: ", now.hour, ":", now.minute, ":", now.second)

# api_key
newsapi = NewsApiClient(api_key='e65f8f56bf7a4bdeb9a2923031113604')

# api
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/headline', methods=['GET'])
def get_headline():
    country = request.args.get('country')
    category = request.args.get('category')

    if country and category is not None:
        headline = newsapi.get_top_headlines(country=country, category=category)
    else:
        headline = newsapi.get_top_headlines(country='kr', category='general')

    return jsonify({'result': 'success', 'msg': '헤드라인 뉴스를 가져옵니다.', 'headline': headline})

@app.route('/everything', methods=['GET'])
def get_everything():
    keyword = request.args.get('q')
    sort_by = request.args.get('sort_by')

    if keyword and sort_by is not None:
        everything = newsapi.get_everything(q=keyword, sort_by=sort_by)
    else:
        everything = newsapi.get_everything(q='속보', sort_by='publishedAt')

    return jsonify({'result': 'success', 'msg': '키워드 뉴스를 가져옵니다.', 'everything': everything})

# scrap_function
# @app.route('/scrap', methods=['GET'])
# def read_headline():
#     scrap_list = list(db.scrap_article.find({}, {'_id': False}).sort("_id", -1))
#     return jsonify({'result': 'success', 'msg': '스크랩한 기사들을 불러옵니다.', 'scrap_list': scrap_list})

# init 
if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)