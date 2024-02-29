import sqlite3
import os
import logging
from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
from flask import flash
from flask import redirect
from werkzeug.exceptions import abort


def get_db_connection():
    file_db = "database.db"
    if not os.path.exists(file_db):
        logging.basicConfig(
            filename="app.log",
            filemode="w",
            format="%(name)s - %(levelname)s - %(message)s",
        )
        logging.error("Exception Can't find this db %s", file_db)
        abort(500)
    conn = sqlite3.connect(file_db)
    conn.row_factory = sqlite3.Row
    return conn


def get_post(post_id):
    conn = get_db_connection()
    try:
        post = conn.execute("SELECT * FROM posts WHERE id = ? ", (post_id,)).fetchone()
    except sqlite3.Error as e:
        logging.basicConfig(
            filename="app.log",
            filemode="w",
            format="%(name)s - %(levelname)s - %(message)s",
        )
        logging.error("SQlite Error: %s ", e, exc_info=True)
        abort(500)
    finally:
        conn.close()

    if post is None:
        abort(404)
    return post


def get_all_posts(type_id):
    conn = get_db_connection()
    try:
        posts = conn.execute(
            "SELECT * FROM posts where type_id = ?", (type_id,)
        ).fetchall()

    except sqlite3.Error as e:
        logging.basicConfig(
            filename="app.log",
            filemode="w",
            format="%(name)s - %(levelname)s - %(message)s",
        )
        logging.error("SQlite Error: %s ", e, exc_info=True)
        abort(500)
    finally:
        if conn:
            conn.close()
    return posts


def get_type_id(id):
    conn = get_db_connection()
    try:
        post_type = conn.execute(
            "SELECT type_id FROM posts WHERE id = ? ", (id,)
        ).fetchone()[0]
    except sqlite3.Error as e:
        logging.basicConfig(
            filename="app.log",
            filemode="w",
            format="%(name)s - %(levelname)s - %(message)s",
        )
        logging.error("SQlite Error: %s ", e, exc_info=True)
        abort(500)
    finally:
        conn.close()
    return post_type


app = Flask(__name__, template_folder="template")
app.config["SECRET_KEY"] = "xfDwsAuM7xXROnBiqkV3fQ"


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500


@app.route("/")
def index():
    type_id = 2
    posts = get_all_posts(type_id)
    return render_template("index.html", posts=posts)


@app.route("/<int:post_id>")
def post(post_id):
    post = get_post(post_id)
    return render_template("post.html", post=post)


@app.route("/about")
def about():
    conn = get_db_connection()
    try:
        main_post_id = conn.execute(
            "SELECT id FROM posts where type_id = 1"
        ).fetchone()[0]
    except sqlite3.Error as e:
        logging.basicConfig(
            filename="app.log",
            filemode="w",
            format="%(name)s - %(levelname)s - %(message)s",
        )
        logging.error("SQlite Error: %s ", e, exc_info=True)
        abort(500)
    except Exception as e:
        logging.error("Error: %s ", e, exc_info=True)
        abort(404)
    finally:
        conn.close()
    post = get_post(main_post_id)
    return render_template("about.html", post=post)


@app.route("/friends")
def friends():
    type_id = 3
    posts = get_all_posts(type_id)
    return render_template("friends.html", posts=posts)


@app.route("/create", methods=("GET", "POST"))
def create():
    conn = get_db_connection()
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        photo = request.form["photo"]
        photo_name = request.form["photo_name"]
        type_id = int(request.form["type_id"])

        if not title:
            flash("Title is required!")
        else:
            try:
                conn.execute(
                    "INSERT INTO posts (title, content, photo, photo_name, type_id) VALUES (?, ?, ?, ?, ?)",
                    (title, content, photo, photo_name, type_id),
                )
                conn.commit()
            except sqlite3.Error as e:
                logging.basicConfig(
                    filename="app.log",
                    filemode="w",
                    format="%(name)s - %(levelname)s - %(message)s",
                )
                logging.error("SQlite Error: %s ", e, exc_info=True)
                abort(500)
            finally:
                conn.close()

            return redirect(url_for("index"))

    return render_template("create.html")


@app.route("/<int:id>/edit", methods=("GET", "POST"))
def edit(id):
    conn = get_db_connection()
    post = get_post(id)
    post_type = get_type_id(id)

    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        photo = request.form["photo"]
        photo_name = request.form["photo_name"]
        type_id = int(request.form["type_id"])

        if not title:
            flash("Title is required!")
        else:
            try:
                post_type = conn.execute(
                    "SELECT type_id FROM posts WHERE id = ? ", (id,)
                ).fetchone()[0]
                conn.execute(
                    "UPDATE posts SET title = ?, content = ?, photo = ?, photo_name = ?, type_id = ?"
                    " WHERE id = ?",
                    (title, content, photo, photo_name, type_id, id),
                )
                conn.commit()
            except sqlite3.Error as e:
                logging.basicConfig(
                    filename="app.log",
                    filemode="w",
                    format="%(name)s - %(levelname)s - %(message)s",
                )
                logging.error("SQlite Error: %s ", e, exc_info=True)
                abort(500)
            finally:
                conn.close()

            if type_id == 1:
                return redirect(url_for("about"))
            elif type_id == 2:
                return redirect(url_for("index"))
            else:
                return redirect(url_for("friends"))

    return render_template("edit.html", post=post, post_type=post_type)


@app.route("/<int:id>/delete", methods=("POST",))
def delete(id):
    conn = get_db_connection()
    post = get_post(id)
    try:
        conn.execute("DELETE FROM posts WHERE id = ?", (id,))
        conn.commit()

    except sqlite3.Error as e:
        logging.basicConfig(
            filename="app.log",
            filemode="w",
            format="%(name)s - %(levelname)s - %(message)s",
        )
        logging.error("SQlite Error: %s ", e, exc_info=True)
        abort(500)
    finally:
        conn.close()
    flash('"{}" was successfully deleted!'.format(post["title"]))
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True, port=5001)
