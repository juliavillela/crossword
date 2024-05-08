import os
import uuid
import zipfile

from flask import Flask, request, session, flash, render_template, redirect, send_from_directory, url_for, send_file

from .helpers import validate_word_list, clean_word_list_input, delete_session_files
from .crosword_generator import CrosswordGenerator

app = Flask(__name__)
#testing secret key
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'

media_folder = os.path.join(app.root_path, 'media')

@app.route("/", methods = ["GET"])
def index():
    if not session.get("session_id"):
        session["session_id"] = str(uuid.uuid4())
    if request.method == "GET":
        return render_template("index.html")

@app.route("/create", methods=["GET", "POST"])
def create_form():
    if request.method == "POST":
        form_data = request.form
        word_list = [form_data[name] for name in form_data if form_data[name] != ""]
        session["word_list"] = clean_word_list_input(word_list)
        (valid, message) = validate_word_list(session["word_list"])
        if valid:
            session["word_list_is_valid"] = True
            return redirect("/generate_crossword")
            
        else:
            session["word_list_is_valid"] = False
            flash(message)
            return redirect("/create")
    else:
        context = {
            "word_list": session.get("word_list")
        }
        return render_template("word_form.html", context=context)

@app.route("/clear", methods=["GET"])
def clear():
    session["word_list"] = None
    session["word_list_is_valid"] = False
    delete_session_files(session, media_folder)
    
    return redirect("create")

@app.route("/generate_crossword", methods =["GET"])
def generate_crossword():
    if not session.get("word_list") or not session.get("word_list_is_valid"):
        flash("you don't have a valid wordlist to create from")
        return redirect("/create")
    else:
        gen = CrosswordGenerator(session.get("word_list"))
        crossword = gen.generate()
        if crossword:
            crossword.save_key_img(os.path.join(media_folder, f'{session.get("session_id")}key.png'))
            crossword.save_blank_img(os.path.join(media_folder, f'{session.get("session_id")}blank.png'))
        else:
            print("COULD NOT generate")
        return redirect("/custom")
    
@app.route("/custom", methods =["GET"])
def custom_crossword():
    print("get request on custom crossword")
    context = {
        "word_list": session.get('word_list'),
        "key_img_path": url_for('media', filename=f'{session.get("session_id")}key.png'),
        "blank_img_path": url_for('media', filename=f'{session.get("session_id")}blank.png'),
    }
    return render_template("crossword.html", context=context)

@app.route("/download", methods=["GET"])
def download():
    key_path = os.path.join(media_folder, f'{session.get("session_id")}key.png')
    blank_path = os.path.join(media_folder, f'{session.get("session_id")}blank.png')
    
    # this would cause trouble if 2 different sessions are saving at the exact same time
    zip_filename = "media/my_crossword.zip"

    #create zip file:
    with zipfile.ZipFile(zip_filename, "w") as zip_file:
        zip_file.write(key_path, "key.png")
        zip_file.write(blank_path, "blank.png")

    return send_file(zip_filename, as_attachment=True)

@app.route('/media/<path:filename>')
def media(filename):
    return send_from_directory('media', filename)