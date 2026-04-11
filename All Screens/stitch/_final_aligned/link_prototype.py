import os
import re

base_dir = r"c:\Users\shobhit.sharma\Downloads\AI First banker analysis\All Screens\stitch\_final_aligned"
files = ["01_dashboard.html", "02_customer_360.html", "03_ai_meeting_brief.html", "04_post_meeting_follow_up.html", "05_documents_workbench.html"]

link_map = {
    "dashboard": "01_dashboard.html",
    "groups": "02_customer_360.html",
    "calendar_today": "03_ai_meeting_brief.html",
    "description": "05_documents_workbench.html",
    "shortcut": "04_post_meeting_follow_up.html"
}

file_to_icon = {
    "01_dashboard.html": "dashboard",
    "02_customer_360.html": "groups",
    "03_ai_meeting_brief.html": "calendar_today",
    "04_post_meeting_follow_up.html": "shortcut",
    "05_documents_workbench.html": "description"
}

inactive_class = "cursor-pointer hover:translate-x-1 transform transition-transform text-slate-500 dark:text-slate-400 flex items-center gap-3 px-4 py-3 hover:text-blue-600 dark:hover:text-blue-300 transition-all duration-200"
active_class = "cursor-pointer hover:translate-x-1 transform transition-transform text-blue-700 dark:text-blue-400 font-bold bg-white dark:bg-slate-950/50 rounded-md flex items-center gap-3 px-4 py-3 transition-all duration-200"

def set_attr(tag, attr, value):
    attr_pattern = rf'\b{attr}="[^"]*"'
    if re.search(attr_pattern, tag):
        return re.sub(attr_pattern, f'{attr}="{value}"', tag, count=1)
    return re.sub(r'(/?>)$', f' {attr}="{value}"\\1', tag)

for filename in files:
    path = os.path.join(base_dir, filename)
    if not os.path.exists(path):
        continue
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    for icon, target in link_map.items():
        pattern = re.compile(rf'(<a\b[^>]*?)(?=[^>]*?data-icon="{re.escape(icon)}")', re.IGNORECASE | re.DOTALL)
        content = pattern.sub(lambda m, t=target: set_attr(m.group(0), "href", t), content)
        cls = active_class if file_to_icon.get(filename) == icon else inactive_class
        content = pattern.sub(lambda m, c=cls: set_attr(m.group(0), "class", c), content)
    
    content = content.replace("scale 0.98x", "")
    content = re.sub(r'<span class="[^"]*font-bold[^"]*" data-icon="dashboard">', '<span class="material-symbols-outlined" data-icon="dashboard">', content)
    
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

print("Linked all screens and applied active states successfully.")
