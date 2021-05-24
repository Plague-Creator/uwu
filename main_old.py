try:
    import asyncio
    
    import os
    
    
    import sanic
    import keep_alive
    

    import json
    from functools import partial

    import random as rand

    from colorama import Fore, Back, Style, init

    init(autoreset=True)

    import fortnitepy
    from fortnitepy.ext import commands
    import BenBotAsync
    import aiohttp
    import requests

except ModuleNotFoundError as e:
    print(e)
    print(
        Fore.RED
        + " â€¢ "
        + Fore.RESET
        + 'Failed to import 1 or more modules. Run "INSTALL PACKAGES.bat'
    )
    exit()

os.system("cls||clear")

intro = (
    Fore.LIGHTCYAN_EX
    + """ 
    GhostFN for an easy lobby bot! Join here if you need help or found any bugs\n https://discord.gg/rAd9YnHjV3, LOGIN WITH YOUR BOT ACCOUNT HERE COPY AND PASTE THE CODE! http://bit.ly/38URYTD
                                                                    
 """
)

print(intro)

sanic_app = sanic.Sanic(__name__) 
server = None

name = ""

filename = 'device.json'

@sanic_app.route('/', methods=['GET'])
async def accept_ping(request: sanic.request.Request):
    return sanic.response.json({"status": "online"})


@sanic_app.route('/name', methods=['GET'])
async def accept_ping(request: sanic.request.Request):
    return sanic.response.json({"display_name": name})


def lenPartyMembers():
    members = client.party.members
    return len(members)


def warn(*args, **kwargs):
    pass


import warnings

warnings.warn = warn


def lenFriends():
    friends = client.friends
    return len(friends)


def getNewSkins():
    r = requests.get("https://benbotfn.tk/api/v1/files/added")

    response = r.json()

    cids = []

    for cid in [
        item for item in response if item.split("/")[-1].upper().startswith("CID_")
    ]:
        cids.append(cid.split("/")[-1].split(".")[0])

    return cids


def getNewEmotes():
    r = requests.get("https://benbotfn.tk/api/v1/files/added")

    response = r.json()

    eids = []

    for cid in [
        item for item in response if item.split("/")[-1].upper().startswith("EID_")
    ]:
        eids.append(cid.split("/")[-1].split(".")[0])

    return eids


def get_device_auth_details():
    if os.path.isfile("auths.json"):
        with open("auths.json", "r") as fp:
            return json.load(fp)
    else:
        with open("auths.json", "w+") as fp:
            json.dump({}, fp)
    return {}


def store_device_auth_details(email, details):
    existing = get_device_auth_details()
    existing[email] = details

    with open("auths.json", "w") as fp:
        json.dump(existing, fp)


with open("config.json") as f:
    try:
        data = json.load(f)
    except json.decoder.JSONDecodeError as e:
        print(
            Fore.RED
            + " [ERROR] "
            + Fore.RESET
            + "There was an error in one of the bot's files! (config.json). GhostFN for an easy lobby bot! Join here if you need help or found any bugs\n https://discord.gg/rAd9YnHjV3"
        )
        print(Fore.LIGHTRED_EX + f"\n {e}")
        exit(1)


with open("info.json") as f:
    try:
        info = json.load(f)
    except json.decoder.JSONDecodeError as e:
        print(
            Fore.RED
            + " [ERROR] "
            + Fore.RESET
            + "There was an error in one of the bot's files! (info.json) GhostFN for an easy lobby bot! Join here if you need help or found any bugs\n https://discord.gg/rAd9YnHjV3"
        )
        print(Fore.LIGHTRED_EX + f"\n {e}")
        exit(1)


def is_admin():
    async def predicate(ctx):
        return ctx.author.id in info["FullAccess"]

    return commands.check(predicate)


device_auth_details = get_device_auth_details().get(data["email"], {})

prefix = data["prefix"]

client = commands.Bot(
    command_prefix=prefix,
    case_insensitive=True,
    auth=fortnitepy.AdvancedAuth(
        email=data["email"],
        password=data["password"],
        prompt_authorization_code=True,
        delete_existing_device_auths=True,
        **device_auth_details,
    ),
    platform=fortnitepy.Platform.XBOX_X,
)
client.sanic_app = sanic_app
client.server = server




@client.event
async def event_device_auth_generate(details, email):
    store_device_auth_details(email, details)


@client.event
async def event_ready():
    
    os.system("cls||clear")
    print(intro)
    print(
        Fore.LIGHTCYAN_EX
        + " â€¢ "
        + Fore.RESET
        
        + "Client ready as "
        + Fore.LIGHTCYAN_EX
        + f"{client.user.display_name}"
    )

    member = client.party.me

    await member.edit_and_keep(
        partial(fortnitepy.ClientPartyMember.set_outfit, asset=data["cid"]),
        partial(fortnitepy.ClientPartyMember.set_backpack, asset=data["bid"]),
        partial(fortnitepy.ClientPartyMember.set_pickaxe, asset=data["pid"]),
        partial(
            fortnitepy.ClientPartyMember.set_banner,
            icon='InfluencerBanner17',
            color='defaultcolor22',
            season_level='999',
        ),
        partial(
            fortnitepy.ClientPartyMember.set_battlepass_info,
            has_purchased=True,
            level='999',
        ),
    )

    client.set_avatar(
        fortnitepy.Avatar(
            asset='CID_017_Athena_Commando_M', background_colors=["#ffffff", "#ffffff", "#ffffff"]
        )
    )
    client.message='test'
    


@client.event
async def event_party_invite(invite):
    if data["joinoninvite"].lower() == "true":
        try:
            await invite.accept()
            print(
                Fore.LIGHTCYAN_EX
                + " â€¢ "
                + Fore.RESET
                + "Accepted party invite from"
                + Fore.LIGHTCYAN_EX
                + f"{invite.sender.display_name}"
            )
        except Exception:
            pass
    elif data["joinoninvite"].lower() == "false":
        if invite.sender.id in info["FullAccess"]:
            await invite.accept()
            print(
                Fore.LIGHTCYAN_EX
                + " â€¢ "
                + Fore.RESET
                + "Accepted party invite from "
                + Fore.LIGHTCYAN_EX
                + f"{invite.sender.display_name}"
            )
        else:
            print(
                Fore.LIGHTCYAN_EX
                + " â€¢ "
                + Fore.RESET
                + "Never accepted party invite from "
                + Fore.LIGHTCYAN_EX
                + f"{invite.sender.display_name}"
            )


@client.event
async def event_friend_request(request):
    if data["friendaccept"].lower() == "true":
        try:
            await request.accept()
            print(
                f" â€¢ Accepted friend request from {request.display_name}"
                + Fore.LIGHTBLACK_EX
                + f" ({lenFriends()})"
            )
        except Exception:
            pass
    elif data["friendaccept"].lower() == "false":
        if request.id in info["FullAccess"]:
            try:
                await request.accept()
                print(
                    Fore.LIGHTCYAN_EX
                    + " â€¢ "
                    + Fore.RESET
                    + "Accepted friend request from "
                    + Fore.LIGHTCYAN_EX
                    + f"{request.display_name}"
                    + Fore.LIGHTBLACK_EX
                    + f" ({lenFriends()})"
                )
            except Exception:
                pass
        else:
            print(f" â€¢ Never accepted friend request from {request.display_name}")

banned = []

@client.event
async def event_party_message(message: fortnitepy.PartyMessage):
    if message.content == "LupusLeaks" and client.party.me.leader:
        await message.author.kick()
        banned.append(message.author.id)
@client.event
async def event_party_message( message: fortnitepy.PartyMessage):
    if message.content == "LupusLeaks" and client.party.me.leader:
        await ctx.send("Lupus is really bad at making bots -_-")
@client.event
async def event_party_member_confirm(confirmation: fortnitepy.PartyJoinConfirmation):
    if confirmation.user.id not in banned:
        await confirmation.accept()

banned = []


@client.event
async def event_party_message(message: fortnitepy.PartyMessage):
    if message.content == "Heyy :bruh)                                                                                                                                For your own bot:                                                                                                                                : Youtube: LupusLeaks                                                                                                                                - TikTok: LupusLeaks                                                                                                                                -Instagram: LupusLeaks                                                                                                                                -Discord: https://ezfn.net/discord"and client.party.me.leader:
        await message.author.kick()
        banned.append(message.author.id)

@client.event
async def event_party_member_confirm(confirmation: fortnitepy.PartyJoinConfirmation):
    if confirmation.user.id not in banned:
        await confirmation.accept()

@client.event
async def event_party_member_join(member: fortnitepy.PartyMember) -> None:
    
    await client.party.send(
        f" Welcome {member.display_name}, \n Made with GhostFN \n Youtube: GhostLeaks to get your bot \n Join https://discord.gg/rAd9YnHjV3 for help!"
    )
    await client.party.me.set_emote(asset="EID_ElectroShuffle_V2")
    await asyncio.sleep(30.02)
    await client.party.me.clear_emote()
    await client.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

@client.command()
@is_admin()
async def leave(member: fortnitepy.PartyMember) -> None:
    
    
    await client.party.me.set_emote(asset="EID_Snap")
    await asyncio.sleep(1.50)
    await client.party.me.leave()
    await client.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
    

@client.command()
@is_admin()
async def block(ctx, *, user = None):
    if user is not None:
        try:
            user = await client.fetch_profile(user)
            friends = client.friends

            if user.id in friends:
                try:
                    await user.block()
                    await ctx.send(f"Added to blacklist {user.display_name}")
                except fortnitepy.HTTPException:
                    await ctx.send("Something went wrong trying to block that user.")

            elif user.id in client.blocked_users:
                await ctx.send(f"I already have {user.display_name} blocked.")
        except AttributeError:
            await ctx.send("Can't find this user")
    else:
        await ctx.send(f"No user was given. Try: {prefix}block (friend)")      

@client.command()
@is_admin()
async def unblock(ctx, *, user = None):
    if user is not None:
        try:
            member = await client.fetch_profile(user)
            blocked = client.blocked_users
            if member.id in blocked:
                try:
                    await client.unblock_user(user.id)
                    await ctx.send(f'Unblocked {user.display_name}')
                except fortnitepy.HTTPException:
                    await ctx.send('Something went wrong trying to unblock that user.')
            else:
                await ctx.send('That user is not blocked')
        except AttributeError:
            await ctx.send("Can’t find this user")
    else:
        await ctx.send(f'No user was given. Try: {prefix}unblock (blocked user)') 

@client.command()
@is_admin()
async def blocked(ctx):

    blockedusers = []

    for b in client.blocked_users:
        user = client.get_blocked_user(b)
        blockedusers.append(user.display_name)

    await ctx.send(f'Client has {len(blockedusers)} users blocked!')
    for x in blockedusers:
        if x is not None:
            await ctx.send(x)                

@client.event
async def event_party_member_confirm(confirmation):
    if confirmation.user.id in client.blocked_users:
        await confirmation.reject()
    else:
        await confirmation.confirm()


