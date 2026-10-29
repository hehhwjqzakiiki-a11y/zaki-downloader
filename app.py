from flask import Flask, request, send_file, render_template_string
import yt_dlp
import os
import glob
import time

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Zaki Downloader</title>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap" rel="stylesheet">
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Cairo', sans-serif; }
        body { background-color: #0f172a; color: #fff; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .container { background-color: #1e293b; padding: 40px; border-radius: 15px; box-shadow: 0 10px 25px rgba(0,0,0,0.5); width: 90%; max-width: 500px; text-align: center; }
        h1 { color: #38bdf8; margin-bottom: 10px; font-size: 2rem; }
        p { color: #94a3b8; margin-bottom: 30px; font-size: 1rem; }
        input[type="text"] { width: 100%; padding: 15px; border-radius: 8px; border: 2px solid #334155; background-color: #0f172a; color: #fff; font-size: 1rem; margin-bottom: 20px; transition: border 0.3s; }
        input[type="text"]:focus { outline: none; border-color: #38bdf8; }
        button { width: 100%; padding: 15px; background-color: #38bdf8; color: #0f172a; border: none; border-radius: 8px; font-size: 1.2rem; font-weight: bold; cursor: pointer; transition: background 0.3s; }
        button:hover { background-color: #0ea5e9; }
        .msg { margin-top: 20px; padding: 15px; border-radius: 8px; font-weight: bold; }
        .success { background-color: #064e3b; color: #34d399; }
        .error { background-color: #7f1d1d; color: #f87171; text-align: left; direction: ltr; font-size: 0.9rem; word-wrap: break-word;}
    </style>
</head>
<body>
    <div class="container">
        <h1>Zaki Downloader 🚀</h1>
        <p>حمل الفيديوهات من يوتيوب، تيك توك، إنستغرام.</p>
        <form action="/download" method="post">
            <input type="text" name="url" placeholder="حط رابط الفيديو هنا..." required>
            <button type="submit">تحميل الفيديو 🎬</button>
        </form>
        {% if message %}
            <div class="msg {{ msg_type }}">{{ message }}</div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_PAGE)

@app.route('/download', methods=['POST'])
def download_video():
    video_url = request.form.get('url')
    if not video_url:
        return render_template_string(HTML_PAGE, message="عافاك حط رابط صحيح.", msg_type="error")
    
    unique_id = int(time.time())
    output_template = f'downloaded_video_{unique_id}.%(ext)s'
    
    # استراتيجيات التحميل: كيجرب أحسن جودة، وإلا كيرجع لصيغة mp4 جاهزة
    ydl_opts = {
        'format': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]/best[ext=mp4]/best',
        'outtmpl': output_template,
        'quiet': False,
        'noplaylist': True,
        'nocheckcertificate': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
            
        video_files = glob.glob(f'downloaded_video_{unique_id}.*')
        if not video_files:
            return render_template_string(HTML_PAGE, message="الملف ماتحملش (ما لقيت حتى ملف).", msg_type="error")
            
        video_path = video_files[0]
        return send_file(video_path, as_attachment=True, download_name="video.mp4")
        
    except Exception as e:
        error_msg = str(e)
        print(f"\n❌ الخطأ: {error_msg}\n")
        return render_template_string(HTML_PAGE, message=f"Error: {error_msg}", msg_type="error")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
