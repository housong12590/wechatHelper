from flask import Flask, jsonify, json, request
from redis import Redis
import requests
import config

app = Flask(__name__)

redis = Redis(host='123.207.152.86', port=6379, db=0)


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
        if token:
            redis.setex('wx_token', 7200, token or '')
            return None, token
        return data.get('errmsg'), None
    else:
        return req.text, None


@app.route('/access_token')
def access_token():
    update = request.args.get('update', False)
    if update is False:
        token = redis.get('wx_token')
        if token:
            return token.decode('utf8')
    errmsg, token = refresh_token()
    if token:
        return jsonify({'access_token': token})
    else:
        return jsonify({'errmsg': errmsg})


if __name__ == '__main__':
    app.run()
