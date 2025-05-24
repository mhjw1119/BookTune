from django.shortcuts import render
from django.http import JsonResponse
import requests
import time
import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from .serializers import CreatedSongSerializer
from decouple import config
from .genmusic import generate_music_with_webhook
from pathlib import Path
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import CreatedSong

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_music(request):
    prompt = request.data.get('prompt')
    book_id = request.data.get('book_id')  # book_id 받기

    if not prompt:
        return Response({"error": "prompt가 필요합니다."}, status=400)

    try:
        # book_id가 있는 경우 해당 책이 존재하는지 확인
        book = None
        if book_id:
            try:
                from books.models import Books  # Books로 수정
                book = Books.objects.get(id=book_id)
            except Books.DoesNotExist:
                return Response({"error": "해당 책을 찾을 수 없습니다."}, status=404)

        # 음악 생성 요청을 pending 상태로 저장
        song = CreatedSong.objects.create(
            user=request.user,
            book=book,  # book 정보 저장
            prompt=prompt,
            status='pending'
        )

        # Suno API 호출
        response = generate_music_with_webhook(prompt)
        
        if response and 'task_id' in response:
            # task_id 저장
            song.task_id = response['task_id']
            song.status = 'processing'
            song.save()
            
            return Response({
                "message": "음악 생성이 시작되었습니다.",
                "task_id": response['task_id'],
                "status": "processing",
                "book_id": book_id
            })
        else:
            song.status = 'failed'
            song.save()
            return Response({"error": "음악 생성 요청 실패"}, status=500)
            
    except Exception as e:
        if 'song' in locals():
            song.status = 'failed'
            song.save()
        return Response({"error": str(e)}, status=500)

@api_view(['POST', 'PUT'])  # Suno API 웹훅은 POST로 오지만, 내부적으로는 PUT 작업을 수행
@permission_classes([AllowAny])  # 웹훅은 인증 없이 접근 가능해야 함
def suno_webhook_callback(request):
    """
    Suno API의 웹훅 콜백을 처리하는 함수.
    POST 요청으로 들어오지만, 내부적으로는 기존 CreatedSong 객체를 업데이트하는 PUT 작업을 수행합니다.
    """
    print(f"[🔔] 웹훅 콜백 수신: {request.data}")  # 디버깅을 위한 로깅
    
    data = request.data
    task_id = data.get("data", {}).get("task_id")  # taskId -> task_id로 수정
    audio_items = data.get("data", {}).get("data", [])

    if not task_id:
        print(f"[❌] task_id 없음: {data}")  # 디버깅을 위한 로깅
        return Response({"error": "task_id가 없습니다."}, status=400)

    if not audio_items:
        print(f"[❌] audio_items 비어있음: {data}")  # 디버깅을 위한 로깅
        return Response({"error": "audio_items 비어 있음"}, status=400)

    # task_id로 음악 생성 요청을 찾습니다
    try:
        song = CreatedSong.objects.get(task_id=task_id)
    except CreatedSong.DoesNotExist:
        return Response({"error": "해당 task_id에 대한 음악 생성 요청을 찾을 수 없습니다."}, status=404)

    saved_songs = []
    for item in audio_items:
        audio_url = item.get("audio_url")
        title = item.get("title") or item.get("id") or "suno_music"
        duration = item.get("duration")
        prompt = item.get("prompt", "")
        filename = f"{title.replace(' ', '_')}.mp3"

        if not audio_url:
            continue

        try:
            # 음악 파일 다운로드 및 저장
            audio_response = requests.get(audio_url)
            if audio_response.status_code == 200:
                media_path = Path(settings.MEDIA_ROOT) / "aisong" / filename
                media_path.parent.mkdir(parents=True, exist_ok=True)
                
                with open(media_path, "wb") as f:
                    f.write(audio_response.content)

                # 기존 song 객체의 필드들을 업데이트
                song.audio_file = f"aisong/{filename}"
                song.audio_url = audio_url
                song.title = title
                song.duration = duration
                song.status = 'completed'
                song.save()  # 데이터베이스에 변경사항 저장
                
                # 시리얼라이저를 사용하여 응답 데이터 생성
                serializer = CreatedSongSerializer(song, context={'request': request})
                saved_songs.append(serializer.data)
                
                print(f"[📁] 저장 완료: {media_path}")
            else:
                print(f"❌ 다운로드 실패: {audio_response.status_code}")
                # 실패 상태로 업데이트
                song.status = 'failed'
                song.save()
                serializer = CreatedSongSerializer(song, context={'request': request})
                saved_songs.append(serializer.data)
        except Exception as e:
            print(f"❌ 예외 발생: {e}")
            # 실패 상태로 업데이트
            song.status = 'failed'
            song.save()
            serializer = CreatedSongSerializer(song, context={'request': request})
            saved_songs.append(serializer.data)

    return Response({
        "saved_songs": saved_songs,
        "message": f"{len(saved_songs)}개의 음악이 성공적으로 저장되었습니다."
    }, status=200)

