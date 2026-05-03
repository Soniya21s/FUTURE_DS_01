from flask import Flask
from routes.main_routes import main_bp
from routes.prediction_routes import prediction_bp
from routes.dashboard_routes import dashboard_bp

app = Flask(__name__)

app.register_blueprint(main_bp)
app.register_blueprint(prediction_bp)
app.register_blueprint(dashboard_bp)

if __name__ == "__main__":
    app.run(debug=True)