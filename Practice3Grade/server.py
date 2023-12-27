from flask import Flask, request, jsonify
import json
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)

log_formatter = logging.Formatter('%(asctime)s [%(levelname)s] - %(message)s')
file_handler = RotatingFileHandler('server.log', maxBytes=1024 * 1024, backupCount=1)
file_handler.setFormatter(log_formatter)
console_handler = logging.StreamHandler()
console_handler.setFormatter(log_formatter)

app.logger.addHandler(file_handler)
app.logger.addHandler(console_handler)
app.logger.setLevel(logging.INFO)

try:
    with open('db.json', 'r') as db_file:
        data = json.load(db_file)
except FileNotFoundError:
    data = {'posts': [], 'comments': [], 'profile': {}}
    with open('db.json', 'w') as db_file:
        json.dump(data, db_file)

posts = data['posts']
comments = data['comments']
profile = data['profile']

def log_data(route, data):
    app.logger.info(f"Route: {route}, Data: {json.dumps(data)}")

@app.route("/posts", methods=["GET"])
def get_posts():
    log_data("get_posts", request.args)
    return jsonify(posts)

@app.route("/posts", methods=["POST"])
def create_post():
    global posts
    data = request.get_json()
    post = {"ID": len(posts) + 1, "Title": data["title"], "Author": data["author"]}
    posts.append(post)
    log_data("create_post", data)
    update_db()
    return jsonify(post)

@app.route("/posts/<int:id>", methods=["GET"])
def get_post(id):
    log_data("get_post", {"id": id})
    for item in posts:
        if item["ID"] == id:
            return jsonify(item)
    return jsonify({})

@app.route("/posts/<int:id>", methods=["PUT"])
def update_post(id):
    global posts
    data = request.get_json()
    log_data("update_post", {"id": id, "data": data})
    for index, item in enumerate(posts):
        if item["ID"] == id:
            posts[index] = {"ID": id, "Title": data["title"], "Author": data["author"]}
            update_db()
            return jsonify(posts[index])
    return jsonify({})

@app.route("/posts/<int:id>", methods=["DELETE"])
def delete_post(id):
    global posts
    log_data("delete_post", {"id": id})
    posts = [item for item in posts if item["ID"] != id]
    update_db()
    return jsonify(posts)

@app.route("/posts/author/<author>", methods=["GET"])
def get_author_posts(author):
    log_data("get_author_posts", {"author": author})
    author_posts = [item for item in posts if item["Author"] == author]
    return jsonify(author_posts)

@app.route("/posts/<int:id>/comments", methods=["GET"])
def get_post_comments(id):
    log_data("get_post_comments", {"id": id})
    post_comments = [comment for comment in comments if comment["PostID"] == id]
    return jsonify(post_comments)

@app.route("/comments", methods=["GET"])
def get_comments():
    log_data("get_comments", request.args)
    return jsonify(comments)

@app.route("/comments", methods=["POST"])
def create_comment():
    global comments
    data = request.get_json()
    comment = {"ID": len(comments) + 1, "Body": data["body"], "PostID": data["postID"]}
    comments.append(comment)
    log_data("create_comment", data)
    update_db()
    return jsonify(comment)

@app.route("/comments/<int:id>", methods=["GET"])
def get_comment(id):
    log_data("get_comment", {"id": id})
    for item in comments:
        if item["ID"] == id:
            return jsonify(item)
    return jsonify({})

@app.route("/comments/<int:id>", methods=["PUT"])
def update_comment(id):
    global comments
    data = request.get_json()
    log_data("update_comment", {"id": id, "data": data})
    for index, item in enumerate(comments):
        if item["ID"] == id:
            comments[index] = {"ID": id, "Body": data["body"], "PostID": data["postID"]}
            update_db()
            return jsonify(comments[index])
    return jsonify({})

@app.route("/comments/<int:id>", methods=["DELETE"])
def delete_comment(id):
    global comments
    log_data("delete_comment", {"id": id})
    comments = [item for item in comments if item["ID"] != id]
    update_db()
    return jsonify(comments)

@app.route("/comments/post/<int:postID>", methods=["GET"])
def get_comments_post(postID):
    log_data("get_comments_post", {"postID": postID})
    post_comments = [comment for comment in comments if comment["PostID"] == postID]
    return jsonify(post_comments)

@app.route("/profile", methods=["GET"])
def get_profile():
    log_data("get_profile", request.args)
    return jsonify(profile)

@app.route("/profile", methods=["POST"])
def create_profile():
    global profile
    data = request.get_json()
    profile = {"name": data["name"]}
    log_data("create_profile", data)
    update_db()
    return jsonify(profile)

@app.route("/profile", methods=["PUT"])
def update_profile():
    global profile
    data = request.get_json()
    profile = {"name": data["name"]}
    log_data("update_profile", data)
    update_db()
    return jsonify(profile)

@app.route("/profile", methods=["DELETE"])
def delete_profile():
    global profile
    profile = {}
    log_data("delete_profile", {})
    update_db()
    return jsonify(profile)

def update_db():
    global posts, comments, profile
    data = {'posts': posts, 'comments': comments, 'profile': profile}
    with open('db.json', 'w') as db_file:
        json.dump(data, db_file, indent=2)

if __name__ == "__main__":
    app.run(port=5050)
