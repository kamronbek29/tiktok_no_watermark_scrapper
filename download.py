import os
from uuid import uuid4

import aiohttp


async def download_video(video_url):
    if not os.path.exists('downloads'):
        os.mkdir('downloads')

    file_directory = 'downloads/{}.mp4'.format(str(uuid4()).replace('-', ''))
    async with aiohttp.ClientSession() as session:
        async with session.get(video_url) as get_video:
            with open(file_directory, "wb") as file_to_save:
                file_content = await get_video.content.read()
                file_to_save.write(file_content)

            return file_directory
