import os
import sqlite3
from time import sleep
from datetime import datetime

import telebot

import config
from KeyboardsMarkup import *

# Colors
normal = '\x1b[0m'
red = '\x1b[31m'
green = '\x1b[32m'
yellow = '\x1b[33m'
blue = '\x1b[34m'
purple = '\x1b[35m'

os.system('clear')  # Clear Konsole
bot = telebot.TeleBot(config.BotToken)

text_start = '''Пожалуйста выберите тему:
1) Nope
2) Nope
3) «Береги честь смолоду» Гринёв и Швабрин
4) Смысыл названия романа А. С. Пушкина «Капитанская дочка»
5) Образ Савельича в романе «Капитанская дочка»'''
text1 = None
text2 = None
text3 = '''Произведение "Капитанская дочка" написано А. С. Пушкиным и опубликовано в 1836 году. В нём рассказывается история о двух героях - Гриневе и Швабрине, которые имеют некоторые общие черты, но совершенно разные взгляды на жизнь.

Алексей Иванович Швабрин – молодой офицер из богатой аристократической семьи. Он был подвергнут разжалованию из-за того, что убил своего сослуживца и отправлен для службы в Белогорускую крепость.

Пётр Гринёв – благородный и честный человек. Проиграв Зурину сто рублей, он заставляет Савельича вернуть долг, считая это долгом чести. Доброта и великодушие Гринёва очень пригодилось ему, ведь Пугачёв помнил подарок и только поэтому его помиловал. При разговоре с Емельяном Пугачевым, он не стал ему врать, а прямо сказал, что не перейдёт на его сторону, а если прикажут, будет сражаться против него, тем самым Гринёв показал себя храбрым, смелым и ответственным человеком. Пётр не побоялся отправиться спасать Машу от Швабрина, хотя знал, что его могут поймать и убить. Он рисковал жизнью, пробираясь в крепость, проявил мужество и смекалку. Таким образом этот герой оставался честен во всех жизненных трудных обстоятельствах, ни разу не придав присяги, родителей, любимую девушку.

1) Общее у Гринёва и Швабрина: оба являются офицерами, служат в армии, прошли через военные испытания.

2) Отношение к людям: Гринёв отличается состраданием и милосердием, проявляет заботу о ближних. Швабрин же выделяется эгоизмом и безразличием к чужим страданиям.

3) Поступки в ситуациях выбора: Гринёв всегда стремится к справедливости и делает правильный выбор, даже если это противоречит его собственным интересам. Швабрин же склонен к жестокости и нетерпимости, выбирая путь наименьшего сопротивления.

4) Любовь или долг: Швабрин не искренне любил Машу, его чувства были скорее эгоистичными и связаны с желанием достичь своих целей. В то время как Гринёв искренне и бескорыстно любит Машу.

5) Судьба героев и эпиграф: Судьба героев соотносится с эпиграфом к роману, который гласит "Береги честь смолоду". Гринёв, придерживаясь высоких моральных принципов, сохраняет свою честь и достоинство, в то время как Швабрин, отступая от них, сталкивается с падением и наказанием.'''
text4 = '''«Береги честь смолоду» – именно такие слова говорил Гриневу отец, как завет  напутствие на жизнь. Примечательно, что Маше таких слов, возможно, никто и не говорил, но именно в ней воплотился идеал чести и достоинства, который она смогла сберечь, ни разу не изменив себе даже в самой страшной ситуации.
«Капитанская дочка» – произведение о чести и достоинстве. Их воплощением стала Маша Миронова, именно поэтому Пушкин назвал свое произведение не иначе как «Капитанская дочка».

1) Первое впечатление Гринёва от Маши Мироновой было положительным. Он был восхищен ее красотой и нежностью. Внешность Маши символизирует ее доброту, чистоту и невинность.

2) В характере Маши проявляются такие черты, как преданность, сдержанность, ум и чувство долга. Она уважает и заботится о своих родителях, а также проявляет сострадание и понимание к родителям Гринёва. Она отвергает Швабрина и сохраняет верность Гринёву.

3) Личность Маши раскрывается в ее любви к Гринёву. Она готова преодолеть множество испытаний, чтобы быть рядом с ним. Ее любовь к Гринёву выражает ее героизм, самоотверженность и способность преодолевать трудности.

4) Другие герои романа относятся к Маше с уважением и восхищением. Они видят в ней символ идеалов чести, добродетели и патриотизма. Маша становится вдохновением для них и влияет на их поступки.

5) Эпизод поездки Маши в Петербург к Екатерине II дополняет образ Маши, показывая ее готовность преодолеть преграды и бороться за свои убеждения. Эта поездка также подчеркивает ее патриотизм и искреннее стремление служить Родине.

6) Основная идея романа заключается в показе силы духа и мужества, способных преодолеть любые испытания. Эта идея воплощается в образе Маши Мироновой, которая, несмотря на свою юность и женскую слабость, проявляет героизм, принципиальность и преданность своим убеждениям. Маша становится символом русской духовности и героизма.'''
text51 = '''Краткая характеристика:
Полное имя — Архип Савельев.
Возраст — мужчина преклонных лет.
Род занятий — стремянной, затем — дядька (наставник) молодого барина Петра Гринёва.
Семья — нет семьи.
Социальное положение — крепостной крестьянин.
Происхождение — родом из семьи крепостных крестьян.
Воспитание — несмотря на происхождение, имеет хорошее воспитание.
Образование — достаточно высокое, умеет свободно писать и читать, изъяснять свои мысли.
Внешность — не указано, седовласый мужчина преклонных лет.
Характер — упрямый, настойчивый, добрый, ответственный, благородный, трудолюбивый, бережливый.
Положительные черты — добрый, ответственный, храбрый, самоотверженный,
Отрицательные черты — упрямый, занудный.

Портрет
Художественный портрет Савельича основан на том, что он является дядькой, то есть первым педагогом и наставником юного дворянина Петра Гринёва. В прошлом Савельич был стремянным — главным конюхом.
«С пятилетнего возраста отдан я был на руки стремянному Савельичу, за трезвое поведение пожалованному мне в дядьки…»  Источник: Глава I

Полное имя героя — Архип Савельев. По своему происхождению он является крепостным крестьянином, принадлежащим семейству Гринёвых.
«Верный холоп ваш Архип Савельев…» Источник: Глава V
«…я человек подневольный…» Источник: Глава IX 
    
Портретная характеристика Савельича основана на том, что он является грамотным, образованным человеком. Именно с его помощью Пётр Гринёв овладел грамотой.
«Я взял из рук его бумагу: это был ответ Савельича на полученное им письмо…» Источник: Глава V
«Под его надзором на двенадцатом году выучился я русской грамоте…»

Будучи в прошлом стремянным и хорошо разбираясь в охотничьих собаках, Савельич смог обучить этому и Петра Гринёва.
«Под его надзором… мог очень здраво судить о свойствах борзого кобеля».
Источник: Глава I

Внешность

Савельич — мужчина преклонных лет, «старик».

"«Старость проклятая помешала…»"
Источник: Глава V

"«…старик был неутешен…» "
Источник: Глава V

"«…дожил до седых волос…»"
Источник: Глава V

Черты характера и поступки
Савельич — старый опытный слуга, который очень ревностно относится к приезду гувернёра-француза. Он считает, что способен самостоятельно ухаживать за вверенным ему Петром.
«Приезд его сильно не понравился Савельичу. «Слава богу, — ворчал он про себя, — кажется, дитя умыт, причёсан, накормлен. Куда как нужно тратить лишние деньги и нанимать мусье, как будто и своих людей не стало!» Источник: Глава I'''
text52 = '''Савельич — человек очень надёжный. Гринёвы доверяют ему не только воспитание сына: старик следит за безопасностью Петра, помогает ему в решении проблем, держит при себе хозяйские деньги.
«…обратясь к Савельичу, который был и денег, и белья, и дел моих рачитель…» Источник: Глава I
«Деньги мои были у Савельича…» Источник: Глава I
«Батюшка и матушка тебе верят…» Источник: Глава XIII
        
Савельич отличается большим упрямством, и его почти невозможно уговорить сделать что-то против его воли.
«Я подумал, что если в сию решительную минуту не переспорю упрямого старика, то уж в последствии времени трудно мне будет освободиться от его опеки…» Источник: Глава I
«Дело что-то не ладно. Воля твоя, сударь, а денег я не выдам…» Источник: Глава I
«Я знал, что с Савельичем спорить было нечего, и позволил ему приготовляться в дорогу» Источник: Глава ХI
«Зная упрямство дядьки моего, я вознамерился убедить его лаской и искренностью». Источник: Глава ХIII
        
Любимое занятие Савельича — читать нотации своему воспитаннику, ворчать при каждом удобном случае.
«Но Савельича мудрено было унять, когда бывало примется за проповедь…» Источник: Глава I
«Он мало-помалу успокоился, хотя всё еще изредка ворчал про себя…» Источник: Глава II
«Савельич встретил меня с обыкновенным своим увещанием…» Источник: Глава ХI
        
Савельич чувствует ответственность не только за воспитание, но и за будущее Петра Гринёва. Он не может себе простить временной отлучки, когда Пётр умудрился проиграть крупную сумму в бильярд.
«Сержусь-то я на самого себя; сам я кругом виноват. Как мне было оставлять тебя одного в трактире! Что делать?.. Беда да и только! Как покажусь я на глаза господам? что скажут они, как узнают, что дитя пьёт и играет». Источник: Глава II
        
Савельич — невероятно отважный, бесстрашный человек, способный отдать жизнь за своего воспитанника.
«Бог видит, бежал я заслонить тебя своею грудью от шпаги Алексея Иваныча! Старость проклятая помешала». Источник: Глава V
«Гляжу: Савельич лежит в ногах у Пугачёва. «Отец родной!— говорил бедный дядька.— Что тебе в смерти барского дитяти? Отпусти его; за него тебе выкуп дадут; а для примера и страха ради вели повесить хоть меня старика!» Источник: Глава VII
«Чтоб я тебя пустил одного! Да этого и во сне не проси. Коли ты уж решился ехать, то я хоть пешком да пойду за тобой, а тебя не покину». Источник: Глава ХI
        
Савельич — бесконечно преданный семье Гринёвых слуга. Малейшее подозрение в его неверности глубоко оскорбляет его.
«Очевидно было, что Савельич передо мною был прав и что я напрасно оскорбил его упрёком и подозрением. Я просил у него прощения; но старик был неутешен». Источник: Глава V
«…верный ваш слуга, господских приказаний слушаюсь и усердно вам всегда служил и дожил до седых волос». Источник: Глава V
«…читая грамоту доброго старика…» Источник: Глава V'''
text53 = '''Савельич — человек бесстрашный. Отвоёвывая хозяйское добро, он не боится требовать справедливости у самого Пугачёва.
«Савельич крякнул и стал объясняться. «Это, батюшка, изволишь видеть, реестр барскому добру, раскраденному злодеями…»  Источник: Глава IX
«…я человек подневольный и за барское добро должен отвечать…» Источник: Глава IX
        
Даже в разлуке с Петром Гринёвым верный Савельич продолжает честно служить своему хозяину, приглядывая за Марьей Мироновой.
«…с верным Савельичем, который, насильственно разлучённый со мною, утешался по крайней мере мыслию, что служит наречённой моей невесте». Источник: Глава XIV

Характеристика Савельича другими героями
Пётр Гринёв
Савельич — очень упрямый человек, и Петру Гринёву не всегда удаётся переубедить своего наставника.
«Я подумал, что если в сию решительную минуту не переспорю упрямого старика, то уж в последствии времени трудно мне будет освободиться от его опеки…»  Источник: Глава I
        
Савельич — преданный слуга, который долгие годы честно служит Гринёвым.
«Очевидно было, что Савельич передо мною был прав и что я напрасно оскорбил его упрёком и подозрением. Я просил у него прощения; но старик был неутешен». Источник: Глава V
        
Пётр Гринёв считает Савельича своим верным другом. Он знает, что родители верят старому слуге, и обращается к нему за помощью — уговорить их на свадьбу с любимой, Машей Мироновой.
«Друг ты мой, Архип Савельич! — сказал я ему…»  Источник: Глава XIII
«Батюшка и матушка тебе верят: ты будешь за нас ходатаем, не так ли?» Источник: Глава XIII

Гринёв-старший
Отец Петра Гринёва не церемонится с Савельичем, которому доверил своего сына. Он напоминает старому слуге его зависимое положение и прямые обязанности, в гневе оскорбляет его. Савельич не может достойно ответить, поскольку является крепостным.
«Стыдно тебе, старый пёс, что ты, невзирая на мои строгие приказания, мне не донёс о сыне моём Петре Андреевиче и что посторонние принуждены уведомлять меня о его проказах. Так ли исполняешь ты свою должность и господскую волю? Я тебя, старого пса! пошлю свиней пасти за утайку правды и потворство к молодому человеку. С получением сего приказываю тебе немедленно отписать ко мне…» Источник: Глава V
        
Пугачёв
Пугачёв напоминает, что Пётр Гринёв не был повешен благодаря своевременному вмешательству отважного Савельича.
«А покачался бы на перекладине, если б не твой слуга. Я тотчас узнал старого хрыча». Источник: Глава VIII
        
Пугачёв удивляется храбрости Савельича, который даже под угрозой смертельной опасности требует от разбойников вернуть барское добро.
«Глупый старик! Их обобрали: экая беда? Да ты должен, старый хрыч, вечно бога молить за меня да за моих ребят за то, что ты и с барином-то своим не висите здесь вместе с моими ослушниками…» Источник: Глава IX'''
text54 = '''Народная характеристика
Мы постарались составить для вас максимально полный анализ персонажа. Возможно, мы пропустили какой-то интересный или важный фрагмент этой мозаики. Будем рады услышать ваши предложения.
Все подошедшие рекомендации мы опубликуем, а вы получите промокод на бесплатную грамоту.
Давайте создадим самую подробную характеристику Савельича вместе!

Биография
Архип Савельев, или попросту Савельич, — дворовой крепостной, принадлежащий помещикам Гринёвым. Долгое время служил стремянным, сопровождая барина во время охоты и следя за порядком в конюшне.
В отличие от большинства крепостных мужиков, Савельич — грамотный и непьющий мужик. Благодаря этим качествам он был выбран Гринёвым-старшим в качестве дядьки к пятилетнему Петруше. В обязанности Савельича входило воспитание маленького барчука, обучение его грамоте. Когда же к подросшему Петруше приставили гувернёра-француза, самолюбие Савельича было задето, однако в итоге он так и остался дядькой Петра.
В возрасте 16 лет Пётр Гринёв был отправлен отцом на службу, и верный Савельич стал его провожатым. Он следил за тем, чтобы молодой барин в силу своей неопытности не попал в какую-либо передрягу, оберегал его от проблем, контролировал расходы.
Во время взятия Белогорской крепости Савельич показал себя самоотверженным, верным слугой, готовым отдать собственную жизнь ради спасения Петра. Он бесстрашно просил о пощаде барина у самого Пугачёва, и только благодаря ему Пётр остался в живых.

Образ Савельича
В образе Савельича автор смог воплотить лучшие качества широкой русской души, своеобразие характера простого русского народа. Он чрезвычайно упрям, его практически невозможно переспорить, однако за этим кроется твёрдость, несгибаемость его натуры, вера в то, что он делает всё правильно, по совести.
В основе упрямства Савельича лежит его искренняя забота о благополучии молодого барина. Верный слуга всю свою жизнь положил на то, чтобы вырастить Петрушу Гринёва, защитить его от житейских бурь, злых людей, вывести подготовленным во взрослую жизнь.
В образе Савельича переплетаются противоречивые, на первый взгляд, качества: подозрительность, скупость, великодушие, самоотверженность. Но это несоответствие обусловлено отношением Савельича к Петру: он считает его не просто воспитанником, а родным сыном, которого нужно и пожурить при случае, и поддержать, и наставить на путь истинный. Пётр Гринёв чувствует безусловную любовь и преданность Савельича и считает его своим другом, на которого всегда можно положиться в трудную минуту.

1) Савельич - верный слуга и няня в семье помещиков Гриневых. Он заботится о Гриневе с момента его рождения и является почти как член семьи.

2) Характер Савельича проявляется через его преданность, заботу и отвагу. Он обладает сильным характером, мудростью и стойкостью.

3) Савельич попадает в несколько ситуаций выбора, например, когда ему приходится решить, как поступить во время бунта Пугачева. Он всегда выбирает верный и справедливый путь, действуя в интересах своих хозяев.

4) Гринев и другие герои романа относятся к Савельичу с уважением и признанием его преданности и доброты. Автор также высоко ценит Савельича, показывая его как пример нравственности и человечности.

5) Речь Савельича характеризуется простотой, но в то же время в ней присутствуют мудрость и глубина мысли. Он использует простые выражения, но способен передать сложные идеи и эмоции.

6) Савельич - бескорыстно любящий человек, который готов пожертвовать своим счастьем и благополучием ради блага других. Он преданный холоп, но его преданность и любовь идут далеко за рамки обычной службы.

7) Личное отношение к Савельичу может быть положительным, так как его образ символизирует верность, доброту и преданность. Он воплощает идеалы нравственности и героизма, заслуживая уважение и восхищение.'''
text_hastory_kinf = '''Конфуцианство в Китае:

Конфуцианство - философская и социальная система, возникшая в Китае и оказавшая значительное влияние на культуру и общество. Основанная на учениях Конфуция, она подчеркивает важность моральных ценностей, гармонии в обществе и роли правителя как мудрого и добродетельного лидера.

Конфуцианство акцентирует внимание на пяти ключевых отношениях: отношениях между правителем и подданными, отцом и сыном, мужем и женой, старшим и младшим братьями, а также между друзьями. Оно подчеркивает важность этих отношений для гармонии и благополучия общества.

В конфуцианской традиции уделяется внимание образованию и развитию личности. Ученики должны стремиться к знанию, мудрости и самосовершенствованию. Конфуцианство также признает важность ритуалов и этикета в общении и поведении.

В современном Китае конфуцианство продолжает играть значительную роль в культуре и образовании. Оно способствует формированию устойчивых социальных связей, уважению к авторитету и поддержанию гармоничного баланса между обществом и индивидуумом.'''
def loging(logger_level: str, user_id: str, do: str):
    current_time = datetime.now().strftime('%H:%M:%S')
    if logger_level == 'INFO':
        print('%-15s %-20s %-15s %-10s' % (green+f'[{logger_level}]', purple+f'{user_id}', blue+f'{current_time}', normal+f'{do}'))
    elif logger_level == 'WARN':
        print('%-15s %-20s %-15s %-10s' % (yellow+f'[{logger_level}]', purple+f'{user_id}', blue+f'{current_time}', normal+f'{do}'))
    elif logger_level == 'ERROR':
        print('%-15s %-20s %-15s %-10s' % (red+f'[{logger_level}]', purple+f'{user_id}', blue+f'{current_time}', normal+f'{do}'))
    else:
        print(red+f'ERROR: Unknown logger_level {logger_level}'+normal)
        bot.send_message(config.admin_id_1, f'ERROR: Unknown logger_level {logger_level}')
        exit(1)


