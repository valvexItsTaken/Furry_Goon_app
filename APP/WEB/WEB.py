from flask import Flask, render_template, jsonify, request
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/media_list')
def media_list():
    try:
        with open('media.json', 'r') as file:
            media_list = json.load(file)
        return jsonify(media_list)
    except FileNotFoundError:
        return jsonify([])

@app.route('/add_media', methods=['POST'])
def add_media():
    data = request.json
    new_media = {
        "name": data.get("name"),
        "url": data.get("url"),
        "image": data.get("image", "")
    }
    try:
        with open('media.json', 'r') as file:
            media_list = json.load(file)
    except FileNotFoundError:
        media_list = []
    media_list.append(new_media)
    with open('media.json', 'w') as file:
        json.dump(media_list, file, indent=4)
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(debug=True)