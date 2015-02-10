#!/usr/bin/env python
#coding: utf-8
"""
This module simply sends request to the Digital Ocean API,
and returns their response as a dict.
"""

import requests
import json as json_module

API_ENDPOINT = 'https://api.digitalocean.com'

class DoError(RuntimeError):
    pass

class DoManager(object):

    def __init__(self, client_id, api_key, api_version=1):
        self.api_endpoint = API_ENDPOINT
        self.client_id = client_id
        self.api_key = api_key
        self.api_version = int(api_version)

        if self.api_version == 2:
            self.api_endpoint += '/v2'
        if self.api_version == 1:
            self.api_endpoint += '/v1'

    def all_active_droplets(self):
        json = self.request('/droplets/')
        if self.api_version == 2:
            for index in range(len(json['droplets'])):
                try:
                    json['droplets'][index][u'ip_address'] = json['droplets'][index]['networks']['v4'][0]['ip_address']
                except IndexError:
                    json['droplets'][index][u'ip_address'] = ''
        return json['droplets']

    def new_droplet(self, name, size_id, image_id, region_id,
            ssh_key_ids=None, virtio=True, private_networking=False,
            backups_enabled=False, user_data=None):

        if self.api_version == 2:
            params = {
                'name': str(name),
                'size': str(size_id),
                'image': str(image_id),
                'region': str(region_id),
                'virtio': str(virtio).lower(),
                'private_networking': str(private_networking).lower(),
                'backups_enabled': str(backups_enabled).lower(),
            }
            if ssh_key_ids:
                # Need to be an array in v2
                if isinstance(ssh_key_ids, basestring):
                    ssh_key_ids = [ssh_key_ids]

                if type(ssh_key_ids) == list:
                    for index in range(len(ssh_key_ids)):
                        ssh_key_ids[index] = str(ssh_key_ids[index])

                params['ssh_keys'] = ssh_key_ids

            if user_data:
                params['user_data'] = user_data

            json = self.request('/droplets', params=params, method='POST')
            created_id = json['droplet']['id']
            json = self.show_droplet(created_id)
            return json
        else:
            params = {
                'name': str(name),
                'size_id': str(size_id),
                'image_id': str(image_id),
                'region_id': str(region_id),
                'virtio': str(virtio).lower(),
                'private_networking': str(private_networking).lower(),
                'backups_enabled': str(backups_enabled).lower(),
            }
            if ssh_key_ids:
                # Need to be a comma separated string 
                if type(ssh_key_ids) == list:
                    ssh_key_ids = ','.join(ssh_key_ids)
                params['ssh_key_ids'] = ssh_key_ids

            json = self.request('/droplets/new', params=params)
            return json['droplet']

    def show_droplet(self, droplet_id):
        json = self.request('/droplets/%s' % droplet_id)
        if self.api_version == 2:
            try:
                json['droplet'][u'ip_address'] = json['droplet']['networks']['v4'][0]['ip_address']
            except IndexError:
                json['droplet'][u'ip_address'] = ''
        return json['droplet']

    def droplet_v2_action(self, droplet_id, droplet_type, params={}):
        params = {
            'type': droplet_type
        }
        json = self.request('/droplets/%s/actions' % droplet_id, params=params, method='POST')
        return json

    def reboot_droplet(self, droplet_id):
        if self.api_version == 2:
            json = self.droplet_v2_action(droplet_id, 'reboot')
        else:
            json = self.request('/droplets/%s/reboot/' % droplet_id)
        json.pop('status', None)
        return json

    def power_cycle_droplet(self, droplet_id):
        if self.api_version == 2:
            json = self.droplet_v2_action(droplet_id, 'power_cycle')
        else:
            json = self.request('/droplets/%s/power_cycle/' % droplet_id)
        json.pop('status', None)
        return json

    def shutdown_droplet(self, droplet_id):
        if self.api_version == 2:
            json = self.droplet_v2_action(droplet_id, 'shutdown')
        else:
            json = self.request('/droplets/%s/shutdown/' % droplet_id)
        json.pop('status', None)
        return json

    def power_off_droplet(self, droplet_id):
        if self.api_version == 2:
            json = self.droplet_v2_action(droplet_id, 'power_off')
        else:
            json = self.request('/droplets/%s/power_off/' % droplet_id)
        json.pop('status', None)
        return json

    def power_on_droplet(self, droplet_id):
        if self.api_version == 2:
            json = self.droplet_v2_action(droplet_id, 'power_on')
        else:
            json = self.request('/droplets/%s/power_on/' % droplet_id)
        json.pop('status', None)
        return json

    def password_reset_droplet(self, droplet_id):
        if self.api_version == 2:
            json = self.droplet_v2_action(droplet_id, 'password_reset')
        else:
            json = self.request('/droplets/%s/password_reset/' % droplet_id)
        json.pop('status', None)
        return json

    def resize_droplet(self, droplet_id, size_id):
        if self.api_version == 2:
            params = {'size': size_id}
            json = self.droplet_v2_action(droplet_id, 'resize', params)
        else:
            params = {'size_id': size_id}
            json = self.request('/droplets/%s/resize/' % droplet_id, params)
        json.pop('status', None)
        return json

    def snapshot_droplet(self, droplet_id, name):
        params = {'name': name}
        if self.api_version == 2:
            json = self.droplet_v2_action(droplet_id, 'snapshot', params)
        else:
            json = self.request('/droplets/%s/snapshot/' % droplet_id, params)
        json.pop('status', None)
        return json

    def restore_droplet(self, droplet_id, image_id):
        if self.api_version == 2:
            params = {'image': image_id}
            json = self.droplet_v2_action(droplet_id, 'restore', params)
        else:
            params = {'image_id': image_id}
            json = self.request('/droplets/%s/restore/' % droplet_id, params)
        json.pop('status', None)
        return json

    def rebuild_droplet(self, droplet_id, image_id):
        if self.api_version == 2:
            params = {'image': image_id}
            json = self.droplet_v2_action(droplet_id, 'rebuild', params)
        else:
            params = {'image_id': image_id}
            json = self.request('/droplets/%s/rebuild/' % droplet_id, params)
        json.pop('status', None)
        return json

    def enable_backups_droplet(self, droplet_id):
        if self.api_version == 2:
            json = self.droplet_v2_action(droplet_id, 'enable_backups')
        else:
            json = self.request('/droplets/%s/enable_backups/' % droplet_id)
        json.pop('status', None)
        return json

    def disable_backups_droplet(self, droplet_id):
        if self.api_version == 2:
            json = self.droplet_v2_action(droplet_id, 'disable_backups')
        else:
            json = self.request('/droplets/%s/disable_backups/' % droplet_id)
        json.pop('status', None)
        return json

    def rename_droplet(self, droplet_id, name):
        params = {'name': name}
        if self.api_version == 2:
            json = self.droplet_v2_action(droplet_id, 'rename', params)
        else:
            json = self.request('/droplets/%s/rename/' % droplet_id, params)
        json.pop('status', None)
        return json

    def destroy_droplet(self, droplet_id, scrub_data=True):
        if self.api_version == 2:
            json = self.request('/droplets/%s' % droplet_id, method='DELETE')
        else:
            params = {'scrub_data': '1' if scrub_data else '0'}
            json = self.request('/droplets/%s/destroy/' % droplet_id, params)
        json.pop('status', None)
        return json

