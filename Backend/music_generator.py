from transformers import AutoProcessor, MusicgenForConditionalGeneration
import scipy.io.wavfile as wavfile
import torch

processor = AutoProcessor.from_pretrained("facebook/musicgen-medium")
model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-medium")

# GPU 사용 가능시 GPU 사용
device = "cuda" if torch.cuda.is_available() else "cpu"
model = model.to(device)

def generate_music(prompt, output_path="generated_music.wav"):
    """
    주어진 프롬프트를 기반으로 음악을 생성합니다.
    
    Args:
        prompt (str): 음악 생성을 위한 텍스트 설명
        output_path (str): 생성된 음악을 저장할 경로
    """
    # 모델과 프로세서 로드


    # 입력 텍스트 처리
    inputs = processor(
        text=[prompt],
        padding=True,
        return_tensors="pt",
    ).to(device)
    
    # 음악 생성
    audio_values = model.generate(
        **inputs,
        max_new_tokens=600,
        do_sample=True,
        guidance_scale=3.0,
    )
    
    # 오디오 데이터를 numpy 배열로 변환
    audio_data = audio_values[0, 0].cpu().numpy()
    
    # WAV 파일로 저장
    wavfile.write(output_path, rate=model.config.audio_encoder.sampling_rate, data=audio_data)
    
    return output_path

generate_music("편안하고 차분한 스타일의 음악을 만들어줘")