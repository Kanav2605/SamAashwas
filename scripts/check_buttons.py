import re, os

with open('frontend/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

calls = set(re.findall(r'onclick=[\'"]([a-zA-Z0-9_]+)\(', html))

js_content = ''
for p in ['frontend/js/app.js', 'frontend/js/map_view.js', 'frontend/js/sticker_theme.js', 'frontend/js/whatsapp_bot.js']:
    if os.path.exists(p):
        with open(p, 'r', encoding='utf-8') as f:
            js_content += '\n' + f.read()

missing = []
for c in sorted(calls):
    if not (f'function {c}' in js_content or f'window.{c}' in js_content or f'{c} =' in js_content):
        missing.append(c)

print(f'Total unique onclick functions tested: {len(calls)}')
if missing:
    print('MISSING FUNCTIONS:', missing)
    exit(1)
else:
    print('ALL BUTTON ONCLICK HANDLERS ARE FULLY WIRED AND DEFINED!')
