# Glare

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/git/external?repository-url=https%3A%2F%2Fgithub.com%2FContextualist%2Fglare&project-name=glare&repo-name=glare&demo-title=Glare&demo-description=gracefully%20download%20(latest)%20releases%20from%20GitHub&demo-url=https%3A%2F%2Fgithub.com%2FContextualist%2Fglare&demo-image=https%3A%2F%2Frepository-images.githubusercontent.com%2F77979589%2Fa6437980-6472-11e9-9660-133b39d9978f)

A little service for you to download releases from GitHub gracefully. Simply make a get request to Glare with the repo name (with an optional version) and release file name regex, and she will lead you to the way.

**NOTE:** You might want to use [GitHub's direct link](https://help.github.com/en/articles/linking-to-releases#linking-to-the-latest-release) to the latest release asset (e.g. `github.com/{owner}/{repo}/releases/latest/download/asset-name.zip`) if the asset name is a constant string. Otherwise Glare is still helpful for matching the asset with regex.

### Demo
The following will redirect you to `https://github.com/xtaci/kcptun/releases/download/{latest_version_tag}/kcptun-linux-amd64-{latest_version_number}.tar.gz`, and download the latest release of kcptun for linux-amd64. 
```bash
curl -fLO https://glare.now.sh/xtaci/kcptun/linux-amd64
```

Or you might want to have a version constraint:
```bash
curl -fLO https://glare.now.sh/v2fly/v2ray-core@v4.x/linux-64
```

## Motivation
Sometimes when I'm writing a Dockerfile, I need to install packages from their GitHub latest releases. A neat way is to parse JSON responses from GitHub API with [`jq`](https://stedolan.github.io/jq) and get the desire link. Such way requires downlaoding `jq` from GitHub (The binary from Alpine apk is lack of regex feature). Still, the expression with `jq` is not clear enough, and parsing JSON with `sed` is way dirtier. So I spend a little time to write Glare. I hope she will save you a few minutes or from a frustring moment.

## Usage
```
# To get the latest release...
/{owner}/{repo}/{file_name_regex}

# To get a specific version or pick within a version range...
/{owner}/{repo}@{tag|semver}/{file_name_regex}
```
`{file_name_regex}` is a regular expression to match the file (or specially, it can be `tar` or `zip` standing for the source code download in the respective format). It should match at least one file among the latest release files, otherwise Glare will throw an error. If multiple files are matched, Glare returns the one with shortest length.

If `{tag}` is given, Glare looks for a release with exact matching tag. For `{semver}` provided, Glare treats it as a [npm-flavor semver](https://semver.npmjs.com/) and matches all release tag names against it. The highest of all satisfied versions is chosen.

Tip: to check if a request leads to the desired redirection, `curl` it without any option.
