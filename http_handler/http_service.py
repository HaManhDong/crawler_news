import requests
import json
from requests.adapters import ConnectionError

MAX_URI_LEN = 8192
USER_AGENT = 'crawler'
accepted_list = (requests.codes.ok,
                 requests.codes.created,
                 requests.codes.accepted,
                 requests.codes.no_content)


# ENDPOINT_URL = u'http://localhost:8080/api/'


def request(url, method, body=None, **kwargs):
    try:
        resp = requests.request(
            method,
            url,
            data=body,
            **kwargs)
        status_code = resp.status_code
        if status_code in accepted_list:
            data = json.loads(resp.text)
            return data
        else:
            return "Error"
    except:
        raise ConnectionError


def get_worker_ip_list(manager_node_ip):
    endpoint = u'http://' + manager_node_ip + ":9090/get_worker_ip_list"
    return request(endpoint, method='GET', body={})


def get_crawled_url_list(manager_node_ip):
    endpoint = u'http://' + manager_node_ip + ":9090/get_crawled_url_list"
    return request(endpoint, method='GET', body={})


def join_worker_node(manager_node_ip, new_worker_node_ip):
    body = {"new_node_ip": new_worker_node_ip}
    endpoint = u'http://' + manager_node_ip + ":9090/join_worker_node"
    # requests.post('http://127.0.0.1:9090/join_worker_node', data={'new_node_ip': '99.666.33'})
    return request(endpoint, method='POST', body=body)


def send_crawled_url_to_manager(manager_ip, crawled_url):
    body = {"new_crawled_url": crawled_url}
    endpoint = u'http://' + manager_ip + ":9090/add_new_crawled_url"
    return request(endpoint, method='POST', body=body)


def send_crawled_url_to_worker(worker_ip, crawled_url):
    body = {"new_crawled_url": crawled_url}
    endpoint = u'http://' + worker_ip + ":9091/add_new_crawled_url"
    return request(endpoint, method='POST', body=body)
