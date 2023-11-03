#!/usr/bin/env python
# -*- coding: utf-8 -*一
import os
import time

import urllib3

from dotenv import load_dotenv
from igpsport import igpsport
from imxingzhe import imxingzhe
from onelap import onelap

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_last_sync_id(export_platform):
    file_path = './.' + export_platform + '.tmp'
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            file_content = file.read()
            try:
                return int(file_content)
            except ValueError:
                return 0
    return 0


def set_last_sync_id(export_platform, activity_id):
    file_path = './.' + export_platform + '.tmp'
    with open(file_path, 'w') as file:
        file.write(str(activity_id))


def main():
    load_dotenv()
    export_platform = os.getenv('EXPORT_PLATFORM')
    import_platform = os.getenv('IMPORT_PLATFORM')
    platform_list = {
        'igpsport': igpsport(),
        'imxingzhe': imxingzhe(),
        'onelap': onelap(),
    }
    if export_platform not in platform_list:
        raise Exception('导出平台配置不正确')
    if import_platform not in platform_list:
        raise Exception('导入平台配置不正确')
    export_platform_obj = platform_list[export_platform]
    import_platform_obj = platform_list[import_platform]
    # 平台初始化 如果账户密码错误抛出异常
    export_platform_obj.login()
    import_platform_obj.login()
    # 开始同步
    last_sync_id = get_last_sync_id(export_platform)
    while True:
        activity_list = export_platform_obj.get_activity_list()
        for activity in activity_list:
            if activity['ride_id'] > last_sync_id:
                fit_file = export_platform_obj.export_fit(activity['origin_activity'])
                import_platform_obj.import_fit(fit_file, activity['title'])
                last_sync_id = activity['ride_id']
                set_last_sync_id(export_platform, last_sync_id)
        time.sleep(60)


if __name__ == '__main__':
    main()