@client.event
async def event_party_member_leave(member):
    
    await client.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
    if client.user.display_name != member.display_name:
        try:
            print(
                Fore.LIGHTYELLOW_EX
                + f" â€¢ {member.display_name}"
                + Fore.RESET
                + " has left the lobby."
                + Fore.LIGHTBLACK_EX
                + f" ({lenPartyMembers()})"
            )
        except fortnitepy.HTTPException:
            pass


@client.event
async def event_party_message(message):
    if message.author.id in info["FullAccess"]:
        name = Fore.LIGHTCYAN_EX + f"{message.author.display_name}"
    else:
        name = Fore.RESET + f"{message.author.display_name}"
    print(Fore.GREEN + " â€¢ [Party] " + f"{name}" + Fore.RESET + f": {message.content}")


@client.event
async def event_friend_message(message):
    if message.author.id in info["FullAccess"]:
        name = Fore.LIGHTMAGENTA_EX + f"{message.author.display_name}"
    else:
        name = Fore.RESET + f"{message.author.display_name}"
    print(
        Fore.LIGHTMAGENTA_EX
        + " â€¢ [Whisper] "
        + f"{name}"
        + Fore.RESET
        + f": {message.content}"
    )

    if message.content.upper().startswith("CID_"):
        await client.party.me.set_outfit(asset=message.content.upper())
        await message.reply(f"Skin set to: {message.content}")
    elif message.content.upper().startswith("BID_"):
        await client.party.me.set_backpack(asset=message.content.upper())
        await message.reply(f"Backpack set to: {message.content}")
    elif message.content.upper().startswith("EID_"):
        await client.party.me.set_emote(asset=message.content.upper())
        await message.reply(f"Emote set to: {message.content}")
    elif message.content.upper().startswith("PID_"):
        await client.party.me.set_pickaxe(asset=message.content.upper())
        await message.reply(f"Pickaxe set to: {message.content}")
    elif message.content.startswith("Playlist_"):
        try:
            await client.party.set_playlist(playlist=message.content)
            await message.reply(f"Playlist set to: {message.content}")
        except fortnitepy.Forbidden:
            await message.reply(
                f"I can not set gamemode because I am not party leader."
            )
    elif message.content.lower().startswith("prefix"):
        await message.reply(f"Current prefix: !")


@client.event
async def event_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"")
    elif isinstance(error, IndexError):
        pass
    elif isinstance(error, fortnitepy.HTTPException):
        pass
    elif isinstance(error, commands.CheckFailure):
        await ctx.send("")
    elif isinstance(error, TimeoutError):
        await ctx.send("You took too long to respond!")
    else:
        print(error)

@client.command()
async def ghostleaks(ctx):
    await ctx.send('With GhostFN you can easly create your own lobby bot in less than 5 minutes!')
    
     
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
#Gold-style
    
@client.command()
async def goldcat(ctx):
    variants = client.party.me.create_variants(progressive=4)

    await client.party.me.set_outfit(
        asset='CID_693_Athena_Commando_M_BuffCat',
        variants=variants,
        enlightenment=(2, 350)
    )

    await ctx.send('Skin set to: Golden cat')
    
@client.command()
async def goldtnt(ctx):
    variants = client.party.me.create_variants(progressive=8)

    await client.party.me.set_outfit(
        asset='CID_691_Athena_Commando_F_TNTina',
        variants=variants,
        enlightenment=(2, 350)
    )

    await ctx.send('Skin set to: Golden Tntina')
    
@client.command()
async def goldpeely(ctx):
    variants = client.party.me.create_variants(progressive=4)

    await client.party.me.set_outfit(
        asset='CID_701_Athena_Commando_M_BananaAgent',
        variants=variants,
        enlightenment=(2, 350)
    )

    await ctx.send('Skin set to: Golden Peely')
@client.command()
async def dab(ctx, *, content=None):
    await client.party.me.set_emote(asset="eid_dab")
    
    
    
    
@client.command()
async def sit(ctx, *, content=None):
    await client.party.me.set_emote(asset="eid_sitpapayacomms")
    
    

@client.command()
async def goldskye(ctx):
    variants = client.party.me.create_variants(progressive=4)

    await client.party.me.set_outfit(
        asset='CID_690_Athena_Commando_F_Photographer',
        variants=variants,
        enlightenment=(2, 350)
    )

    await ctx.send('Skin set to: Golden Skye')
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
#GOLD SEASON 14 style-skin

    
@client.command()
async def thor2(ctx):
    variants = client.party.me.create_variants(progressive=2)

    await client.party.me.set_outfit(
        asset='CID_845_Athena_Commando_M_HightowerTapas',
        variants=variants,
        enlightenment=(2, 350)
    )

    await ctx.send('Skin set to: lightning thor')
    
    
    
    
    
    
    
    
    
    
    
    
    
#style-skin
@client.command()
async def pinkghoul(ctx):
    variants = client.party.me.create_variants(material=3)

    await client.party.me.set_outfit(
        asset='CID_029_Athena_Commando_F_Halloween',
        variants=variants
    )

    await ctx.send('Skin set to: Pink ghoul')
    await ctx.send('To get your OWN Lobby Bot: \n1) Join our Discord at: https://discord.gg/rAd9YnHjV3 \n2)YouTube: Ghost Leaks\n3) TikTok: Ghost_Leaks\n4) Instagram: ghost__leaks\nMade with GhostFN!')
@client.command()
async def purpleskull(ctx):
    variants = client.party.me.create_variants(clothing_color=1)

    await client.party.me.set_outfit(
        asset='CID_030_Athena_Commando_M_Halloween',
        variants=variants
    )

    await ctx.send('Skin set to: purple skull')
    await ctx.send('To get your OWN Lobby Bot: \n1) Join our Discord at: https://discord.gg/rAd9YnHjV3 \n2)YouTube: Ghost Leaks\n3) TikTok: Ghost_Leaks\n4) Instagram: ghost__leaks\nMade with GhostFN!')
    
@client.command()
async def renegade2(ctx):
    variants = client.party.me.create_variants(material=2)

    await client.party.me.set_outfit(
        asset='CID_028_Athena_Commando_F',
        variants=variants
    )

    await ctx.send('Skin set to: Checkered Renegade')
    await ctx.send('To get your OWN Lobby Bot: \n1) Join our Discord at: https://discord.gg/rAd9YnHjV3 \n2)YouTube: Ghost Leaks\n3) TikTok: Ghost_Leaks\n4) Instagram: ghost__leaks\nMade with GhostFN!')    
    
    
    
    
    
    
@client.command()
async def magic(ctx: fortnitepy.ext.commands.Context):
    await client.party.me.set_emote(asset="EID_Wizard")
    await asyncio.sleep(2.00)
    await client.party.me.set_outfit("CID_Invisible") 
    await ctx.send('Poof, magic treack!')   
    
    
    
    
    
    
    
    
    
    
    
# customize command

@client.command()
async def defaults(ctx):
    await ctx.send(f"old defaults..")
    await client.party.me.set_outfit(asset="cid_001_athena_commando_f_default")
    await asyncio.sleep(1.25)
    await client.party.me.set_outfit(asset="cid_002_athena_commando_f_default")
    await asyncio.sleep(1.25)
    await client.party.me.set_outfit(asset="cid_003_athena_commando_f_default")
    await asyncio.sleep(1.25)
    await client.party.me.set_outfit(asset="cid_004_athena_commando_f_default")
    await asyncio.sleep(1.25)
    await client.party.me.set_outfit(asset="cid_005_athena_commando_m_default")
    await asyncio.sleep(1.25)
    await client.party.me.set_outfit(asset="cid_006_athena_commando_m_default")
    await asyncio.sleep(1.25)
    await client.party.me.set_outfit(asset="cid_007_athena_commando_m_default")
    await asyncio.sleep(1.25)
    await client.party.me.set_outfit(asset="cid_008_athena_commando_m_default")
    await asyncio.sleep(2.25)
    await ctx.send(f"Chapter 2!!")
    await client.party.me.set_outfit(asset="cid_556_athena_commando_f_rebirthdefaulta")
    await asyncio.sleep(1.25)
    await client.party.me.set_outfit(asset="cid_557_athena_commando_f_rebirthdefaultb")
    await asyncio.sleep(1.25)
    await client.party.me.set_outfit(asset="cid_558_athena_commando_f_rebirthdefaultc")
    await asyncio.sleep(1.25)
    await client.party.me.set_outfit(asset="cid_559_athena_commando_f_rebirthdefaultd")
    await asyncio.sleep(1.25)
    await client.party.me.set_outfit(asset="cid_560_athena_commando_m_rebirthdefaulta")
    await asyncio.sleep(1.25)
    await client.party.me.set_outfit(asset="cid_561_athena_commando_m_rebirthdefaultb")
    await asyncio.sleep(1.25)
    await client.party.me.set_outfit(asset="cid_562_athena_commando_m_rebirthdefaultc")
    await asyncio.sleep(1.25)
    await client.party.me.set_outfit(asset="cid_563_athena_commando_m_rebirthdefaultd")
    await asyncio.sleep(1.25)

    await ctx.send(
        f"There was all defaults! "
    )
    await ctx.send('To get your OWN Lobby Bot: \n1) Join our Discord at: https://discord.gg/rAd9YnHjV3 \n2)YouTube: Ghost Leaks\n3) TikTok: Ghost_Leaks\n4) Instagram: ghost__leaks\nMade with GhostFN!')
