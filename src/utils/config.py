from os import getenv

secret = getenv('SECRET')
database_url = getenv('DATABASE_URL')
mode = getenv('mode')

csp = {
    'default-src': [
        '\'self\'',
        'https://fonts.googleapis.com/',
        'https://fonts.gstatic.com/',
        'code.getmdl.io',
        'cdn.jsdelivr.net',
        '\'unsafe-inline\'',
        'data:',
    ]
}
