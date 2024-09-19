from flask import Flask, render_template, redirect, url_for, flash, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import bcrypt

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///C:/Users/Nethmi/Desktop/flask project/todo.db'
app.config["SQLALCHEMY_BINDS"] = {'login': 'sqlite:///C:/Users/Nethmi/Desktop/flask project/log.db'}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'jbjbvjhjdhvk jvlzkn'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    status = db.Column(db.Boolean, default=False)
    name = db.Column(db.String(100))


class User(db.Model):
    __bind_key__ = "login"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))


@app.route("/")
def home():
    todos = Todo.query.all()
    total = Todo.query.count()
    com_todo = Todo.query.filter_by(status=True).count()
    return render_template("home.html", todos=todos, total=total, com_todo=com_todo)


@app.route("/add", methods=["POST"])
def add():
    title = request.form.get('title')
    new_todo = Todo(title=title)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for('home'))


@app.route("/delete/<int:id>")
def delete(id):
    todo = Todo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('home'))


@app.route("/update/<int:id>")
def update(id):
    todo = Todo.query.get_or_404(id)
    todo.status = not todo.status
    db.session.commit()
    return redirect(url_for('home'))


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['Password']
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            session['email'] = user.email
            session['password'] = user.password
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password', category='error')
            return render_template('login.html', error='Invalid user')

    return render_template('login.html')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        password2 = request.form['password2']

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email is already used', category='error')
        elif password != password2:
            flash('Passwords do not match', category='error')
        elif len(password) < 5:
            flash('Password must be at least 5 characters long', category='error')
        else:
            new_user = User(name=name, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful. Please log in.', category='success')
            return redirect(url_for('login'))

    return render_template('register.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
