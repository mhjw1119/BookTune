import subprocess
import time
import requests
import json
from pathlib import Path

ENV_PATH = Path(".env")

def start_ngrok(port=8000):
    # Windows에서는 shell=True가 필요할 수 있음
    subprocess.Popen(f"ngrok http {port}", shell=True)
    print(f"[🔌] ngrok http {port} 실행 중...")
    time.sleep(3)

    try:
        tunnel_info = requests.get("http://localhost:4040/api/tunnels").json()
        public_url = tunnel_info["tunnels"][0]["public_url"]
        print(f"[🌍] ngrok URL 감지됨: {public_url}")
        return public_url
    except Exception as e:
        print("❌ ngrok URL 가져오기 실패:", e)
        return None

def update_env(ngrok_url):
    lines = []
    found = False

    if ENV_PATH.exists():
        with open(ENV_PATH, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("NGROK_URL="):
                    lines.append(f"NGROK_URL={ngrok_url}\n")
                    found = True
                else:
                    lines.append(line)

    if not found:
        lines.append(f"NGROK_URL={ngrok_url}\n")

    with open(ENV_PATH, "w", encoding="utf-8") as f:
        f.writelines(lines)

    print(f"[✅] .env 파일에 NGROK_URL={ngrok_url} 저장 완료")

if __name__ == "__main__":
    url = start_ngrok(8000)
    if url:
        update_env(url)
