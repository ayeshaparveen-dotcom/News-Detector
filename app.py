from flask import Flask, render_template, request
from utils import detect_news

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    
    if request.method == "POST":
        article = request.form["article"]
        result = detect_news(article)
    
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True, port=5001, host="0.0.0.0")