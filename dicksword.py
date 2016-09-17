import sqlite3
import discord
import asyncio
import logging
import signal
import sys
import random
import yaml

config = yaml.load(open('config.yaml', 'r'))

wordlist = config['wordlist']

fortune_file = open(config['fortune_file'], 'r')

fortunes = fortune_file.read().split('%')

logging.basicConfig(level=logging.INFO)

client = discord.Client()

conn = sqlite3.connect(config['db_file'])
c = conn.cursor()
c.execute('create table if not exists tallies (id integer primary key, user text, tally integer)')

class GracefulKiller:
    """."""

    def exit_gracefully(self, signum, frame):
        """."""
        conn.close()
        client.close()
        sys.exit(0)

    signal.signal(signal.SIGINT, exit_gracefully)
    signal.signal(signal.SIGTERM, exit_gracefully)


@client.event
async def on_ready():
    """."""
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(message):
    """Yep."""
    if message.content.startswith(config['prefix'] + 'stats'):
        if len(message.content.split(' ')) == 1:
            c.execute('SELECT * FROM tallies WHERE ?=id',
                      (str(message.author.id),))
            row = c.fetchone()
            if row is None:
                await client.send_message(message.channel, str(message.author.name) + ' has mentioned ' + config['wordlist_keyword'] + ' 0 times')
            else:
                await client.send_message(message.channel, str(message.author.name) + ' has mentioned ' + config['wordlist_keyword'] + ' ' + str(row[2]) + ' times')
        else:
            c.execute('SELECT * FROM tallies WHERE ? LIKE user',
                      (' '.join(message.content.split(' ')[1:]),))
            row = c.fetchone()
            if row is None:
                await client.send_message(message.channel, ' '.join(message.content.split(' ')[1:]) + ' has mentioned ' + config['wordlist_keyword'] + ' 0 times')
            else:
                await client.send_message(message.channel, ' '.join(message.content.split(' ')[1:]) + ' has mentioned ' + config['wordlist_keyword'] + ' ' + str(row[2]) + ' times')
    elif message.content.startswith(config['prefix'] + config['fortune_keyword']):
        await client.send_message(message.channel, fortunes[random.randrange(0, len(fortunes))])
    elif client.user == message.author:
        pass
    else:
        #        print(message.author.id)
        for w in wordlist:
            if w.lower() in message.content.lower():
                #               await client.send_message(message.channel, '+D')
                #               print(type(message.author))
                #               print(message.author.name)
                c.execute('SELECT * FROM tallies WHERE ?=id',
                          (str(message.author.id),))
                row = c.fetchone()
    #            print(row)
                if row is None:
                    c.execute('INSERT OR REPLACE INTO tallies VALUES (?, ?, ?)', (message.author.id, str(message.author), 1))
                else:
                    if (int(row[2]) + 1) % 10 == 0:
                        await client.send_message(message.channel, '+10D')
                    c.execute('INSERT OR REPLACE INTO tallies VALUES (?, ?, ?)', (message.author.id, str(message.author), row[2] + 1))

                conn.commit()

client.run(config['token'])
