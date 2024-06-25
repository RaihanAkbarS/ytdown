from flask import Flask, render_template, request, Response
import yt_dlp

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
        'outtmpl': '-',  # Stream directly to stdout
    }

    def generate():
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info_dict = ydl.extract_info(url, download=False)
                ydl.download([url])
            except yt_dlp.utils.DownloadError as e:
                yield str(e)
    
    return Response(generate(), mimetype='video/mp4', headers={"Content-Disposition": "attachment; filename=video.mp4"})

if __name__ == '__main__':
    app.run(debug=True)
