# Little Sister is watching you.

from disco.bot import Plugin
from queue import Queue
import gevent

class ActivityWatcherPlugin(Plugin):
    def load(self, ctx):
        super(ActivityWatcherPlugin, self).load(ctx)
        self.data = ctx
        self.muted = 555580008673050643 # hardcoded "muted" role id
        self.threshold = 22
        self.time_muted = 3600
        if not self.data :
            self.data = {}

    def unload(self, ctx):
        ctx = self.data
        # TODO persist muting data
        super(ExamplePlugin, self).unload(ctx)

    @Plugin.command('ping')
    def command_ping(self, event):
        event.msg.reply('お兄ちゃん大好き')

# TODO Add ability for user to mute themself
    @Plugin.command('muteme')
    def command_muteme(self, event):
        event.msg.reply("兄ちゃん偉い、偉い。" + str(self.time_muted / 60) + " minute time out.")
        event.guild.get_member(event.author).add_role(self.muted)
        self.data[event.msg.author.id] = 0
        gevent.sleep(self.time_muted)
        event.guild.get_member(event.author).remove_role(self.muted)

    @Plugin.listen('MessageCreate')
    def on_message_create(self, event):
        if event.message.author.id == self.bot.client.state.me.id:
            return
        elif not (event.message.author.id in self.data) :
            self.data[event.message.author.id] = 1
        elif self.data[event.message.author.id] < self.threshold :
            self.data[event.message.author.id] = self.data[event.message.author.id] + 1
        else :
            for key, value in event.guild.roles.items() : 
                print(key, value.name) 
            event.guild.get_member(event.message.author).add_role(self.muted) 
            event.message.reply("お兄ちゃんのばか！" + str(self.time_muted / 60) + " minute time out!")
            self.data[event.message.author.id] = 0
            gevent.sleep(self.time_muted)
            event.guild.get_member(event.message.author).remove_role(self.muted)

        print(event.message.author, self.data[event.message.author.id])
