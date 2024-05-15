from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Update the database URI to match your MySQL database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:example@db/student_database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Suppress SQLAlchemy warning

db = SQLAlchemy(app)

# Define the Student model
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    cgpa = db.Column(db.Float, nullable=False)

# Home route to render index.html
@app.route('/')
def index():
    return render_template('index.html')

# Route to add student to the database
@app.route('/add_student', methods=['POST'])
def add_student():
    name = request.form['name']
    age = int(request.form['age'])
    cgpa = float(request.form['cgpa'])
    new_student = Student(name=name, age=age, cgpa=cgpa)
    db.session.add(new_student)
    db.session.commit()
    # Redirect to the student list page after adding a student
    return redirect(url_for('student_list'))

# Route to display list of students
@app.route('/student_list')
def student_list():
    students = Student.query.all()
    return render_template('student_list.html', students=students)

if __name__ == '__main__':
    # Create application context
    with app.app_context():
        # Create database tables if they don't exist
        db.create_all()
    # Run the application
    app.run(host='0.0.0.0', port=5000, debug=True)
