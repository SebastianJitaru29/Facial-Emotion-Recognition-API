from flask import Flask
from routes.video_routes import video_routes
import logging
import coloredlogs

app = Flask(__name__)
app.register_blueprint(video_routes)

if __name__ == "__main__":
    coloredlogs.install(level="INFO", fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    logger = logging.getLogger(__name__)
    logger.info("Starting the application on: http://localhost:5000/")
    app.run(host="127.0.0.1", port=5000, debug=True)
