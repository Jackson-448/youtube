from __future__ import unicode_literals

from .common import InfoExtractor


class AparatCamIE(InfoExtractor):
    _VALID_URL = r'https?://aparat.cam/(?P<id>[^/?#]+)'
    _TESTS = []

    def _real_extract(self, url):
        video_id = self._match_id(url)

        webpage = self._download_webpage(url, video_id)

        video = self._parse_json(
            self._html_search_regex(r'src:\s*(?P<data>"(?:[^\\"]|\\.)*")',
                                    webpage, 'video', group='data'),
            video_id)

        try:
            poster = self._parse_json(
                self._html_search_regex(r'poster:\s*(?P<data>"(?:[^\\"]|\\.)*")',
                                        webpage, 'poster', group='data'),
                video_id)
        except ValueError:
            poster = None

        title = self._html_search_regex(r'<title>(?P<data>.*?)</title>',
                                        webpage, 'title', group='data',
                                        default=None)
        if title and title.startswith('Watch '):
            title = title[6:]

        return {
            'id': video_id,
            'url': video,
            'title': title,
            'thumbnail': poster,
            'age_limit': 18,
            'protocol': 'm3u8',
            'ext': 'mp4',
        }
