from flask import Flask, flash, redirect, render_template, request
import wave
from pydub import AudioSegment
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('numbers.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    db = get_db_connection()
    langs = db.execute("SELECT tbl_name FROM sqlite_master WHERE type = 'table';").fetchall()
    max = db.execute("SELECT MAX(number) FROM english;").fetchall()[0]["MAX(number)"]
    db.close()
    return render_template("index.html", langs=langs, max=max)
    
@app.route("/counter", methods=["POST"])
def Counter():
    dbb = get_db_connection()
    db = dbb.cursor()
    max = db.execute("SELECT MAX(number) FROM english;").fetchall()[0]["MAX(number)"]
    a = db.execute("SELECT COUNT(tbl_name) FROM sqlite_master WHERE type='table';").fetchall()[0]["COUNT(tbl_name)"]
    langs2 = db.execute("SELECT tbl_name FROM sqlite_master WHERE type = 'table';").fetchall()
    langs = []
    for i in range(a):
        langs.append(langs2[i]["tbl_name"])
    lang = request.form.get('lang')
    try:
        number = int(request.form.get('number'))
    except ValueError:
        eror = "Please select the desired number"
        return render_template("eror.html", eror=eror)
    if number > max:
        eror = "The desired number is greater than the maximum!"
        return render_template("eror.html", eror=eror)
    if number < 1 :
        eror = "Your number must be greater than 1!"
        return render_template("eror.html", eror=eror)
    try:
        sepetition = int(request.form.get('sepetition'))
    except ValueError:
        eror = "Please select the desired sepetition"
        return render_template("eror.html", eror=eror)
    try:    
        speed = float(request.form.get('speed'))
    except ValueError:
        eror = "Please select the desired speed"
        return render_template("eror.html", eror=eror)
    if (lang == None):
        eror = "Please select the desired language"
        return render_template("eror.html", eror=eror)
    if (speed < 0.5):
        eror = "Speed must be greater than 0.5"
        return render_template("eror.html", eror=eror)
    if (lang not in langs):
        eror = "The language you want is not available"
        return render_template("eror.html", eror=eror)
    name = db.execute("SELECT tbl_name FROM sqlite_master WHERE type = 'table' AND name = ?", (lang,)).fetchall()[0]["tbl_name"]
    numbers = db.execute(f"SELECT file FROM {name} WHERE number <= {number}").fetchall()
    num = []
    for i in range(number):
        num.append(numbers[i]["file"])
    db.close()
    infiles = num
    outfile = "counter.wav"
    data= []
    for infile in infiles:
        w = wave.open(infile, 'rb')
        data.append( [w.getparams(), w.readframes(w.getnframes())] )
        w.close()
    output = wave.open(outfile, 'wb')
    output.setparams(data[0][0])
    for i in range(number):
        output.writeframes(data[i][1])
    output.close()

    sep = []
    for i in range(sepetition):
        sep.append("counter.wav") 
    infiles = sep
    outfile = "counter2.wav"
    data= []
    for infile in infiles:
        w = wave.open(infile, 'rb')
        data.append( [w.getparams(), w.readframes(w.getnframes())] )
        w.close()
    output = wave.open(outfile, 'wb')
    output.setparams(data[0][0])
    for i in range(sepetition):
        output.writeframes(data[i][1])
    output.close()

    if speed > 0.5:
        root = r'counter2.wav'
        velocidad_X = speed * 2
        sound = AudioSegment.from_file(root)
        so = sound.speedup(velocidad_X, 150, 25)
        so.export('static\sound\Counter.mp3', format = 'mp3')
    else:
        root = r'counter2.wav'
        sound = AudioSegment.from_file(root)
        sound.export('static\sound\Counter.mp3', format = 'mp3')

    return render_template("Output.html")


