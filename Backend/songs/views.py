from django.shortcuts import render
from songs.utils import generate_music_from_prompt
from django.http import JsonResponse

def generate_music_view(request):
    prompt = request.POST.get('prompt', '')
    music_path = generate_music_from_prompt(
        prompt=prompt,
        output_filename='my_music.wav',
        duration=15  # 15초 길이의 음악 생성
    )
    return JsonResponse({'music_path': music_path})