from flask import Flask, jsonify, redirect
import requests
import re

app = Flask(__name__)

@app.route('/<user>/<repo>/<name_re>')
def get_latest_release(user, repo, name_re):
    try:
        name_reobj = re.compile(name_re)
    except re.error as e:
        return jsonify(message="bad regular expression: {}".format(e.message)), 400

    resp = requests.get("https://api.github.com/repos/{user}/{repo}/releases/latest"
                        .format(user=user, repo=repo))
    if resp.status_code != 200:
        return jsonify(message="error from GitHub api",
                       github_api_msg=resp.json()), resp.status_code

    if name_re == 'tar':
        return redirect(resp.json()['tarball_url'])
    if name_re == 'zip':
        return redirect(resp.json()['zipball_url'])
    assets = resp.json()['assets']
    matched = [x['browser_download_url'] for x in assets if name_reobj.search(x['name'])]
    n = len(matched)
    if n == 0:
        return jsonify(message="no file matched"), 404
    matched = sorted(matched, key=len)
    return redirect(matched[0])

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=1080)
