from flask import *
from werkzeug.utils import secure_filename
import pytesseract
#import pyperclip
import re
import cv2


app = Flask(__name__)
app.config['MAX_CONTENT_PATH'] = 52428000
FileName = ""
extractedText = {"content": ""}

@app.route("/")
def home_page():
    return render_template('index.html')

@app.route("/convert" , methods = [ 'GET', 'POST'])
def convert():
    global FileName
    if request.method == 'POST':
        f = request.files['uploadFile']
        f.save(secure_filename(f.filename))
        FileName = f.filename
        return redirect(url_for('progress'))


@app.route("/extract")
def progress():
    return render_template('progress.html')


@app.route("/output")
def output():
    global extractedText
    img = cv2.imread(FileName)
    gimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gimg = cv2.threshold(gimg, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    out_below = pytesseract.image_to_string(gimg)
    # out_below = out_below[::-1]
    extractedText['content'] = out_below
    return render_template('output.html', extractedText = extractedText)

@app.route("/copytoclipboard")
def copytoclipboard():
    #pyperclip.copy(extractedText['content'])
    return render_template('output.html', extractedText = extractedText)
