import os
from flask_redis import FlaskRedis

# Redis configuration
redis_client = FlaskRedis()

def init_redis(app):
    app.config['REDIS_URL'] = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
    redis_client.init_app(app)

# Mongo configuration
class Config:
    MONGO_URI = 'mongodb://root:root1234@mongodb:27017/dogs_db?authSource=admin'


