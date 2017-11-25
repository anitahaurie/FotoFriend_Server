import pytest
from flask import url_for
import urllib.request
import base64

class TestStoreImage:
    @pytest.mark.dependency()
    def test_storeImage(self, client):
        urllib.request.urlretrieve('http://www.catster.com/wp-content/uploads/2017/08/A-fluffy-cat-looking-funny-surprised-or-concerned.jpg', 'tmp.jpg')
        file = open('tmp.jpg', 'rb').read()
        res = client.post(url_for('storeimage'), data=dict(file=base64.b64encode(file), filename='tmp.jpg', username='fotofriendtest'))
        assert res.status_code == 200