#regions==========================================
    def all_regions(self):
        json = self.request('/regions/')
        return json['regions']

#images==========================================
    def all_images(self, filter='global'):
        params = {'filter': filter}
        json = self.request('/images/', params)
        return json['images']

    def image_v2_action(self, image_id, image_type, params={}):
        params = {
            'type': image_type
        }
        json = self.request('/images/%s/actions' % image_id, params=params, method='POST')
        return json

    def show_image(self, image_id):
        params = {'image_id': image_id}
        json = self.request('/images/%s' % image_id)
        return json['image']

    def destroy_image(self, image_id):
        if self.api_version == 2:
            self.request('/images/%s' % image_id, method='DELETE')
        else:
            self.request('/images/%s/destroy' % image_id)
        return True

    def transfer_image(self, image_id, region_id):
        if self.api_version == 2:
            params = {'region': region_id}
            json = self.image_v2_action(image_id, 'transfer', params)
        else:
            params = {'region_id': region_id}
            json = self.request('/images/%s/transfer' % image_id, params)
        json.pop('status', None)
        return json

#ssh_keys=========================================
    def all_ssh_keys(self):
        if self.api_version == 2:
            json = self.request('/account/keys')
        else:
            json = self.request('/ssh_keys/')
        return json['ssh_keys']

    def new_ssh_key(self, name, pub_key):
        if self.api_version == 2:
            params = {'name': name, 'public_key': pub_key}
            json = self.request('/account/keys', params, method='POST')
        else:
            params = {'name': name, 'ssh_pub_key': pub_key}
            json = self.request('/ssh_keys/new/', params)
        return json['ssh_key']

    def show_ssh_key(self, key_id):
        if self.api_version == 2:
            json = self.request('/account/keys/%s/' % key_id)
        else:
            json = self.request('/ssh_keys/%s/' % key_id)
        return json['ssh_key']

    def edit_ssh_key(self, key_id, name, pub_key):
        if self.api_version == 2:
            params = {'name': name} # v2 API doesn't allow to change key body now
            json = self.request('/account/keys/%s/' % key_id, params, method='PUT')
        else:
            params = {'name': name, 'ssh_pub_key': pub_key}  # the doc needs to be improved
            json = self.request('/ssh_keys/%s/edit/' % key_id, params)
        return json['ssh_key']

    def destroy_ssh_key(self, key_id):
        if self.api_version == 2:
            self.request('/account/keys/%s' % key_id, method='DELETE')
        else:
            self.request('/ssh_keys/%s/destroy/' % key_id)
        return True

