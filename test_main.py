from main import app
from result import Ok, Err, Result

def app_context(tfn):
    def into_result(rv) -> Result[str, str]:
        if (redirect := rv.headers.get('Location')) is not None:
            return Ok(redirect)
        return Err(rv.get_json()['message'])
    def __wrapped():
        with app.test_client() as c:
            tfn(lambda url: into_result(c.get(url)))
    return __wrapped

ok = lambda r: r.expect(f"Expect Ok, got {r}")
err = lambda r: r.expect_err(f"Expect Err, got {r}")

@app_context
def test_regex(get):
    assert ok(get(r"/v2fly/v2ray-core/macos-64\.zip$")).endswith("v2ray-macos-64.zip")
    assert err(get(r"/_user/_repo/[0-9.*\.tar\.gz")).startswith("bad regular expression")

@app_context
def test_github(get):
    assert err(get(r"/_user/_repo/_file")) == "error from GitHub API"

@app_context
def test_file_match(get):
    assert "kcptun-darwin-amd64" in ok(get(r"/xtaci/kcptun/darwin-amd64"))
    assert "zipball" in ok(get(r"/xtaci/kcptun/zip")) # zip/tar
    assert err(get(r"/xtaci/kcptun/plan9")) == "no file matched"
    assert ok(get(r"/v2fly/v2ray-core/macos-64")).endswith("v2ray-macos-64.zip") # shortest of multiple
