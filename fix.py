import re
with open('C:/Users/USUARIO/Documents/savalgarciabogados/blog/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

content = re.sub(r'link:\s*"(.*?)/index\.html"', r'slug: "\1"', content)

with open('C:/Users/USUARIO/Documents/savalgarciabogados/blog/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
