"""
handlers/menu.py — Бас мәзір обработчиктері
Тіл: Таза, дұрыс, мұғалімдік қазақ тілі
"""
import os
import random
import datetime
from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup,
    ReplyKeyboardMarkup, KeyboardButton
)
try:
    from telegram import WebAppInfo
    HAS_WEBAPP = True
except ImportError:
    HAS_WEBAPP = False
from telegram.ext import CallbackContext
from database import get_or_create_user, get_level_info

# Webapp URL конфигурациясы
WEBAPP_URL        = os.getenv('WEBAPP_URL', '').strip()
KOYEB_BASE        = 'https://controversial-rosaleen-t44t-00f78407.koyeb.app'

def get_webapp_url():
    """Mini App URL — әрқашан дұрыс https URL қайтарады"""
    url = WEBAPP_URL
    if url:
        if not url.startswith('https://'):
            url = 'https://' + url.lstrip('http://')
        if url.endswith('/health'):
            url = url.replace('/health', '/app')
        if not url.endswith('/app'):
            url = url.rstrip('/') + '/app'
        return url
    return KOYEB_BASE + '/app'


# Күнделікті қызықты деректер — таза қазақ тілінде
DAILY_FACTS = [
    "💡 Абайдың шын есімі — Ибраһим. «Абай» лақап атын сүйіктілі алтын шәкіртіне оның әжесі Зере берген!",
    "💡 Жамбыл Жабаев 99 жыл өмір сүрді — қазақ ақындарының ішіндегі ең ұзақ ғұмырлысы!",
    "💡 «Абай жолы» роман-эпопеясы дүние жүзіндегі 100-ден аса тілге аударылды!",
    "💡 Ахмет Байтұрсынов 1912 жылы қазақ жазуын реформалап, латын негізінде жаңа алфавит жасады!",
    "💡 Сәкен Сейфуллин, Беймбет Майлин, Ілияс Жансүгіров — үшеуі де 1938 жылы Сталиндік репрессияның құрбаны болды!",
    "💡 Мұхтар Әуезов өмірінде 50-ден астам пьеса жазды — қазақ драматургиясының алыбы!",
    "💡 «Абай жолы» роман-эпопеясы 1959 жылы Лениндік сыйлыққа ие болды!",
    "💡 Ыбырай Алтынсарин Қазақстанда алғашқы 4 орыс-қазақ мектебін ашқан ұлы ағартушы!",
    "💡 Мағжан Жұмабаев репрессияға ұшырап, 1938 жылы атылды. Тек 1960 жылдары ғана ақталды!",
    "💡 Сұлтанмахмұт Торайғыров небәрі 27 жасында өкпе ауруынан дүниеден өтті, бірақ мол мұра қалдырды!",
    "💡 Бауыржан Момышұлы Мәскеу шайқасында (1941) ерлік көрсетіп, Кеңес Одағының Батыры атанды!",
    "💡 «Қозы Көрпеш — Баян сұлу» — дүние жүзіндегі ең ежелгі сүйіспеншілік жырларының бірі саналады!",
    "💡 Абай Пушкиннің «Евгений Онегин» поэмасынан «Татьянаның хатын» қазақшаға алғаш аударған!",
    "💡 Жамбыл Жабаев домбырасын серік етіп, айтыс өнерінде ешкімге жеңіліс бермеген жыр алыбы!",
    "💡 Алаш зиялылары 1917 жылы Алаш автономиясын жариялап, қазақ мемлекеттігін қалпына келтіруге ұмтылды!",
    "💡 Шәкәрім Құдайбердіұлы — ақын ғана емес, философ, тарихшы, аудармашы. Ол «Мұсылмандық шарты» еңбегін жазды!",
    "💡 Мұқағали Мақатаев «өлеңді ауаша жазам» деген — оның лирикасы қазақ жастарының жүрегіне жол тапты!",
    "💡 Іле Есенберлиннің «Көшпенділер» трилогиясы қазақтың мыңжылдық тарихын суреттейді!",
]

MAIN_MENU_TEXT = (
    "<b>📚 ҚАЗАҚ ӘДЕБИЕТІ — БІЛІМ КІТАПХАНАСЫ</b>\n\n"
    "🎓 5-11 сынып қазақ әдебиеті — тақырыптар, авторлар, сұрақ-жауап\n\n"
    "👇 <b>Бөлімді таңдаңыз:</b>"
)


def _open_app_reply_kb(webapp_url: str):
    """
    Чат төменгі жағындағы «Open App» батырмасы.
    Суреттегі сияқты — input жолының үстінде тұрады.
    """
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(
                text="🎮  Open App",
                web_app=WebAppInfo(url=webapp_url)
            )]
        ],
        resize_keyboard=True,          # кішірек, ықшам
        input_field_placeholder="Бөлімді таңдаңыз..."
    )


def _build_inline_menu():
    """Inline мәзір батырмалары (хабарлама ішінде)"""
    from utils.keyboards import main_menu_keyboard
    return main_menu_keyboard()


