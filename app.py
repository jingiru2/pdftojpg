import os
import zipfile
import uuid
from flask import Flask, render_template, request, jsonify, send_from_directory, url_for
from pdf2image import convert_from_path
from PIL import Image

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['CONVERT_FOLDER'] = 'static/converted'
POPPLER_PATH = r'C:\path\to\poppler\bin'  # Windows 사용자만 필요

# 폴더 생성
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['CONVERT_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert_pdf():
    if 'pdf' not in request.files:
        return jsonify({'success': False, 'error': '파일이 없음'})

    pdf_file = request.files['pdf']
    if pdf_file.filename == '':
        return jsonify({'success': False, 'error': '파일이 선택되지 않음'})

    # 파일 저장
    filename = str(uuid.uuid4()) + '.pdf'
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    pdf_file.save(filepath)

    try:
        # PDF → 이미지로 변환
        images = convert_from_path(filepath, dpi=200, poppler_path=POPPLER_PATH)
        image_urls = []
        zip_filename = str(uuid.uuid4()) + '.zip'
        zip_path = os.path.join(app.config['CONVERT_FOLDER'], zip_filename)

        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for i, img in enumerate(images):
                img_filename = f"{filename[:-4]}_{i+1}.jpg"
                img_path = os.path.join(app.config['CONVERT_FOLDER'], img_filename)
                img.save(img_path, 'JPEG')

                # URL 경로
                img_url = url_for('static', filename=f'converted/{img_filename}')
                image_urls.append(img_url)

                # Zip 파일에 추가
                zipf.write(img_path, arcname=img_filename)

        zip_url = url_for('static', filename=f'converted/{zip_filename}')
        return jsonify({'success': True, 'images': image_urls, 'zip_url': zip_url})

    except Exception as e:
        print("에러 발생:", e)
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
