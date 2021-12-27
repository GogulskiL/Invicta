from flask import Flask
from flask.helpers import send_file
from sqlite3.dbapi2 import Error
import requests
import json
import sqlite3
import csv


url_user = "https://jsonplaceholder.typicode.com/users"
url_todos = "https://jsonplaceholder.typicode.com/todos"
database = "demo.db"


def get_json(url):
    response = requests.get(url)
    return json.loads(response.text)


def user_json_praser(data_json_user):
    users = []
    for one_user in range(len(data_json_user)):
        row = {}
        row["id"] = data_json_user[one_user]["id"]
        row["name"] = data_json_user[one_user]["name"]
        row["city"] = data_json_user[one_user]["address"]["city"]
        users.append(row)
    return users


def todos_json_praser(data_jason_todos):
    todos = []
    for one_todos in range(len(data_jason_todos)):
        row = {}
        row["userId"] = data_jason_todos[one_todos]["userId"]
        row["id"] = data_jason_todos[one_todos]["id"]
        row["title"] = data_jason_todos[one_todos]["title"]
        row["completed"] = data_jason_todos[one_todos]["completed"]
        todos.append(row)
    return todos


def connect_database(database):
    conn = sqlite3.connect(database)
    return conn


def create_table_user(databes):
    conn = connect_database(databes)
    c = conn.cursor()
    c.execute(""" CREATE TABLE IF NOT EXISTS users (id INTEGER, name TEXT, city TEXT); """)
    conn.commit()
    c.close()
    conn.close()


def create_table_todos(database):
    conn = connect_database(database)
    c = conn.cursor()
    c.execute(""" CREATE TABLE IF NOT EXISTS todos (userId INTEGER, id INTEGER, title TEXT, completed INTEGER);""")
    conn.commit()
    c.close()
    conn.close()


def fill_user_column(url, database):
    table = user_json_praser(get_json(url))
    conn = connect_database(database)
    c = conn.cursor()
    for i in table:
        id = i["id"]
        name = i["name"]
        city = i["city"]
        data_tuple = (id, name, city)
        c.execute(
            """ SELECT * FROM users WHERE id = ? AND name =? AND city = ? """, (data_tuple))
        result = c.fetchone()
        if result:
            print("Dane już istnieją")
        else:
            sql_insert = (
                """ INSERT INTO users (id, name, city) VALUES (?, ?, ?) """)
            c.execute(sql_insert, data_tuple)
    conn.commit()
    c.close()
    conn.close()


def fill_todos_column(url, database):
    table = todos_json_praser(get_json(url))
    conn = connect_database(database)
    c = conn.cursor()
    for i in table:
        userID = i["userId"]
        id = i["id"]
        title = i["title"]
        completed = i["completed"]
        if completed == True:
            completed = 1
        else:
            completed = 0
        data_tuple = (userID, id, title, completed)
        c.execute(
            """ SELECT * FROM todos WHERE userId = ? AND id = ? AND title = ? AND completed = ? """, (data_tuple))
        result = c.fetchone()
        if result:
            print("Dane już istnieją")
        else:
            sql_insert = (
                """ INSERT INTO todos (userId, id, title, completed) VALUES (?, ?, ?, ?) """)
            c.execute(sql_insert, data_tuple)
    conn.commit()
    c.close()
    conn.close()


def users(url, databes):
    create_table_user(databes)
    fill_user_column(url, databes)


def todos(url, database):
    create_table_todos(database)
    fill_todos_column(url, database)


def serch_data(database):
    conn = connect_database(database)
    c = conn.cursor()
    query = c.execute(
        """ SELECT name, city, title, completed FROM users JOIN todos ON users.id = todos.userId ORDER BY users.id """)
    data_tuple = []
    for i in query:
        x = [i[0], i[1], i[2], i[3]]
        data_tuple.append(x)
    data_users = []
    for i in data_tuple:
        completed = i[3]
        if completed == 1:
            completed = True
        else:
            completed = False
        x = [i[0], i[1], i[2], completed]
        data_users.append(x)
    conn.commit()
    c.close()
    conn.close()
    return data_users


def csv_file_create(database):
    data = serch_data(database)
    with open("import_data_db.csv", "w", newline="") as csvfile:
        csvwirter = csv.writer(csvfile)
        csvwirter.writerow(["name", "city", "title", "completed"])
        for i in data:
            csvwirter.writerow(i)


def main(url_user, url_todos, database):
    users(url_user, database)
    todos(url_todos, database)
    csv_file_create(database)


main(url_user, url_todos, database)


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


# if __name__ == '__main__':
#     app.run(debug=True, port=8080)
