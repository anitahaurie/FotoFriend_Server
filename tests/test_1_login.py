import pytest
from flask import url_for
import json
import os
from pymongo import MongoClient

class TestLogin:
    def test_login(self, client):
        res = client.post(url_for('login'), data=json.dumps({'username': 'fotofriendtest'}))
        assert res.status_code == 200
        assert res.json == { 'Links': ['https://s3-us-west-2.amazonaws.com/foto-friend/5a1848632bc46432713be66d/dog.jpg'] }

    def test_newacct(self, client):
        res = client.post(url_for('login'), data=json.dumps({'username': 'newuser'}))
        assert res.status_code == 200
        assert res.json == { 'Links': [''] }
        client = MongoClient("mongodb://admin:%s@fotofrienddb-shard-00-00-5xqww.mongodb.net:27017,fotofrienddb-shard-00-01-5xqww.mongodb.net:27017,fotofrienddb-shard-00-02-5xqww.mongodb.net:27017/test?ssl=true&replicaSet=FotoFriendDB-shard-0&authSource=admin" % os.environ['MONGO_PWD'])
        db = client.FotoFriendUserData
        db.newuser.drop()