print('[FORMAN]   [ID]             [TIME]    [DO]')
loging(logger_level='INFO', user_id='nope', do='The bot is running . . .')
sleep(1)

def db_error(Error):
    now = datetime.now()
    current_time = now.strftime('%H:%M:%S')
    print(Error)  # Вывод к консоль
    bot.reply_to(config.admin_id_1, f'Ошибка подключения к SQLite\nName database = \'{config.name_database}\'')  # Вывод админу
    log_name = f'log_error_connection_sql_database_{current_time}.log'  # имя лог файла
    log = open(str(log_name), 'w')
    log.write(f'Time: {current_time}\n\nERROR: {Error}')
    log.close()
    sleep(1)
    bot.send_message(config.admin_id_1, f'log сохранён в файле {log_name}\nРабота бота преостановлена!\n<u><i>Завершение работы через 10 минут!</i></u>', parse_mode='HTML')
    sleep(5)
    bot.close()
    sleep(600)
    exit(1)


try:
    loging(logger_level='INFO', user_id='none', do='Connecting to db . . .')
    sleep(1)
    conn = sqlite3.connect(config.name_database, check_same_thread=False)
    loging(logger_level='INFO', user_id='none', do='Create a course . . .')
    sleep(1)
    cursor = conn.cursor()
except Exception as Error:
    db_error(Error)

