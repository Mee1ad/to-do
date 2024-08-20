from fasthtml import Script
from fasthtml.common import fast_app

tailwind = Script(src="https://cdn.tailwindcss.com")
app, rt = fast_app(hdrs=(tailwind,), debug=True, live=True, reload_interval=1, pico=False)
