#!/usr/bin/python3
#coding=utf-8

import iciba
import json

def main(event='event', context='context'):
    # 微信配置 in wechat.json
    wechat_config={}
    with open("./wechat.json",'r') as f:
        wechat_config = json.load(f)
    icb = iciba.iciba(wechat_config)
    icb.run()

if __name__ == '__main__':
    main()
