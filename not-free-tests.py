#!/usr/bin/env python
# Copyright 2013 Abram Hindle, Cole Mackenzie
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# run: python not-free-tests.py

import urllib.request
import unittest
import os

BASEURL = "http://127.0.0.1:8080"

class TestYourWebserver(unittest.TestCase):
    def setUp(self,baseurl=BASEURL):
        """do nothing"""
        self.baseurl = baseurl

    def test_get_root(self):
        url = self.baseurl + "/"
        req = urllib.request.urlopen(url, None, 3)
        self.assertTrue( req.getcode()  == 200 , "200 OK Not FOUND!")

    def test_get_deep(self):
        url = self.baseurl + "/deep/"
        req = urllib.request.urlopen(url, None, 3)
        self.assertTrue( req.getcode()  == 200 , "200 OK Not FOUND!")


    def test_get_index(self):
        url = self.baseurl + "/index.html"
        req = urllib.request.urlopen(url, None, 3)
        self.assertTrue( req.getcode()  == 200 , "200 OK Not FOUND!")

    def test_get_404(self):
        url = self.baseurl + "/do-not-implement-this-page-it-is-not-found"
        try:
            req = urllib.request.urlopen(url, None, 3)
            self.assertTrue( False, "Should have thrown an HTTP Error!")
        except urllib.request.HTTPError as e:
            self.assertTrue( e.getcode()  == 404 , ("404 Not FOUND! %d" % e.getcode()))
        else:
            self.assertTrue( False, "Another Error was thrown!")

    def test_get_group(self):
        """ how secure are you? """
        url = self.baseurl + "/../../../../../../../../../../../../etc/group"
        try:
            req = urllib.request.urlopen(url, None, 3)
            self.assertTrue( False, "Should have thrown an HTTP Error! [%d]" % req.getcode())
        except urllib.request.HTTPError as e:
            self.assertTrue( e.getcode()  == 404 , ("404 Not FOUND! %d" % e.getcode()))
        else:
            self.assertTrue( false, "Another Error was thrown!")
        
    def test_css(self):
        url = self.baseurl + "/base.css"
        req = urllib.request.urlopen(url, None, 3)
        self.assertTrue( req.getcode()  == 200 , "200 OK Not FOUND!")
        self.assertTrue( req.info().gettype() == "text/css", ("Bad mimetype for css! %s" % req.info().gettype()))

    def test_html(self):
        url = self.baseurl + "/index.html"
        req = urllib.request.urlopen(url, None, 3)
        self.assertTrue( req.getcode()  == 200 , "200 OK Not FOUND!")
        self.assertTrue( req.info().gettype() == "text/html", ("Bad mimetype for html! %s" % req.info().gettype()))

    def test_hardcode(self):
        os.system("cp -r www/deep www/hardcode")
        url = self.baseurl + "/hardcode/index.html"
        req = urllib.request.urlopen(url, None, 3)
        self.assertTrue( req.getcode()  == 200 , "200 OK Not FOUND! Hardcoding? /hardcode/index.html")
        self.assertTrue( req.info().gettype() == "text/html", ("Bad mimetype for html! %s" % req.info().gettype()))
        url = self.baseurl + "/hardcode/"
        req = urllib.request.urlopen(url, None, 3)
        self.assertTrue( req.getcode()  == 200 , "200 OK Not FOUND! Hardcoding? /hardcode/")
        self.assertTrue( req.info().gettype() == "text/html", ("Bad mimetype for html! %s" % req.info().gettype()))

    def test_hardcode2(self):
        url = self.baseurl + "/deep.css"
        try:
            req = urllib.request.urlopen(url, None, 3)
            self.assertTrue( False, "Should have thrown an HTTP Error for /deep.css!")
        except urllib.request.HTTPError as e:
            self.assertTrue( e.getcode()  == 404 , ("404 Not FOUND! %d" % e.getcode()))
        else:
            self.assertTrue( False, "Another Error was thrown!")
        url = self.baseurl + "/deep/deep"
        try:
            req = urllib.request.urlopen(url, None, 3)
            self.assertTrue( False, "Should have thrown an HTTP Error for /deep/deep!")
        except urllib.request.HTTPError as e:
            self.assertTrue( e.getcode()  == 404 , ("404 Not FOUND! %d" % e.getcode()))
        else:
            self.assertTrue( False, "Another Error was thrown!")

if __name__ == '__main__':
    unittest.main()
