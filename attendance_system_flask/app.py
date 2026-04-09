import os
from flask import Flask, render_template
from config import Config  # Config loads .env first

app = Flask(__name__)
app.config.from_object(Config)

# Import and register blueprints
from admin.routes import admin_bp
from lecturer.routes import lecturer_bp

app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(lecturer_bp, url_prefix='/lecturer')

@app.route('/')
def index():
    return render_template('index.html')

@app.errorhandler(404)
def not_found(e):
    return render_template('index.html'), 404

@app.errorhandler(500)
def server_error(e):
    return f"<h2>Server Error</h2><pre>{e}</pre>", 500

if __name__ == '__main__':
    app.run(debug=True)
