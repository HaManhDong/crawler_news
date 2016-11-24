from flask import Flask
from flask import request
from database.db_http_listener_connection import db_session, UrlSet, WorkerNodeIp
import json

app = Flask(__name__)


@app.route('/add_new_crawled_url', methods=['POST', ])
def add_new_crawled_url():
    crawled_url = request.form['new_crawled_url']
    check_exist = db_session.query(UrlSet).filter_by(url=crawled_url).all()
    if len(check_exist) == 0:
        new_crawled_url = UrlSet(url=crawled_url)
        db_session.add(new_crawled_url)
        db_session.commit()
        return json.dumps({'message': 'success'})

    return json.dumps({'error': 'invalid parameter'})


@app.route('/add_new_worker_node', methods=['POST', ])
def add_new_worker_node():
    new_node_ip = request.form['new_node_ip']
    check_exist = db_session.query(WorkerNodeIp).filter_by(ip=new_node_ip).all()
    if len(check_exist) == 0:
        new_host = WorkerNodeIp(ip=new_node_ip)
        db_session.add(new_host)
        db_session.commit()
        return json.dumps({'message': 'success'})
    return json.dumps({'error': 'invalid parameter'})