@client.command()
async def exclusive(ctx):
      await ctx.send(f"Exclusive skins..")
      await client.party.me.set_outfit(asset="CID_114_Athena_Commando_F_TacticalWoodland")
      await asyncio.sleep(2)
      await client.party.me.set_emote(asset="EID_HipHop01")
      await asyncio.sleep(7)
      await client.party.me.set_outfit(asset="CID_174_Athena_Commando_F_CarbideWhite")
      await asyncio.sleep(2)
      await client.party.me.set_emote(asset="EID_LookAtThis")
      await asyncio.sleep(7)
      await client.party.me.set_outfit(asset="CID_175_Athena_Commando_M_Celestial")
      await asyncio.sleep(2)
      await client.party.me.set_emote(asset="EID_HandsUp")
      await asyncio.sleep(7)
      await client.party.me.set_outfit(asset="CID_183_Athena_Commando_M_ModernMilitaryRed")
      await asyncio.sleep(2)
      await client.party.me.set_emote(asset="EID_TwistDaytona")
      await asyncio.sleep(7)
      await client.party.me.set_outfit(asset="CID_342_Athena_Commando_M_StreetRacerMetallic")
      await asyncio.sleep(2)
      await client.party.me.set_emote(asset="EID_JanuaryBop")
      await asyncio.sleep(7)
      await client.party.me.set_outfit(asset="CID_313_Athena_Commando_M_KpopFashion")
      await asyncio.sleep(2)
      await client.party.me.set_emote(asset="EID_Kpopdance03")
      await asyncio.sleep(7)
      await client.party.me.set_outfit(asset="CID_386_Athena_Commando_M_StreetOpsStealth")
      await asyncio.sleep(2)
      await client.party.me.set_emote(asset="EID_Bollywood")
      await asyncio.sleep(7)
      await client.party.me.set_outfit(asset="CID_434_Athena_Commando_F_StealthHonor")
      await asyncio.sleep(2)
      await client.party.me.set_emote(asset="EID_MathDance")
      await asyncio.sleep(7)
      await ctx.send(f"To get your OWN Lobby Bot: \n1) Join our Discord at: https://discord.gg/rAd9YnHjV3 \n2)YouTube: Ghost Leaks\n3) TikTok: Ghost_Leaks\n4) Instagram: ghost__leaks\nMade with GhostFN!")
      await client.party.me.set_outfit(asset="CID_371_Athena_Commando_M_SpeedyMidnight")
      await asyncio.sleep(2)
      await client.party.me.set_emote(asset="EID_LasagnaDance")
      await asyncio.sleep(7)
      await client.party.me.set_outfit(asset="CID_479_Athena_Commando_F_Davinci")
      await asyncio.sleep(2)
      await client.party.me.set_emote(asset="EID_Davinci")
      await asyncio.sleep(7)
      await client.party.me.set_outfit(asset="CID_516_Athena_Commando_M_BlackWidowRogue")
      await asyncio.sleep(2)
      await client.party.me.set_emote(asset="EID_TorchSnuffer")
      await asyncio.sleep(7)
      await client.party.me.set_outfit(asset="CID_757_Athena_Commando_F_WildCat")
      await asyncio.sleep(2)
      await client.party.me.set_emote(asset="EID_Saxophone")
      await asyncio.sleep(7)
      await client.party.me.set_outfit(asset="CID_441_Athena_Commando_F_CyberScavengerBlue")
      await asyncio.sleep(2)
      await client.party.me.set_emote(asset="EID_Sprinkler")
      await asyncio.sleep(7)
      await client.party.me.set_outfit(asset="CID_113_Athena_Commando_M_BlueAce")
      await asyncio.sleep(2)
      await client.party.me.set_emote(asset="EID_PopLock")
      await asyncio.sleep(7)
      await client.party.me.set_outfit(asset="CID_052_Athena_Commando_F_PSBlue")
      await asyncio.sleep(2)
      await client.party.me.set_emote(asset="EID_HotStuff")
      await asyncio.sleep(7)
      await client.party.me.set_outfit(asset="CID_360_Athena_Commando_M_TechOpsBlue")
      await asyncio.sleep(2)
      await client.party.me.set_emote(asset="EID_Dab")
      await asyncio.sleep(7)

      await ctx.send(
        f"There was all exclusive!"
    ) 
      await ctx.send('To get your OWN Lobby Bot: \n1) Join our Discord at: https://discord.gg/rAd9YnHjV3 \n2)YouTube: Ghost Leaks\n3) TikTok: Ghost_Leaks\n4) Instagram: ghost__leaks\nMade with GhostFN!')

@client.command()
async def s2(ctx):
      await ctx.send(f"S2 pass..")
      await client.party.me.set_outfit(asset="CID_032_Athena_Commando_M_Medieval")
      await asyncio.sleep(2)
      await client.party.me.set_emote(asset="EID_Wave")
      await asyncio.sleep(5)
      await client.party.me.set_outfit(asset="CID_033_Athena_Commando_F_Medieval")
      await asyncio.sleep(2)
      await client.party.me.set_emote(asset="EID_DanceMoves")
      await asyncio.sleep(5)
      await client.party.me.set_outfit(asset="CID_039_Athena_Commando_F_Disco")
      await asyncio.sleep(2)
      await client.party.me.set_emote(asset="EID_RideThePonyTwo")
      await asyncio.sleep(5)
      await client.party.me.set_outfit(asset="CID_035_Athena_Commando_M_Medieval")
      await asyncio.sleep(2)
      await client.party.me.set_emote(asset="EID_Floss")
      await asyncio.sleep(5)
      await ctx.send(f"To get your OWN Lobby Bot: \n1) Join our Discord at: https://discord.gg/rAd9YnHjV3 \n2)YouTube: Ghost Leaks\n3) TikTok: Ghost_Leaks\n4) Instagram: ghost__leaks\nMade with GhostFN!")
      await client.party.me.set_emote(asset="EID_Dab")
      await ctx.send(
        f"S2 reel"
      )

@client.command()
async def s1(ctx):
      await ctx.send(f"S1 pass..")
      await client.party.me.set_outfit(asset="CID_017_Athena_Commando_M")
      await asyncio.sleep(2)
      await client.party.me.set_emote(asset="EID_Dab")
      await asyncio.sleep(5)
      await client.party.me.set_outfit(asset="CID_022_Athena_Commando_F")
      await asyncio.sleep(2)
      await client.party.me.set_emote(asset="EID_Fresh")
      await asyncio.sleep(5)
      await client.party.me.set_outfit(asset="CID_029_Athena_Commando_F_Halloween")
      await asyncio.sleep(2)
      await client.party.me.set_emote(asset="EID_FingerGuns")
      await asyncio.sleep(5)
      await client.party.me.set_outfit(asset="CID_030_Athena_Commando_M_Halloween")
      await asyncio.sleep(2)
      await client.party.me.set_emote(asset="")
      await asyncio.sleep(5)
      await client.party.me.set_outfit(asset="CID_028_Athena_Commando_F")
      await asyncio.sleep(2)
      await client.party.me.set_emote(asset="EID_ElectroShuffle")
      await asyncio.sleep(5)
      await ctx.send(f"To get your OWN Lobby Bot: \n1) Join our Discord at: https://discord.gg/rAd9YnHjV3 \n2)YouTube: Ghost Leaks\n3) TikTok: Ghost_Leaks\n4) Instagram: ghost__leaks\nMade with GhostFN!")
      await client.party.me.set_emote(asset="EID_Dab")
      await ctx.send(
        f"S1 reel"
      )        

@client.command()
async def s3(ctx):
      await ctx.send(f"S3 pass..")
      await client.party.me.set_outfit(asset="CID_080_Athena_Commando_M_Space")
      await asyncio.sleep(2)
      await client.party.me.set_emote(asset="")
      await asyncio.sleep(5)
      await client.party.me.set_outfit(asset="CID_081_Athena_Commando_F_Space")
      await asyncio.sleep(2)
      await client.party.me.set_emote(asset="EID_BestMates")
      await asyncio.sleep(5)
      await client.party.me.set_outfit(asset="CID_082_Athena_Commando_M_Scavenger")
      await asyncio.sleep(2)
      await client.party.me.set_emote(asset="")
      await asyncio.sleep(5)
      await client.party.me.set_outfit(asset="CID_088_Athena_Commando_M_SpaceBlack")
      await asyncio.sleep(2)
      await client.party.me.set_emote(asset="")
      await asyncio.sleep(5)
      await client.party.me.set_outfit(asset="CID_083_Athena_Commando_F_Tactical")
      await asyncio.sleep(2)
      await client.party.me.set_emote(asset="EID_Robot")
      await asyncio.sleep(5)
      await client.party.me.set_outfit(asset="CID_084_Athena_Commando_M_Assassin")
      await asyncio.sleep(2)
      await client.party.me.set_emote(asset="EID_TakeTheL")
      await asyncio.sleep(5)
      await ctx.send(f"To get your OWN Lobby Bot: \n1) Join our Discord at: https://discord.gg/rAd9YnHjV3 \n2)YouTube: Ghost Leaks\n3) TikTok: Ghost_Leaks\n4) Instagram: ghost__leaks\nMade with GhostFN!")
      await client.party.me.set_emote(asset="EID_Dab")
      await ctx.send(
        f"S3 reel"
      )  

@client.command()
async def s4(ctx):
      await ctx.send(f"S4 pass..")
      await client.party.me.set_outfit(asset="CID_115_Athena_Commando_M_CarbideBlue")
      await asyncio.sleep(2)
      await client.party.me.set_emote(asset="EID_KungFuSalute")
      await asyncio.sleep(5)
      await client.party.me.set_outfit(asset="CID_117_Athena_Commando_M_TacticalJungle")
      await asyncio.sleep(2)
      await client.party.me.set_emote(asset="EID_Hype")
      await asyncio.sleep(5)
      await client.party.me.set_outfit(asset="CID_118_Athena_Commando_F_Valor")
      await asyncio.sleep(2)
      await client.party.me.set_emote(asset="")
      await asyncio.sleep(5)
      await client.party.me.set_outfit(asset="CID_120_Athena_Commando_F_Graffiti")
      await asyncio.sleep(2)
      await client.party.me.set_emote(asset="EID_GoodVibes")
      await asyncio.sleep(5)
      await client.party.me.set_outfit(asset="CID_125_Athena_Commando_M_TacticalWoodland")
      await asyncio.sleep(2)
      await client.party.me.set_emote(asset="")
      await asyncio.sleep(5)
      await client.party.me.set_outfit(asset="CID_119_Athena_Commando_F_Candy")
      await asyncio.sleep(2)
      await client.party.me.set_emote(asset="EID_GrooveJam")
      await asyncio.sleep(5)
      await asyncio.sleep(5)
      await client.party.me.set_outfit(asset="CID_116_Athena_Commando_M_CarbideBlack")
      await asyncio.sleep(2)
      await client.party.me.set_emote(asset="")
      await asyncio.sleep(5)
      await asyncio.sleep(5)
      await client.party.me.set_outfit(asset="CID_140_Athena_Commando_M_Visitor")
      await asyncio.sleep(2)
      await client.party.me.set_emote(asset="EID_Popcorn")
      await asyncio.sleep(5)
      await ctx.send(f"To get your OWN Lobby Bot: \n1) Join our Discord at: https://discord.gg/rAd9YnHjV3 \n2)YouTube: Ghost Leaks\n3) TikTok: Ghost_Leaks\n4) Instagram: ghost__leaks\nMade with GhostFN!")
      await client.party.me.set_emote(asset="EID_Dab")
      await ctx.send(
        f"S4 reel"
      )

@client.command()
async def s5(ctx):
      await ctx.send(f"S5 pass..")
      await client.party.me.set_outfit(asset="CID_161_Athena_Commando_M_Drift")
      await asyncio.sleep(2)
      await client.party.me.set_emote(asset="EID_YoureAwesome")
      await asyncio.sleep(5)
      await client.party.me.set_outfit(asset="CID_163_Athena_Commando_F_Viking")
      await asyncio.sleep(2)
      await client.party.me.set_emote(asset="")
      await asyncio.sleep(5)
      await client.party.me.set_outfit(asset="CID_162_Athena_Commando_F_StreetRacer")
      await asyncio.sleep(2)
      await client.party.me.set_emote(asset="")
      await asyncio.sleep(5)
      await client.party.me.set_outfit(asset="CID_166_Athena_Commando_F_Lifeguard")
      await asyncio.sleep(2)
      await client.party.me.set_emote(asset="EID_HipHopS5")
      await asyncio.sleep(5)
      await client.party.me.set_outfit(asset="CID_167_Athena_Commando_M_TacticalBadass")
      await asyncio.sleep(2)
      await client.party.me.set_emote(asset="")
      await asyncio.sleep(5)
      await client.party.me.set_outfit(asset="CID_173_Athena_Commando_F_StarfishUniform")
      await asyncio.sleep(2)
      await client.party.me.set_emote(asset="")
      await asyncio.sleep(5)
      await asyncio.sleep(5)
      await client.party.me.set_outfit(asset="CID_165_Athena_Commando_M_DarkViking")
      await asyncio.sleep(2)
      await client.party.me.set_emote(asset="EID_SwipeIt")
      await asyncio.sleep(5)
      await asyncio.sleep(5)
      await client.party.me.set_outfit(asset="CID_200_Athena_Commando_M_DarkPaintballer")
      await asyncio.sleep(2)
      await client.party.me.set_emote(asset="EID_StageBow")
      await asyncio.sleep(5)
      await ctx.send(f"To get your OWN Lobby Bot: \n1) Join our Discord at: https://discord.gg/rAd9YnHjV3 \n2)YouTube: Ghost Leaks\n3) TikTok: Ghost_Leaks\n4) Instagram: ghost__leaks\nMade with GhostFN!")
      await client.party.me.set_emote(asset="EID_Dab")
      await ctx.send(
        f"S5 reel"
      )

