import re

from collections import namedtuple

import aiohttp

from discord.ext import commands


API_BASE_URL = 'https://atcoder-api.appspot.com/'
CONTESTS_URL = 'contests'

Rank = namedtuple('Rank', 'low high title title_abbr color_graph color_embed')
RATED_RANKS = (
    Rank(-10 ** 9, 1650, 'Gray', 'N', '#b7b7b7', 0x808080),
    Rank(1650, 1750, 'Green', 'P', '#70ad47', 0x008000),
    Rank(1750, 2000, 'Blue', 'E', '#3c78d8', 0x0000ff),
    Rank(2000, 2200, 'Purple', 'CM', '#7030a0', 0xaa00aa),
    Rank(2200, 2500, 'Yellow', 'IM', '#f6b26b', 0xf57500),
    Rank(2500, 3000, 'Red', 'IGM', '#FF0000', 0xff0000),
    Rank(3000, 10 ** 9, 'Legend', 'LGM', '#AA0000', 0xcc0000)
)

RatingChange = namedtuple('RatingChange', 'rating time')


class AtcoderApiError(commands.CommandError):
    """Base class for all API related errors."""
    def __init__(self, message=None):
        super().__init__(message or 'AtCoder API error')


class ClientError(AtcoderApiError):
    """An error caused by a request to the API failing."""
    def __init__(self):
        super().__init__('Error connecting to AtCoder API')


class TrueApiError(AtcoderApiError):
    """An error originating from a valid response of the API."""
    def __init__(self, comment, message=None):
        super().__init__(message)
        self.comment = comment


_session = None


async def initialize():
    global _session
    _session = aiohttp.ClientSession()


async def _query_api(path, params=None):
    url = API_BASE_URL + path
    try:
        async with _session.get(url, params=params) as resp:
            try:
                respjson = await resp.json(content_type=None, encoding='utf-8')
            except aiohttp.ContentTypeError as e:
                # 'AtCoder API did not respond with JSON, status {resp.status}.'
                raise AtcoderApiError
            if resp.status == 200:
                return respjson
            comment = f'HTTP Error {resp.status}, {respjson.get("errorCode")}'
    except aiohttp.ClientError as e:
        # 'Request to AtCoder API encountered error: {e!r}'
        raise ClientError from e
    raise TrueApiError(comment)


async def contests():
    resp = await _query_api(CONTESTS_URL)
    parsed_contests = []
    for entry in resp:
        parsed_contests.append(entry)

    return parsed_contests

# async def rating(*, username):
#     params = {'username': username}
#     try:
#         resp = await _query_api(CONTEST_HISTORY_URL, params)
#     except TrueApiError as e:
#         if 'NOT_FOUND' in e.comment:
#             raise HandleNotFoundError(e.comment, username)
#         # if 'should contain' in e.comment:
#         #     raise HandleInvalidError(e.comment, handle)
#         raise
#
#     data, contests_map = resp['data'], resp['contestsMap']
#     return [RatingChange(contest_history['rating']['publicRating'], contests_map[contest_history['contestJid']]['beginTime'])
#             for contest_history in data if contest_history['rating']]
#
#     # return resp
#     # return [make_from_dict(RatingChange, ratingchange_dict) for ratingchange_dict in resp]