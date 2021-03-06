import logging
import random
from datetime import time
from typing import Dict

import telegram
from telegram import Bot
from telegram.ext import JobQueue, Job, CallbackContext

from neocortex import memories

THE_TIME = time(hour=13, minute=37)
log = logging.getLogger()
user_jobs = {}  # type: Dict[telegram.User, Job]
exactly_1337_emoji = "🎮🍸🎪🐯💇🎥🐁🐳💴📲🕝💱🍆🍼👱🕐🏇🏂💵🔍💤🔙🏡🍋🌑💣🐛🎿🍡🌹👀🎸🍟🗾🐘🐹🍎📪🐗🍲🕢🍂💡🎴🍲👫🔒👮🕖🕝🎑🌘🔃🐒" \
                     "🏈🔝🍭👈🔏🍋💍💇🕧🔟💶🎂🎐🏂💈🍋🍁💞🗾💍🔆📲👈💯🕠📉💙👻👕🔝🐽👂🎰🍌🔠🏈🕙🎨💫💀🏀👥🍒📠🕢🌛👮🍓🌞👬💸🍻🔜🌹" \
                     "🔡🎽🎩🍍💀💾💌👓🎊🌺🐂🐤🎹🍡🌇👰🌾🎦💕🐟🍨💪🌘🐈🔜💆🍶👳🌸🏃🏯👃🍵📵👾🐷🗻🕝👙🍷👕🏃👀🕒👢🐟💭💽💺💇🍶📮🌇" \
                     "📄🎇🐒👗🔭🏤📵💲🔨🐱🐗🐦🎯🔝🎪👓👗🏪💱🔍👟🌾🕂💘💒🔈🍐🏀🕙📥👥🕥🌶🐀🔂📋🔇🌉👍📔🔷🐩👍👘🌊🔀📣🌃🍔🔄👰🏨🎲🔙" \
                     "🏬💜👎👜🍢👣📫🐺🔃💡👣👋👬🌘🐭🎻🌈👷🐸🌿🍜🎩🐖🔡🐣🐐🍧🐙👥📘🎈👽🔪💢🏣🍝🌸👾🐎🍃🏃👔📪🕜📌💹💄📂🕝👇💥🕜🌉👌" \
                     "🔅👪📡💣🍍🔷👥🔴🎴🐠🌾🔸💟🏨🎳📹🔖👸💯🍧🍣🐍🎊🔡🐮💃💪👸🎠💁🔡🐝🎈🔽🔫🔬🔴🔕🕛🕕👘📰📪🍥🎣💿🔗🏩🔇🐝🔷👦🐂🏃" \
                     "🐾💚🍚🍝🐰📕👥🐭💔🍰🕘🐪🔄👗🎆🍋🕖🐚📐🐖🍪🎿🌽🔨📺👥🎏👢🐮📨👕🔐🐚🍫🍼📝💔🌂🐕💕👣📆🌠🌊🐵🍮🌰👀👺🍏🕠🍚🔼🌌" \
                     "🌅👜💰🎉💄👏🌓👧🎷🎳📃🏃👊🍲💯📄💌🎓🔊📜🍩👔🔇🏬💚🌿💦🍅🍪👂🎶🍯💲🍎🔱🐈🐬🔵👉🐳🏢🐩📻🔂📻🎱👞🎲👇🎂🐔🌒👞👍" \
                     "🎏💊🍌💣🏨🔜💎🏨💰🌍🎋🐩🍺🎿🕔👙🍁🎿🗾🌚💀👄📯🌂🍞👉👅🌆🍈🔲📧👖🌽🐃🔥🎾🌁🏰🔍📢🌀📖🔑👓🔗👯👌🕛👩🏆🍳💉📆🏁" \
                     "📑🌶🔴🐴🕔🎀👝👟🐢🍯🔆🌎🍟📈📖🏇🎱💋🔠🐓💃🔮🔧🐞👍🌵🐱🍂🐻🕤🎶📨🐒🍼💁👩👜🕟👆💄💠🕡👚📼🐯👥🏯🔓🐟🎓🔳📋🕦📪" \
                     "🕜🕃🔝🍤💉🕑🔼💰🍎🍏👓🔣🎐🔋🐾📰🔨🕧🎲💉💐💊🐫🌷🔯🍦👋💄🍯👕🎈🔡🎮👵📍👘🗼🐐🏀🌘🔭💪🐍🔼🌾🌄📙💊👉🕞👀📓🎵📚📇" \
                     "💻🔼💡📚🐦🍗🔨🍷🐸💹💷👄🗻📮🐝🌺🍪🔒👌💀💗👱🔈🌍💻💰💼🐜🍎📀🏠🔚🎡📅🕠💛🕡👐🐢🍣🕧👪🐬📳💙🔉👄🔧🐯👥👤🕕🎓📹💥" \
                     "🔅👄💬🍫💔🍅👵📲🍴🔒📻🏦🏥🗽📷🌴🎒🐦🌕🌸🕃🌠🏃🐇🍤🎶🎐🔭💵🎿🐗🏪🐼🐮🔨🕤📘🏃🏨💓📢🌷📄👃🍺📦🔷📠📳🌛🎼💎👮👅🐐" \
                     "👶📣👾🔵🔅📑📙👗🔀🐠🌓🍅🐼🐅📎🌻💢🎳🕞🎌👭🎴💁🍸🐢💵🏠🍒🍚📁💿📴🍢💔🔨📊💀🍟🐉💂🌲💧💶💔📑🍴💦🎫🎪💙🌾🔚📕🔤" \
                     "👵🔑🌾🔇🏄🍲🎈🎿📎💛💗💃🏄💙🍐🐜🎷📣🍁🍈👝🏢🔚🎋🐂🍒🐐🍝💳🔆🔼🌙👯🕤🐑🍦📠🔲👱🌀👝🍭🐾🔂🎰🔻👲🕘🎬🌈🌜👲🎯🎤" \
                     "💗💯🕘💹💺🔔💴🎐👘🔄👯👪🐋🔭🎿🌞🌖👖🎬🎇🕛🌏👖🕚🔷📔🍜🍟🎺💁📬🕗🔄🌺🏭💫🔙🐒🎐💕🎇💆💇🐧🔽🌟👾🍉🔍🍷🔡👧💙🍯" \
                     "🍧🌘🐸🐘🍞👽📞📁🍖💂🔂🍷🏣🍔🍋🏦🐘🕥🍎🎎🌌🎄🎱🐑📩📑💖🌍🔣📮🍬🎏🐒🐓🔥👄🐬🔹🎫🐜🎻🐗📞🌰🎮🎰🎒🔣👑🌇🎢🔲👓👢" \
                     "💰🌟🍆🏄💯👔💕💤📚👰🎉📇📛🐺🌁🔑🐜🔙🏦🍉🕝👟👡🐬🍠📥🔷🍋💘🎱🌅🔣💇🕂💳🐈🎄🐀🎸🌟🏤🏣📳🔣👾🍳👼🏇🍛📴🎵🐕📉📴" \
                     "🏤📃🎳🕔🌂🐦🌇🍰🏃👹🔯🗻🐘🍩🔁🔷💵💻📅🎀👋🔒🏮🔓🕟🍺🎡🌸🔨🏯💛🌔🗻🕖🐗💳🕀🐀🐾🏆🍥👫🔲🌶💮📱👱🌼👣💲📝👍💆🌱" \
                     "🎷🎿💕👕💁🎼🔋🌶🐚📄🐠🌷🕛🕃📬🐄💑💐🎡🔙🌵🎦🍈💊🎉🎰📪🏢🔚🏪🍣💧🍎🌆👰🔦🍑📃🔖🍥🐇💥💹🍧🔀🎄📮💇👡🎿🌼🐃🍞👍" \
                     "🕚🍺🏈👇🍃💭🐗👑🌝🎵🎐💃🔓👹👆🐈🌚💩👱📃🔎🍝📑📈🔸🌞🍡🕟🔝🕒💯👇👲🎈🔌💪📶🍦🐾🏉🐤📒📍🌙🏉🕟🔉🎭🌇🍫📏🍢👍💚" \
                     "📄🎑📼🐲👡🔋🍙👑🏫💃🌴👩🔷🐡🎇💠🎵📚📏📖🔈🔔📑🍥💐👳🌳🎢🔲🍯🌌💉📗📕🌝🔒👾🕖🏨💉💧🔬🕥🕝🍱📣👮🏦💓🕠💎🌍🎐🐃💎" \
                     "🐀🐔🐁🐛💱💨👩🔅🕔🎂🍢👭🔇🎃👩🔳🍛👊🏁📕🗾👚🌎🐇💐🐟🔁🏰💜🏆🐭👗🌱🌲🔒🔸💜🍄📚🌍💧🕀🎺💕🌴📰🔬🍵🌍👪📫🕝🎂🍯" \
                     "🕜🌜🔘👛🐤🎻🍫💝🍫💦🏤🍖🌺🕟🍅🏣🐝🕙🐙📜🍖🐚💕💘🔫💿👡📉💒🍴💛🍱🍬📊👹🐳💖📯🍒💱🗼📼🍘📔👈🎆🐴📵🔷🍏🐩💡🌛" \
                     "🔞📁💑🔀👋🌾🐵🐤🐢🏆💥🎇👌🔦🐠🕐🔒🐗🎊🌻💗📙🏥🎬🐯🍊📁🐑📼👪💏👪🏩💦🐫🔷🐴📑📩 "


