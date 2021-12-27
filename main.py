from flask import Flask
from flask.helpers import send_file


app = Flask(__name__)


@app.route("/")
def home():
    return f"<h1> Plik dostępny pod adresem <a href='http://127.0.0.1:8080/app/user_task'> http://127.0.0.1:8080/app/user_task</a></h1>"


@app.route("/app/user_task")
def get_file():
    return send_file('import_data_db.csv',
                     mimetype='text/csv',
                     attachment_filename='user_task.csv',
                     as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True, port=8080)
