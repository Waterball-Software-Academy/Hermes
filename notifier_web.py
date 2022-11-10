from multiprocessing import Pool

from flask import Flask, request, render_template, Response
from flask_cors import CORS

import access_token_repository
import properties
from access_token_repository import upsert
from lotify_client import get_lotify_client

app = Flask(__name__)
# enable CORS
CORS(app, resources={r'/': {'origins': ''}})
lotify_client = get_lotify_client()


@app.route("/subscribe", methods=['GET'])
def subscribe():
    args = request.args
    code = args['code']
    discord_user_id = args['state']
    access_token = lotify_client.get_access_token(code=code)
    upsert(access_token=access_token, discord_user_id=discord_user_id)
    return render_template('success.html')


@app.route("/notify", methods=['POST'])
def notify():
    auth_key = request.headers.get('x-auth-key')
    if auth_key != properties.NOTIFY_API_KEY:
        return Response(response="Unauthorized", status=401)

    request_data = request.get_json()
    message = request_data['message']
    with Pool(5) as p:
        success = 0
        fail = 0
        for token in access_token_repository.find_all_tokens():
            try:
                p.starmap(lotify_client.send_message, [(token, message)])
                success = success + 1
            except:
                fail = fail + 1
            print(f'success {success}\nfail {fail}\n')
    return Response(response="success", status=201)


def start():
    app.run('0.0.0.0', properties.PORT, False, True)
