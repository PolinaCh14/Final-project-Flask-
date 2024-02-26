import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort


def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute("SELECT * FROM posts WHERE id = ? ", (post_id,)).fetchone()
    conn.close()

    if post is None:
        abort(404)
    return post


app = Flask(__name__, template_folder="template")


@app.route("/")
def index():
    conn = get_db_connection()
    posts = conn.execute("SELECT * FROM posts where type_id = 2").fetchall()
    conn.close()
    return render_template("index.html", posts=posts)


@app.route("/<int:post_id>")
def post(post_id):
    post = get_post(post_id)
    return render_template("post.html", post=post)


@app.route("/about")
def about():
    conn = get_db_connection()
    main_post_id = conn.execute("SELECT id FROM posts where type_id = 1").fetchone()[0]
    post = get_post(main_post_id)
    conn.close()
    return render_template("about.html", post=post)


@app.route("/friends")
def friends():
    conn = get_db_connection()
    posts = conn.execute("SELECT * FROM posts where type_id = 3").fetchall()
    # post = get_post(f_post_id)
    conn.close()
    return render_template("friends.html", posts=posts)


@app.route("/create", methods=("GET", "POST"))
def create():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        photo = request.form["photo"]
        photo_name = request.form["photo_name"]
        type_id = int(request.form["type_id"])

        if not title:
            flash("Title is required!")
        else:
            conn = get_db_connection()
            conn.execute(
                "INSERT INTO posts (title, content, photo, photo_name, type_id) VALUES (?, ?, ?, ?, ?)",
                (title, content, photo, photo_name, type_id),
            )
            conn.commit()
            conn.close()
            return redirect(url_for("index"))

    return render_template("create.html")


@app.route("/<int:id>/edit", methods=("GET", "POST"))
def edit(id):
    post = get_post(id)
    conn = get_db_connection()
    post_type = conn.execute(
        "SELECT type_id FROM posts WHERE id = ? ", (id,)
    ).fetchone()[0]
    conn.close()

    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        photo = request.form["photo"]
        photo_name = request.form["photo_name"]
        type_id = int(request.form["type_id"])

        if not title:
            flash("Title is required!")
        else:
            conn = get_db_connection()

            conn.execute(
                "UPDATE posts SET title = ?, content = ?, photo = ?, photo_name = ?, type_id = ?"
                " WHERE id = ?",
                (title, content, photo, photo_name, type_id, id),
            )
            conn.commit()
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
    post = get_post(id)
    conn = get_db_connection()
    conn.execute("DELETE FROM posts WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post["title"]))
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True, port=5001)
