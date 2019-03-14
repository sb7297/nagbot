# Little Sister is watching you.

from disco.bot import Plugin
from queue import Queue

class ActivityWatcherPlugin(Plugin):
    def load(self, ctx):
        super(ActivityWatcherPlugin, self).load(ctx)
        self.data = ctx
        self.muted = 555220262510002179 # hardcoded "muted" role id
        self.threshold = 5
        self.time_muted = 120
        self.user_queue = Queue()
        if not self.data :
            self.data = {}

    def unload(self, ctx):
        ctx = self.data
        super(ExamplePlugin, self).unload(ctx)

    @Plugin.command('ping')
    def command_ping(self, event):
        event.msg.reply('お兄ちゃん大好き')
    
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
            self.user_queue.put(event.guild.get_member(event.message.author))
            self.data[event.message.author.id] = 0
            self.register_schedule(self.unmute, self.time_muted, init=False)
        print(event.message.author, self.data[event.message.author.id])

    def unmute(self):
        user = self.user_queue.get()
        user.remove_role(self.muted)
