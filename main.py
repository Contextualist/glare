from flask import Flask, jsonify, redirect
import httpx
import semver
import re

app = Flask(__name__)

@app.route('/')
def redir():
    return redirect("https://github.com/Contextualist/glare")

@app.route('/<user>/<repo_ver>/<name_re>')
def get_release(user, repo_ver, name_re):
    try:
        name_reobj = re.compile(name_re)
    except re.error as e:
        return jsonify(message=f"bad regular expression: {e.msg}"), 400

    repo_ver = repo_ver.split('@', 1)
    repo = repo_ver[0]
    if len(repo_ver) == 2: # versioned
        ver = repo_ver[1]
        all_releases, err = api_req(f"https://api.github.com/repos/{user}/{repo}/releases?per_page=100")
        if err: return err
        all_tags = [x['tag_name'] for x in all_releases]
        if ver in all_tags: # exact match
            tag = f"tags/{ver}"
        else:
            try:
                v = semver.max_satisfying(all_tags, ver)
            except Exception as e:
                return jsonify(message=f"error matching the tag: {e}"), 400
            if v is None:
                return jsonify(message="no tag matched"), 404
            tag = f"tags/{v}"
    else:
        tag = "latest"

    release, err = api_req(f"https://api.github.com/repos/{user}/{repo}/releases/{tag}")
    if err: return err

    if name_re == 'tar':
        return redirect(release['tarball_url'])
    if name_re == 'zip':
        return redirect(release['zipball_url'])
    assets = release['assets']
    matched = [x['browser_download_url'] for x in assets if name_reobj.search(x['name'])]
    if len(matched) == 0:
        return jsonify(message="no file matched"), 404
    matched.sort(key=len)
    return redirect(matched[0])

def api_req(url):
    resp = httpx.get(url)
    if resp.status_code != 200:
        return None, (jsonify(message="error from GitHub API",
                              github_api_msg=resp.json()), resp.status_code)
    return resp.json(), None
