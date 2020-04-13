# from cogs.puzzles.scripts import *
from data.data import data
import importlib
import asyncio
import os


async def loader(self, msg):
    if msg.author.id is not self.bot.user.id:
        progress = data.base['progress'].find_one(user_id=msg.author.id)
        if progress is not None:
            script = data.base['puzzle'].find_one(chapter=progress['chapter'], page=progress['page'])['script']
        else:
            script = 'beginning'
        abspath = os.path.abspath('.')
        t = importlib.import_module(f'cogs.scripts.scripts.{script}', abspath)
        await asyncio.sleep(1)
        r = await t.run(self, msg)
        if r is not None:
            new = str(r).split('.')
            data.base['progress'].upsert(dict(user_id=msg.author.id, chapter=new[0], page=new[1]), ['user_id'])

    pass
