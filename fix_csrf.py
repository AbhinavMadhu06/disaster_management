import re

urls_file = r'd:\untitled3\myapp\urls.py'
views_file = r'd:\untitled3\myapp\views.py'

with open(urls_file, 'r', encoding='utf-8') as f:
    text = f.read()

flutter_section = text.split('# 📱 FLUTTER API ENDPOINTS')[1]
views_to_exempt = re.findall(r"views\.([a-zA-Z0-9_]+)", flutter_section)

with open(views_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

count = 0
for view in set(views_to_exempt):
    for i, line in enumerate(lines):
        if line.startswith(f"def {view}("):
            if i > 0 and "@csrf_exempt" not in lines[i-1]:
                lines.insert(i, "@csrf_exempt\n")
                count += 1
            break

with open(views_file, 'w', encoding='utf-8') as f:
    f.write("".join(lines))

print(f"Applied @csrf_exempt to {count} additional endpoints out of {len(set(views_to_exempt))} total.")
