from flask import Flask, request, jsonify, render_template
import mysql.connector
import subprocess
import tempfile
import re
import os

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "localhost"),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", "root"),
        database=os.getenv("MYSQL_DB", "devops")
    )


def get_cached_transcript(youtube_url):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM transcripts WHERE youtube_url = %s", (youtube_url,))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result["content"] if result else None

def save_transcript(youtube_url, content):   
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("INSERT INTO transcripts (youtube_url, content) VALUES (%s, %s)", (youtube_url, content))
    connection.commit()
    cursor.close()
    connection.close()
    return True

import re

def clean_vtt(vtt_text: str) -> str:
    lines = []
    for line in vtt_text.splitlines():
        line = line.strip()
        if (
            not line
            or line.startswith("WEBVTT")
            or "-->" in line
            or line.startswith("Kind:")
            or line.startswith("Language:")
        ):
            continue

        line = re.sub(r"<[^>]+>", "", line)

        line = line.replace("&gt;", "")
        lines.append(line)


    cleaned = []
    for l in lines:
        if not cleaned or cleaned[-1] != l:
            cleaned.append(l)

    return " ".join(cleaned)

def fetch_transcript(youtube_url):
    with tempfile.TemporaryDirectory() as tmpdir:
        cmd = [
            "yt-dlp",
            "--skip-download",
            "--write-auto-sub",
            "--sub-lang", "en",
            "--sub-format", "vtt",
            "-o", f"{tmpdir}/%(id)s.%(ext)s",
            youtube_url
        ]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            raise Exception(f"yt-dlp error: {result.stderr}")

        for file in os.listdir(tmpdir):
            if file.endswith(".vtt"):
                with open(os.path.join(tmpdir, file), "r") as f:
                    return f.read()

        raise Exception("Transcript not found")

@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200


@app.route("/transcript", methods=["POST"])
def transcript():
    data = request.get_json()

    if not data or "youtube_url" not in data:
        return jsonify({"error": "youtube_url is required"}), 400

    youtube_url = data["youtube_url"]

    cached = get_cached_transcript(youtube_url)
    if cached:
        return jsonify({"source": "cache", "content": cached})

    try:
        raw_vtt = fetch_transcript(youtube_url)
        transcript_text = clean_vtt(raw_vtt)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    save_transcript(youtube_url, transcript_text)

    return jsonify({"source": "fetched", "content": transcript_text})

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)