import pytest
from flask import url_for
import json

class TestDeleteImage:
    @pytest.mark.dependency(depends=['test_storeImage'])
    def test_deleteImage(self, client):
        response = client.post(url_for('deleteimage'), data = json.dumps({'url': "https://s3-us-west-2.amazonaws.com/foto-friend/5a1848632bc46432713be66d/tmp.jpg", 'username': "fotofriendtest"}))
        assert response.status_code == 200