
#!/usr/bin/env python

#Thanks to Venthur.

try:
    # python 2
    from urllib2 import Request, urlopen, quote
except ImportError:
    # python 3
    from urllib.request import Request, urlopen, quote

try:
    # python 2
    from htmlentitydefs import name2codepoint
except ImportError:
    # python 3
    from html.entities import name2codepoint

import re
import hashlib
import random
# fake google id (looks like it is a 16 elements hex)
rand_str = str(random.random()).encode('utf8')
google_id = hashlib.md5(rand_str).hexdigest()[:16]

GOOGLE_SCHOLAR_URL = "http://scholar.google.com"
# the cookie looks normally like:
#        'Cookie' : 'GSP=ID=%s:CF=4' % google_id }
# where CF is the format (e.g. bibtex). since we don't know the format yet, we
# have to append it later
HEADERS = {'User-Agent': 'Mozilla/5.0',
           'Cookie': 'GSP=ID=%s' % google_id}

FORMAT_BIBTEX = 1



def query(searchstr, outformat=FORMAT_BIBTEX, allresults=False):
    searchstr = '/scholar?q='+quote(searchstr)
    url = GOOGLE_SCHOLAR_URL + searchstr
    header = HEADERS
    header['Cookie'] = header['Cookie'] + ":CF=%d" % outformat
    request = Request(url, headers=header)
    response = urlopen(request)
    html = response.read()
    html = html.decode('utf8')
    tmp = get_links(html, outformat)
    result = list()
    if not allresults:
        tmp = tmp[:1]
    for link in tmp:
        url = GOOGLE_SCHOLAR_URL+link
        request = Request(url, headers=header)
        response = urlopen(request)
        bib = response.read()
        bib = bib.decode('utf8')
        result.append(bib)
    return result


def get_links(html, outformat):
    if outformat == FORMAT_BIBTEX:
        refre = re.compile(r'<a href="(/scholar\.bib\?[^"]*)')
    reflist = refre.findall(html)
    # escape html entities
    reflist = [re.sub('&(%s);' % '|'.join(name2codepoint), lambda m:
                      chr(name2codepoint[m.group(1)]), s) for s in reflist]
    return reflist



def _get_bib_element(bibitem, element):
    lst = [i.strip() for i in bibitem.split("\n")]
    for i in lst:
        if i.startswith(element):
            value = i.split("=", 1)[-1]
            value = value.strip()
            while value.endswith(','):
                value = value[:-1]
            while value.startswith('{') or value.startswith('"'):
                value = value[1:-1]
            return value
    return None




