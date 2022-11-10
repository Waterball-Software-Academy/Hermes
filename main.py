import threading

import discord_bot
import notifier_web

if __name__ == '__main__':
    threading.Thread(target=notifier_web.start).start()
    print('start discord bot\n')
    discord_bot.start()
