from flask import Flask, render_template, request, redirect, url_for
from models import db, User
from forms import UsersForm


app = Flask(__name__)

db.init_app(app)

app.secret_key='e14a-key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Swagger123!@localhost/usersdb'

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/users', methods=['GET', 'POST'])
def users():
  saved_users = User.query.all()
  return render_template('users.html', saved_users=saved_users)

@app.route('/add-user', methods=['GET','POST'])
def add_user():
    form = UsersForm()
    if request.method == 'GET':
        return render_template('add_user.html', form=form)
    else:
        if form.validate_on_submit():
            first_name = request.form['first_name']
            age = request.form['age']
            new_user = User(first_name=first_name, age=age)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('index'))

@app.route("/update", methods=["POST"])
def update():
    newtitle = request.form.get("newname")
    oldtitle = request.form.get("oldname")
    user = User.query.filter_by(first_name=oldtitle).first()
    user.first_name = newtitle
    db.session.commit()

    return redirect("/")

@app.route("/update2", methods=["POST"])
def update2():
    newage = request.form.get("newage")
    oldage = request.form.get("oldage")
    user = User.query.filter_by(age=oldage).first()
    user.age = newage
    db.session.commit()

    return redirect("/")

@app.route("/delete", methods=["POST"])
def delete():
    first_name = request.form.get("user")
    user = User.query.filter_by(first_name=first_name).first()
    db.session.delete(user)
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)