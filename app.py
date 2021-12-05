from flask import *
from werkzeug.utils import secure_filename
import os
import tempfile
import shutil
import img2pdf
from PIL import Image



app = Flask(__name__, static_url_path="/static")



@app.route('/', methods = ['GET', 'POST'])
def upload_file():
    # dirname = tempfile.TemporaryDirectory(dir="./")
    dirpath = tempfile.mkdtemp()
    button = ""
    if request.method == 'POST':
        f = request.files['file']
        f.save(os.path.join(dirpath, secure_filename(f.filename)))
        filename = os.listdir(dirpath)[0]
        image_path = f"{dirpath}/{filename}"
        pdf_path = f"static/downloads/output.pdf"
        image = Image.open(image_path)
        pdf_bytes = img2pdf.convert(image.filename)
        file = open(pdf_path, "wb")
        file.write(pdf_bytes)
        image.close()
        file.close()
        print("Successfully made pdf file")
        button = "done"
        shutil.rmtree(dirpath)

    return render_template("index.html", button=button)

@app.route('/download')
def download_file():
	path = f"static/downloads/output.pdf"
	return send_file(path, as_attachment=True)

if __name__ == '__main__':
   app.run(threaded=True)
