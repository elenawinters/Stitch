from enum import Enum, auto
from core.ext import assets


class ReturnType(Enum):
    default = 'UnknownReturn'
    success = 'ReturnSuccess'
    error = 'ReturnError'
    fail = 'ReturnFail'
    none = 'ReturnNone'


class CommandArgs(Enum):
    default = 'UnknownArgument'
    optional = 'OptionalArgument'
    error = 'ArgumentError'
    fail = 'ArgumentFail'
    none = 'NoArgument'


class LogLevel(Enum):
    silent = 0  # Reworked loglevels
    info = auto()  # 1
    warn = auto()  # 2
    error = auto()  # 3
    fatal = auto()  # 4
    debug = auto()  # 5

    # silent = 0
    # fatal = auto()  # 1
    # error = auto()  # 2
    # warn = auto()  # 3
    # info = auto()  # 4
    # debug = auto()  # 5

    # Aliases
    none = silent
    panic = silent
    quiet = silent
    warning = warn
    information = info
    verbose = info
    default = info
    normal = info
    dbg = debug

    # Backwards compatibility
    calm = info
    extra = info
    errors = warn
    critical = fatal
    all = debug


# class LogLevel(Enum):
#     silent      = 'LogSilent'
#     default     = 'LogDefault'
#     warn        = 'LogWarnings'
#     errors      = 'LogErrors'
#     debug       = 'LogDebug'
#     warning = warn
#     error = errors
#     quiet = silent


class MusicTests(Enum):  # Will be removed soon.
    voyager = 'https://www.youtube.com/watch?v=L6zulqXLPUw'  # Melodysheep - Children of Planet Earth: The Voyager Golden Record Remixed - Symphony of Science
    sammy = 'https://www.youtube.com/playlist?list=PL9Hp6xxvWgsygoIy6shbakwjpKpQS8PqK'  # Sammy Copley - All Music
    tls_tests = 'https://www.youtube.com/playlist?list=PLPh99DH836cgK3bJsNeBRMOAejTdQEqkt'  # BFR Test Playlist
    test2 = 'https://www.youtube.com/playlist?list=PLPh99DH836ciH5Xkd8Pmsorj0aD0vIxRx' # Test playlist 2
    top40 = 'https://www.youtube.com/playlist?list=PLgz_Ist_hI3rW43lLctvLjd2zHEfNVG5_'  # Top 40, 2000-2016
    dream = 'https://soundcloud.com/elenawinters/the-final-dream'  # Elena Winters - The Final Dream
    bad_apple = 'https://www.youtube.com/watch?v=j8wZXyR2SUM'  # The Musical Ghost - Bad Apple!!
    rexha = 'https://www.youtube.com/watch?v=g6xvHG8nd5U'  # Bebe Rexha - The Way I Dance
    billie = 'https://www.youtube.com/watch?v=gBRi6aZJGj4'  # Billie Eilish - Bellyache
    queen = 'https://www.youtube.com/watch?v=MhkPWV97GQU'  # Queen - Bohemian Rhapsody
    dane = 'https://www.youtube.com/watch?v=4l5qmoe9CNA'  # Dapper Dog - Frontier Justice (Uncle Dane Theme)
    gone = 'https://www.youtube.com/watch?v=dVVZaZ8yO6o'  # Jonathan Coulton - Want You Gone
    hate = 'https://www.youtube.com/watch?v=07Ir2A0pNI8'  # dot.darkness - I Don't Hate You [Portal Parts I and II]
    piano_man = 'https://www.youtube.com/watch?v=acJ-Wt3rpfc'  # Billy Joel - Piano Man
    sammy_man = 'https://www.youtube.com/watch?v=ujpGtwPMnso'  # Billy Joel - Piano Man (Sammy Copley Cover)
    darkness_og = 'https://www.youtube.com/watch?v=4fWyzwo1xg0'  # Simon & Garfunkel - The Sounds of Silence
    disturbed = 'https://www.youtube.com/watch?v=_gRsZqSNvKU'  # Disturbed - The Sound of SIlence
    mess = 'https://www.youtube.com/watch?v=LdH7aFjDzjI'  # Bebe Rexha - I'm A Mess
    ladykiller = 'https://www.youtube.com/watch?v=P2rT2vw9i_k'  # G-Eazy - Lady Killers ft. Hoodie Allen
    greatest = 'https://www.youtube.com/watch?v=GKSRyLdjsPA'  # Sia - The Greatest
    intoxicated = 'https://www.youtube.com/watch?v=94Rq2TX0wj4'  # Martin Solveig & GTA - Intoxicated
    happier = 'https://www.youtube.com/watch?v=QGtPHnCBH3w'  # Marshmello ft. Bastille - Happier (Stripped)
    hotline = 'https://www.youtube.com/watch?v=cycUHgg0zzU'  # Logic - 1-800-273-8255 ft. Alessia Cara & Khalid
    suicide = 'https://www.youtube.com/watch?v=Wc76Ber-OS8'  # James Arthur - Suicide
    retrograde = 'https://www.youtube.com/watch?v=XClvMMxBg1k'  # James Blake - Retrograde
    rich = 'https://www.youtube.com/watch?v=25ngvtk1k7w'  # Cosmo Sheldrake - Rich (Ft. Anndreyah Vargas)
    darkness = darkness_og
    piano = piano_man
    apple = bad_apple
    test = tls_tests
    bebe = rexha


class SoundFiles(Enum):
    connect = 'cogs\\music\\media\\connect.mp3'
    singing = 'cogs\\music\\media\\singing.mp3'


ImageURLs = assets.Discord
DiscordAvatars = assets.Discord.Avatars