def start_command(update: Update, context: CallbackContext):
    """Бот іске қосылғанда немесе /start командасы"""
    user    = update.effective_user
    db_user = get_or_create_user(user.id, user.username, user.full_name)
    level   = db_user.get('level', 1)
    emoji, name = get_level_info(level)
    points  = db_user.get('points', 0)
    streak  = db_user.get('streak', 0)
    webapp_url = get_webapp_url()

    streak_txt = f"🔥 {streak} күндік серпіліс!\n" if streak > 1 else ""

    welcome = (
        f"🎓 <b>Қош келдіңіз, {user.first_name}!</b>\n\n"
        f"{emoji} Деңгей: <b>{name}</b>\n"
        f"⭐ Жинаған ұпай: <b>{points}</b>\n"
        f"{streak_txt}\n"
        f"<b>📚 ҚАЗАҚ ӘДЕБИЕТІ — БІЛІМ КІТАПХАНАСЫ</b>\n\n"
        f"🎓 5–11 сынып қазақ әдебиеті — тақырыптар, авторлар, сұрақ-жауап\n\n"
        f"👇 <b>Бөлімді таңдаңыз:</b>"
    )

    # Inline мәзір әрдайым шығады
    update.message.reply_text(
        welcome.strip(),
        parse_mode='HTML',
        reply_markup=_build_inline_menu()
    )


def main_menu_callback(update: Update, context: CallbackContext):
    """Бас мәзірге оралу"""
    query = update.callback_query
    query.answer()
    user    = update.effective_user
    db_user = get_or_create_user(user.id, user.username, user.full_name)
    level   = db_user.get('level', 1)
    emoji, name = get_level_info(level)
    points  = db_user.get('points', 0)

    text = (
        f"{emoji} <b>{name}</b>  |  ⭐ {points} ұпай\n\n"
        f"📚 <b>ҚАЗАҚ ӘДЕБИЕТІ — БІЛІМ КІТАПХАНАСЫ</b>\n"
        f"👇 <b>Бөлімді таңдаңыз:</b>"
    )
    query.edit_message_text(
        text.strip(), parse_mode='HTML',
        reply_markup=_build_inline_menu()
    )





def daily_fact_callback(update: Update, context: CallbackContext):
    """Күнделікті қызықты дерек"""
    query = update.callback_query
    query.answer()
    day_idx = datetime.date.today().toordinal() % len(DAILY_FACTS)
    fact = DAILY_FACTS[day_idx]
    from utils.keyboards import back_to_main
    query.edit_message_text(
        f"📅 <b>БҮГІНГІ ДЕРЕКТАМАЛЫҚ МӘЛІМЕТ</b>\n\n"
        f"{fact}\n\n"
        f"<i>Ертең жаңа дерек күтеді! Білімге деген ынта — жеңістің кілті!</i> 😊",
        parse_mode='HTML',
        reply_markup=back_to_main()
    )


def help_callback(update: Update, context: CallbackContext):
    """Анықтама"""
    query = update.callback_query
    query.answer()
    from utils.keyboards import back_to_main
    help_text = (
        "ℹ️ <b>АНЫҚТАМА — Қалай пайдалану керек?</b>\n\n"
        "📖 <b>САБАҚТАР (1–11 сынып)</b>\n"
        "   Сыныбыңды таңда → Тақырыпты оқы → Ұпай жина!\n\n"
        "🎮 <b>ОЙЫНДАР — 6 түрлі</b>\n"
        "   🎯 Викторина — 4 нұсқалы сұрақтар\n"
        "   ✍️ Кім жазды? — шығарманың авторын тап\n"
        "   📚 Шығарманы тап! — авторынан шығармасын тап\n"
        "   💬 Цитата жарысы — дәйексөзді кімнікі екенін айт\n"
        "   ⚡ Блиц-тур — жылдам жауап (20 сек)\n"
        "   👥 Кейіпкерлер — кейіпкерді шығармасына сай\n\n"
        "👤 <b>АВТОРЛАР</b>\n"
        "   20+ авторлардың өмірбаяны, шығармалары, цитаталары\n\n"
        "📊 <b>МЕНІҢ ПРОГРЕСІМ</b>\n"
        "   Ұпайлар, деңгей, стрик, жетістіктер\n\n"
        "🏆 <b>РЕЙТИНГ</b>\n"
        "   Үздік оқушылар кестесі\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "💰 <b>Ұпай жүйесі:</b>\n"
        "   • Дұрыс жауап → <b>+10 ұпай</b>\n"
        "   • Тақырып аяқтауы → <b>+15 ұпай</b>\n"
        "   • Автор биографиясын оқу → <b>+5 ұпай</b>\n"
        "   • Мінсіз викторина (10/10) → <b>+50 бонус</b>\n\n"
        "🎓 <b>Деңгейлер:</b> Оқушыдан → Қазақ Әдебиеті Ұстасына дейін 11 деңгей!"
    )
    query.edit_message_text(help_text, parse_mode='HTML', reply_markup=back_to_main())
