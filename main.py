
import pkg_resources
import subprocess
import sys

def check_and_install(package):
    try:
        pkg_resources.get_distribution(package)
    except pkg_resources.DistributionNotFound:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

check_and_install("discord.py-self")
check_and_install("rich")

import discord
from discord import Client, AuditLogAction
from rich.console import Console
from rich.progress import Progress
from rich.prompt import Prompt
from rich.status import Status
console = Console()

token = Prompt.ask("[bold green]Please enter your bot token[/bold green]")
guild_id = int(Prompt.ask("[bold green]Please enter the guild ID[/bold green]"))

bot = Client()

@bot.event
async def on_ready():
        console.print(f"[bold blue]Bot is now running and monitoring for vanity URL theft in guild {guild_id}...[/bold blue]")


@bot.event
async def on_audit_log_entry_create(entry):
    if entry.guild.id == guild_id and entry.action is AuditLogAction.guild_update and hasattr(entry.after, "vanity_url_code") and entry.user.id != bot.user.id:
        await entry.guild.edit(vanity_code=entry.before.vanity_url_code)
        await entry.user.ban()
        console.log(f"[bold red]Vanity URL stolen by {entry.user.name} ({entry.user.id}). User has been banned and vanity URL has been restored.[/bold red]")



if __name__ == "__main__":
    with console.status("[bold purple]Bot is waiting...[/bold purple]", spinner="dots"):
        bot.run(token, log_handler=None)
