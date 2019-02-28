from flask import send_from_directory,Flask, jsonify, request
import sqlite3
import os

static_file_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)),'static')

CONST_BOT_ID = "Y2lzY29zcGFyazovL3VzL0FQUExJQ0FUSU9OL2QzYzlmYmFmLTUxNTQtNGFhMC1hMjAxLTdlOTYyMWU5MTYwOQ"
CONST_BOT_ACCESS_TOKEN = "ZTMyYmRjNzEtMWNhNC00NmEwLTkyZjEtMDQ1ZjMwOTdhYTVlNTFkOTgzOTItYmM3_PF84_consumer"
CONST_MESSAGE_URL = "https://api.ciscospark.com/v1/messages"
name = "Móré Roland"
age = "16"
def push(name, age):
    with sqlite3.connect('about.db') as conn:
        cur = conn.cursor()
        sql = f"INSERT INTO person (name, age) VALUES ('{name}', {age});"
        cur.execute(sql)
        conn.commit()
def fetch():
    with sqlite3.connect('about.db') as conn:
        cur = conn.cursor()
        result = cur.execute("SELECT * FROM person ORDER BY id DESC;").fetchone()
        return jsonify(id = result[0], name = result[1], age = result[2])
def initDatabase():
    conn = sqlite3.connect('about.db')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS person (id INTEGER PRIMARY KEY, name VARCHAR(100), age INTEGER)")
    conn.commit()
def send_text(roomID,text):
    r = requests.post(CONST_MESSAGE_URL,headers={'Authorization': 'Bearer ' + CONST_BOT_ACCESS_TOKEN},data={'roomId': roomID, 'text': text})
    return True
app = Flask(__name__)
@app.route("/api/requests", methods = ['POST'])
def handle_ask():
    message = request.json
    print(message)
    id = message["data"]["id"]
    print(id)
    r = requests.get(CONST_MESSAGE_URL + "/" + id, headers={'Authorization': 'Bearer ' + CONST_BOT_ACCESS_TOKEN})
    message = r.json()["text"]
    print(message)
    message_array = message.split(" ")
    if message_array[1] == "Hello":
        roomID = r.json()["roomId"]
        send_text(roomID,text)
    return jsonify(message)


def index():
    return app.send_static_file('index.html')
@app.route("/api/bot")
@app.route('/<path:path>', methods=['GET'])
def static_page(path):
    return send_from_directory(static_file_dir,path)
@app.route("/api/about", methods = ['POST', 'GET'])
def about():
    if request.method == 'GET':
        return fetch()
    elif request.method == 'POST':
        r = request.json
        name = r["name"]
        age = r["age"]
        push(name,age)
        return jsonify(name = name, age = age)
@app.route("/api/helloworld")
def hello():
    return "Hello World!"
initDatabase()
push("Charles Webex",15)
if __name__ == "__main__":
    app.run()