#sizes============================================
    def sizes(self):
        json = self.request('/sizes/')
        return json['sizes']

#domains==========================================
    def all_domains(self):
        json = self.request('/domains/')
        return json['domains']

    def new_domain(self, name, ip):
        params = {
                'name': name,
                'ip_address': ip
            }
        if self.api_version == 2:
            json = self.request('/domains', params=params, method='POST')
        else:
            json = self.request('/domains/new/', params)
        return json['domain']

    def show_domain(self, domain_id):
        json = self.request('/domains/%s/' % domain_id)
        return json['domain']

    def destroy_domain(self, domain_id):
        if self.api_version == 2:
            self.request('/domains/%s' % domain_id, method='DELETE')
        else:
            self.request('/domains/%s/destroy/' % domain_id)
        return True

    def all_domain_records(self, domain_id):
        json = self.request('/domains/%s/records/' % domain_id)
        if self.api_version == 2:
            return json['domain_records']
        return json['records']

    def new_domain_record(self, domain_id, record_type, data, name=None, priority=None, port=None, weight=None):
        params = {'data': data}

        if self.api_version == 2:
            params['type'] = record_type
        else:
            params['record_type'] = record_type

        if name: params['name'] = name
        if priority: params['priority'] = priority
        if port: params['port'] = port
        if weight: params['weight'] = weight

        if self.api_version == 2:
            json = self.request('/domains/%s/records/' % domain_id, params, method='POST')
        else:
            json = self.request('/domains/%s/records/new/' % domain_id, params)
        return json['record']

    def show_domain_record(self, domain_id, record_id):
        json = self.request('/domains/%s/records/%s' % (domain_id, record_id))
        if self.api_version == 2:
            return json['domain_record']
        return json['record']

    def edit_domain_record(self, domain_id, record_id, record_type, data, name=None, priority=None, port=None, weight=None):
        if self.api_version == 2:
            params['name'] = name # API v.2 allows only record name change
            json = self.request('/domains/%s/records/%s' % (domain_id, record_id), params, method='PUT')
            return json['domain_record']

        params = {
            'record_type': record_type,
            'data': data,
        }

        if name: params['name'] = name
        if priority: params['priority'] = priority
        if port: params['port'] = port
        if weight: params['weight'] = weight
        json = self.request('/domains/%s/records/%s/edit/' % (domain_id, record_id), params)
        return json['record']

    def destroy_domain_record(self, domain_id, record_id):
        if self.api_version == 2:
            self.request('/domains/%s/records/%s' % (domain_id, record_id), method='DELETE')
        else:
            self.request('/domains/%s/records/%s/destroy/' % (domain_id, record_id))
        return True

