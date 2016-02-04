# -*- coding:utf-8 -*-
import urllib
import urllib2
import cookielib
import re
import json
import socket
import sys

class SDU:

    def __init__(self):
        print "Please enter your ip...."
        self.myip        = raw_input()
        self.loginUrl    = 'https://zcms.ericsson.se/zcms_security_check'
        self.pending_url = 'https://zcms.ericsson.se/approvalQueue/listPolicies.html'
        self.addreq_url  = 'https://zcms.ericsson.se/zoneRequest/addRequest.html'
        self.req_headers = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
                             'Referer'    : self.addreq_url,
                           }
        self.cookies     = cookielib.CookieJar()
        self.postdata    = urllib.urlencode({
            'j_username':'username',
            'j_password':'password',
            'submit':'Login'
         })
        self.opener      = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookies))

    def check_ip(self):
        try:
            socket.inet_aton(self.myip)
        except socket.error:
            print "illegal IP!! :("
            sys.exit(1)

    def getPage(self):
        self.check_ip()
        self.opener.open('https://zcms.ericsson.se')
        for item in self.cookies:
            mycookie = item.name + item.value
        refurl = ('https://zcms.ericsson.se/login.html;'+mycookie).lower()
        self.headers = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
                         'Referer'    : refurl,
                       }
        request     = urllib2.Request(
            url     = self.loginUrl,
            data    = self.postdata,
            headers = self.headers)
        result = self.opener.open(request)
        result = self.opener.open(self.pending_url)
        req_ip = urllib.urlencode({ 'ipStart': self.myip,
                   'routingDomain.id': '23',
                   'routingDomain.name': 'ECN',
                   'fromCoReq': 'false'
                 })
        request_add_req     = urllib2.Request(
            url             = 'https://zcms.ericsson.se/zoneRequest/checkIp.html',
            data            = req_ip,
            headers         = self.headers)
        result = self.opener.open(request_add_req)
        dic = json.loads(result.read())
        print dic['zone']

sdu = SDU()
sdu.getPage()
