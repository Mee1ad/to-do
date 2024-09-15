from fasthtml import Script
from fasthtml.common import fast_app, Link, Style

from middleware.session import RedisSessionMiddleware
from settings import env

tailwind = Script(src="https://cdn.tailwindcss.com")
feather_icons = Script(src='https://unpkg.com/feather-icons')
tailwind_settings = Script(src="tailwind.config.js")
sortable = Script(src="https://cdn.jsdelivr.net/npm/sortablejs@latest/Sortable.min.js")
global_css = Link(rel="stylesheet", href="global.css", type="text/css")
font_inter = Link(rel="stylesheet", href="https://rsms.me/inter/inter.css")
css = Style('body { font-family: Inter var, sans;}')

debug = True
live = True


if env.stage.lower() == 'prod':
    debug = False
    live = False

app, rt = fast_app(
    hdrs=(tailwind, tailwind_settings, global_css, font_inter, css, feather_icons, sortable),
    debug=debug, live=live, reload_interval=1, pico=False,
)

app.add_middleware(RedisSessionMiddleware)
