import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect


app = Flask(__name__, template_folder="template")


if __name__ == "__main__":
    app.run(debug=True, port=5001)