#events(actions in v2 API)========================
    def show_all_actions(self):
        if self.api_version == 2:
            json = self.request('/actions')
            return json['actions']
        return False # API v.1 haven't this functionality

    def show_action(self, action_id):
        if self.api_version == 2:
            json = self.request('/actions/%s' % event_id)
            return json['action']
        return show_event(self, action_id)

    def show_event(self, event_id):
        if self.api_version == 2:
            return show_action(self, event_id)
        json = self.request('/events/%s' % event_id)
        return json['event']

#low_level========================================
    def request(self, path, params={}, method='GET'):
        if not path.startswith('/'):
            path = '/'+path
        url = self.api_endpoint+path

        if self.api_version == 2:
            headers = {'Authorization': "Bearer %s" % self.api_key}
            resp = self.request_v2(url, params=params, headers=headers, method=method)
        else:
            params['client_id'] = self.client_id
            params['api_key'] = self.api_key
            resp = self.request_v1(url, params, method=method)

        return resp

    def request_v1(self, url, params={}, method='GET'):
        try:
            resp = requests.get(url, params=params, timeout=60)
            json = resp.json()
        except ValueError:  # requests.models.json.JSONDecodeError
            raise ValueError("The API server doesn't respond with a valid json")
        except requests.RequestException as e:  # errors from requests
            raise RuntimeError(e)

        if resp.status_code != requests.codes.ok:
            if json:
                if 'error_message' in json:
                    raise DoError(json['error_message'])
                elif 'message' in json:
                    raise DoError(json['message'])
            # The JSON reponse is bad, so raise an exception with the HTTP status
            resp.raise_for_status()
        if json.get('status') != 'OK':
            raise DoError(json['error_message'])

        return json

    def request_v2(self, url, headers={}, params={}, method='GET'):
        headers['Content-Type'] = 'application/json'
        try:
            if method == 'POST':
                resp = requests.post(url, data=json_module.dumps(params), headers=headers, timeout=60)
                json = resp.json()
            elif method == 'DELETE':
                resp = requests.delete(url, headers=headers, timeout=60)
                json = {'status': resp.status_code}
            elif method == 'PUT':
                resp = requests.put(url, headers=headers, params=params, timeout=60)
                json = resp.json()
            elif method == 'GET':
                resp = requests.get(url, headers=headers, params=params, timeout=60)
                json = resp.json()
            else:
                raise DoError('Unsupported method %s' % method)

        except ValueError:  # requests.models.json.JSONDecodeError
            raise ValueError("The API server doesn't respond with a valid json")
        except requests.RequestException as e:  # errors from requests
            raise RuntimeError(e)

        if resp.status_code != requests.codes.ok:
            if json:
                if 'error_message' in json:
                    raise DoError(json['error_message'])
                elif 'message' in json:
                    raise DoError(json['message'])
            # The JSON reponse is bad, so raise an exception with the HTTP status
            resp.raise_for_status()

        if json.get('id') == 'not_found':
            raise DoError(json['message'])

        return json


if __name__ == '__main__':
    import os
    if os.environ.get('DO_API_VERSION') == '2':
        api_token = os.environ.get('DO_API_TOKEN') or os.environ['DO_API_KEY']
        do = DoManager(None, api_token, 2)
    else:
        client_id = os.environ['DO_CLIENT_ID']
        api_key = os.environ['DO_API_KEY']
        do = DoManager(client_id, api_key, 1)
    import sys
    fname = sys.argv[1]
    import pprint
    # size_id: 66, image_id: 1601, region_id: 1
    pprint.pprint(getattr(do, fname)(*sys.argv[2:]))