@client.command()
async def s6(ctx):
      await ctx.send(f"S6 pass..")
      await client.party.me.set_outfit(asset="CID_233_Athena_Commando_M_FortniteDJ")
      await asyncio.sleep(2)
      await client.party.me.set_emote(asset="EID_Octopus")
      await asyncio.sleep(5)
      await client.party.me.set_outfit(asset="CID_237_Athena_Commando_F_Cowgirl")
      await asyncio.sleep(2)
      await client.party.me.set_emote(asset="EID_RunningMan")
      await asyncio.sleep(5)
      await client.party.me.set_outfit(asset="CID_234_Athena_Commando_M_LlamaRider")
      await asyncio.sleep(2)
      await client.party.me.set_emote(asset="")
      await asyncio.sleep(5)
      await client.party.me.set_outfit(asset="CID_231_Athena_Commando_F_RedRiding")
      await asyncio.sleep(2)
      await client.party.me.set_emote(asset="EID_NeedToGo")
      await asyncio.sleep(5)
      await client.party.me.set_outfit(asset="CID_232_Athena_Commando_F_HalloweenTomato")
      await asyncio.sleep(2)
      await client.party.me.set_emote(asset="EID_RegalWave")
      await asyncio.sleep(5)
      await client.party.me.set_outfit(asset="CID_227_Athena_Commando_F_Vampire")
      await asyncio.sleep(2)
      await client.party.me.set_emote(asset="")
      await asyncio.sleep(5)
      await asyncio.sleep(5)
      await client.party.me.set_outfit(asset="CID_230_Athena_Commando_M_Werewolf")
      await asyncio.sleep(2)
      await client.party.me.set_emote(asset="EID_Flamenco")
      await asyncio.sleep(5)
      await asyncio.sleep(5)
      await client.party.me.set_outfit(asset="CID_267_Athena_Commando_M_RobotRed")
      await asyncio.sleep(2)
      await client.party.me.set_emote(asset="")
      await asyncio.sleep(5)
      await ctx.send(f"To get your OWN Lobby Bot: \n1) Join our Discord at: https://discord.gg/rAd9YnHjV3 \n2)YouTube: Ghost Leaks\n3) TikTok: Ghost_Leaks\n4) Instagram: ghost__leaks\nMade with GhostFN!")
      await client.party.me.set_emote(asset="EID_Dab")
      await ctx.send(
        f"S6 reel"
      )      


@client.command()
async def zombie(ctx):
    await client.party.me.set_outfit(asset="cid_589_athena_commando_m_soccerzombiea")
    await client.party.me.set_emote(asset="eid_zombiewalk")
    await asyncio.sleep(2.25)
    await client.party.me.clear_emote()
    await client.party.me.set_outfit(asset="cid_590_athena_commando_m_soccerzombieb")
    await client.party.me.set_emote(asset="eid_zombiewalk")
    await asyncio.sleep(2.25)
    await client.party.me.clear_emote()
    await client.party.me.set_outfit(asset="cid_591_athena_commando_m_soccerzombiec")
    await client.party.me.set_emote(asset="eid_zombiewalk")
    await asyncio.sleep(2.25)
    await client.party.me.clear_emote()
    await client.party.me.set_outfit(asset="cid_592_athena_commando_m_soccerzombied")
    await client.party.me.set_emote(asset="eid_zombiewalk")
    await asyncio.sleep(2.25)
    await client.party.me.clear_emote()
    await client.party.me.set_outfit(asset="cid_593_athena_commando_f_soccerzombiea")
    await client.party.me.set_emote(asset="eid_zombiewalk")
    await asyncio.sleep(2.25)
    await client.party.me.clear_emote()
    await client.party.me.set_outfit(asset="cid_594_athena_commando_f_soccerzombieb")
    await client.party.me.set_emote(asset="eid_zombiewalk")
    await asyncio.sleep(2.25)
    await client.party.me.clear_emote()
    await client.party.me.set_outfit(asset="cid_595_athena_commando_f_soccerzombiec")
    await client.party.me.set_emote(asset="eid_zombiewalk")
    await asyncio.sleep(2.25)
    await client.party.me.clear_emote()
    await client.party.me.set_outfit(asset="cid_596_athena_commando_f_soccerzombied")
    await client.party.me.set_emote(asset="eid_zombiewalk")
    await asyncio.sleep(2.25)
    await client.party.me.clear_emote()
    await ctx.send(
        f"Zombie skins! "
    )
    await ctx.send('To get your OWN Lobby Bot: \n1) Join our Discord at: https://discord.gg/rAd9YnHjV3 \n2)YouTube: Ghost Leaks\n3) TikTok: Ghost_Leaks\n4) Instagram: ghost__leaks\nMade with GhostFN!')
@client.command()
async def soccer(ctx):
    await client.party.me.set_outfit(asset="cid_144_athena_commando_m_soccerdudea")
    await client.party.me.set_emote(asset="eid_soccerjuggling")
    await asyncio.sleep(2.25)
    await client.party.me.clear_emote()
    await client.party.me.set_outfit(asset="cid_145_athena_commando_m_soccerdudeb")
    await client.party.me.set_emote(asset="eid_soccerjuggling")
    await asyncio.sleep(2.25)
    await client.party.me.clear_emote()
    await client.party.me.set_outfit(asset="cid_146_athena_commando_m_soccerdudec")
    await client.party.me.set_emote(asset="eid_soccerjuggling")
    await asyncio.sleep(2.25)
    await client.party.me.clear_emote()
    await client.party.me.set_outfit(asset="cid_147_athena_commando_m_soccerduded")
    await client.party.me.set_emote(asset="eid_soccerjuggling")
    await asyncio.sleep(2.25)
    await client.party.me.clear_emote()
    await client.party.me.set_outfit(asset="cid_148_athena_commando_f_soccergirla")
    await client.party.me.set_emote(asset="eid_soccerjuggling")
    await asyncio.sleep(2.25)
    await client.party.me.clear_emote()
    await client.party.me.set_outfit(asset="cid_149_athena_commando_f_soccergirlb")
    await client.party.me.set_emote(asset="eid_soccerjuggling")
    await asyncio.sleep(2.25)
    await client.party.me.clear_emote()
    await client.party.me.set_outfit(asset="cid_150_athena_commando_f_soccergirlc")
    await client.party.me.set_emote(asset="eid_soccerjuggling")
    await asyncio.sleep(2.25)
    await client.party.me.clear_emote()
    await client.party.me.set_outfit(asset="cid_151_athena_commando_f_soccergirld")
    await client.party.me.set_emote(asset="eid_soccerjuggling")
    await asyncio.sleep(2.25)
    await client.party.me.clear_emote()
    await ctx.send('To get your OWN Lobby Bot: \n1) Join our Discord at: https://discord.gg/rAd9YnHjV3 \n2)YouTube: Ghost Leaks\n3) TikTok: Ghost_Leaks\n4) Instagram: ghost__leaks\nMade with GhostFN!')
 
