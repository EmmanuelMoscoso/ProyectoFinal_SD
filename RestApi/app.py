from flask import Flask
from infrastructure.mongo import mongo
from infrastructure.swagger import init_swagger
from config import Config, init_redis
from controllers.dog_controller import dog_api
from controllers.user_controller import user_api

app = Flask(__name__)
app.config.from_object(Config)

#Mongo
mongo.init_app(app)

app.register_blueprint(dog_api, url_prefix="/dogs")
app.register_blueprint(user_api, url_prefix='/users')

# Initialize Swagger UI
init_swagger(app)

#Redis
init_redis(app)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