def db_table_val(user_id: int, user_name: str, user_surname: str, username: str,  user_lang: str, user_phone_number: str):
    loging(logger_level='INFO', user_id=f'{user_id}', do='Adding data to db . . .')
    cursor.execute(
        'INSERT OR REPLACE INTO users (user_id, user_name, user_surname, username, user_lang, user_phone_number) VALUES (?, ?, ?, ?, ?, ?)',
        (user_id, user_name, user_surname, username, user_lang, user_phone_number))
    conn.commit()

def db_table_user_location(user_id: int, user_location: str, latitude: str, longitude: str):
    loging(logger_level='INFO', user_id=f'{user_id}', do='Adding user_location in db . . .')
    cursor.execute('UPDATE users SET user_location=? WHERE user_id=?', (user_location, user_id))
    loging(logger_level='INFO', user_id=f'{user_id}', do='Adding latitude in db . . .')
    cursor.execute('UPDATE users SET latitude=? WHERE user_id=?', (latitude, user_id))
    loging(logger_level='INFO', user_id=f'{user_id}', do='Adding longitude in db . . .')
    cursor.execute('UPDATE users SET longitude=? WHERE user_id=?', (longitude, user_id))
    conn.commit()


def status_text(message):
    loging(logger_level='INFO', user_id=f'{message.chat.id}', do='Send status . . .')
    bot.send_chat_action(message.chat.id, action='typing')


