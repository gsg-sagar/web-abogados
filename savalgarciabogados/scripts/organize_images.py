import os
import shutil

blog_dir = 'C:/Users/USUARIO/Documents/savalgarciabogados/blog'
images_dir = os.path.join(blog_dir, 'images')

if not os.path.exists(images_dir):
    os.makedirs(images_dir)

images = ['opcioncompra.webp', 'renta2026image.jpg', 'terceriadominio.webp']

for img in images:
    src = os.path.join(blog_dir, img)
    if os.path.exists(src):
        shutil.move(src, os.path.join(images_dir, img))

html_files = []
for root, dirs, files in os.walk(blog_dir):
    for f in files:
        if f.endswith('.html'):
            html_files.append(os.path.join(root, f))

for html_file in html_files:
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    modified = False
    for img in images:
        if ('../' + img) in content:
            content = content.replace('../' + img, '../images/' + img)
            modified = True
        elif ('"' + img + '"') in content:
            content = content.replace('"' + img + '"', '"images/' + img + '"')
            modified = True
            
    if modified:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
print('Done!')
