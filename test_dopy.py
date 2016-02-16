import json
import responses
import unittest
from urlparse import urljoin
import dopy
from dopy.manager import DoError
from dopy.manager import DoManager
from dopy.manager import API_ENDPOINT


API_V2_ENDPOINT = urljoin(API_ENDPOINT, 'v2/')


forbidden_response = {
    "id": "forbidden",
    "message": "You do not have access for the attempted action.",
}

rate_limit_response = {
    "id": "too_many_requests",
    "message": "API Rate limit exceeded.",
}


error_responses = {
    403: forbidden_response,
    429: rate_limit_response,
}


class TestAllActiveDroplets(unittest.TestCase):
    def setUp(self):
        self.ins = DoManager(
            None,
            'fake_token',
        )

    @staticmethod
    def test_version():
        assert dopy.__version__ == '0.3.7a'

    @responses.activate
    def test_all_active_droplets_0(self):
        """
        Check forbidden response
        """
        responses.add(
            responses.GET,
            urljoin(API_V2_ENDPOINT, 'droplets/'),
            body=json.dumps(forbidden_response),
            status=403,
            content_type="application/json",
        )

        try:
            self.ins.all_active_droplets()
        except DoError as e:
            assert e.message == forbidden_response.get("message")


    @responses.activate
    def test_all_active_droplets_1(self):
        """
        Check reach rate limit response
        """
        responses.add(
            responses.GET,
            urljoin(API_V2_ENDPOINT, 'droplets/'),
            body=json.dumps(rate_limit_response),
            status=429,
            content_type="application/json",
        )

        try:
            self.ins.all_active_droplets()
        except DoError as e:
            assert e.message == rate_limit_response.get("message")


    @responses.activate
    def test_all_active_droplets_2(self):
        """
        Check a successful request.
        """

        test_response = open('test_samples/all_active_droplets.txt', 'r').read()
        responses.add(
            responses.GET,
            urljoin(API_V2_ENDPOINT, 'droplets/'),
            body=test_response,
            status=200,
            content_type="application/json",
        )
        result = self.ins.all_active_droplets()
        assert len(result) == 1

        instance = result[0]
        assert instance.get('status') == 'active'
        assert instance.get('ip_address') == '1.2.3.4'

    @responses.activate
    def test_all_regions(self):
        """
         Check response of getting all regions.
        """
        test_response = open('test_samples/all_regions.txt', 'r').read()
        responses.add(
            responses.GET,
            urljoin(API_V2_ENDPOINT, 'regions/'),
            body=test_response,
            status=200,
            content_type="application/json",
        )
        result = self.ins.all_regions()
        assert len(result) == 11
        assert [ i.get('name') for i in result ] == [
            u'New York 1',
            u'Amsterdam 1',
            u'San Francisco 1',
            u'New York 2',
            u'Amsterdam 2',
            u'Singapore 1',
            u'London 1',
            u'New York 3',
            u'Amsterdam 3',
            u'Frankfurt 1',
            u'Toronto 1'
        ]


    @responses.activate
    def test_all_ssh_keys(self):
        """
         Check all ssh keys
        """
        test_response = open('test_samples/all_ssh_keys.txt', 'r').read()
        responses.add(
            responses.GET,
            urljoin(API_V2_ENDPOINT, 'account/keys'),
            body=test_response,
            status=200,
            content_type="application/json",
        )
        result = self.ins.all_ssh_keys()
        assert len(result) == 2
        assert [i.get("id") for i in result] == [401185, 1439642]


    @responses.activate
    def test_all_images(self):
        """
         Check all images
        """
        test_response = open('test_samples/all_images.txt', 'r').read()
        responses.add(
            responses.GET,
            urljoin(API_V2_ENDPOINT, 'images/'),
            body=test_response,
            status=200,
            content_type="application/json",
        )
        result = self.ins.all_images()
        assert len(result) == 12
        assert [i.get('name') for i in result] == [
            u'ownCloud 8.2.2 on 14.04',
            u'Redis 3.0.6 on 14.04',
            u'Ghost 0.7.5 on 14.04',
            u'Dokku v0.4.12 on 14.04',
            u'Ruby on Rails on 14.04 (Postgres, Nginx, Unicorn)',
            u'Magento 2.0.2 CE on 14.04',
            u'Discourse on 14.04',
            u'WordPress on 14.04',
            u'node v4.3.0 on 14.04',
            u'GitLab 8.4.4 CE on 14.04',
            u'Redmine on 14.04',
            u'initialized'
        ]


    @responses.activate
    def test_sizes(self):
        """
         Check sizes
        """
        test_response = open('test_samples/sizes.txt', 'r').read()
        responses.add(
            responses.GET,
            urljoin(API_V2_ENDPOINT, 'sizes/'),
            body=test_response,
            status=200,
            content_type="application/json",
        )
        result = self.ins.sizes()
        assert len(result) == 9
        assert [i.get("memory") for i in result] == [
            512, 1024, 2048, 4096, 8192, 16384, 32768, 49152, 65536,
        ]


    @responses.activate
    def test_new_droplet(self):
        """
         Check New droplet
        """
        test_response = open('test_samples/new_droplet.txt', 'r').read()
        droplet_id = json.loads(test_response)['droplet']["id"]
        responses.add(
            responses.POST,
            urljoin(API_V2_ENDPOINT, 'droplets'),
            body=test_response,
            status=200,
            content_type="application/json",
        )
        responses.add(
            responses.GET,
            urljoin(API_V2_ENDPOINT, 'droplets/%s' % droplet_id),
            body=test_response,
            status=200,
            content_type="application/json",
        )
        result = self.ins.new_droplet(
            name="TestMachine",
            size_id="512mb",
            image_id="15389362",
            region_id="sgp1",
            ssh_key_ids="402179",
        )


    @responses.activate
    def test_others(self):
        """
         Check some other tests.
        """
        assert self.ins.api_key == 'fake_token'
