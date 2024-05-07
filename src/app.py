from flask import Flask, request,session, flash, render_template, redirect


app = Flask(__name__)
#testing secret key
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'

word_list = None

@app.route("/", methods = ["GET"])
def index():
    if request.method == "GET":
        context = {
            "word_list": session.get("word_list"),
        }
        return render_template("index.html", context=context)

@app.route("/create", methods=["GET", "POST"])
def create_form():
    from .helpers import validate_word_list, clean_word_list_input
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
    return redirect("create")

@app.route("/generate_crossword", methods =["GET"])
def generate_crossword():
    from .crosword_generator import CrosswordGenerator
    if not session.get("word_list") or not session.get("word_list_is_valid"):
        flash("you don't have a valid wordlist to create from")
        return redirect("/create")
    else:
        gen = CrosswordGenerator(session.get("word_list"))
        crossword = gen.generate()
        if crossword:
            crossword.save_key_img("./static/js/media/test_key.png")
            crossword.save_blank_img("./static/js/media/test_blank.png")
        else:
            print("COULD NOT generate")
        return redirect("/custom")
    
@app.route("/custom", methods =["GET"])
def custom_crossword():
    print("get request on custom crossword")
    context = {
        "word_list": session.get('word_list'),
        "key_img_path": "static/js/media/test_key.png",
        "blank_img_path": "static/js/media/test_blank.png"
    }
    return render_template("crossword.html", context=context)