@client.command()
async def randomize(ctx):
      await ctx.send(f"Starting..")
      await client.party.me.set_outfit(asset="CID_041_Athena_Commando_F_District")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_005_Athena_Commando_M_Default")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_175_Athena_Commando_M_Celestial")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_183_Athena_Commando_M_ModernMilitaryRed")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_028_Athena_Commando_F")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_114_Athena_Commando_F_TacticalWoodland")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_030_Athena_Commando_M_Halloween")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_716_Athena_Commando_M_BlueFlames")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_111_Athena_Commando_F_Robo")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_342_Athena_Commando_M_StreetRacerMetallic")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_172_Athena_Commando_F_SharpDresser")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_219_Athena_Commando_M_Hacivat")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_175_Athena_Commando_M_Celestial")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_222_Athena_Commando_F_DarkViking")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_682_Athena_Commando_M_VirtualShadow")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_783_Athena_Commando_M_AquaJacket")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_174_Athena_Commando_F_CarbideWhite")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_981_Athena_Commando_M_JonesyHoliday")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_233_Athena_Commando_M_FortniteDJ")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_920_Athena_Commando_M_PartyTrooper")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_336_Athena_Commando_M_DragonMask")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_178_Athena_Commando_F_StreetRacerCobra")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_175_Athena_Commando_M_Celestial")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_085_Athena_Commando_M_Twitch")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_071_Athena_Commando_M_Wukong")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_114_Athena_Commando_F_TacticalWoodland")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_017_Athena_Commando_M")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_725_Athena_Commando_F_AgentX")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_183_Athena_Commando_M_ModernMilitaryRed")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_689_Athena_Commando_M_SpyTechHacker")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_079_Athena_Commando_F_Camo")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_916_Athena_Commando_F_FuzzyBearSkull")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_742_Athena_Commando_M_ChocoBunny")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_320_Athena_Commando_M_Nautilus")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_342_Athena_Commando_M_StreetRacerMetallic")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_088_Athena_Commando_M_SpaceBlack")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_913_Athena_Commando_F_York_D")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_175_Athena_Commando_M_Celestial")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_036_Athena_Commando_M_WinterCamo")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_053_Athena_Commando_M_SkiDude")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_576_Athena_Commando_M_CODSquadPlaid")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_174_Athena_Commando_F_CarbideWhite")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_022_Athena_Commando_F")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_051_Athena_Commando_M_HolidayElf")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_605_Athena_Commando_M_TourBus")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_527_Athena_Commando_F_StreetFashionRed")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_340_Athena_Commando_F_RobotTrouble")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_175_Athena_Commando_M_Celestial")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_333_Athena_Commando_M_Squishy")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_253_Athena_Commando_M_MilitaryFashion2")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_162_Athena_Commando_F_StreetRacer")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_760_Athena_Commando_F_NeonTightSuit")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_159_Athena_Commando_M_GumshoeDark")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_313_Athena_Commando_M_KpopFashion")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_342_Athena_Commando_M_StreetRacerMetallic")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_171_Athena_Commando_M_SharpDresser")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_174_Athena_Commando_F_CarbideWhite")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_219_Athena_Commando_M_Hacivat")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_061_Athena_Commando_F_SkiGirl")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_169_Athena_Commando_M_Luchador")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_696_Athena_Commando_F_DarkHeart")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_041_Athena_Commando_F_District")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_005_Athena_Commando_M_Default")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_891_Athena_Commando_M_LunchBox")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_397_Athena_Commando_F_TreasureHunterFashion")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_028_Athena_Commando_F")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_186_Athena_Commando_M_Exercise")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_030_Athena_Commando_M_Halloween")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_764_Athena_Commando_F_Loofah")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_111_Athena_Commando_F_Robo")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_699_Athena_Commando_F_BrokenHeart")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_172_Athena_Commando_F_SharpDresser")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_219_Athena_Commando_M_Hacivat")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_175_Athena_Commando_M_Celestial")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_381_Athena_Commando_F_BaseballKitbash")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_682_Athena_Commando_M_VirtualShadow")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_783_Athena_Commando_M_AquaJacket")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_023_Athena_Commando_F")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_981_Athena_Commando_M_JonesyHoliday")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_416_Athena_Commando_M_AssassinSuit")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_920_Athena_Commando_M_PartyTrooper")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_336_Athena_Commando_M_DragonMask")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_178_Athena_Commando_F_StreetRacerCobra")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_175_Athena_Commando_M_Celestial")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_085_Athena_Commando_M_Twitch")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_071_Athena_Commando_M_Wukong")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_114_Athena_Commando_F_TacticalWoodland")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_703_Athena_Commando_M_Cyclone")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_A_007_Athena_Commando_F_StreetFashionEclipse")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_400_Athena_Commando_M_AshtonSaltLake")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_676_Athena_Commando_M_CODSquadHoodie")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_196_Athena_Commando_M_Biker")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_736_Athena_Commando_F_DonutDish")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_927_Athena_Commando_M_NauticalPajamas")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_410_Athena_Commando_M_CyberScavenger")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_342_Athena_Commando_M_StreetRacerMetallic")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_202_Athena_Commando_F_DesertOps")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_742_Athena_Commando_M_ChocoBunny")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_975_Athena_Commando_F_Cherry_B8XN5")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_036_Athena_Commando_M_WinterCamo")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_053_Athena_Commando_M_SkiDude")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_205_Athena_Commando_F_GarageBand")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_174_Athena_Commando_F_CarbideWhite")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_022_Athena_Commando_F")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_051_Athena_Commando_M_HolidayElf")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_598_Athena_Commando_M_Mastermind")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_218_Athena_Commando_M_GreenBeret")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_340_Athena_Commando_F_RobotTrouble")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_175_Athena_Commando_M_Celestial")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_183_Athena_Commando_M_ModernMilitaryRed")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_253_Athena_Commando_M_MilitaryFashion2")
      await asyncio.sleep(0.13)
      await ctx.send(f"3")
      await client.party.me.set_outfit(asset="CID_223_Athena_Commando_M_Dieselpunk")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_726_Athena_Commando_M_TargetPractice")
      await asyncio.sleep(0.13)
      await ctx.send(f"2")
      await client.party.me.set_outfit(asset="CID_159_Athena_Commando_M_GumshoeDark")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_418_Athena_Commando_F_Geisha")
      await asyncio.sleep(0.13)
      await ctx.send(f"1")
      await client.party.me.set_outfit(asset="CID_675_Athena_Commando_M_TheGoldenSkeleton")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_114_Athena_Commando_F_TacticalWoodland")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_033_Athena_Commando_F_Medieval")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_219_Athena_Commando_M_Hacivat")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_061_Athena_Commando_F_SkiGirl")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_169_Athena_Commando_M_Luchador")
      await asyncio.sleep(0.13)
      await client.party.me.set_outfit(asset="CID_576_Athena_Commando_M_CODSquadPlaid")
      await asyncio.sleep(0.13)

      await ctx.send(
        f"Stopped!"
    ) 
      await ctx.send('To get your OWN Lobby Bot: \n1) Join our Discord at: https://discord.gg/rAd9YnHjV3 \n2)YouTube: Ghost Leaks\n3) TikTok: Ghost_Leaks\n4) Instagram: ghost__leaks\nMade with GhostFN!')

@client.command()
async def ecu(ctx):
    await client.party.me.set_outfit(asset="cid_226_athena_commando_f_octoberfest")
    await client.party.me.set_emote(asset="eid_bollywood")

@client.command()
async def zerotwo(ctx):
    await client.party.me.set_outfit(asset="CID_753_Athena_Commando_F_Hostile")
    await client.party.me.set_backpack(asset="bid_600_CID")
    await client.party.me.set_emote(asset="EID_KpopDance04")
    await ctx.send('ZeroTwo is really an important memory for GhostLeaks and I think his story is an example for everyone...')    

@client.command()
async def fruit(ctx):
    await client.party.me.set_outfit(asset="CID_764_Athena_Commando_F_Loofah")
    await client.party.me.set_backpack(asset="BID_000_CID")
    await client.party.me.set_emote(asset="EID_Loofah")
    

@client.command()
async def nessa(ctx):
    await client.party.me.set_outfit(
        asset='CID_313_Athena_Commando_M_KpopFashion'
    )
    
    await ctx.send("Skin set to: ikonik")
    
@client.command()
async def witch(ctx):
    await client.party.me.set_outfit(
        asset='CID_608_Athena_Commando_F_ModernWitch'
    )
    
    await ctx.send("Skin set to: witch")
    
@client.command()
async def bot(ctx):
    await client.party.me.set_outfit(
        asset='CID_NPC_Athena_Commando_M_HightowerHenchman'
    )
    
    await ctx.send("Skin set to: bot")


# basic commands
@client.command()
async def skin(ctx, *, content = None):
    if content is None:
        await ctx.send(f'No skin was given, try: {prefix}skin (skin name)')
    elif content.upper().startswith('CID_'):
        await client.party.me.set_outfit(asset=content.upper())
        await ctx.send(f'Skin set to: {content}')
    else:
        try:
            cosmetic = await BenBotAsync.get_cosmetic(
                lang="en",
                searchLang="en",
                name=content,
                backendType="AthenaCharacter"
            )
            await client.party.me.set_outfit(asset=cosmetic.id)
            await ctx.send(f'Skin set to: {cosmetic.name}')
        except BenBotAsync.exceptions.NotFound:
            await ctx.send(f'Could not find a skin named: {content}')


@client.command()
async def back(ctx, *, content = None):
    if content is None:
        await ctx.send(f'No backpack was given, try: {prefix}backpack (backpack name)')
    elif content.lower() == 'none':
        await client.party.me.clear_backpack()
        await ctx.send('Backpack set to: None')
    elif content.upper().startswith('BID_'):
        await client.party.me.set_backpack(asset=content.upper())
        await ctx.send(f'Backpack set to: {content}')
    else:
        try:
            cosmetic = await BenBotAsync.get_cosmetic(
                lang="en",
                searchLang="en",
                matchMethod="contains",
                name=content,
                backendType="AthenaBackpack"
            )
            await client.party.me.set_backpack(asset=cosmetic.id)
            await ctx.send(f'Backpack set to: {cosmetic.name}')
        except BenBotAsync.exceptions.NotFound:
            await ctx.send(f'Could not find a backpack named: {content}')


@client.command()
async def emote(ctx, *, content = None):
    if content is None:
        await ctx.send(f'No emote was given, try: {prefix}emote (emote name)')
    elif content.lower() == 'floss':
        await client.party.me.clear_emote()
        await client.party.me.set_emote(asset='EID_Floss')
        await ctx.send(f'Emote set to: Floss')
    elif content.lower() == 'none':
        await client.party.me.clear_emote()
        await ctx.send(f'Emote set to: None')
    elif content.upper().startswith('EID_'):
        await client.party.me.clear_emote()
        await client.party.me.set_emote(asset=content.upper())
        await ctx.send(f'Emote set to: {content}')
    else:
        try:
            cosmetic = await BenBotAsync.get_cosmetic(
                lang="en",
                searchLang="en",
                matchMethod="contains",
                name=content,
                backendType="AthenaDance"
            )
            await client.party.me.clear_emote()
            await client.party.me.set_emote(asset=cosmetic.id)
            await ctx.send(f'Emote set to: {cosmetic.name}')
        except BenBotAsync.exceptions.NotFound:
            await ctx.send(f'Could not find an emote named: {content}')

@client.command()
async def pickaxe(ctx, *, content = None):
    if content is None:
        await ctx.send(f'No pickaxe was given, try: {prefix}pickaxe (pickaxe name)')
    elif content.upper().startswith('Pickaxe_'):
        await client.party.me.set_pickaxe(asset=content.upper())
        await ctx.send(f'Pickaxe set to: {content}')
    else:
        try:
            cosmetic = await BenBotAsync.get_cosmetic(
                lang="en",
                searchLang="en",
                matchMethod="contains",
                name=content,
                backendType="AthenaPickaxe"
            )
            await client.party.me.set_pickaxe(asset=cosmetic.id)
            await ctx.send(f'Pickaxe set to: {cosmetic.name}')
        except BenBotAsync.exceptions.NotFound:
            await ctx.send(f'Could not find a pickaxe named: {content}')


@client.command()
async def pet(ctx, *, content = None):
    if content is None:
        await ctx.send(f'No pet was given, try: {prefix}pet (pet name)')
    elif content.lower() == 'none':
        await client.party.me.clear_pet()
        await ctx.send('Pet set to: None')
    else:
        try:
            cosmetic = await BenBotAsync.get_cosmetic(
                lang="en",
                searchLang="en",
                matchMethod="contains",
                name=content,
                backendType="AthenaPet"
            )
            await client.party.me.set_pet(asset=cosmetic.id)
            await ctx.send(f'Pet set to: {cosmetic.name}')
        except BenBotAsync.exceptions.NotFound:
            await ctx.send(f'Could not find a pet named: {content}')

@client.command()
@is_admin()
async def members(ctx: fortnitepy.ext.commands.Context):
    pmembers = client.party.members
    partyMembers = []
    
    for m in pmembers:
        member = client.get_user(m)
        partyMembers.append(member.display_name)
    
    await ctx.send(f"There are {len(partyMembers)} members in {client.user.display_name}'s party:")
    for x in partyMembers:
        if x is not None:
            await ctx.send(x)


@client.command()
async def emoji(ctx, *, content = None):
    if content is None:
        await ctx.send(f'No emoji was given, try: {prefix}emoji (emoji name)')
    try:
        cosmetic = await BenBotAsync.get_cosmetic(
            lang="en",
            searchLang="en",
            matchMethod="contains",
            name=content,
            backendType="AthenaEmoji"
        )
        await client.party.me.clear_emoji()
        await client.party.me.set_emoji(asset=cosmetic.id)
        await ctx.send(f'Emoji set to: {cosmetic.name}')
    except BenBotAsync.exceptions.NotFound:
        await ctx.send(f'Could not find an emoji named: {content}')

    

