from flask import Flask, render_template, request, jsonify, Response
import requests
import re

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    
    # Step 1: Get the apikey and sid from Keepv.id
    result = requests.get('https://keepv.id', headers={'User-Agent': 'Mozilla/5.0'})
    matches = re.findall(r"<script>apikey='(.*)';sid='(.*)';</script>", result.text)
    
    if not matches:
        return "Unable to extract API key and SID", 500
    
    apikey, sid = matches[0]
    set_cookie = result.headers['Set-Cookie']
    
    # Step 2: Send the POST request with the video URL and SID
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': set_cookie,
        'User-Agent': 'Mozilla/5.0'
    }
    data = {
        'url': url,
        'sid': sid
    }
    
    result2 = requests.post('https://keepv.id/api/ajaxSearch', headers=headers, data=data)
    
    # Step 3: Extract download link from the response
    matches2 = re.findall(r'href="(.*?)" download=', result2.text)
    
    if not matches2:
        return "Unable to extract download link", 500
    
    download_url = matches2[0]
    
    # Stream the video content
    def generate():
        with requests.get(download_url, stream=True) as r:
            r.raise_for_status()
            for chunk in r.iter_content(chunk_size=8192):
                yield chunk
    
    return Response(generate(), mimetype='video/mp4', headers={"Content-Disposition": "attachment; filename=video.mp4"})

if __name__ == '__main__':
    app.run(debug=True)
