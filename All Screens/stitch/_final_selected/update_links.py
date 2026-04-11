import os
import re

directory = r'c:\Users\shobhit.sharma\Downloads\AI First banker analysis\All Screens\stitch\_final_selected'
files = [f for f in os.listdir(directory) if f.endswith('.html')]

mappings = {
    'Dashboard': '01_dashboard.html',
    'Customers': '02_customer_360.html',
    'Meetings': '03_ai_meeting_brief.html',
    'Follow-ups': '04_post_meeting_follow_up.html',
    'Documents': '05_documents_workbench.html'
}

for file in files:
    filepath = os.path.join(directory, file)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    for name, link in mappings.items():
        pattern = re.compile(r'(href=)"#"(>[\s\S]{1,300}?<span[^>]*>' + name + r'<\/span>)', re.IGNORECASE)
        content = pattern.sub(r'\g<1>"' + link + r'"\g<2>', content)
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print(f'Updated {len(files)} files!')
