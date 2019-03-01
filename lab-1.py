from flask import send_from_directory,Flask, jsonify, request
import sqlite3
import os
import requests

static_file_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)),'static')

CONST_BOT_ID = "Y2lzY29zcGFyazovL3VzL0FQUExJQ0FUSU9OL2QzYzlmYmFmLTUxNTQtNGFhMC1hMjAxLTdlOTYyMWU5MTYwOQ"
CONST_BOT_ACCESS_TOKEN = "ZTMyYmRjNzEtMWNhNC00NmEwLTkyZjEtMDQ1ZjMwOTdhYTVlNTFkOTgzOTItYmM3_PF84_consumer"
CONST_MESSAGE_URL = "https://api.ciscospark.com/v1/messages"
name = "Móré Roland"
age = "16"
def init_Database():
    #conn = sqlite3.connect('about.db')
    #cur = conn.cursor()
    #cur.execute("CREATE TABLE IF NOT EXISTS person (id INTEGER PRIMARY KEY, name VARCHAR(100), age INTEGER)")
    #conn.commit()

    conn = sqlite3.connect('about.db')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS teams (id INTEGER PRIMARY KEY, name VARCHAR(100), teamid VARCHAR(100))")
    conn.commit()
def push(name, age):
    with sqlite3.connect('about.db') as conn:
        cur = conn.cursor()
        sql = f"INSERT INTO person (name, age) VALUES ('{name}', {age});"
        cur.execute(sql)
        conn.commit()
def insert_team(name):
    r = requests.post("https://api.ciscospark.com/v1/teams",headers={'Authorization': 'Bearer ' + CONST_BOT_ACCESS_TOKEN},data={'name': name})
    with sqlite3.connect('about.db') as conn:
        cur = conn.cursor()
        name = r.json()["text"]["name"]
        teamid=r.json()["text"]["id"]
        sql = f"INSERT INTO teams (name, teamid) VALUES ('{name}', {teamid});"
        cur.execute(sql)
        conn.commit()
def return_team():
    with sqlite3.connect('about.db') as conn:
        cur = conn.cursor()
        result = cur.execute("SELECT * FROM teams ORDER BY id DESC;").fetchone()
        return str(jsonify(id = result[0], name = result[1], teamid = result[2]))
def fetch():
    with sqlite3.connect('about.db') as conn:
        cur = conn.cursor()
        result = cur.execute("SELECT * FROM person ORDER BY id DESC;").fetchone()
        return jsonify(id = result[0], name = result[1], age = result[2])
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
    message_text = r.json()["text"]
    print(message_text)
    message_array = message_text.split(" ")
    if message_text.lower() == "hello" and message["data"]["personId"] != CONST_BOT_ID:
        roomID = r.json()["roomId"]
        send_text(roomID,"Szia!")
        return jsonify(message)
    elif message_text.lower() == "us" and message["data"]["personId"] != CONST_BOT_ID:
        roomID = r.json()["roomId"]
        send_text(roomID,"Roland botja vagyok")
        return jsonify(message)
    elif message_text.lower() == "help" and message["data"]["personId"] != CONST_BOT_ID:
        roomID = r.json()["roomId"]
        send_text(roomID,"->hello\n->us\n->help")
    elif message_text.lower() == "teams" and message["data"]["personId"] != CONST_BOT_ID:
        if message_array[1] == "show":
            roomID = r.json()["roomId"]
            send_text(roomID,return_team())
        elif message_array[1] == "create":
            roomID = r.json()["roomId"]
            send_text(roomID,insert_team(message_array[2]))



    elif len(message_array) > 1:
        if message_array[1].lower() == "hello":
            roomID = r.json()["roomId"]
            send_text(roomID,"Szia!")
            return jsonify(message)
        elif message_array[1].lower() == "us":
            roomID = r.json()["roomId"]
            send_text(roomID,"Roland botja vagyok")
            return jsonify(message)
        elif message_array[1].lower() == "help":
            roomID = r.json()["roomId"]
            send_text(roomID,"->hello\n->us\n->help")
            return jsonify(message)
        elif message_array[1].lower() == "teams":
            if message_array[2] == "show":
                roomID = r.json()["roomId"]
                send_text(roomID,return_team())
            elif message_array[2] == "create":
                roomID = r.json()["roomId"]
                send_text(roomID,insert_team(message_array[3]))
            return jsonify(message)
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
push("Charles Webex",15)
init_Database()
if __name__ == "__main__":
    app.run()
