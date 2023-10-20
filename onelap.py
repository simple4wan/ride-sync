#!/usr/bin/env python
# -*- coding: utf-8 -*一
import hashlib
import os

import requests


class onelap:
    def __init__(self):
        self.session = requests.session()
        self.session.verify = False
        if os.getenv('DEBUG_MODE') == 'True':
            self.session.proxies = {
                'http': '127.0.0.1:8888',
                'https': '127.0.0.1:8888'
            }

    def login(self):
        url = 'http://www.onelap.cn/api/login'
        params = {
            'account': os.getenv('ONELAP_USERNAME'),
            'password': hashlib.md5(os.getenv('ONELAP_PASSWORD').encode()).hexdigest()
        }
        response = self.session.post(url, json=params)
        content = response.json()
        if 'code' not in content or content['code'] != 200:
            raise Exception('顽鹿登陆失败：' + content['error'])

    def get_activity_list(self):
        url = 'http://u.onelap.cn/analysis/list'
        response = self.session.get(url)
        content = response.json()
        if 'data' not in content:
            raise Exception('顽鹿获取活动列表失败')
        activity_list = []
        for activity in reversed(content['data']):
            activity_list.append({
                'ride_id': activity['created_at'],
                'title': activity['name'] if activity['name'] else activity['date'] + '的骑行',
                'origin_activity': activity,
            })
        return activity_list

    def export_fit(self, activity):
        if not activity['durl'].startswith('http'):
            activity['durl'] = 'http://u.onelap.cn' + activity['durl']
        url = activity['durl']
        response = self.session.get(url)
        content = response.content
        if response.status_code != 200:
            raise Exception('迹驰导出fit文件失败：' + url)
        return content

    def import_fit(self, fit_file, title):
        pass