@bot.message_handler(commands=['start'])
def start(message):
    loging(logger_level='INFO', user_id=f'{message.chat.id}', do='Received \'/start\'')
    if message.chat.id == config.admin_id_1 or message.chat.id == config.admin_id_2 or message.chat.id == config.admin_id_3:
        status_text(message)
        loging(logger_level='INFO', user_id=f'{message.chat.id}', do='Admin pressed \'/start\'')
        bot.send_message(message.chat.id, f'Для доступа к админ панели введите: \n/{config.commands_admin}')
        bot.send_message(message.chat.id, text_start, reply_markup=markup_start)
    else:
        status_text(message)
        loging(logger_level='INFO', user_id=f'{message.chat.id}', do='User pressed \'/start\'')
        bot.send_message(message.chat.id, 'Add the necessary data for the bot to work properly.\n⚙ Send your phone number to continue.', reply_markup=markup_send_nummer)


@bot.message_handler(content_types=['contact'])
def contact(message):
    if message.contact is not None:
        loging(logger_level='INFO', user_id=f'{message.chat.id}', do='Received \'[contact]\'')
        try:
            db_table_val(user_id=message.from_user.id, user_name=message.from_user.first_name, user_surname=message.from_user.last_name, username=message.from_user.username, user_lang=message.from_user.language_code, user_phone_number=message.contact.phone_number)
            status_text(message)
            # bot.send_message(message.chat.id, '⚙ Send your geolocation to continue.', reply_markup=markup_send_geolocation)
            bot.send_message(message.chat.id, text_start, reply_markup=markup_start)
        except Exception as Error:
            db_error(Error)


