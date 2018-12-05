from flask import Flask, jsonify, json
from redis import Redis
import requests
import config

app = Flask(__name__)

redis = Redis(host='123.207.152.86', port=6379, db=0)


def get_access_token():
    token = redis.get('wx_token')
    if token:
        return token.decode('utf8')
    url = 'https://api.weixin.qq.com/cgi-bin/token'
    params = {
        'grant_type': 'client_credential',
        'appid': config.APP_ID,
        'secret': config.APP_SECRET
    }
    req = requests.get(url, params)
    if req.status_code == 200:
        data = json.loads(req.text, encoding='utf8')
        token = data.get('access_token')
        print(data)
        redis.setex('wx_token', 10, token)
    return token


@app.route('/access_token')
def access_token():
    return jsonify({'access_token': get_access_token()})


if __name__ == '__main__':
    app.run()
