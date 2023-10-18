#!/usr/bin/env python
# -*- coding: utf-8 -*一
import base64
import re
import os

import requests
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA


class imxingzhe:
    def __init__(self):
        self.session = requests.session()
        self.session.verify = False
        if os.getenv('DEBUG_MODE'):
            self.session.proxies = {
                'http': '127.0.0.1:8888',
                'https': '127.0.0.1:8888'
            }

    def login(self):
        url = 'https://www.imxingzhe.com/user/login'
        response = self.session.get(url)
        content = response.text
        m = re.search('<textarea class="hidden" hidden id="pubkey">(.*?)</textarea>', content, re.DOTALL)
        if m:
            safe_password = os.getenv('IMXINGZHE_PASSWORD') + ';' + response.cookies.get('rd')
            recipient_key = RSA.import_key(m.group(1))
            cipher = PKCS1_v1_5.new(recipient_key)
            encrypted_password = base64.b64encode(cipher.encrypt(safe_password.encode())).decode()
            params = {
                'account': os.getenv('IMXINGZHE_USERNAME'),
                'password': encrypted_password,
                'source': 'web'
            }
            url = 'https://www.imxingzhe.com/api/v4/account/login'
            response = self.session.post(url, json=params)
            content = response.json()
            if 'res' not in content or content['res'] != 1:
                raise Exception('行者登陆失败：' + content['error_message'])

    def get_activity_list(self):
        pass

    def export_fit(self, ride_id):
        pass

    def import_fit(self, fit_file, title):
        file = {
            'upload_file_name': fit_file
        }
        params = {
            'title': title,
            'device': 3,
            'sport': 3
        }
        url = 'https://www.imxingzhe.com/api/v4/upload_fits'
        response = self.session.post(url, data=params, files=file)
        content = response.json()
        if (response.status_code == 400 and ('code' not in content or content['code'] != 9007)) or (
                response.status_code == 200 and ('serverId' not in content)):
            raise Exception('上传轨迹失败：' + response.text)
