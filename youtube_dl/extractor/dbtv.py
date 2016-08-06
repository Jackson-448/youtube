# coding: utf-8
from __future__ import unicode_literals

import re

from .common import InfoExtractor


class DBTVIE(InfoExtractor):
    _VALID_URL = r'https?://(?:www\.)?dbtv\.no/(?:[^/]+/)?(?P<id>[0-9]+)(?:#(?P<display_id>.+))?'
    _TESTS = [{
        'url': 'http://dbtv.no/3649835190001#Skulle_teste_ut_fornøyelsespark,_men_kollegaen_var_bare_opptatt_av_bikinikroppen',
        'md5': '2e24f67936517b143a234b4cadf792ec',
        'info_dict': {
            'id': '3649835190001',
            'display_id': 'Skulle_teste_ut_fornøyelsespark,_men_kollegaen_var_bare_opptatt_av_bikinikroppen',
            'ext': 'mp4',
            'title': 'Skulle teste ut fornøyelsespark, men kollegaen var bare opptatt av bikinikroppen',
            'description': 'md5:1504a54606c4dde3e4e61fc97aa857e0',
            'thumbnail': 're:https?://.*\.jpg',
            'timestamp': 1404039863,
            'upload_date': '20140629',
            'duration': 69.544,
            'uploader_id': '1027729757001',
        },
        'add_ie': ['BrightcoveNew']
    }, {
        'url': 'http://dbtv.no/3649835190001',
        'only_matching': True,
    }, {
        'url': 'http://www.dbtv.no/lazyplayer/4631135248001',
        'only_matching': True,
    }, {
        'url': 'http://dbtv.no/vice/5000634109001',
        'only_matching': True,
    }, {
        'url': 'http://dbtv.no/filmtrailer/3359293614001',
        'only_matching': True,
    }]

    def _real_extract(self, url):
        video_id, display_id = re.match(self._VALID_URL, url).groups()

        return {
            '_type': 'url_transparent',
            'url': 'http://players.brightcove.net/1027729757001/default_default/index.html?videoId=%s' % video_id,
            'id': video_id,
            'display_id': display_id,
            'ie_key': 'BrightcoveNew',
        }


class DagbladetArticleIE(InfoExtractor):
    _VALID_URL = r'https?://(?:www\.)?dagbladet\.no/(?:\d+/){3}(?:[\w-]+/)+(?P<id>\d+)'
    _TEST = {
        'url': 'http://www.dagbladet.no/2016/02/23/nyheter/nordlys/ski/troms/ver/43254897/',
        'info_dict': {
            'id': '43254897',
            'title': 'Etter ett \xe5rs planlegging, klaffet endelig alt: - Jeg m\xe5tte ta en liten dans',
        },
        'playlist_count': 3,
    }

    def _real_extract(self, url):
        article_id = self._match_id(url)
        webpage = self._download_webpage(url, article_id)
        iframe_urls = re.findall(r'<iframe src="([^"]+(?:lazy)?player[^"]+)"', webpage)

        entries = [self.url_result(self._proto_relative_url(iframe_url))
            for iframe_url in iframe_urls]
        return self.playlist_result(entries, article_id, self._og_search_title(webpage))
