'''utils.py utilities for the dataspec package'''

import contextlib
import os
import urllib


@contextlib.contextmanager
def url_to_file(url):
    '''Return a pathname to a file on disk, given a URL

    :param url: URL to download, or if "file:" url, convert to file path

    A "with" statement should be used to scope the temporary file, e.g.

    with url_to_file(url) as path:
        image = cv2.imread(path)

    :returns: file name
    '''
    if url.startswith("file:"):
        yield urllib.url2pathname(url[5:])
    else:
        temppath, result = urllib.urlretrieve(url)
        yield temppath
        os.remove(temppath)

all = [url_to_file]
