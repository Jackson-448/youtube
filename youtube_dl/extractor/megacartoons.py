# coding: utf-8
from __future__ import unicode_literals

import json
from ..utils import url_or_none

from .common import InfoExtractor


class MegaCartoonsIE(InfoExtractor):
    _VALID_URL = r'https?://(?:www\.)?megacartoons\.net/(?P<id>[a-z-]+)/'
    _TEST = {
        'url': 'https://www.megacartoons.net/help-wanted/',
        'md5': '4ba9be574f9a17abe0c074e2f955fded',
        'info_dict': {
            'id': 'help-wanted',
            'title': 'Help Wanted',
            'ext': 'mp4',
            'thumbnail': r're:^https?://.*\.jpg$',
            'description': 'md5:2c909daa6c6cb16b2d4d791dd1a31632'
        }
    }

    def _real_extract(self, url):
        # ID is equal to the episode name
        video_id = self._match_id(url)
        webpage = self._download_webpage(url, video_id)

        # Try to find a good title or fallback to the ID
        title = self._og_search_title(webpage) or video_id

        # Video data is stored in a json -> extract it from the raw html
        url_json = json.loads(self._html_search_regex(r'<div.*data-item=["/\'](?P<videourls>{.*})["/\'].*>', webpage, 'videourls'))

        video_url = url_or_none(url_json.get('sources')[0].get('src') or self._og_search_video_url(webpage))   # Get the video url
        video_thumbnail = url_or_none(url_json.get('splash') or self._og_search_thumbnail(webpage))            # Get the thumbnail

        # Find the <article> class in the html
        article = self._search_regex(
            r'(?s)<article\b[^>]*?\bclass\s*=\s*[^>]*?\bpost\b[^>]*>(.+?)</article\b', webpage, 'post', default='')

        # Extract the actual description from it
        video_description = (self._html_search_regex(r'(?s)<p>\s*([^<]+)\s*</p>', article, 'videodescription', fatal=False)
                            or self._og_search_description(webpage))

        return {
            'id': video_id,
            'title': title,
            'url': video_url,
            'thumbnail': video_thumbnail,
            'description': video_description,
        }
