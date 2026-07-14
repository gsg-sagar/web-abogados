import os, re

base_dir = r"C:\Users\USUARIO\Documents\savalgarciabogados"

municipios = {
    "abogados-alfaz-del-pi.html": "Alfaz del Pi",
    "abogados-alicante.html": "Alicante",
    "abogados-altea-hills.html": "Altea Hills",
    "abogados-altea.html": "Altea",
    "abogados-beniarda.html": "Beniardá",
    "abogados-benidorm.html": "Benidorm",
    "abogados-bolulla.html": "Bolulla",
    "abogados-calpe.html": "Calpe",
    "abogados-finestrat.html": "Finestrat",
    "abogados-guadalest.html": "Guadalest",
    "abogados-la-nucia.html": "La Nucía",
    "abogados-la-vila-joiosa.html": "La Vila Joiosa",
    "abogados-polop.html": "Polop",
    "abogados-tarbena.html": "Tàrbena"
}

for filename, municipio in municipios.items():
    filepath = os.path.join(base_dir, filename)
    if not os.path.exists(filepath):
        continue
        
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
        
    title = f"Abogados {municipio} | Saval García"
    desc = f"Despacho de abogados y asesoría jurídica en {municipio}. Asesor fiscal y mercantil con más de 35 años de experiencia. Especialistas en Derecho Civil, Penal, Laboral, Fiscal, Mercantil y Segunda Oportunidad. Atendemos toda la Marina Baixa."
    
    # Replace <title>
    content = re.sub(r'<title>.*?</title>', f'<title>{title}</title>', content)
    
    # Replace <meta name="description" ...>
    content = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{desc}">', content)
    
    # Replace <meta property="og:title" ...>
    content = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{title}">', content)
    
    # Replace <meta property="og:description" ...>
    content = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{desc}">', content)
    
    # Replace <meta name="twitter:title" ...>
    content = re.sub(r'<meta name="twitter:title" content="[^"]*">', f'<meta name="twitter:title" content="{title}">', content)
    
    # Replace <meta name="twitter:description" ...>
    content = re.sub(r'<meta name="twitter:description" content="[^"]*">', f'<meta name="twitter:description" content="{desc}">', content)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
        
print("Metadata updated successfully.")
