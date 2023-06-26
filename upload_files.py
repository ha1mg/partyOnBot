import os
import asyncio
import logging
from aiogram import Bot
# from sqlalchemy import create_engine
# from sqlalchemy.orm import scoped_session, sessionmaker
#
# from db_map import Base, MediaIds
import sqlite3
from config import TOKEN, ADMIN_ID
from config import DIRECTORY

directory = r'{0}\botuploads.db'.format(DIRECTORY)

logging.basicConfig(format=u'%(filename)s [ LINE:%(lineno)+3s ]#%(levelname)+8s [%(asctime)s]  %(message)s',
                    level=logging.DEBUG)

connection = sqlite3.connect(directory)
cur = connection.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS botuploads (id INTEGER PRIMARY KEY AUTOINCREMENT,file_id TEXT UNIQUE NOT NULL,
                                   filename TEXT NOT NULL);''')

connection.commit()
cur.close()

bot = Bot(token=TOKEN)


BASE_MEDIA_PATH = '.\media'


async def uploadMediaFiles(folder, method, file_attr):
    folder_path = os.path.join(BASE_MEDIA_PATH, folder)
    for filename in os.listdir(folder_path):
        if filename.startswith('.'):
            continue

        logging.info(f'Started processing {filename}')
        with open(os.path.join(folder_path, filename), 'rb') as file:
            msg = await method(ADMIN_ID, file, disable_notification=True)
            if file_attr == 'photo':
                file_id = msg.photo[-1].file_id
            else:
                file_id = getattr(msg, file_attr).file_id
            connection = sqlite3.connect(directory)
            cur = connection.cursor()
            try:
                cur.execute("INSERT INTO botuploads(file_id, filename) VALUES (?, ?)", (file_id, filename))
                connection.commit()
            except Exception as e:
                logging.error(
                    'Couldn\'t upload {}. Error is {}'.format(filename, e))
            else:
                logging.info(
                    f'Successfully uploaded and saved to DB file {filename} with id {file_id}')
            finally:
                cur.close()

loop = asyncio.get_event_loop()

tasks = [
    loop.create_task(uploadMediaFiles('pics', bot.send_photo, 'photo')),
    # loop.create_task(uploadMediaFiles('videos', bot.send_video, 'video')),
    # loop.create_task(uploadMediaFiles('videoNotes', bot.send_video_note, 'video_note')),
    # loop.create_task(uploadMediaFiles('files', bot.send_document, 'document')),
    # loop.create_task(uploadMediaFiles('ogg', bot.send_voice, 'voice')),
]

wait_tasks = asyncio.wait(tasks)

loop.run_until_complete(wait_tasks)
loop.close()
# Session.remove()