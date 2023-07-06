import requests
from flask import Flask, jsonify,request,make_response
from flask_cors import CORS
app = Flask(__name__)
# Initialize CORS
CORS(app)

# 测试连接口
@app.route('/pin', methods=['POST'])
def pin_data():
    data = request.get_json()
    # 处理您的逻辑
    return jsonify({'message': 'Data pinned successfully'})



#twitter-
# 推特获取刷新令牌
@app.route('/oauth/callback', methods=['POST'])
def get_access_token():
    data = request.get_json()
    code = data.get('code')
    code_verifier = data.get('code_verifier')

    url = 'https://api.twitter.com/2/oauth2/token'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    payload = {
        'code': code,
        'grant_type': 'authorization_code',
        'client_id': 'dUVORHA5OGN3MWV4LXRGWkNKS0o6MTpjaQ',   #如要修改项目可修改client_id
        'redirect_uri': 'http://www.localhost:3000/oauth/twitter',  #回调给前端的地址
        'code_verifier': code_verifier,
        'code_challenge_method': 'S256'
    }

    print("client_id:",payload['client_id'])

    try:
        response = requests.post(url, headers=headers, data=payload)
        if response.status_code == 200:
            access_token = response.json().get('access_token')

            me_url = 'https://api.twitter.com/2/users/me'
            me_headers = {
                'Authorization': 'Bearer ' + access_token
            }
            print("me_headers",me_headers)
            me_response = requests.get(me_url, headers=me_headers)
            

            
            me_response.raise_for_status()

            if me_response.status_code == 200:
                user_data = me_response.json()
                user_id = user_data['data']['id']
                name = user_data['data']['name']
                username = user_data['data']['username']

                response_data = {
                  'code': 200,
                    'data': {
                        'user_id': user_id,
                        'name': name,
                        'username': username,
                        'access_token': access_token
                    }
                }
                print(access_token)
                return jsonify(response_data), 200
            else:
                error_message = me_response.json()
                error_response_data = {
                    'code': 400,
                    'error': str(error_message)
                }
                return make_response(jsonify(error_response_data), 200)
        else:
            error_message = response.json()
            error_response_data = {
                    'code': 400,
                    'error': str(error_message)
                }
            return make_response(jsonify(error_response_data), 200)
    except requests.exceptions.RequestException as e:
        return make_response(jsonify({'error': str(e)}), 200)


# 推特发布推文
@app.route('/release_tweets', methods=['POST'])  
def release_tweets():
    data = request.get_json()
    access_token = data.get('access_token')
    tweet_text = data.get('tweet_text')

    print(tweet_text)

    if not access_token or not tweet_text:
        return jsonify({'error': 'Access token or tweet text is missing'})

    url = 'https://api.twitter.com/2/tweets'
    headers = {
        'Authorization': 'Bearer ' + access_token,
        'Content-Type': 'application/json'
    }
    payload = {
        'text': tweet_text
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 201:
            return jsonify({'success': 'Tweet posted successfully'})
        else:
            error_message = response.json()
            return jsonify({'error': error_message})
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9696)


