from reddit.api import get_new_posts_from_subreddit as gs
from reddit.download_photo import download_medias
import pprint
import asyncio
from reddit.classes import Media
from vk.vk import upload_medias, api
from vk import VK_USER_ID

posts = gs(sreddit="FortniteLeaks", limit=5)

async def test(post):
    attachments = ''
    if post.media and post.media[0].file_type != 'video':
        await download_medias(post.media)
        ids = await upload_medias(post.media)
        for id in ids:
            attachments += f'photo{VK_USER_ID}_{id},'
        await api.wall.post(owner_id=-220785898,
                            message=post.title,
                            attachments=attachments[:-1])
    else:
        await api.wall.post(owner_id=-220785898,
                            message=post.title)
#posts = gs(sreddit="FortniteLeaks", limit=1)
#for post in posts:
#   if post.media:
#      asyncio.run(download_medias(post.media))

#pprint.pprint(gs(sreddit="FortniteLeaks", limit=1))

for post in posts:
    asyncio.get_event_loop().run_until_complete(test(post))

media_1 = Media(
        media_url='https://preview.redd.it/lh8gkdb2hugb1.jpg?auto=webp&s=56e35b9c2a83e0d14305664dc282b74c6ec74f2d',
        format_file='png',
        filename='8ydf6qajqugb1',
        file_type='image')


media_2 = Media(
        media_url='https://preview.redd.it/c3isy96frpgb1.jpg?width=750&format=pjpg&auto=webp&s=74f5b9369d7e4b890da079ac74924598c3b39a4b',
        format_file='jpg',
        filename='c3isy96frpgb1',
        file_type='image')
