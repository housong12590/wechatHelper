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
    token = refresh_token() or ''
    return token


@app.route('/refresh_token')
def refresh_token():
    url = 'https://api.weixin.qq.com/cgi-bin/token'
    params = {
        'grant_type': 'client_credential',
        'appid': config.APP_ID,
        'secret': config.APP_SECRET
    }
    req = requests.get(url, params)
    if req.status_code == 200:
        data = json.loads(req.text, encoding='utf8')
        print(data)
        token = data.get('access_token')
        redis.setex('wx_token', 7200, token or '')
        return token
    else:
        return req.text


@app.route('/access_token')
def access_token():
    return jsonify({'access_token': get_access_token()})


if __name__ == '__main__':
    app.run()
