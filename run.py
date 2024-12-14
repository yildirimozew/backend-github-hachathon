import flask
from flask import request
import json
from app.models.mongoDBmanager import MongoDBManager
from flask_cors import CORS
import aio_pika

async def connectRabbitMQ(app):    
    connection = await aio_pika.connect_robust('amqp://localhost',heartbeat=10)
    channel = await connection.channel()
    channel.declare_queue("answer_queue")
    app.state.conn, app.state.channel = (connection, channel)


app = flask.Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'files'

CORS(app)
mongoManager = MongoDBManager("Chat")

from app.modules.ask.controller import *
from app.modules.chat_history.controller import *
from app.modules.file.controller import *

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')