@bot.message_handler(content_types=['location'])
def location(message):
    if message.location.latitude and message.location.longitude is not None:
        loging(logger_level='INFO', user_id=f'{message.chat.id}', do='Received \'[location]\'')
        try:
            db_table_user_location(user_id=message.chat.id, user_location=f'Широта: {message.location.latitude} Долгота: {message.location.longitude}', latitude=message.location.latitude, longitude=message.location.longitude)
            status_text(message)
            bot.send_message(message.chat.id, text_start, reply_markup=markup_start)
        except Exception as Error:
            db_error(Error)


@bot.message_handler(content_types=['text'])
def logic(message):
    if message.text == '1️⃣':
        status_text(message)
        bot.send_message(message.chat.id, 'Nope')
    elif message.text == '2️⃣':
        status_text(message)
        bot.send_message(message.chat.id, 'Nope')
    elif message.text == '3️⃣':
        status_text(message)
        bot.send_message(message.chat.id, text3)
        # Admin Panel
    elif message.text == '4️⃣':
        status_text(message)
        bot.send_message(message.chat.id, text4)
    elif message.text == '5️⃣':
        status_text(message)
        bot.send_message(message.chat.id, text51)
        bot.send_message(message.chat.id, text52)
        bot.send_message(message.chat.id, text53)
        bot.send_message(message.chat.id, text54)
    elif message.text == 'История (Конфуцианство в Китае)':
        status_text(message)
        bot.send_message(message.chat.id, text_hastory_kinf)
    elif message.text == f'/{config.commands_admin}':
        if message.chat.id == config.admin_id_1 or message.chat.id == config.admin_id_2 or message.chat.id == config.admin_id_3:
            status_text(message)
            loging(logger_level='WARN', user_id=message.chat.id, do='Admin logged into the panel . . .')
            bot.send_message(message.chat.id, '''🛠Вы в админ-панели!\nБудте осторожны‼️''', reply_markup=markup_admin_panel)
        else:
            status_text(message)
            loging(logger_level='WARN', user_id=f'{message.chat.id}', do='❌ Error: You do not have access to this command ! ❌')
            bot.send_message(message.chat.id, '❌ Error: You do not have access to this command ! ❌')
    elif message.text == 'Перезагрузка 🔄':
        if message.chat.id == config.admin_id_1 or message.chat.id == config.admin_id_2 or message.chat.id == config.admin_id_3:
            status_text(message)
            bot.send_message(message.chat.id, '⚠️ Бот будет перезагружен !\n\nПодождите ~20 секунд.')
            loging(logger_level='WARN', user_id=message.chat.id, do='Admin will reboot the bot . . .')
            loging(logger_level='INFO', user_id=message.chat.id, do='Saving data to db . . .')
            conn.commit()
            loging(logger_level='WARN', user_id=message.chat.id, do='Disconnect from db . . .')
            conn.close()
            loging(logger_level='INFO', user_id=message.chat.id, do='Successfully !')
            loging(logger_level='WARN', user_id=message.chat.id, do='Rebooting . . .')
            sleep(1)
            os.system(config.reboot_command)
        else:
            status_text(message)
            loging(logger_level='WARN', user_id=f'{message.chat.id}', do='❌ Error: You do not have access to this command ! ❌')
            bot.send_message(message.chat.id, '❌ Error: You do not have access to this command ! ❌')
    elif message.text == 'Бэкап базы данных 📑':
        if message.chat.id == config.admin_id_1 or message.chat.id == config.admin_id_2 or message.chat.id == config.admin_id_3:
            with open('sql_damp.txt', 'w') as f:
                for sql in conn.iterdump():
                    f.write(sql)
            status_text(message)
            loging(logger_level='WARN', user_id=message.chat.id, do='Admin performs db backup . . .')
            bot.send_message(message.chat.id, '✅Бэкап базы данных готов!\nОтправляю . . .')
            loging(logger_level='WARN', user_id=message.chat.id, do='The backup copy of the database is ready, I’m sending it. . .')
            bot.send_chat_action(message.chat.id, 'upload_document')
            bot.send_document(message.chat.id, document=open('sql_damp.txt', 'rb'))
            sleep(1)
            loging(logger_level='WARN', user_id=message.chat.id, do='Deleting a database backup . . .')
            os.system('rm sql_damp.txt')
        else:
            status_text(message)
            loging(logger_level='WARN', user_id=f'{message.chat.id}', do='❌ Error: You do not have access to this command ! ❌')
            bot.send_message(message.chat.id, '❌ Error: You do not have access to this command ! ❌')
    elif message.text == 'Статус сервера 🛠️':
        if message.chat.id == config.admin_id_1 or message.chat.id == config.admin_id_2 or message.chat.id == config.admin_id_3:
            loging(logger_level='INFO', user_id=message.chat.id, do='Аdmin requested a server status report, generation . . .')
            status_text(message)
            import platform
            import psutil
            loging(logger_level='INFO', user_id=message.chat.id, do='Generating information about: SystemName')
            SystemName = str(platform.system())
            loging(logger_level='INFO', user_id=message.chat.id, do='Generating information about: SystemRelease')
            SystemRelease = str(platform.release())
            loging(logger_level='INFO', user_id=message.chat.id, do='Generating information about: PythonVersion')
            PythonVersion = str(platform.python_version())
            loging(logger_level='INFO', user_id=message.chat.id, do='Generating information about: Compiler')
            Compiler = str(platform.python_compiler())
            # Загруженость
            # CPU
            loging(logger_level='INFO', user_id=message.chat.id, do='Generating information about: CPU, CPU_stats')
            cpu = psutil.cpu_times()
            cpu_stats = psutil.cpu_stats()
            # Memory
            loging(logger_level='INFO', user_id=message.chat.id, do='Generating information about: Memory_Virtual, Memory_Swap')
            Memory_Virtual = psutil.virtual_memory()
            Memory_Swap = psutil.swap_memory()
            # Disks
            loging(logger_level='INFO', user_id=message.chat.id, do='Generating information about: Disks')
            Disks = psutil.disk_io_counters()
            # Network
            loging(logger_level='INFO', user_id=message.chat.id, do='Generating information about: Network')
            Network = psutil.net_if_addrs()
            loging(logger_level='INFO', user_id=message.chat.id, do='Generating a report based on the data received . . .')
            info = f'''OS: {SystemName} {SystemRelease}
Python: {PythonVersion} Version
Server: {Compiler}
-------------------
Загруженость:
#~CPU~#
CPU: {cpu}
CPU Stats: {cpu_stats}
#~MEMORY~#
Memory Virtual: = {Memory_Virtual}
Memory Swap: = {Memory_Swap}
#~DISKS~#
Disks: {Disks}
#~NETWORK~#
Network: = {Network}'''
            loging(logger_level='INFO', user_id=message.chat.id, do='Successfully !')
            status_text(message)
            loging(logger_level='INFO', user_id=message.chat.id, do='Report Sent !')
            bot.send_message(message.chat.id, info)
        else:
            status_text(message)
            loging(logger_level='WARN', user_id=f'{message.chat.id}', do='❌ Error: You do not have access to this command ! ❌')
            bot.send_message(message.chat.id, '❌ Error: You do not have access to this command ! ❌')
    else:
        status_text(message)
        loging(logger_level='INFO', user_id=f'{message.chat.id}', do=f'❌ The command was not found ! ❌ text:[\'{message.text}\']')
        bot.send_message(message.chat.id, '❌ Error: The command was not found ! ❌')


loging(logger_level='INFO', user_id='nope', do='Sending notifications to admins . . .')
sleep(1)

bot.send_message(config.admin_id_1, f'⚠Бот запущен!⚠\nДля доступа к админ панели введите: \n/{config.commands_admin}')
bot.send_message(config.admin_id_2, f'⚠Бот запущен!⚠\nДля доступа к админ панели введите: \n/{config.commands_admin}')
bot.send_message(config.admin_id_3, f'⚠Бот запущен!⚠\nДля доступа к админ панели введите: \n/{config.commands_admin}')


if __name__ == '__main__':
    bot.infinity_polling(none_stop=True, long_polling_timeout=60, logger_level=1, interval=0)  # Запуск бота
