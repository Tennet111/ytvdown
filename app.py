"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/

This file creates your application.
"""

import os
import glob
import lizhi
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'this_should_be_configured')

"""
def set_ffmpeg_env():
    files = glob.glob("./.heroku/python/bin/*")
    filenames = ''.join(files)
    if 'ffmpeg' not in filenames:
        print('Cannot find ffmpeg')
        os.system("cp ./ffmpeg/ffmpeg ./.heroku/python/bin/")
"""

###
# Routing for your application.
###


@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')

@app.route('/instruction/')
def instruction():
    """Render the website's about page."""
    return render_template('instruction.html')

@app.route('/download', methods=["get", "post"])
def download():
    if request.method == 'POST':
        # set_ffmpeg_env()
        url = request.form['url']
        if "lizhi.fm" in url:
            os.system("python lizhi.py " + url + " > static/downloads/log.txt &")    
        else:
            os.system("you-get " + url + " -o static/downloads/ > static/downloads/log.txt &")
        return "开始下载视频. 请在一段时间后回来查看已下载的视频. "
    else:
        return redirect("/")

@app.route('/files', methods=['POST', 'GET'])
def check_files():
  files = os.listdir('static/downloads');
  files.sort()
  converted_filenames = []
  for filename in files:
      filename = filename.replace('?', '%3F')
      filename = filename.replace('#', '%23')
      converted_filenames.append(filename)
  return render_template('files.html', files=converted_filenames)

@app.route('/delete', methods=['POST'])
def delete():
    filename = request.form['filename']
    os.system('rm \"./static/downloads/' + filename + '\"')
    return redirect('/files')

@app.route('/convert_mp3', methods=['POST', 'GET'])
def convert_mp3():
  if request.methd == 'POST':
    filename = request.form['filename']
    fileout = filename[:-4] + ".mp3"
    os.system('./ffmpeg/ffmpeg -i \"./static/downloads/' + filename + '\" -b:a 32k ' + '\"./static/downloads/' + fileout + '\" > static/downloads/log.txt &')
    return "开始转换. 请在一段时间后回来查看转换好的音频. "
  else:
    return redirect("/")

###
# The functions below should be applicable to all Flask apps.
###

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=600'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8080)
