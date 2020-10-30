from flask import Flask
from flask import render_template
from flask import request
import sqlite3 as sql

app = Flask(__name__)


@app.route('/admin')
def admin_login_page():
    return render_template('admin_login.html')


@app.route('/validate_admin', methods=['POST'])
def validateAdmin():
    uname = request.form.get("t1")
    upass = request.form.get("t2")

    if uname == "Sunil" and upass == "Sunil@2914":
        return render_template("admin_welcome.html")
    else:
        mess = {"error": "Invalid User"}
        return render_template("admin_login.html", message=mess)


@app.route('/admin_home')
def adminHome():
    return render_template("admin_welcome.html")


@app.route('/new_class')
def newClass():
    return render_template("new_class.html")


@app.route('/save_course', methods=['POST'])
def save_course():
    cname = request.form.get("c1")
    fname = request.form.get("c2")
    date = request.form.get("c3")
    time = request.form.get("c4")
    fee = request.form.get("c5")
    dur = request.form.get("c6")

    conn = sql.connect("onlineclasses.sqlite2")
    curs = conn.cursor()
    curs.execute("select max(cno) from course")
    res = curs.fetchone()

    if res[0]:
        cno = res[0] + 1
    else:
        cno = 1001
    curs.execute("insert into course values (?,?,?,?,?,?,?)", (cno, cname, fname, date, time, fee, dur))
    conn.commit()
    conn.close()
    return render_template("new_class.html", message="New class is Saved")

@app.route('/view_schedule_class')
def view_schedule_class():
    conn =sql.connect("onlineclasses.sqlite2")
    curs =conn.cursor()
    curs.execute("select * from course")
    result=curs.fetchall()
    conn.close()
    return render_template("view_schedule_class.html",data=result)

@app.route('/update_course')
def update_course():
    idno=request.args.get("cid")
    conn = sql.connect("onlineclasses.sqlite2")
    curs = conn.cursor()
    curs.execute("select * from course where cno =?",(idno,))
    res=curs.fetchone()
    return render_template('update_course.html',data=res)

@app.route('/save_update_course',methods=['POST'])
def save_update_course():
    cid=request.form.get("c0")
    cname = request.form.get("c1")
    fname = request.form.get("c2")
    date = request.form.get("c3")
    time = request.form.get("c4")
    fee = request.form.get("c5")
    dur = request.form.get("c6")

    conn = sql.connect("onlineclasses.sqlite2")
    curs = conn.cursor()
    curs.execute("update course set course_name =?,faculty_name=?,class_date=?,class_time=?,fee=?,duration=? where cno=?",(cname,fname,date,time,fee,dur,cid))
    conn.commit()
    return  view_schedule_class()

if __name__ == '__main__':
    app.run(debug=True)
