import sqlite3
import discord
import asyncio
import logging

logging.basicConfig(level=logging.INFO)

client = discord.Client()

conn = sqlite3.connect('dicksword.db')
c = conn.cursor()
c.execute('create table if not exists tallies (user text primary key, tally integer)')

wordlist = ["dick", "dong", "hung", "cock",
            "penis", "schlong", "shlong", "weener", "+D"]


@client.event
async def on_ready():
    """Yep."""
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(message):
    """Yep."""
    if message.content.startswith('$dstats'):
        if len(message.content.split(' ')) == 1:
            c.execute('SELECT * FROM tallies WHERE ?=user',
                      (str(message.author),))
            row = c.fetchone()
            if row is None:
                await client.send_message(message.channel, str(message.author) + ' has mentioned dongs 0 times')
            else:
                await client.send_message(message.channel, str(message.author) + ' has mentioned dongs ' + str(row[1]) + ' times')
        else:
            c.execute('SELECT * FROM tallies WHERE ?=user',
                      (' '.join(message.content.split(' ')[1:]),))
            row = c.fetchone()
            if row is None:
                await client.send_message(message.channel, ' '.join(message.content.split(' ')[1:]) + ' has mentioned dongs 0 times')
            else:
                await client.send_message(message.channel, ' '.join(message.content.split(' ')[1:]) + ' has mentioned dongs ' + str(row[1]) + ' times')
    elif client.user == message.author:
        pass
    else:
        #        print(message.author.id)
        for w in wordlist:
            if w in message.content.lower():
                #               await client.send_message(message.channel, '+D')
                #               print(type(message.author))
                #               print(message.author.name)
                c.execute('SELECT * FROM tallies WHERE ?=user',
                          (str(message.author),))
                row = c.fetchone()
    #            print(row)
                if row is None:
                    c.execute('INSERT OR REPLACE INTO tallies VALUES (?, ?)', (
                        str(message.author), 1))
                else:
                    if (int(row[1]) + 1) % 10 == 0:
                        await client.send_message(message.channel, '+10D')
                    c.execute('INSERT OR REPLACE INTO tallies VALUES (?, ?)', (
                        str(message.author), row[1] + 1))

                conn.commit()

client.run('token')
