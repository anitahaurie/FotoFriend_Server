import pytest
from flask import url_for
import json

def request(client, tags, username):
    data = json.dumps({'keywords': tags, 'username': username})
    response = client.post(url_for('filter'), data=data, content_type='application/json')
    return response

class TestFilter:
    def test_default(self, client):
        response = request(client, ["Default"], "fotofriendtest")
        assert response.status_code == 200
        assert len(response.json['Links']) == 1

    def test_one(self, client):
        response = request(client, ["dog"], "fotofriendtest")
        assert response.status_code == 200
        assert len(response.json['Links']) == 1

    def test_two(self, client):
        response = request(client, ["dog", "grass"], "fotofriendtest")
        assert response.status_code == 200
        assert len(response.json['Links']) == 1

    def test_multiple(self, client):
        response = request(client, ["dog", "pet", "grass", "flower"], "fotofriendtest")
        assert response.status_code == 200
        assert len(response.json['Links']) == 1

    def test_no_tags(self, client):
        response = request(client, [], "fotofriendtest")
        assert response.status_code == 200
        assert len(response.json['Links']) == 1

    def test_none(self, client):
        response = request(client, ["cat"], "fotofriendtest")
        assert response.status_code == 200
        assert len(response.json['Links']) == 0