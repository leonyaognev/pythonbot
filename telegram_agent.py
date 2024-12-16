from telethon.tl.functions.channels import InviteToChannelRequest, CreateChannelRequest, CheckUsernameRequest, UpdateUsernameRequest, DeleteChannelRequest, EditPhotoRequest
from telethon.tl.functions.messages import ExportChatInviteRequest
from telethon.types import MessageService
from natsort import natsorted
from os import system, listdir
import dbfile as db
from telethon import TelegramClient
from search import lexemes, induction
import json as js

db.create_tables()


async def create_channel(client, file_data):
    file_data = file_data.split('.')
    file_data = file_data[0].split()
    file_data[0] = file_data[0].replace('_', ' ')
    chanel = db.ChanelService().add(file_data[0])
    if chanel:
        result = await client(
            CreateChannelRequest(
                chanel.chanelname.replace('-', ' '),
                'больше контента в нашем боте @leognburs_bot',
                megagroup=False
            )
        )
        channel = result.chats[0]
        db.ChanelService().update_link(channel.id, chanel.id)
        invite_link = await client(ExportChatInviteRequest(channel.id))
        db.ChanelService().update_inviteLink(
            invite_link.__dict__['link'], chanel.id)

        with open('caption.json', 'r') as data:
            penis = js.load(data)
        print(penis)
        db.ChanelService().update_caption(
            penis[f'{chanel.chanelname}'], chanel.id)
        del penis[f'{chanel.chanelname}']

        with open('caption.json', 'w') as data:
            js.dump(penis, data)

        for linkfile in listdir('photo'):
            if file_data[0] in linkfile:
                file = await client.upload_file(f'photo/{linkfile}')
                await client(EditPhotoRequest(
                    channel=channel.id, photo=file))
                message = await client.send_file('me',
                                                 file,
                                                 force_document=False,
                                                 caption=str(chanel.id),
                                                 )
                await client.forward_messages(
                    entity='leognburs_bot',
                    messages=message.id,
                    from_peer='me')
                break
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
        # await client.send_code_request(phone)
        await client.sign_in(phone, input('Enter code: '))
    await client.start()
    return client


def caption(name):
    name = name.split('.')
    name = name[0].split('_')
    name[0] = name[0].replace('-', ' ')
    return name[0] + ' сезон: ' + name[1] + ' серия: ' + name[2]


async def send_all_files():
    client = await client_start()
    for channel_name in listdir('files'):
        channel = await create_channel(client, channel_name)
        for sesons in natsorted(listdir(f'files/{channel_name}')):
            for file in natsorted(listdir(f'files/{channel_name}/{sesons}')):
                linkfile = f'files/{channel_name}/{sesons}/{file}'
                system(
                    f'ffmpeg -i {linkfile} -ss 00:00:01 -vframes 1 thumbnail.jpg')
                await client.send_file(channel.linkchanel,
                                       linkfile,
                                       caption=caption(file),
                                       supports_streaming=True,
                                       video=True,
                                       force_document=False,
                                       thumb='thumbnail.jpg'
                                       )
                system('rm -rf thumbnail.jpg')
        system(f'rm -rf /home/ognev/Documents/pythonbot/files/{channel_name}')
    await client.disconnect()


async def parse_chats(source_chat, channel_name):
    client = await client_start()
    penis = list()
    async for message in client.iter_messages(source_chat):
        penis.append(message)
    channel = await create_channel(client, channel_name)
    for message in penis[::-1]:
        if isinstance(message, MessageService):
            continue
        await client.send_message(channel.linkchanel, message)
    await client.disconnect()
    return channel.id


async def rename_parsed_messages(channel_id, seasons, *args):
    series = (0, *args)
    series = [int(i) for i in series]
    print(channel_id, seasons, series)
    client = await client_start()
    channel = db.ChanelService().get_by_id(channel_id)
    messages = list()
    async for message in client.iter_messages(channel.linkchanel, reverse=True):
        messages.append(message.id)
    messages = messages[2:]

    for seson in range(1, seasons+1):
        for index, message in enumerate(messages[series[seson-1]:series[seson]]):
            await client.edit_message(
                channel.linkchanel,
                message,
                text=f'{channel.chanelname.replace("-", " ")} сезон: {seson} серия: {index+1}')

    await client.disconnect()
    return True
