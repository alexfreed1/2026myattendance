from flask import Flask, render_template, redirect, url_for, session, request

app = Flask(__name__)
app.config.from_pyfile('config.py')

# Import and register blueprints
from admin.routes import admin_bp
from lecturer.routes import lecturer_bp

app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(lecturer_bp, url_prefix='/lecturer')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
