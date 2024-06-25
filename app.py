from flask import Flask, render_template, request, Response, send_file
import yt_dlp
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    quality = request.form['quality']

    ydl_opts = {
        'format': f'best[height<={quality}]',
        'outtmpl': 'downloads/%(title)s.%(ext)s',  # Ensure the file is saved to a known location
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info_dict)
            
            if os.path.exists(file_path):
                return send_file(file_path, as_attachment=True)
            else:
                return "File not found", 404
    except yt_dlp.utils.DownloadError as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(debug=True)
