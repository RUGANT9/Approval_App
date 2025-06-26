from flask import Blueprint, render_template, redirect, url_for, request, flash
from app.generator import generate_sample_test
from pathlib import Path
import subprocess
from threading import Thread
import os
from pathlib import Path

main = Blueprint("main", __name__)
REPO_PATH = Path(os.environ.get("REPO_PATH", Path(__file__).resolve().parents[1]))
GEN_FILE = REPO_PATH / "generated" / "auto_test.py"

@main.route("/latest")
def latest():
    content = GEN_FILE.read_text() if GEN_FILE.exists() else "[No test generated]"
    return render_template("latest.html", content=content, gen_path=str(GEN_FILE))

@main.route("/approve", methods=["POST"])
def approve():
    Thread(target=commit_and_push, daemon=True).start()
    return redirect(url_for("main.latest"))

@main.route("/generate", methods=["GET", "POST"])
def generate():
    if request.method == "POST":
        try:
            a = int(request.form["a"])
            b = int(request.form["b"])
            generate_sample_test(a, b)
            flash("✅ Test generated!", "success")
            return redirect(url_for("main.latest"))
        except ValueError:
            flash("❌ Please enter valid integers.", "error")
            return redirect(url_for("main.generate"))
    return render_template("generate.html")

def commit_and_push():
    subprocess.run(["git", "add", str(GEN_FILE)], cwd=REPO_PATH)
    subprocess.run(["git", "commit", "-m", "feat: approve test [ci skip]"], cwd=REPO_PATH, check=False)
    subprocess.run(["git", "push", "origin", "main"], cwd=REPO_PATH)
