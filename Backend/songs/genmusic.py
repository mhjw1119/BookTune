import os
import time
import json
import requests
from decouple import config
from django.conf import settings
from pathlib import Path
CALLBACK_URL = config("NGROK_URL") + "/api/songs/callback/"

SUNO_API_KEY = config('SUNO_API_KEY')
API_BASE_URL = 'https://apibox.erweima.ai'
HEADERS = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization': f'Bearer {SUNO_API_KEY}'
}

def generate_music_with_webhook(prompt):
    generate_url = f"{API_BASE_URL}/api/v1/generate"
    payload = json.dumps({
        "prompt": prompt,
        "customMode": False,
        "instrumental": True,
        "model": "V4",
        "callBackUrl": CALLBACK_URL
    })

    response = requests.post(generate_url, headers=HEADERS, data=payload)
    res_data = response.json()

    task_id = res_data.get("data", {}).get("taskId")
    if not task_id:
        raise Exception("taskId가 응답에 없습니다.")

    return {"task_id": task_id, "status": "pending"}
