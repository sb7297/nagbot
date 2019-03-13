# Little Sister is watching you.

from disco.bot import Plugin

class ActivityWatcherPlugin(Plugin):
    def load(self, ctx):
        super(ActivityWatcherPlugin, self).load(ctx)
        self.data = ctx
        if not self.data :
            self.data = {
                'seen_users' : {},
                'message_counter': 0
            }

    def unload(self, ctx):
        ctx = self.data
        super(ExamplePlugin, self).unload(ctx)

    @Plugin.command('ping')
    def command_ping(self, event):
        event.msg.reply('お兄ちゃん大好き')
    
    @Plugin.listen('MessageCreate')
    def on_message_create(self, event):
        if event.message.author.id == self.bot.client.state.me.id:
            pass
        elif self.data['message_counter'] < 5 : # TODO Make message threshold configurable
            self.data['message_counter'] = self.data['message_counter'] + 1
        else :
            # TODO mute channe
            for key, value in event.guild.roles.items() : 
                print(key, value.name) 
            event.guild.get_member(event.message.author).add_role(555220262510002179) # hardcoded "muted" role id
            print(event.message.id)
            event.message.reply("お兄ちゃんのばか！")
            self.data['message_counter'] = 0
        print(event.message.author, self.data['message_counter'])
