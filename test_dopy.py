import json
import requests
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

not_found_response = {
    "id": "not_found",
    "message": "The resource you were accessing could not be found.",
}

error_responses = {
    403: forbidden_response,
    404: not_found_response,
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
        assert result.get("id") == 11134178
        assert result.get("ip_address") == "127.0.0.1"


    @responses.activate
    def test_all_floating_ips(self):
        """
        Check all floating ips
        """
        test_response = open('test_samples/all_floating_ips.txt', 'r').read()
        responses.add(
            responses.GET,
            urljoin(API_V2_ENDPOINT, 'floating_ips'),
            body=test_response,
            status=200,
            content_type="application/json",
        )
        result = self.ins.all_floating_ips()
        assert [i.get("ip") for i in result] == [
            "1.2.3.4",
            "1.2.3.5"
        ]


    @responses.activate
    def test_new_floating_ip(self):
        """
         Check new floating ip
        """
        test_response = open('test_samples/new_floating_ip.txt', 'r').read()
        responses.add(
            responses.POST,
            urljoin(API_V2_ENDPOINT, 'floating_ips'),
            body=test_response,
            status=200,
            content_type="application/json",
        )
        result = self.ins.new_floating_ip(droplet_id="10495857")
        assert result.get("ip") == "111.111.111.111"


    @responses.activate
    def test_destroy_floating_ip_1(self):
        """
         Check destroy floating ip
        """
        ip_to_destroy = "127.0.0.0"
        responses.add(
            responses.DELETE,
            urljoin(API_V2_ENDPOINT, 'floating_ips/%s' % ip_to_destroy),
            body=json.dumps(not_found_response),
            status=404,
            content_type="application/json",
        )


        # TODO: destroy_floating_ip should not raise requests.exceptions.HTTPError
        # It should handle this error and raise DoError with message from resp.json()
        # line 519: `resp.raise_for_status()`  in dopy/manager.py
        try:
            self.ins.destroy_floating_ip(ip_to_destroy)
        except requests.exceptions.HTTPError as e:
            assert e.response.status_code == 404

    @responses.activate
    def test_destroy_floating_ip_2(self):
        """
         Check destroy floating ip
        """
        ip_to_destroy = "127.0.0.1"
        responses.add(
            responses.DELETE,
            urljoin(API_V2_ENDPOINT, 'floating_ips/%s' % ip_to_destroy),
            body="",
            status=200,
            content_type="application/json",
        )

        # This call does not return anything
        self.ins.destroy_floating_ip(ip_to_destroy)


    @responses.activate
    def test_ssh_key_invalid(self):
        """
         Check new floating ip
        """
        test_response = open('test_samples/new_ssh_key_invalid.txt', 'r').read()
        responses.add(
            responses.POST,
            urljoin(API_V2_ENDPOINT, 'account/keys'),
            body=test_response,
            status=422,
            content_type="application/json",
        )
        try:
            self.ins.new_ssh_key("InvalidKey", "LaLaLaLaLa")
        except DoError as e:
            assert str(e) == 'Key invalid, key should be of the format `type key [comment]`'

    @responses.activate
    def test_ssh_key(self):
        """
         Check new floating ip
        """
        test_response = open('test_samples/new_ssh_key.txt', 'r').read()
        responses.add(
            responses.POST,
            urljoin(API_V2_ENDPOINT, 'account/keys'),
            body=test_response,
            status=200,
            content_type="application/json",
        )

        fake_key = "ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEA4VCOWFrARc1m3MfEAL50v2Z2siavO3Ijpr/LZ00EZah8EjfZhqjAc/agkljyXmNGpVDpRdtlYco8h3P5vegXOEgKcX74fDYm0vNdVABVD1XSD8ElNyLTCCNk7rZJbi3htJox3Q1n0vnMmB5d20d9occkAx4Ac94RWNS33EC5CszNTMgAIn+uZl0FlQklS1oSyWFahSTWyA6b33qG7Y5E4b6J/caObnPx6EgtBrgi97gXJHZWyYlGrpWmUuhPqs5XToRB08CVxAyzewtq1MXv0p+Po4L1pbHLRf+TSoZ5RSBZZjY4/JMAzdXHNtrrrrrrrrNrbBXKUcNSAHZssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEA4VCOWFrARc1m3MfEAL50v2Z2siavO3Ijpr/LZ00EZah8EjfZhqjAc/agkljyXmNGpVDpRdtlYco8h3P5vegXOEgKcX74fDYm0vNdVABVD1XSD8ElNyLTCCNk7rZJbi3htJox3Q1n0vnMmB5d20d9occkAx4Ac94RWNS33EC5CszNTMgAIn+uZl0FlQklS1oSyWFahSTWyA6b33qG7Y5E4b6J/caObnPx6EgtBrgi97gXJHZWyYlGrpWmUuhPqs5XToRB08CVxAyzewtq1MXv0p+Po4L1pbHLRf+TSoZ5RSBZZjY4/JMAzdXHNtrrrrrrrrNrbBXKUcNSAHZssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEA4VCOWFrARc1m3MfEAL50v2Z2siavO3Ijpr/LZ00EZah8EjfZhqjAc/agkljyXmNGpVDpRdtlYco8h3P5vegXOEgKcX74fDYm0vNdVABVD1XSD8ElNyLTCCNk7rZJbi3htJox3Q1n0vnMmB5d20d9occkAx4Ac94RWNS33EC5CszNTMgAIn+uZl0FlQklS1oSyWFahSTWyA6b33qG7Y5E4b6J/caObnPx6EgtBrgi97gXJHZWyYlGrpWmUuhPqs5XToRB08CVxAyzewtq1MXv0p+Po4L1pbHLRf+TSoZ5RSBZZjY4/JMAzdXHNtrrrrrrrrNrbBXKUcNSAHssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEA4VCOWFrARc1m3MfEAL50v2Z2siavO3Ijpr/LZ00EZah8EjfZhqjAc/agkljyXmNGpVDpRdtlYco8h3P5vegXOEgKcX74fDYm0vNdVABVD1XSD8ElNyLTCCNk7rZJbi3htJox3Q1n0vnMmB5d20d9occkAx4Ac94RWNS33EC5CszNTMgAIn+uZl0FlQklS1oSyWFahSTWyA6b33qG7Y5E4b6J/caObnPx6EgtBrgi97gXJHZWyYlGrpWmUuhPqs5XToRB08CVxAyzewtq1MXv0p+Po4L1pbHLRf+TSoZ5RSBZZjY4/JMAzdXHNtrrrrrrrrNrbBXKUcNSAHZZ"
        result = self.ins.new_ssh_key("GoodKey", fake_key)
        assert result.get("name") == "GoodKey"
        assert result.get("id") == 1706860



    @responses.activate
    def helper_function(self, action, action_key):
        droplet_id = "11373834"
        test_response = open('test_samples/%s.txt' % action, 'r').read()
        responses.add(
            responses.POST,
            urljoin(API_V2_ENDPOINT, 'droplets/%s/actions' % droplet_id),
            body=test_response,
            status=200,
            content_type="application/json",
        )

        if action == "restore_droplet":
            result = getattr(self.ins, action)(droplet_id, 15937659)
        elif action == "snapshot_droplet":
            result = getattr(self.ins, action)(droplet_id, "TestSnapshot")
        elif action == "resize_droplet":
            result = getattr(self.ins, action)(droplet_id, "1gb")
        elif action == "rebuild_droplet":
            result = getattr(self.ins, action)(droplet_id, "15066966")
        elif action == "rename_droplet":
            result = getattr(self.ins, action)(droplet_id, "An-another-name")
        else:
            result = getattr(self.ins, action)(droplet_id)

        # Check POST data of the request
        assert json.loads(responses.calls[0].request.body).get("type") == action_key

        # Check response data
        assert result['action']['type'] == action_key

    def test_actions(self):
        """
         Check actions
        """

        actions = [
            ("reboot_droplet", "reboot"),
            ("power_cycle_droplet", "power_cycle"),
            ("power_on_droplet", "power_on"),
            ("resize_droplet", "resize"),
            ("snapshot_droplet", "snapshot"),
            ("power_off_droplet", "power_off"),
            ("shutdown_droplet", "shutdown"),
            ("restore_droplet", "restore"),
            ("rebuild_droplet", "rebuild"),
            ("enable_backups_droplet", "enable_backups"),
            ("disable_backups_droplet", "disable_backups"),
            ("rename_droplet", "rename"),
            ("password_reset_droplet", "password_reset"),
        ]

        for action, action_key in actions:
            self.helper_function(action, action_key)

    @responses.activate
    def test_destroy_droplet(self):
        droplet_id = "11373834"
        responses.add(
            responses.DELETE,
            urljoin(API_V2_ENDPOINT, 'droplets/%s' % droplet_id),
            body="",
            status=200,
            content_type="application/json",
        )
        result = self.ins.destroy_droplet(droplet_id)
        assert result == dict()

    @responses.activate
    def test_others(self):
        """
         Check some other tests.
        """
        assert self.ins.api_key == 'fake_token'
