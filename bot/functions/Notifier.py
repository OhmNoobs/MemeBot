import logging
import random
from datetime import time
from typing import Dict

import telegram
from telegram import Bot
from telegram.ext import JobQueue, Job

THE_TIME = time(hour=13, minute=37)
log = logging.getLogger('meme-bot')
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
    job = job_queue.run_daily(callback=notify_subscriber, time=THE_TIME, context=user, name="1337")
    user_jobs[user] = job
    return "You will be notified."


def unsubscribe(user: telegram.User) -> str:
    job = user_jobs.pop(user)
    job.schedule_removal()
    return "You won't be notified anymore."


def notify_subscriber(bot: Bot, job: Job) -> None:
    user = job.context  # type: telegram.User
    text = "It is time.\n\n" + "".join(random.sample(exactly_1337_emoji, random.randint(13, 37)))
    try:
        bot.send_message(chat_id=user.id, text=text)
    except telegram.error.Unauthorized:
        unsubscribe(user)
        log.info('Someone blocked the bot but still had an active subscription. Unsubscribed him.')
