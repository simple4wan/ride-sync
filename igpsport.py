#!/usr/bin/env python
# -*- coding: utf-8 -*一
import os

import requests


class igpsport:
    def __init__(self):
        self.session = requests.session()
        self.session.verify = False
        if os.getenv('DEBUG_MODE') == 'True':
            self.session.proxies = {
                'http': '127.0.0.1:8888',
                'https': '127.0.0.1:8888'
            }

    def login(self):
        url = 'https://my.igpsport.com/Auth/Login'
        params = {
            'username': os.getenv('IGPSPORT_USERNAME'),
            'password': os.getenv('IGPSPORT_PASSWORD')
        }
        response = self.session.post(url, data=params)
        content = response.json()
        if 'Code' not in content or content['Code'] != 0:
            raise Exception('迹驰登陆失败：' + content['Message'])

    def get_activity_list(self):
        url = 'https://my.igpsport.com/Activity/MyActivityList'
        response = self.session.get(url)
        content = response.json()
        if 'item' not in content:
            raise Exception('迹驰获取活动列表失败')
        activity_list = []
        for activity in reversed(content['item']):
            activity_list.append({
                'ride_id': activity['RideId'],
                'title': activity['StartTimeString'] + activity['Title'],
                'origin_activity': activity,
            })
        return activity_list

    def export_fit(self, activity):
        url = 'https://my.igpsport.com/fit/activity?type=0&rideid=' + str(activity['RideId'])
        response = self.session.get(url)
        content = response.content
        if response.status_code != 200:
            raise Exception('迹驰导出fit文件失败：' + str(activity['RideId']))
        return content

    def import_fit(self, fit_file, title):
        pass
