#!/usr/bin/env python
# -*- coding: utf-8 -*一
import os
import time

import urllib3

from dotenv import load_dotenv
from igpsport import igpsport
from imxingzhe import imxingzhe

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def main():
    load_dotenv()
    export_platform = os.getenv('EXPORT_PLATFORM')
    import_platform = os.getenv('IMPORT_PLATFORM')
    platform_list = {
        'igpsport': igpsport(),
        'imxingzhe': imxingzhe(),
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
    last_activity_id = 0
    while True:
        activity_list = export_platform_obj.get_activity_list()
        for activity in activity_list:
            if activity['ride_id'] > last_activity_id:
                fit_file = export_platform_obj.export_fit(str(activity['ride_id']))
                import_platform_obj.import_fit(fit_file, activity['title'])
                last_activity_id = activity['ride_id']
        time.sleep(60)


if __name__ == '__main__':
    main()
