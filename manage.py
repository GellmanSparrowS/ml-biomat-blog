"""Local build, verification and publishing for ml-biomat.com (stdlib only)."""
from __future__ import annotations
import argparse
import os
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
ORIGIN = "https://github.com/GellmanSparrowS/ml-biomat-blog.git"
MANAGED = ("content", "static", "docs", "build.py", "config.py", "qa_check.py", "preview.py",
           "snapshot.py", "article_writer.py", "auto_writer.py", "chart_gen.py", "content_tools",
           "manage.py", "README.md", "AGENTS.md", ".gitignore", "vercel.json",
           "_files_test.txt", "root_test.txt", "test_write.txt", "repo-payload.json")


def run(*args, capture=False):
    return subprocess.run(args, cwd=ROOT, check=True, text=True, encoding="utf-8",
                          stdout=subprocess.PIPE if capture else None,
                          env={**os.environ, "PYTHONIOENCODING": "utf-8"}).stdout


def git(*args, capture=False):
    return run("git", *args, capture=capture)


def build():
    run(sys.executable, "build.py")
    run(sys.executable, "qa_check.py")


def verify_origin():
    if git("remote", "get-url", "origin", capture=True).strip() != ORIGIN:
        raise RuntimeError("Expected the clean HTTPS origin for GellmanSparrowS/ml-biomat-blog.")


def check_staged():
    names = git("diff", "--cached", "--name-only", "-z", capture=True).split("\0")
    forbidden = re.compile(r"(?i)(^|/)(\.env(?:\..*)?|\.secrets.*|.*token.*|.*recovery.*|.*\.(pem|key))$")
    for name in filter(None, names):
        if forbidden.search(name):
            raise RuntimeError("Credential-like staged filename: " + name)
        if not any(name == p or name.startswith(p + "/") for p in MANAGED):
            raise RuntimeError("Review staged path outside the publish set: " + name)
    # Inspect only added text, without printing its contents.
    diff = git("diff", "--cached", "--no-ext-diff", "--unified=0", capture=True)
    added = "\n".join(line[1:] for line in diff.splitlines() if line.startswith("+") and not line.startswith("+++"))
    secret = re.compile(r"(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{30,}|-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----)")
    if secret.search(added):
        raise RuntimeError("A credential pattern was found in staged text. Review locally before publishing.")


def publish(message):
    verify_origin()
    if git("branch", "--show-current", capture=True).strip() != "main":
        raise RuntimeError("Publish runs from main. Review and merge the intended work first.")
    if git("diff", "--name-only", "--diff-filter=U", capture=True).strip():
        raise RuntimeError("Resolve merge conflicts before publishing.")
    git("fetch", "origin")
    local = git("rev-parse", "HEAD", capture=True).strip()
    remote = git("rev-parse", "origin/main", capture=True).strip()
    base = git("merge-base", "HEAD", "origin/main", capture=True).strip()
    if base != remote:
        raise RuntimeError("Remote main has newer work. Reconcile it before publishing; no force push is used.")
    build()
    tracked = set(git("ls-files", "-z", capture=True).split("\0"))
    paths = [p for p in MANAGED if (ROOT / p).exists() or p in tracked]
    git("add", "-A", "--", *paths)
    check_staged()
    if git("diff", "--cached", "--name-only", capture=True).strip():
        git("commit", "-m", message)
    elif local == remote:
        print("No changes to publish.")
        return
    git("push", "origin", "HEAD:main")
    head = git("rev-parse", "HEAD", capture=True).strip()
    live = git("ls-remote", "origin", "refs/heads/main", capture=True).split()[0]
    if live != head:
        raise RuntimeError("Remote verification differed from the pushed commit; inspect before retrying.")
    print("Published commit:", head)
    print("Next: verify GitHub Pages deployment and https://ml-biomat.com/about/.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    subs = parser.add_subparsers(dest="command", required=True)
    subs.add_parser("doctor", help="Check local Git identity, repository and working state")
    subs.add_parser("build", help="Build offline and run all site checks")
    subs.add_parser("check", help="Check the already generated site")
    p = subs.add_parser("preview", help="Serve generated pages on this computer")
    p.add_argument("--port", type=int, default=8866)
    p = subs.add_parser("publish", help="Build, check, commit and push the managed site files")
    p.add_argument("--message", required=True)
    args = parser.parse_args()
    if args.command == "doctor":
        verify_origin()
        print("Project:", ROOT)
        print("Python:", sys.version.split()[0])
        print("Origin:", ORIGIN)
        git("status", "--short", "--branch")
        git("config", "--get", "user.name")
        git("config", "--get", "user.email")
    elif args.command == "build": build()
    elif args.command == "check": run(sys.executable, "qa_check.py")
    elif args.command == "preview": run(sys.executable, "preview.py", "--port", str(args.port))
    elif args.command == "publish": publish(args.message)


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, subprocess.CalledProcessError) as exc:
        print("Stopped:", str(exc), file=sys.stderr)
        sys.exit(1)
