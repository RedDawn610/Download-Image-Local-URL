from flask import Flask, request, render_template, redirect, url_for, flash
import os
import requests
import webbrowser
from threading import Timer
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'super secret key'

DOWNLOAD_FOLDER = r'*YOUR DOWNLOAD PATH*'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(url):
    return '.' in url and url.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_image_url():
    if request.method == 'POST':
        image_url = request.form.get('image_url')
        
        if image_url and allowed_file(image_url):
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
                'Referer': 'https://www.instagram.com/'
            }
            
            try:
                response = requests.get(image_url, headers=headers)
                if response.status_code == 200:
                    filename = secure_filename(image_url.split('/')[-1])
                    file_path = os.path.join(DOWNLOAD_FOLDER, filename)
                    
                    with open(file_path, 'wb') as f:
                        f.write(response.content)
                    flash('Image successfully downloaded.')
                    print('Image successfully downloaded.')  
                else:
                    flash('Failed to download image. Status Code: ' + str(response.status_code))
                    print('Failed to download image. Status Code: ' + str(response.status_code))  
            except Exception as e:
                flash(f'An error occurred: {str(e)}')
                print(f'An error occurred: {str(e)}')  
        else:
            flash('Unsupported file type.')
            print('Unsupported file type.')  

        return redirect(url_for('upload_image_url'))

    return render_template('upload.html')

def open_browser():
      webbrowser.open_new('http://127.0.0.1:5000/')

if __name__ == '__main__':
    if not os.path.exists(DOWNLOAD_FOLDER):
        os.makedirs(DOWNLOAD_FOLDER)
    Timer(1, open_browser).start()  
    app.run(debug=True)
