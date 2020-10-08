import asyncio
import sys

import aiohttp
from pyquery import PyQuery as pq

from tiktok_no_watermark_scrapper.download import download_video


async def get_video_without_watermark(url):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://ssstiktok.io/ru') as get_request:
            get_request_content = await get_request.content.read()
            get_request_content_str = str(get_request_content, 'utf-8')

            get_request_pq_obj = pq(get_request_content_str)('form.pure-form')
            request_path = get_request_pq_obj.attr('data-hx-post')
            request_data = get_request_pq_obj.attr('include-vals')

            split_request_data = str(request_data).split(', ')

            tt_data = split_request_data[0].split(':')[1].replace("'", '')
            ts_data = split_request_data[1].split(':')[1]

            post_request_url = 'https://ssstiktok.io{}'.format(request_path)
            data = {'id': url, 'locale': 'ru', 'tt': tt_data, 'ts': ts_data}

        async with session.post(post_request_url, data=data) as post_request:
            post_request_content = await post_request.content.read()
            post_request_content_str = str(post_request_content, 'utf-8')

            post_request_pq_obj_items = pq(post_request_content_str)('div')('a').items()

            for one_item in post_request_pq_obj_items:
                if 'http' in str(one_item):
                    video_url = one_item.attr('href')
                    return video_url


async def main():
    url = input('Paste tiktok video link here: ')
    print('Please, wait. Getting video link...')
    video_url = await get_video_without_watermark(url)

    if video_url is None:
        print('Unable download this video...')
        sys.exit(0)

    print('Downloading the video...')
    file_directory = await download_video(video_url)
    print('Video downloaded! File name: {}'.format(file_directory))


if __name__ == '__main__':
    asyncio.run(main())
