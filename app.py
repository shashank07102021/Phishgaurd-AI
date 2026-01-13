from flask import Flask
from routes.scan import scan_bp
from routes.incidents import incidents_bp
from routes.reports import reports_bp

app = Flask(__name__)

app.register_blueprint(scan_bp)
app.register_blueprint(incidents_bp)
app.register_blueprint(reports_bp)

if __name__ == "__main__":
    app.run(debug=True)