def manage_subscription(user: telegram.User, job_queue: JobQueue) -> str:
    if user in user_jobs:
        return unsubscribe(user)
    else:
        return subscribe(job_queue, user)


def subscribe(job_queue: JobQueue, user: telegram.User) -> str:
    create_and_remember_job(job_queue, user)
    remember_preference_change_of(user)
    return "You will be notified."


def create_and_remember_job(job_queue: JobQueue, user: telegram.User) -> None:
    job = job_queue.run_daily(callback=notify_subscriber, time=THE_TIME, context=user, name="1337")
    # job = job_queue.run_repeating(callback=notify_subscriber, first=0, interval=120, context=user, name="1337")
    user_jobs[user] = job


def unsubscribe(user: telegram.User) -> str:
    job = user_jobs.pop(user)
    job.schedule_removal()
    remember_preference_change_of(user)
    return "You won't be notified anymore."


def remember_preference_change_of(user: telegram.User) -> None:
    memory_of_user = memories.remember_telegram_user(user)
    memories.toggle_wants_notification(memory_of_user)


def notify_subscriber(context: CallbackContext) -> None:
    user = context.job.context  # type: telegram.User
    text = "It is time.\n\n" + "".join(random.sample(exactly_1337_emoji, random.randint(13, 37)))
    try:
        context.bot.send_message(chat_id=user.id, text=text)
    except telegram.error.Unauthorized:
        unsubscribe(user)
        log.info('Someone blocked the bot but still had an active subscription. Unsubscribed him.')


def remember_subscribers(bot: Bot, queue: JobQueue) -> None:
    for subscriber in memories.get_subscribers():
        subscriber.bot = bot
        create_and_remember_job(job_queue=queue, user=subscriber)
