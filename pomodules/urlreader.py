# -*- coding: utf-8 -*-
import os
import gzip
import json
from io import StringIO, BytesIO
from urllib import request

def _uncompressBuffer(buffer):
    if isinstance(buffer, str):
        buf = StringIO(buffer)
    else:
        buf = BytesIO(buffer)
    f = gzip.GzipFile(fileobj=buf)
    data = f.read()
    return data


class Urlreader():

    def __init__(self, url):

        self.url = url
        self.block_sz = 8192

    def _openURL(self):
        """Send a request to url, return the response"""
        try:
            rq = request.Request(self.url)
            rq.add_header('Accept-Encoding', 'gzip')
            response = request.urlopen(rq)
            return response

        except request.HTTPError as e:
            print ("HTTP error reading url:", url)
            print ("Code", e.code)
            print ("Returns", e.read())

        except request.URLError as e:
            print ("URL error reading url:", url)
            print ("Reason:", e.reason)

        return None

    def getDataResponse(self):
        """download into data buffer"""

        data = ""
        response = self._openURL()

        if not response:
            return data

        while True:
            buffer = response.read(self.block_sz)
            if not buffer:
                break

            if not data:
                data = buffer
            else:
                data += buffer
        response.close()
        if response.info().get('Content-Encoding') == 'gzip':
            data = _uncompressBuffer(data)
        return data

    def getJsonResponse(self):
        """load a json structure from a REST-URL, returns a list/dict python object"""

        data = self.getDataResponse()
        if data is None or data == "":
            return None

        d = json.loads(data)
        return d

    def getFileResponse(self, dest):
        """read response from url, save it to dest, returns a filename.
        dest should be a directory
        filename is derived from url or 'unknown.dat'
        """

        data = self.getDataResponse()
        if data is None or data == "":
            return None

        # get file name from url
        file_name = self.url.split('/')[-1].split('?')[0]
        if not file_name:
            file_name = 'unknown.dat' # a default
        # join with destination dir
        file_name = os.path.realpath(os.path.join(dest, file_name))
        # open, write and close
        savefile = open(file_name, 'wb')
        savefile.write(data)
        savefile.close()
        # return saved file name
        return file_name