@client.command()
async def current(ctx, setting = None):
    if setting is None:
        await ctx.send(f"Missing argument. Try: {prefix}current (skin, back, emote, pickaxe, banner)")
    elif setting.lower() == 'banner':
        await ctx.send(f'Banner ID: {client.party.me.banner[0]}  -  Banner Color ID: {client.party.me.banner[1]}')
    else:
        try:
            if setting.lower() == 'skin':
                    cosmetic = await BenBotAsync.get_cosmetic_from_id(
                        cosmetic_id=client.party.me.outfit
                    )

            elif setting.lower() == 'backpack':
                    cosmetic = await BenBotAsync.get_cosmetic_from_id(
                        cosmetic_id=client.party.me.backpack
                    )

            elif setting.lower() == 'emote':
                    cosmetic = await BenBotAsync.get_cosmetic_from_id(
                        cosmetic_id=client.party.me.emote
                    )

            elif setting.lower() == 'pickaxe':
                    cosmetic = await BenBotAsync.get_cosmetic_from_id(
                        cosmetic_id=client.party.me.pickaxe
                    )

            await ctx.send(f"My current {setting} is: {cosmetic.name}")
        except BenBotAsync.exceptions.NotFound:
            await ctx.send(f"I couldn't find a {setting} name for that.")


@client.command()
async def gift(ctx):
    await client.party.me.set_emote(asset="EID_nevergonna")

    await ctx.send(f"What did you think would happen?")
    await asyncio.sleep(10)
    await client.party.me.clear_emote()


@client.command()
async def recruit(ctx):
    await client.party.me.set_outfit(
        asset='CID_001_Athena_Commando_F_Default'
    )

@client.command()
async def marvel(ctx):
    await ctx.send(f"All marvel skins with emotes !")
    await ctx.send(f"Thor !")
    await client.party.me.set_backpack(asset="bid_600_hightowertapas")
    await client.party.me.set_outfit(asset="cid_845_athena_commando_m_hightowertapas")
    await client.party.me.set_emote(asset="eid_hightowertapas")
    await asyncio.sleep(3.25)
    await ctx.send(f"She-Hulk !")
    await client.party.me.set_backpack(asset="bid_594_hightowerhoneydew")
    await client.party.me.set_outfit(
        asset="cid_842_athena_commando_f_hightowerhoneydew"
    )
    await client.party.me.set_emote(asset="eid_hightowerhoneydew")
    await asyncio.sleep(3.25)
    await ctx.send(f"Groot !")
    await client.party.me.set_backpack(asset="bid_598_hightowergrape")
    await client.party.me.set_outfit(asset="cid_840_athena_commando_m_hightowergrape")
    await client.party.me.set_emote(asset="eid_hightowergrape")
    await asyncio.sleep(3.25)
    await ctx.send(f"Storm !")
    await client.party.me.set_outfit(asset="cid_839_athena_commando_f_hightowersquash")
    await client.party.me.set_emote(asset="eid_hightowersquash")
    await asyncio.sleep(3.25)
    await ctx.send(f"Doctor Doom !")
    await client.party.me.set_backpack(asset="bid_599_hightowerdate")
    await client.party.me.set_outfit(asset="cid_846_athena_commando_m_hightowerdate")
    await client.party.me.set_emote(asset="eid_hightowerdate")
    await asyncio.sleep(5.25)
    await ctx.send(f"Mystique !")
    await client.party.me.set_backpack(asset="bid_595_hightowermango")
    await client.party.me.set_outfit(asset="cid_844_athena_commando_f_hightowermango")
    await client.party.me.set_emote(asset="eid_hightowermango")
    await asyncio.sleep(2.25)
    await ctx.send(f"Ironman !")
    await client.party.me.set_backpack(asset="bid_596_hightowertomato")
    await client.party.me.set_outfit(
        asset="cid_843_athena_commando_m_hightowertomato_casual"
    )
    await client.party.me.set_emote(asset="eid_hightowertomato")
    await asyncio.sleep(4.25)
    await ctx.send(f"Wolverine !")
    await client.party.me.set_backpack(asset="bid_597_hightowerwasabi")
    await client.party.me.set_outfit(asset="cid_841_athena_commando_m_hightowerwasabi")
    await client.party.me.set_emote(asset="eid_hightowerwasabi")
    await asyncio.sleep(4.25)
    await ctx.send(f"Silver Surfer !")
    await client.party.me.set_backpack(asset="bid_605_soy_y0dw7")
    await client.party.me.set_skin(asset="cid_847_athena_commando_m_soy_2as3cg")
    await ctx.send(
        f"All the marvel skins! "
    )
    await ctx.send('To get your OWN Lobby Bot: \n1) Join our Discord at: https://discord.gg/rAd9YnHjV3 \n2)YouTube: Ghost Leaks\n3) TikTok: Ghost_Leaks\n4) Instagram: ghost__leaks\nMade with GhostFN!')
@client.command()
async def name(ctx, *, content=None):
    if content is None:
        await ctx.send(f'No ID was given, try: {prefix}name (cosmetic ID)')
    else:
        try:
            cosmetic = await BenBotAsync.get_cosmetic_from_id(
                cosmetic_id=content
            )
            await ctx.send(f'The name for that ID is: {cosmetic.name}')
            print(f' [+] The name for {cosmetic.id} is: {cosmetic.name}')
        except BenBotAsync.exceptions.NotFound:
            await ctx.send(f'Could not find a cosmetic name for ID: {content}')



@client.command()
async def cid(ctx, *, content = None):
    if content is None:
        await ctx.send(f'No skin was given, try: {prefix}cid (skin name)')
    else:
        try:
            cosmetic = await BenBotAsync.get_cosmetic(
                lang="en",
                searchLang="en",
                matchMethod="contains",
                name=content,
                backendType="AthenaCharacter"
            )
            await ctx.send(f'The CID for {cosmetic.name} is: {cosmetic.id}')
            print(f' [+] The CID for {cosmetic.name} is: {cosmetic.id}')
        except BenBotAsync.exceptions.NotFound:
            await ctx.send(f'Could not find a skin named: {content}')
        

@client.command()
async def bid(ctx, *, content):
    if content is None:
        await ctx.send(f'No backpack was given, try: {prefix}bid (backpack name)')
    else:
        try:
            cosmetic = await BenBotAsync.get_cosmetic(
                lang="en",
                searchLang="en",
                matchMethod="contains",
                name=content,
                backendType="AthenaBackpack"
            )
            await ctx.send(f'The BID for {cosmetic.name} is: {cosmetic.id}')
            print(f' [+] The BID for {cosmetic.name} is: {cosmetic.id}')
        except BenBotAsync.exceptions.NotFound:
            await ctx.send(f'Could not find a backpack named: {content}')



@client.command()
async def eid(ctx, *, content):
    if content is None:
        await ctx.send(f'No emote was given, try: {prefix}eid (emote name)')
    elif content.lower() == 'floss':
        await ctx.send(f'The EID for Floss is: EID_Floss')
    else:
        try:
            cosmetic = await BenBotAsync.get_cosmetic(
                lang="en",
                searchLang="en",
                matchMethod="contains",
                name=content,
                backendType="AthenaDance"
            )
            await ctx.send(f'The EID for {cosmetic.name} is: {cosmetic.id}')
            print(f' [+] The EID for {cosmetic.name} is: {cosmetic.id}')
        except BenBotAsync.exceptions.NotFound:
            await ctx.send(f'Could not find an emote named: {content}')



@client.command()
async def pid(ctx, *, content):
    if content is None:
        await ctx.send(f'No pickaxe was given, try: {prefix}pid (pickaxe name)')
    else:
        try:
            cosmetic = await BenBotAsync.get_cosmetic(
                lang="en",
                searchLang="en",
                matchMethod="contains",
                name=content,
                backendType="AthenaPickaxe"
            )
            await ctx.send(f'The PID for {cosmetic.name} is: {cosmetic.id}')
            print(f' [+] The PID for {cosmetic.name} is: {cosmetic.id}')
        except BenBotAsync.exceptions.NotFound:
            await ctx.send(f'Could not find a pickaxe named: {content}')



@client.command()
async def random(ctx, content = None):

    skins = await BenBotAsync.get_cosmetics(
        lang="en",
        backendType="AthenaCharacter"
    )

    skin = rand.choice(skins)

    backpacks = await BenBotAsync.get_cosmetics(
        lang="en",
        backendType="AthenaBackpack"
    )

    backpack = rand.choice(backpacks)

    emotes = await BenBotAsync.get_cosmetics(
        lang="en",
        backendType="AthenaDance"
    )

    emote = rand.choice(emotes)

    pickaxes = await BenBotAsync.get_cosmetics(
        lang="en",
        backendType="AthenaPickaxe"
    )

    pickaxe = rand.choice(pickaxes)

    
    if content is None:
        me = client.party.me
        await me.set_outfit(asset=skin.id)
        await me.set_backpack(asset=backpack.id)
        await me.set_pickaxe(asset=pickaxe.id)

        await ctx.send(f'Loadout randomly set to: {skin.name}, {backpack.name}, {pickaxe.name}')
    else:
        if content.lower() == 'skin':
            await client.party.me.set_outfit(asset=skin.id)
            await ctx.send(f'Skin randomly set to: {skin.name}')

        elif content.lower() == 'backpack':
            await client.party.me.set_backpack(asset=backpack.id)
            await ctx.send(f'Backpack randomly set to: {backpack.name}')

        elif content.lower() == 'emote':
            await client.party.me.set_emote(asset=emote.id)
            await ctx.send(f'Emote randomly set to: {emote.name}')

        elif content.lower() == 'pickaxe':
            await client.party.me.set_pickaxe(asset=pickaxe.id)
            await ctx.send(f'Pickaxe randomly set to: {pickaxe.name}')

        else:
            await ctx.send(f"I don't know that, try: {prefix}random (skin, backpack, emote, pickaxe - og, exclusive, unreleased")

@client.command()
async def hide(ctx, *, user=None):
    if client.party.me.leader:
        if user != "all":
            try:
                if user is None:
                    user = await client.fetch_profile(ctx.message.author.id)
                    member = client.party.members.get(user.id)
                else:
                    user = await client.fetch_profile(user)
                    member = client.party.members.get(user.id)

                raw_squad_assignments = client.party.meta.get_prop(
                    "Default:RawSquadAssignments_j"
                )["RawSquadAssignments"]

                for m in raw_squad_assignments:
                    if m["memberId"] == member.id:
                        raw_squad_assignments.remove(m)

                await set_and_update_party_prop(
                    "Default:RawSquadAssignments_j",
                    {"RawSquadAssignments": raw_squad_assignments},
                )

                await ctx.send(f"Hid {member.display_name}")
            except AttributeError:
                await ctx.send("Can't find that user.")
            except fortnitepy.HTTPException:
                await ctx.send("I am not party leader.")
        else:
            try:
                await set_and_update_party_prop(
                    "Default:RawSquadAssignments_j",
                    {
                        "RawSquadAssignments": [
                            {"memberId": client.user.id, "absoluteMemberIdx": 1}
                        ]
                    },
                )

                await ctx.send("Hid everyone in the party.")
            except fortnitepy.HTTPException:
                await ctx.send("I am not party leader.")
    else:
        await ctx.send("I need party leader to do this!")

