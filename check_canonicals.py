
import os
import re

base_dir = '.'
error_count = 0

for root, dirs, files in os.walk(base_dir):
    for file in files:
        if file.endswith('.html') and file != '404.html' and not file.startswith('google'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
            match = re.search(r'<link rel="canonical" href="([^"]+)">', content)
            if match:
                canonical_url = match.group(1)
                
                rel_path = os.path.relpath(filepath, base_dir).replace(os.sep, '/')
                if rel_path.startswith('blog/') and rel_path.endswith('/index.html') and rel_path != 'blog/index.html':
                    folder = rel_path.split('/')[1]
                    expected_url = f'https://www.savalgarciaabogados.es/blog/{folder}/'
                elif rel_path == 'blog/index.html':
                    expected_url = 'https://www.savalgarciaabogados.es/blog/'
                elif rel_path == 'index.html':
                    expected_url = 'https://www.savalgarciaabogados.es/'
                else:
                    expected_url = f'https://www.savalgarciaabogados.es/{rel_path}'
                
                if canonical_url != expected_url:
                    print(f'MISMATCH in {rel_path}:')
                    print(f'  Found:    {canonical_url}')
                    print(f'  Expected: {expected_url}')
                    error_count += 1

if error_count == 0:
    print('All canonical tags match their expected URLs perfectly!')

