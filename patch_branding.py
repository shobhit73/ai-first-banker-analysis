import re

NEW_HEADER = (
    '<div class="mb-10 px-4 flex flex-col gap-3">\n'
    '<img src="assets/sovereign_logo.png" alt="Sovereign Ledger" class="w-12 h-12 object-contain rounded-lg">\n'
    '<div>\n'
    '<h1 class="text-lg font-black tracking-tighter text-slate-900 dark:text-white uppercase leading-none">Sovereign Ledger</h1>\n'
    '<p class="font-inter text-[10px] font-bold antialiased text-slate-500 dark:text-slate-400 uppercase tracking-widest mt-1">Enterprise Terminal</p>\n'
    '</div>\n'
    '</div>'
)

PATTERN = re.compile(
    r'<div class="mb-10 px-4">\s*<h1[^>]*>Sovereign Ledger</h1>\s*<p[^>]*>Enterprise Terminal</p>\s*</div>',
    re.DOTALL
)

FILES = [
    '02_customer_360.html',
    '05_documents_workbench.html',
]

for fname in FILES:
    with open(fname, 'rb') as f:
        raw = f.read()
    # detect encoding
    if raw[:3] == b'\xef\xbb\xbf':
        encoding = 'utf-8-sig'
    elif raw[:2] in (b'\xff\xfe', b'\xfe\xff'):
        encoding = 'utf-16'
    else:
        encoding = 'utf-8'
    content = raw.decode(encoding, errors='replace')
    new_content, count = PATTERN.subn(NEW_HEADER, content, count=1)
    if count:
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'{fname}: PATCHED ({count} replacement)')
    else:
        print(f'{fname}: NO MATCH FOUND')

# --- Special repair for 04_post_meeting_follow_up.html ---
fname04 = '04_post_meeting_follow_up.html'
with open(fname04, 'rb') as f:
    raw = f.read()
content = raw.decode('utf-8', errors='replace')

# The file has broken HTML: style block runs into nav links without closing
# We need to close .tabular-numbers rule, then close style/head, open body/aside, add logo, then open nav
BROKEN = (
        '        .tabular-numbers {\r\n'
        '            font-variant-numeric: tabular-nums;\r\n'
        '<a class="cursor-pointer hover:translate-x-1 transform transition-transform text-slate-500'
)
BROKEN_LF = BROKEN.replace('\r\n', '\n')

FIXED = (
    '        .tabular-numbers {\n'
    '            font-variant-numeric: tabular-nums;\n'
    '        }\n'
    '    </style>\n'
    '</head>\n'
    '<body class="bg-surface text-on-surface flex min-h-screen">\n'
    '<!-- SideNavBar (Shared Component) -->\n'
    '<aside class="fixed inset-y-0 left-0 w-64 z-50 bg-slate-50 dark:bg-slate-900 border-none flex flex-col p-6 space-y-2 overflow-y-auto">\n'
    '<div class="mb-10 px-4 flex flex-col gap-3">\n'
    '<img src="assets/sovereign_logo.png" alt="Sovereign Ledger" class="w-12 h-12 object-contain rounded-lg">\n'
    '<div>\n'
    '<h1 class="text-lg font-black tracking-tighter text-slate-900 dark:text-white uppercase leading-none">Sovereign Ledger</h1>\n'
    '<p class="font-inter text-[10px] font-bold antialiased text-slate-500 dark:text-slate-400 uppercase tracking-widest mt-1">Enterprise Terminal</p>\n'
    '</div>\n'
    '</div>\n'
    '<nav class="flex-1 space-y-1">\n'
    '<a class="cursor-pointer hover:translate-x-1 transform transition-transform text-slate-500'
)

if BROKEN in content:
    content = content.replace(BROKEN, FIXED, 1)
    with open(fname04, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'{fname04}: REPAIRED (CRLF match)')
elif BROKEN_LF in content:
    content = content.replace(BROKEN_LF, FIXED, 1)
    with open(fname04, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'{fname04}: REPAIRED (LF match)')
else:
    # Show what we actually see around line 92-95
    lines = content.splitlines()
    print(f'{fname04}: NO MATCH - showing lines 90-95:')
    for i, line in enumerate(lines[89:96], start=90):
        print(f'  {i}: {repr(line)}')
