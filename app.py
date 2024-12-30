import os
from flask import Flask, request, jsonify
import parselmouth

app = Flask(__name__)

# 업로드된 파일 저장 경로 설정
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def home():
    return "File Upload and Analysis API is running!"

@app.route("/analyze", methods=["POST"])
def analyze_audio():
    # 파일이 요청에 포함되었는지 확인
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    
    # 파일이 없거나 비어 있는지 확인
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400
    
    # 파일 저장
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(file_path)
    
    try:
        # Praat을 사용해 음성 분석
        sound = parselmouth.Sound(file_path)
        formant = sound.to_formant_burg()
        duration = sound.duration
        
        # 포먼트 값 가져오기
        f1 = formant.get_value_at_time(1, duration / 2)
        f2 = formant.get_value_at_time(2, duration / 2)
        
        # 결과 반환
        result = {
            "filename": file.filename,
            "duration": duration,
            "f1": f1,
            "f2": f2
        }
        return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