@client.command()
async def privacy(ctx, setting = None):
    if setting is not None:
        try:
            if setting.lower() == 'public':
                await client.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                await ctx.send(f"Party Privacy set to: Public")
            elif setting.lower() == 'friends':
                await client.party.set_privacy(fortnitepy.PartyPrivacy.FRIENDS)
                await ctx.send(f"Party Privacy set to: Friends Only")
            elif setting.lower() == 'private':
                await client.party.set_privacy(fortnitepy.PartyPrivacy.PRIVATE)
                await ctx.send(f"Party Privacy set to: Private")
            else:
                await ctx.send("That is not a valid privacy setting. Try: Public, Friends, or Private")
        except fortnitepy.Forbidden:
            await ctx.send("I can not set the party privacy because I am not party leader.")
    else:
        await ctx.send(f"No privacy setting was given. Try: {prefix}privacy (Public, Friends, Private)")

@client.command()
async def invite(ctx, *, member = None):
    if member == 'all':
        friends = client.friends
        invited = []

        try:
            for f in friends:
                friend = client.get_friend(f)

                if friend.is_online():
                    invited.append(friend.display_name)
                    await friend.invite()
            
            await ctx.send(f"Invited {len(invited)} friends to the party.")

        except Exception:
            pass

    else:
        try:
            if member is None:
                user = await client.fetch_profile(ctx.message.author.id)
                friend = client.get_friend(user.id)
            if member is not None:
                user = await client.fetch_profile(member)
                friend = client.get_friend(user.id)

            await friend.invite()
            await ctx.send(f"Invited {friend.display_name} to the party.")
        except fortnitepy.PartyError:
            await ctx.send("That user is already in the party.")
        except fortnitepy.HTTPException:
            await ctx.send("Something went wrong inviting that user.")
        except AttributeError:
            await ctx.send("I can not invite that user. Are you sure I have them friended?")
        except Exception:
            pass     

@client.command()
@is_admin()
async def friends(ctx):
    cfriends = client.friends
    onlineFriends = []
    offlineFriends = []

    try:
        for f in cfriends:
            friend = client.get_friend(f)
            if friend.is_online():
                onlineFriends.append(friend.display_name)
            else:
                offlineFriends.append(friend.display_name)
        
        await ctx.send(f"Client has: {len(onlineFriends)} friends online and {len(offlineFriends)} friends offline")
        await ctx.send("(Check cmd for full list of friends)")

        print(" [+] Friends List: " + Fore.GREEN + f'{len(onlineFriends)} Online ' + Fore.RESET + "/" + Fore.LIGHTBLACK_EX + f' {len(offlineFriends)} Offline ' + Fore.RESET + "/" + Fore.LIGHTWHITE_EX + f' {len(onlineFriends) + len(offlineFriends)} Total')
        
        for x in onlineFriends:
            if x is not None:
                print(Fore.GREEN + " " + x)
        for x in offlineFriends:
            if x is not None:
                print(Fore.LIGHTBLACK_EX + " " + x)
    except Exception:
        pass



@client.command()
async def kick(ctx, *, member = None):
    if member is not None:
        if member.lower() == 'all':
            members = client.party.members

            for m in members:
                try:
                    member = await client.get_user(m)
                    await member.kick()
                except fortnitepy.Forbidden:
                    await ctx.send("I am not party leader.")

            await ctx.send("Kicked everyone in the party")

        else:
            try:
                user = await client.fetch_profile(member)
                member = client.party.members.get(user.id)
                if member is None:
                    await ctx.send("Couldn't find that user. Are you sure they're in the party?")

                await member.kick()
                await ctx.send(f'Kicked: {member.display_name}')
            except fortnitepy.Forbidden:
                await ctx.send("I can't kick that user because I am not party leader")
            except AttributeError:
                await ctx.send("Couldn't find that user.")
    else:
        await ctx.send(f'No member was given. Try: {prefix}kick (user)')

@client.command()
@is_admin()
async def promote(ctx, *, username = None):
    if username is None:
        user = await client.fetch_user(ctx.author.display_name)
        member = client.party.get_member(user.id)
    else:
        user = await client.fetch_user(username)
        member = client.party.get_member(user.id)
    try:
        await member.promote()
        await ctx.send(f"Promoted: {member.display_name}")
    except fortnitepy.Forbidden:
        await ctx.send("Client is not party leader")
    except fortnitepy.PartyError:
        await ctx.send("That person is already party leader")
    except fortnitepy.HTTPException:
        await ctx.send("Something went wrong trying to promote that member")
    except AttributeError:
        await ctx.send("Can’t find this user")


@client.command()
@is_admin()
async def unhide(ctx):
    if client.party.me.leader:
        user = await client.fetch_profile(ctx.message.author.id)
        member = client.party.members.get(user.id)

        await member.promote()

        await ctx.send("Unhid all players.")

    else:
        await ctx.send("I am not party leader.")

@client.command()
async def point(ctx, *, content = None):
    if content is None:
        await client.party.me.clear_emote()
        await client.party.me.set_emote(asset='EID_IceKing')
        await ctx.send(f'Pointing with: {client.party.me.pickaxe}')
    
    else:
        if content.upper().startswith('Pickaxe_'):
            await client.party.me.set_pickaxe(asset=content.upper())
            await client.party.me.clear_emote()
            asyncio.sleep(0.25)
            await client.party.me.set_emote(asset='EID_IceKing')
            await ctx.send(f'Pointing with: {content}')
        else:
            try:
                cosmetic = await BenBotAsync.get_cosmetic(
                    lang="en",
                    searchLang="en",
                    matchMethod="contains",
                    name=content,
                    backendType="AthenaPickaxe"
                )
                await client.party.me.set_pickaxe(asset=cosmetic.id)
                await client.party.me.clear_emote()
                await client.party.me.set_emote(asset='EID_IceKing')
                await ctx.send(f'Pointing with: {cosmetic.name}')
            except BenBotAsync.exceptions.NotFound:
                await ctx.send(f'Could not find a pickaxe named: {content}')





@client.command()
async def floss(ctx, *, content=None):
    await client.party.me.set_emote(asset="eid_floss")





@client.command()
async def ninja(ctx):
    await client.party.me.set_outfit(asset="cid_605_athena_commando_m_tourbus")
    await client.party.me.set_backpack(asset="bid_402_tourbus")
    await client.party.me.set_emote(asset="eid_tourbus")


@client.command()
async def hologram(ctx):
    await client.party.me.set_outfit(
        asset='CID_VIP_Athena_Commando_M_GalileoGondola_SG'
    )
    
    await ctx.send("Skin set to: Hologram")


@client.command()
async def last(ctx):
    await client.party.me.set_emote(
        asset='EID_TwistEternity'
    )
    
    await ctx.send("Emote set to: Last Forever")



@client.command()
async def itemshop(ctx):
    previous_skin = client.party.me.outfit

    store = await client.fetch_item_shop()

    await ctx.send("Equipping all item shop skins + emotes")

    for cosmetic in store.featured_items + store.daily_items:
        for grant in cosmetic.grants:
            if grant['type'] == 'AthenaCharacter':
                await client.party.me.set_outfit(asset=grant['asset'])
                await asyncio.sleep(5)
            elif grant['type'] == 'AthenaDance':
                await client.party.me.clear_emote()
                await client.party.me.set_emote(asset=grant['asset'])
                await asyncio.sleep(5)

    await client.party.me.clear_emote()
    
    await ctx.send("Per ottenere il tuo bot: \n2)YouTube: WonderBot\n3) TikTok: Simon_leaks")

    await asyncio.sleep(1.5)

    await client.party.me.set_outfit(asset=previous_skin)



@client.command()
async def new(ctx, content = None):
    newSkins = getNewSkins()
    newEmotes = getNewEmotes()

    previous_skin = client.party.me.outfit

    if content is None:
        await ctx.send(f'There are {len(newSkins) + len(newEmotes)} new skins + emotes')

        for cosmetic in newSkins + newEmotes:
            if cosmetic.startswith('CID_'):
                await client.party.me.set_outfit(asset=cosmetic)
                await asyncio.sleep(4)
            elif cosmetic.startswith('EID_'):
                await client.party.me.clear_emote()
                await client.party.me.set_emote(asset=cosmetic)
                await asyncio.sleep(4)

    elif 'skin' in content.lower():
        await ctx.send(f'There are {len(newSkins)} new skins')

        for skin in newSkins:
            await client.party.me.set_outfit(asset=skin)
            await asyncio.sleep(4)

    elif 'emote' in content.lower():
        await ctx.send(f'There are {len(newEmotes)} new emotes')

        for emote in newEmotes:
            await client.party.me.clear_emote()
            await client.party.me.set_emote(asset=emote)
            await asyncio.sleep(4)

    await client.party.me.clear_emote()
    
    await ctx.send('Done!')

    await asyncio.sleep(1.5)

    await client.party.me.set_outfit(asset=previous_skin)

    if (content is not None) and ('skin' or 'emote' not in content.lower()):
        ctx.send(f"Not a valid option. Try: {prefix}new (skins, emotes)")



@client.command()
async def ready(ctx):
    await client.party.me.set_ready(fortnitepy.ReadyState.READY)
    await ctx.send('Ready!')



@client.command()
async def unready(ctx):
    await client.party.me.set_ready(fortnitepy.ReadyState.NOT_READY)
    await ctx.send('Unready!')


@client.command()
async def sitin(ctx):
    await client.party.me.set_ready(fortnitepy.ReadyState.NOT_READY)
    await ctx.send('Sitting in')

@client.command()
async def sitout(ctx):
    await client.party.me.set_ready(fortnitepy.ReadyState.SITTING_OUT)
    await ctx.send('Sitting out')


@client.command()
async def tier(ctx, tier = None):
    if tier is None:
        await ctx.send(f'No tier was given. Try: {prefix}tier (tier number)') 
    else:
        await client.party.me.set_battlepass_info(
            has_purchased=True,
            level=tier
        )

        await ctx.send(f'Battle Pass tier set to: {tier}')


@client.command()
async def level(ctx, level = None):
    if level is None:
        await ctx.send(f'No level was given. Try: {prefix}level (number)')
    else:
        await client.party.me.set_banner(season_level=level)
        await ctx.send(f'Level set to: {level}')

client.status = 'Lobby Battle Royale - 1 / 16 '

@client.command()
async def og(ctx):
    previous_skin = client.party.me.outfit
    variants = client.party.me.create_variants(material=1)

    await client.party.me.set_outfit(
        asset="CID_028_Athena_Commando_F", variants=variants
    )
    await ctx.send(f"Renegade Raider")

    await asyncio.sleep(2.25)
    await client.party.me.set_outfit(
        asset="cid_017_athena_commando_m",
    )
    await ctx.send(f"Aerial Assault Trooper")

    await asyncio.sleep(2.25)
    variants = client.party.me.create_variants(material=3)
    await client.party.me.set_outfit(
        asset="CID_029_Athena_Commando_F_Halloween", variants=variants
    )
    await ctx.send("Pink Ghoul Trooper")

    await asyncio.sleep(2.25)
    variants = client.party.me.create_variants(clothing_color=1)

    await client.party.me.set_outfit(
        asset="CID_030_Athena_Commando_M_Halloween", variants=variants
    )
    await ctx.send("Purple Skull Trooper")

    await asyncio.sleep(2.25)
    await client.party.me.set_outfit(asset=previous_skin)

    await ctx.send(
        f"Season one og skins "
     )
    await ctx.send(
      f"To get your OWN Lobby Bot: \n1) Join our Discord at: https://discord.gg/rAd9YnHjV3 \n2)YouTube: Ghost Leaks\n3) TikTok: Ghost_Leaks\n4) Instagram: ghost__leaks\nMade with GhostFN!"
     )

