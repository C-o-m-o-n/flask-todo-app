from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = 'secret key'
#todo database
class Todo(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  item = db.Column(db.String)
  complete = db.Column(db.Boolean)
  
  def __repr__(self):
    return  self.item


with app.app_context():
  @app.route("/", methods=['GET','POST'])
  def home():
    todo = Todo.query.all()
    return render_template("home.html", todo=todo)
  
  @app.route('/add', methods=['POST'])
  def add():
    todo_item = request.form['todoitem']
      todos = Todo(item=todo_item, complete=False)
    db.create_all()
    db.session.add(todos)
    db.session.commit()
    return redirect(url_for('home'))
    
  @app.route('/update/<int:todo_id>')
  def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for('home'))
    
  @app.route('/delete/<int:todo_id>')
  def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('home'))

  
  if __name__ == "__main__":
    app.run(debug=True)