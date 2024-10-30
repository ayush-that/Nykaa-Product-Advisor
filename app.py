from flask import Flask, render_template, request, jsonify
from parse import process_with_gemini
from scrape import scrape_website, extract_body_content, clean_body_content

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        url = request.json.get("url")
        if not url:
            return jsonify({"error": "URL is required"}), 400

        result = scrape_website(url)
        body_content = extract_body_content(result)
        cleaned_content = clean_body_content(body_content)

        return jsonify({"content": cleaned_content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/recommend", methods=["POST"])
def recommend():
    try:
        data = request.json
        content = data.get("content")
        question = data.get("question")

        if not content or not question:
            return jsonify({"error": "Content and question are required"}), 400

        response = process_with_gemini(content, question)
        return jsonify({"recommendation": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/how-to-use")
def how_to_use():
    return render_template("how_to_use.html")


if __name__ == "__main__":
    app.run(debug=True)