@client.command()
async def banner(ctx, args1 = None, args2 = None):
    if (args1 is not None) and (args2 is None):
        if args1.startswith('defaultcolor'):
            await client.party.me.set_banner(
                color = args1
            )
            
            await ctx.send(f'Banner color set to: {args1}')

        elif args1.isnumeric() == True:
            await client.party.me.set_banner(
                color = 'defaultcolor' + args1
            )

            await ctx.send(f'Banner color set to: defaultcolor{args1}')

        else:
            await client.party.me.set_banner(
                icon = args1
            )

            await ctx.send(f'Banner Icon set to: {args1}')

    elif (args1 is not None) and (args2 is not None):
        if args2.startswith('defaultcolor'):
            await client.party.me.set_banner(
                icon = args1,
                color = args2
            )

            await ctx.send(f'Banner icon set to: {args1} -- Banner color set to: {args2}')
        
        elif args2.isnumeric() == True:
            await client.party.me.set_banner(
                icon = args1,
                color = 'defaultcolor' + args2
            )

            await ctx.send(f'Banner icon set to: {args1} -- Banner color set to: defaultcolor{args2}')

        else:
            await ctx.send(f'Not proper format. Try: {prefix}banner (Banner ID) (Banner Color ID)')


copied_player = ""


@client.command()
async def stop(ctx):
    global copied_player
    if copied_player != "":
        copied_player = ""
        await ctx.send(f'Stopped copying all users.')
        return
    else:
        try:
            await client.party.me.clear_emote()
        except RuntimeWarning:
            pass



@client.command()
async def copy(ctx, *, username = None):
    global copied_player

    if username is None:
        member = [m for m in client.party.members if m.id == ctx.author.id][0]

    else:
        user = await client.fetch_user(username)
        member = [m for m in client.party.members if m.id == user.id][0]

    await client.party.me.edit_and_keep(
            partial(
                fortnitepy.ClientPartyMember.set_outfit,
                asset=member.outfit,
                variants=member.outfit_variants
            ),
            partial(
                fortnitepy.ClientPartyMember.set_backpack,
                asset=member.backpack,
                variants=member.backpack_variants
            ),
            partial(
                fortnitepy.ClientPartyMember.set_pickaxe,
                asset=member.pickaxe,
                variants=member.pickaxe_variants
            ),
            partial(
                fortnitepy.ClientPartyMember.set_banner,
                icon=member.banner[0],
                color=member.banner[1],
                season_level=member.banner[2]
            ),
            partial(
                fortnitepy.ClientPartyMember.set_battlepass_info,
                has_purchased=member.battlepass_info[0],
                level=member.battlepass_info[1]
            ),
            partial(
                fortnitepy.ClientPartyMember.set_emote,
                asset=member.emote
            )
        )

    await ctx.send(f"Now copying: {member.display_name}")
    

@client.event()
async def event_party_member_outfit_change(member, before, after):
    if member == copied_player:
        await client.party.me.edit_and_keep(
            partial(
                fortnitepy.ClientPartyMember.set_outfit,
                asset=after,
                variants=member.outfit_variants
            )
        )

@client.event()
async def event_party_member_outfit_variants_change(member, before, after):
    if member == copied_player:
        await client.party.me.edit_and_keep(
            partial(
                fortnitepy.ClientPartyMember.set_outfit,
                variants=member.outfit_variants
            )
        )

@client.event()
async def event_party_member_backpack_change(member, before, after):
    if member == copied_player:
        if after is None:
            await client.party.me.clear_backpack()
        else:
            await client.party.me.edit_and_keep(
                partial(
                    fortnitepy.ClientPartyMember.set_backpack,
                    asset=after,
                    variants=member.backpack_variants
                )
            )

@client.event()
async def event_party_member_backpack_variants_change(member, before, after):
    if member == copied_player:
        await client.party.me.edit_and_keep(
            partial(
                fortnitepy.ClientPartyMember.set_backpack,
                variants=member.backpack_variants
            )
        )

@client.event()
async def event_party_member_emote_change(member, before, after):
    if member == copied_player:
        if after is None:
            await client.party.me.clear_emote()
        else:
            await client.party.me.edit_and_keep(
                partial(
                    fortnitepy.ClientPartyMember.set_emote,
                    asset=after
                )
            )

@client.event()
async def event_party_member_pickaxe_change(member, before, after):
    if member == copied_player:
        await client.party.me.edit_and_keep(
            partial(
                fortnitepy.ClientPartyMember.set_pickaxe,
                asset=after,
                variants=member.pickaxe_variants
            )
        )

@client.event()
async def event_party_member_pickaxe_variants_change(member, before, after):
    if member == copied_player:
        await client.party.me.edit_and_keep(
            partial(
                fortnitepy.ClientPartyMember.set_pickaxe,
                variants=member.pickaxe_variants
            )
        )

@client.event()
async def event_party_member_banner_change(member, before, after):
    if member == copied_player:
        await client.party.me.edit_and_keep(
            partial(
                fortnitepy.ClientPartyMember.set_banner,
                icon=member.banner[0],
                color=member.banner[1],
                season_level=member.banner[2]
            )
        )

@client.event()
async def event_party_member_battlepass_info_change(member, before, after):
    if member == copied_player:
        await client.party.me.edit_and_keep(
            partial(
                fortnitepy.ClientPartyMember.set_battlepass_info,
                has_purchased=member.battlepass_info[0],
                level=member.battlepass_info[1]
            )
        )

async def set_and_update_party_prop(schema_key: str, new_value: str):
    prop = {schema_key: client.party.me.meta.set_prop(schema_key, new_value)}
    await client.party.patch(updated=prop)




@client.command()
async def say(ctx, *, message = None):
    if message is not None:
        await client.party.send(message)
        await ctx.send(f'Sent "{message}" to party chat')
    else:
        await ctx.send(f'No message was given. Try: {prefix}say (message)')



@client.command()
async def admin(ctx, setting = None, *, user = None):
    if (setting is None) and (user is None):
        await ctx.send(f"Missing one or more arguments. Try: {prefix}admin (add, remove, list) (user)")
    elif (setting is not None) and (user is None):

        user = await client.fetch_profile(ctx.message.author.id)

        if setting.lower() == 'add':
            if user.id in info['FullAccess']:
                await ctx.send("You are already an admin")

            else:
                await ctx.send("Password?")
                response = await client.wait_for('friend_message', timeout=20)
                content = response.content.lower()
                if content == data['AdminPassword']:
                    info['FullAccess'].append(user.id)
                    with open('info.json', 'w') as f:
                        json.dump(info, f, indent=4)
                        await ctx.send(f"Correct. Added {user.display_name} as an admin.")
                        print(Fore.GREEN + " [+] " + Fore.LIGHTGREEN_EX + user.display_name + Fore.RESET + " was added as an admin.")
                else:
                    await ctx.send("Incorrect Password.")

        elif setting.lower() == 'remove':
            if user.id not in info['FullAccess']:
                await ctx.send("You are not an admin.")
            else:
                await ctx.send("Are you sure you want to remove yourself as an admin?")
                response = await client.wait_for('friend_message', timeout=20)
                content = response.content.lower()
                if (content.lower() == 'yes') or (content.lower() == 'y'):
                    info['FullAccess'].remove(user.id)
                    with open('info.json', 'w') as f:
                        json.dump(info, f, indent=4)
                        await ctx.send("You were removed as an admin.")
                        print(Fore.BLUE + " [+] " + Fore.LIGHTBLUE_EX + user.display_name + Fore.RESET + " was removed as an admin.")
                elif (content.lower() == 'no') or (content.lower() == 'n'):
                    await ctx.send("You were kept as admin.")
                else:
                    await ctx.send("Not a correct reponse. Cancelling command.")
                
        elif setting == 'list':
            if user.id in info['FullAccess']:
                admins = []

                for admin in info['FullAccess']:
                    user = await client.fetch_profile(admin)
                    admins.append(user.display_name)

                await ctx.send(f"The bot has {len(admins)} admins:")

                for admin in admins:
                    await ctx.send(admin)

            else:
                await ctx.send("You don't have permission to this command.")

        else:
            await ctx.send(f"That is not a valid setting. Try: {prefix}admin (add, remove, list) (user)")
            
    elif (setting is not None) and (user is not None):
        user = await client.fetch_profile(user)

        if setting.lower() == 'add':
            if ctx.message.author.id in info['FullAccess']:
                if user.id not in info['FullAccess']:
                    info['FullAccess'].append(user.id)
                    with open('info.json', 'w') as f:
                        json.dump(info, f, indent=4)
                        await ctx.send(f"Correct. Added {user.display_name} as an admin.")
                        print(Fore.GREEN + " [+] " + Fore.LIGHTGREEN_EX + user.display_name + Fore.RESET + " was added as an admin.")
                else:
                    await ctx.send("That user is already an admin.")
            else:
                await ctx.send("You don't have access to add other people as admins. Try just: !admin add")
        elif setting.lower() == 'remove':
            if ctx.message.author.id in info['FullAccess']:
                if user.id in info['FullAccess']:
                    await ctx.send("Password?")
                    response = await client.wait_for('friend_message', timeout=20)
                    content = response.content.lower()
                    if content == data['AdminPassword']:
                        info['FullAccess'].remove(user.id)
                        with open('info.json', 'w') as f:
                            json.dump(info, f, indent=4)
                            await ctx.send(f"{user.display_name} was removed as an admin.")
                            print(Fore.BLUE + " [+] " + Fore.LIGHTBLUE_EX + user.display_name + Fore.RESET + " was removed as an admin.")
                    else:
                        await ctx.send("Incorrect Password.")
                else:
                    await ctx.send("That person is not an admin.")
            else:
                await ctx.send("You don't have permission to remove players as an admin.")
        else:
            await ctx.send(f"Not a valid setting. Try: {prefix}admin (add, remove) (user)")

keep_alive.keep_alive()#start the server

if (data['email'] and data['password']) and (data['email'] != "" and data['password'] != ""):
    try:
        client.run()
    except fortnitepy.errors.AuthException as e:
        print(Fore.RED + ' [ERROR] ' + Fore.RESET + f'{e}')
    except ModuleNotFoundError:
        print(e)
        print(Fore.RED + f'[-] ' + Fore.RESET + 'Failed to import 1 or more modules. Run "INSTALL PACKAGES.bat')
        exit()
else:
    print(Fore.RED + ' [ERROR] ' + Fore.RESET + 'Can not log in, as no accounts credentials were provided.')
