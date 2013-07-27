# -*- coding: utf-8 -*-

from tornado import httpclient
from toredis import Client


redis_client = Client()
redis_client.connect('localhost')

http_client = httpclient.AsyncHTTPClient()
