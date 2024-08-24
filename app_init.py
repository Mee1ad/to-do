from fasthtml import Script
from fasthtml.common import fast_app, Link, Style

tailwind = Script(src="https://cdn.tailwindcss.com")
tailwind_forms = Script(src="https://cdn.jsdelivr.net/npm/@tailwindcss/forms@0.5.7/src/index.min.js")
font_awesome = Script(src='https://kit.fontawesome.com/0371c877a9.js', crossorigin='anonymous')
tailwind_settings = Script(src="tailwind.config.js")
global_css = Link(rel="stylesheet", href="global.css", type="text/css")
# tailwind_animate = Script(src='https://cdn.jsdelivr.net/npm/tailwindcss-animated@1.1.2/src/index.min.js')
font_inter = Link(rel="stylesheet", href="https://rsms.me/inter/inter.css")
css = Style('body { font-family: Inter var, sans;}')

app, rt = fast_app(hdrs=(tailwind, tailwind_settings, tailwind_forms, global_css, font_inter, css, font_awesome),
                   debug=True, live=True, reload_interval=1, pico=False)
