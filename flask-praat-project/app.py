from flask import Flask, request, jsonify
import parselmouth
import os

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze_audio():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    # 업로드된 파일 저장
    file = request.files['file']
    file_path = os.path.join("uploads", file.filename)
    os.makedirs("uploads", exist_ok=True)
    file.save(file_path)
    
    try:
        # Praat으로 음성 파일 분석
        sound = parselmouth.Sound(file_path)
        formant = sound.to_formant_burg()
        duration = sound.duration
        
        # 포먼트 값 가져오기
        f1 = formant.get_value_at_time(1, duration / 2)
        f2 = formant.get_value_at_time(2, duration / 2)
        
        # 결과 반환
        result = {
            "duration": duration,
            "f1": f1,
            "f2": f2
        }
        return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
