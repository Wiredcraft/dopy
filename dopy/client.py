#coding: utf-8
"""
This module simply sends request to the Digital Ocean API, 
and returns their response as a dict.
"""

import requests

__version__ = '0.1'
DO_HOST = 'https://api.digitalocean.com'

class Droplet(object):
    pass

class Snapshot(object):
    pass

class Region(object):
    pass

class Image(object):
    pass

class Size(object):
    pass

class SSHKey(object):
    pass

class Client(object):

    def __init__(self, client_id, api_key):
        self.client_id = client_id
        self.api_key = api_key

    def show_active(self):
        """
        Returns {u'status': u'OK', u'droplets': [{'name':xxx, ...},{}]}
        """
        return self.request('/droplets/')

    def create(self, name='', size_id=-1, image_id=-1, region_id=-1, ssh_key_ids = None):
        """
        Returns {u'status': u'ERROR', u'error_message': {...}} if failed,
        else {u'status': u'OK', u'droplet': {...}}
        """
        params = {
                'name': name,
                'size_id': size_id,
                'image_id': image_id,
                'region_id': region_id,
            }
        if ssh_key_ids:
            params['ssh_key_ids'] = ssh_key_ids
        return self.request('/droplets/new', params=params)

    def show(self, id):
        """
        Returns {u'status': u'ERROR', u'error_message': u'No Droplets Found'} if not found,
        else {u'status': u'OK', u'droplet': {...}}
        """
        return self.request('/droplets/%s' % id)

    def reboot(self, id):
        return self.request('/droplets/%s/reboot/' % id)

    def power_cycle(self, id):
        return self.request('/droplets/%s/power_cycle/' % id)

    def shutdown(self, id):
        return self.request('/droplets/%s/shutdown/' % id)

    def power_off(self, id):
        return self.request('/droplets/%s/power_off/' % id)

    def power_on(self, id):
        return self.request('/droplets/%s/power_on/' % id)

    def password_reset(self, id):
        return self.request('/droplets/%s/password_reset/' % id)

    def resize(self, id, size_id):
        params = {'size_id': size_id}
        return self.request('/droplets/%s/resize/' % id, params)

    def snapshot(self, id, name):
        params = {'name': name}
        return self.request('/droplets/%s/snapshot/' % id, params)

    def restore(self, id, image_id):
        params = {'image_id': image_id}
        return self.request('/droplets/%s/restore/' % id, params)

    def rebuild(self, id, image_id):
        params = {'image_id': image_id}
        return self.request('/droplets/%s/rebuild/' % id, params)

    def enable_backups(self, id, image_id):
        return self.request('/droplets/%s/enable_backups/' % id)

    def disable_backups(self, id, image_id):
        return self.request('/droplets/%s/disable_backups/' % id)

    def rename(self, id, image_id):
        return self.request('/droplets/%s/rename/' % id)

    def destroy(self, id):
        """
        Return {u'status': u'OK', u'event_id': 1} if succeeded,
        else {u'status': u'ERROR', u'error_message': u'Specified droplet not found.'}
        """
        return self.request('/droplets/%s/destroy/' % id)

#regions==========================================
    def all_regions(self):
        return self.request('/regions/')

#images==========================================
    def all_images(self, filter='global'):
        params = {'filter': filter}
        return self.request('/images/', params)

    def show_image(self, image_id):
        params= {'image_id': image_id}
        return self.request('/images/%s/' % image_id, params)

#ssh_keys=========================================
    def all_ssh_keys(self):
        return self.request('/ssh_keys/')

    def add_ssh_key(self, name, ssh_key_pub):
        params = {'name': name, 'ssh_key_pub': ssh_key_pub}
        return self.request('/ssh_key_put/new/', params)

    def show_ssh_key(self, key_id):
        return self.request('/ssh_keys/%s/' % key_id)

    def edit_ssh_key(self, key_id):
        return self.request('/ssh_keys/%s/edit/' % key_id)

    def destroy_ssh_key(self, key_id):
        return self.request('/ssh_keys/%s/destroy/' % key_id)

#sizes============================================
    def sizes(self):
        return self.request('/sizes/')

#domains==========================================

#low_level========================================
    def request(self, path, params={}, method='GET'):
        params['client_id'] = self.client_id
        params['api_key'] = self.api_key
        if not path.startswith('/'):
            path = '/'+path
        url = DO_HOST+path
        try:
            resp = requests.get(url, params=params, timeout=60)
            json = resp.json()
        except ValueError:  # requests.models.json.JSONDecodeError
            raise ValueError("The API server doesn't respond with a valid json")
        except requests.RequestException as e:  # errors from requests
            raise RuntimeError(e)
        if not resp.ok:
            raise RuntimeError(json['message'])

        return json

if __name__=='__main__':
    import os
    client_id = os.environ['CLIENT_ID']
    api_key = os.environ['API_KEY']
    do = Client(client_id,api_key)
    import sys
    fname = sys.argv[1]
    import pprint
    pprint.pprint(getattr(do, fname)(*sys.argv[2:]))
    # print do.show_active()
    # print do.images('my_images')
    # print do.sizes()
    # print do.create('test', 0, 385625, 1)
    # print do.show_active()
    # print do.power_off(219133)
    # print do.power_on(219133)
    # print do.show(219133)
    # print do.destroy(219254)
    # print do.destroy(219128)
