import nextcord
from nextcord import Interaction
from nextcord.ext import commands

import properties
from lotify_client import get_lotify_client

bot = commands.Bot()
lotify_client = get_lotify_client()


class Subscriptions(nextcord.ui.View):
    def __int__(self):
        super().__init__()

    @nextcord.ui.button(label="LINE", style=nextcord.ButtonStyle.green)
    async def line_subscribe(self, button: nextcord.ui.button, interaction: Interaction):
        discord_user_id = interaction.user.id
        auth_url = lotify_client.get_auth_link(state=discord_user_id)
        await interaction.response.send_message(f'專屬於你的 LINE Notify 訂閱連結\n{auth_url}', ephemeral=True)
        self.stop()


@bot.slash_command(description="選擇要接收通知的平台")
async def subscribe(interaction: nextcord.Interaction):
    view = Subscriptions()
    await interaction.response.send_message('請選擇下方任一平台訂閱通知', view=view, ephemeral=True)
    await view.wait()


def start():
    bot.run(properties.DISCORD_BOT_TOKEN)
