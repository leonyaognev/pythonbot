from telethon.tl.functions.channels import InviteToChannelRequest, CreateChannelRequest, CheckUsernameRequest, UpdateUsernameRequest
from os import listdir
import dbfile as db
from telethon import TelegramClient
from search import lexemes, induction
import re

db.create_tables()


async def create_channel(client, file_data):
    file_data = file_data.split('.')
    file_data = file_data[0].split()
    file_data[0] = file_data[0].replace('_', ' ')
    chanel = db.ChanelService().add(file_data[0])
    if chanel:
        result = await client(
            CreateChannelRequest(
                chanel.chanelname,
                chanel.descrchanel,
                megagroup=False
            )
        )
        channel = result.chats[0]
        db.ChanelService().update_link(channel.id, chanel.id)
        # induction:
        lexemes_list = lexemes(chanel.chanelname)
        induction(lexemes_list, chanel.id)

    return db.ChanelService().get_by_chanelname(file_data[0])


async def client_start():
    entity = 'Flibuster'
    api_id = 23535213
    api_hash = 'aa257f8f5af23d94c60ea4c31ad3a7e7'
    phone = '+79665039590'
    client = TelegramClient(entity, api_id, api_hash)
    await client.connect()
    if not await client.is_user_authorized():
        await client.send_code_request(phone)
        await client.sign_in(phone, input('Enter code: '))
    await client.start()
    return client


def caption(name):
    name = name.split('.')
    name = name[0].split('_')
    name[0] = name[0].replace('-', ' ')
    return name[0] + ' сезон: ' + name[1] + ' серия: ' + name[2]


def extract_numbers(file_name):
    match = re.search(r'_(\d+)_(\d+)', file_name)
    return int(match.group(1)), int(match.group(2))


async def send_all_files():
    client = await client_start()
    for channel_name in listdir('files'):
        channel = await create_channel(client, channel_name)
        for sesons in range(len(listdir(f'files/{channel_name}'))):
            for file in sorted(listdir(f'files/{channel_name}/{sesons+1}'), key=extract_numbers):
                linkfile = f'files/{channel_name}/{sesons + 1}/{file}'
                await client.send_file(channel.linkchanel,
                                       linkfile,
                                       caption=caption(file)
                                       )
