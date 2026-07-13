#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate 22 blog article pages from template, with:
- Proper article content (no emoji)
- Full ES/EN translation system
- Social media links in footer
"""
import os, re, json

BASE = r"C:\Users\USUARIO\Documents\savalgarciabogados\blog"
TEMPLATE = os.path.join(BASE, "campana-de-la-renta-2025", "index.html")

# ─── Read template ───
with open(TEMPLATE, "r", encoding="utf-8") as f:
    TPL = f.read()

# Split template into head (up to </head>), and the rest
head_end = TPL.find("</head>")
tpl_head = TPL[:head_end]
tpl_rest = TPL[head_end:]

# Extract from template: everything from <body> to the ARTICLE HERO section start
body_start = tpl_rest.find("<body>")
hero_marker = tpl_rest.find('<!-- ══════════ ARTICLE HERO ══════════ -->')
content_marker = tpl_rest.find('<!-- ══════════ ARTICLE CONTENT ══════════ -->')
footer_marker = tpl_rest.find('<!-- ══════════ FOOTER ══════════ -->')

# Get the nav/mobile-nav block (between <body> and ARTICLE HERO)
nav_block = tpl_rest[body_start + len("<body>"):hero_marker]

# Get footer block (from footer marker to </body>)
footer_start_idx = tpl_rest.find('<footer')
footer_end_idx = tpl_rest.find('</html>')
footer_and_scripts = tpl_rest[footer_start_idx:footer_end_idx]

# ─── Social media block for inside article ───
SOCIAL_IN_ARTICLE = """
<!-- Redes Sociales -->
<div class="mt-16 pt-8 border-t border-black/10">
  <p class="text-sm font-semibold uppercase tracking-widest mb-4" style="color:var(--gold)">Siguenos en Redes</p>
  <div class="flex items-center gap-5">
    <a href="https://www.facebook.com/61574738267801/about/" target="_blank" rel="noopener" class="transition-all duration-300 hover:-translate-y-1" style="color:var(--carbon)" aria-label="Facebook">
      <svg width="24" height="24" fill="currentColor" viewBox="0 0 24 24"><path d="M22.675 0h-21.35C.597 0 0 .597 0 1.325v21.351C0 23.403.597 24 1.325 24H12.82v-9.294H9.692v-3.622h3.128V8.413c0-3.1 1.893-4.788 4.659-4.788 1.325 0 2.463.099 2.795.143v3.24l-1.918.001c-1.504 0-1.795.715-1.795 1.763v2.313h3.587l-.467 3.622h-3.12V24h6.116c.73 0 1.323-.597 1.323-1.324V1.325C24 .597 23.403 0 22.675 0z"/></svg>
    </a>
    <a href="https://www.instagram.com/savalgarcia_abogados/" target="_blank" rel="noopener" class="transition-all duration-300 hover:-translate-y-1" style="color:var(--carbon)" aria-label="Instagram">
      <svg width="24" height="24" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/></svg>
    </a>
    <a href="https://www.linkedin.com/in/saval-garc%C3%ADa-abogados-b42276407/" target="_blank" rel="noopener" class="transition-all duration-300 hover:-translate-y-1" style="color:var(--carbon)" aria-label="LinkedIn">
      <svg width="24" height="24" fill="currentColor" viewBox="0 0 24 24"><path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/></svg>
    </a>
  </div>
</div>
"""

# ─── Social media links for dark footer ───
SOCIAL_FOOTER = """
  <div class="max-w-7xl mx-auto mb-8 pb-8 border-b border-white/10 flex flex-col sm:flex-row items-center justify-between gap-4">
    <p class="text-[.62rem] font-semibold tracking-[.2em] uppercase text-white/40">Siguenos en Redes</p>
    <div class="flex items-center gap-4">
      <a href="https://www.facebook.com/61574738267801/about/" target="_blank" rel="noopener" class="text-[var(--gold)] hover:text-white hover:-translate-y-1 transition-all duration-300" aria-label="Facebook">
        <svg width="22" height="22" fill="currentColor" viewBox="0 0 24 24"><path d="M22.675 0h-21.35C.597 0 0 .597 0 1.325v21.351C0 23.403.597 24 1.325 24H12.82v-9.294H9.692v-3.622h3.128V8.413c0-3.1 1.893-4.788 4.659-4.788 1.325 0 2.463.099 2.795.143v3.24l-1.918.001c-1.504 0-1.795.715-1.795 1.763v2.313h3.587l-.467 3.622h-3.12V24h6.116c.73 0 1.323-.597 1.323-1.324V1.325C24 .597 23.403 0 22.675 0z"/></svg>
      </a>
      <a href="https://www.instagram.com/savalgarcia_abogados/" target="_blank" rel="noopener" class="text-[var(--gold)] hover:text-white hover:-translate-y-1 transition-all duration-300" aria-label="Instagram">
        <svg width="22" height="22" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/></svg>
      </a>
      <a href="https://www.linkedin.com/in/saval-garc%C3%ADa-abogados-b42276407/" target="_blank" rel="noopener" class="text-[var(--gold)] hover:text-white hover:-translate-y-1 transition-all duration-300" aria-label="LinkedIn">
        <svg width="22" height="22" fill="currentColor" viewBox="0 0 24 24"><path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/></svg>
      </a>
    </div>
  </div>
"""

def build_translation_script(trans_dict):
    """Build the full translation JS block for a blog article."""
    pairs = []
    for es, en in trans_dict.items():
        es_safe = es.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ")
        en_safe = en.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ")
        pairs.append(f'    "{es_safe}": "{en_safe}"')
    dict_entries = ",\n".join(pairs)
    
    return f"""
<!-- Traductor flotante (abajo a la izquierda) -->
<div class="lang-container">
  <button onclick="toggleLanguage()" class="lang-btn" aria-label="Traducir / Translate">
    <span id="lang-flag-icon"></span>
    <span class="lang-btn-text">Translate to English</span>
  </button>
</div>

<script>
(function() {{
  const dictEsToEn = {{
{dict_entries}
  }};

  const dictEnToEs = {{}};
  for (const [k, v] of Object.entries(dictEsToEn)) dictEnToEs[v] = k;

  let currentLang = 'es';
  const originalTexts = new Map();

  function normalize(s) {{ return s.replace(/\\s+/g, ' ').trim(); }}

  function applyLanguage(lang) {{
    currentLang = lang;
    const dict = lang === 'en' ? dictEsToEn : dictEnToEs;
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null, false);
    const nodes = [];
    while (walker.nextNode()) nodes.push(walker.currentNode);

    nodes.forEach(node => {{
      if (node.parentElement && (node.parentElement.tagName === 'SCRIPT' || node.parentElement.tagName === 'STYLE')) return;
      const raw = node.textContent;
      const key = normalize(raw);
      if (!key) return;

      if (lang === 'en' && !originalTexts.has(node)) {{
        originalTexts.set(node, raw);
      }}

      if (lang === 'es' && originalTexts.has(node)) {{
        node.textContent = originalTexts.get(node);
        return;
      }}

      if (dict[key]) {{
        node.textContent = raw.replace(raw.trim(), dict[key]);
      }}
    }});

    // Update button
    const flagIconContainer = document.getElementById('lang-flag-icon');
    const langBtnText = document.querySelector('.lang-btn-text');
    const ukFlag = '<svg viewBox="0 0 24 24" style="border-radius:50%;width:16px;height:16px;display:block"><clipPath id="uk-clip"><circle cx="12" cy="12" r="12"/></clipPath><g clip-path="url(#uk-clip)"><rect width="24" height="24" fill="#00247D"/><line x1="0" y1="0" x2="24" y2="24" stroke="#FFF" stroke-width="3"/><line x1="24" y1="0" x2="0" y2="24" stroke="#FFF" stroke-width="3"/><line x1="0" y1="0" x2="24" y2="24" stroke="#CF142B" stroke-width="1.8"/><line x1="24" y1="0" x2="0" y2="24" stroke="#CF142B" stroke-width="1.8"/><line x1="12" y1="0" x2="12" y2="24" stroke="#FFF" stroke-width="4.5"/><line x1="0" y1="12" x2="24" y2="12" stroke="#FFF" stroke-width="4.5"/><line x1="12" y1="0" x2="12" y2="24" stroke="#CF142B" stroke-width="2.5"/><line x1="0" y1="12" x2="24" y2="12" stroke="#CF142B" stroke-width="2.5"/></g></svg>';
    const esFlag = '<svg viewBox="0 0 24 24" style="border-radius:50%;width:16px;height:16px;display:block"><clipPath id="es-clip"><circle cx="12" cy="12" r="12"/></clipPath><g clip-path="url(#es-clip)"><rect x="0" y="0" width="24" height="6" fill="#AD1519"/><rect x="0" y="6" width="24" height="12" fill="#FABD00"/><rect x="0" y="18" width="24" height="6" fill="#AD1519"/></g></svg>';
    if (langBtnText) langBtnText.textContent = lang === 'es' ? 'Translate to English' : 'Traducir a espanol';
    if (flagIconContainer) flagIconContainer.innerHTML = lang === 'es' ? ukFlag : esFlag;
  }}

  window.toggleLanguage = function() {{
    applyLanguage(currentLang === 'es' ? 'en' : 'es');
  }};

  if (document.readyState === 'loading') {{
    document.addEventListener('DOMContentLoaded', () => applyLanguage(currentLang));
  }} else {{
    applyLanguage(currentLang);
  }}
}})();
</script>
"""

# ─── ARTICLES DATA ───
articles = [
    {
        "slug": "desahucio-grandes-tenedores",
        "title": "El Tribunal Constitucional anula requisitos para plantear demandas de desahucio",
        "desc": "El pasado mes de enero el Tribunal Constitucional anulo requisitos para plantear demandas de desahucio que vinculaban a grandes tenedores.",
        "en_title": "The Constitutional Court annuls requirements for filing eviction lawsuits",
        "body": [
            "Importante noticia.",
            "El pasado mes de enero el Tribunal Constitucional anulo requisitos para plantear demandas de desahucio que vinculaban a grandes tenedores relativos a la necesidad de demostrar la posible situacion de vulnerabilidad del arrendatario.",
            "Pese a los intentos del legislador de defender los intereses de los arrendatarios, se elimina un precepto que era origen de conflictos (debido a su falta de concrecion juridica) a la hora de acreditar por parte del arrendador para consecuentemente iniciar la via judicial."
        ],
        "trans": {
            "Importante noticia.": "Important news.",
            "El pasado mes de enero el Tribunal Constitucional anulo requisitos para plantear demandas de desahucio que vinculaban a grandes tenedores relativos a la necesidad de demostrar la posible situacion de vulnerabilidad del arrendatario.": "Last January, the Constitutional Court annulled requirements for filing eviction lawsuits that linked large holders regarding the need to demonstrate the possible situation of vulnerability of the tenant.",
            "Pese a los intentos del legislador de defender los intereses de los arrendatarios, se elimina un precepto que era origen de conflictos (debido a su falta de concrecion juridica) a la hora de acreditar por parte del arrendador para consecuentemente iniciar la via judicial.": "Despite the legislator's attempts to defend the interests of tenants, a precept that was the source of conflicts (due to its lack of legal specificity) when accrediting by the landlord to consequently initiate legal proceedings is eliminated.",
            "Siguenos en Redes": "Follow us on Social Media"
        }
    },
    {
        "slug": "acuerdo-audiencia-provincial-barcelona-okupas",
        "title": "Importante acuerdo de la Audiencia Provincial de Barcelona sobre okupas",
        "desc": "Los magistrados de la Audiencia Provincial de Barcelona acordaron no considerar delito de coacciones el corte de suministros a un okupa.",
        "en_title": "Important agreement of the Provincial Court of Barcelona on squatters",
        "body": [
            "Importante acuerdo de la Audiencia Provincial de Barcelona.",
            "El pasado mes de marzo, los magistrados de la Audiencia Provincial de Barcelona acordaron no considerar delito de coacciones el corte de suministros a un okupa por parte de un propietario. Sin embargo, este acuerdo es solo un criterio de la Audiencia Provincial y aun queda un largo camino para que se convierta en jurisprudencia consolidada. Aun tendremos que esperar a que el Tribunal Supremo resuelva algun recurso donde se unifiquen criterios.",
            "El acuerdo de la Audiencia Provincial no es definitivo, y por el momento solo afectara a los casos tratados en Barcelona."
        ],
        "trans": {
            "Importante acuerdo de la Audiencia Provincial de Barcelona.": "Important agreement of the Provincial Court of Barcelona.",
            "El pasado mes de marzo, los magistrados de la Audiencia Provincial de Barcelona acordaron no considerar delito de coacciones el corte de suministros a un okupa por parte de un propietario. Sin embargo, este acuerdo es solo un criterio de la Audiencia Provincial y aun queda un largo camino para que se convierta en jurisprudencia consolidada. Aun tendremos que esperar a que el Tribunal Supremo resuelva algun recurso donde se unifiquen criterios.": "Last March, the magistrates of the Provincial Court of Barcelona agreed not to consider the cutting off of supplies to a squatter by an owner a crime of coercion. However, this agreement is only a criterion of the Provincial Court and there is still a long way to go for it to become consolidated jurisprudence. We will still have to wait for the Supreme Court to resolve an appeal where criteria are unified.",
            "El acuerdo de la Audiencia Provincial no es definitivo, y por el momento solo afectara a los casos tratados en Barcelona.": "The agreement of the Provincial Court is not definitive, and for the moment it will only affect cases dealt with in Barcelona.",
            "Siguenos en Redes": "Follow us on Social Media"
        }
    },
    {
        "slug": "libertad-de-expresion-o-revictimizacion",
        "title": "Libertad de expresion o revictimizacion",
        "desc": "El caso de Jose Breton, condenado por el asesinato de sus hijos, vuelve a generar controversia. Una editorial pretende publicar un libro.",
        "en_title": "Freedom of expression or revictimization",
        "body": [
            "Libertad de expresion o revictimizacion.",
            "El caso de Jose Breton, condenado por el asesinato de sus hijos, vuelve a generar controversia. Una editorial pretende publicar un libro con su testimonio desde prision.",
            "La Fiscalia intento frenar su publicacion alegando una posible vulneracion del derecho al honor, pero la medida cautelar fue denegada.",
            "Ahora, la editorial tiene via libre... por el momento. Tanto la Fiscalia como la madre de los ninos aun pueden iniciar un procedimiento judicial para intentar evitar que el libro sea publicado.",
            "Debe permitirse que un condenado por un crimen tan atroz publique su version de los hechos? Donde trazamos el limite entre libertad de expresion y respeto a las victimas?"
        ],
        "trans": {
            "Libertad de expresion o revictimizacion.": "Freedom of expression or revictimization.",
            "El caso de Jose Breton, condenado por el asesinato de sus hijos, vuelve a generar controversia. Una editorial pretende publicar un libro con su testimonio desde prision.": "The case of Jose Breton, convicted for the murder of his children, once again generates controversy. A publisher intends to publish a book with his testimony from prison.",
            "La Fiscalia intento frenar su publicacion alegando una posible vulneracion del derecho al honor, pero la medida cautelar fue denegada.": "The Prosecutor's Office tried to stop its publication alleging a possible violation of the right to honor, but the precautionary measure was denied.",
            "Ahora, la editorial tiene via libre... por el momento. Tanto la Fiscalia como la madre de los ninos aun pueden iniciar un procedimiento judicial para intentar evitar que el libro sea publicado.": "Now, the publisher has a free pass... for the moment. Both the Prosecutor's Office and the mother of the children can still initiate legal proceedings to try to prevent the book from being published.",
            "Debe permitirse que un condenado por un crimen tan atroz publique su version de los hechos? Donde trazamos el limite entre libertad de expresion y respeto a las victimas?": "Should someone convicted of such an atrocious crime be allowed to publish their version of events? Where do we draw the line between freedom of expression and respect for victims?",
            "Siguenos en Redes": "Follow us on Social Media"
        }
    },
    {
        "slug": "reclamacion-clausulas-abusivas-hipotecas",
        "title": "Tienes una hipoteca? Podrias estar pagando de mas sin saberlo",
        "desc": "En muchas hipotecas se incluyen clausulas abusivas que afectan directamente a tu bolsillo y tu podrias reclamarlas.",
        "en_title": "Do you have a mortgage? You could be paying too much without knowing it",
        "body": [
            "Tienes una hipoteca? Podrias estar pagando de mas sin saberlo.",
            "En muchas hipotecas se incluyen clausulas abusivas que afectan directamente a tu bolsillo y tu podrias reclamarlas.",
            "Revisamos tus escrituras sin coste, incluso si ya esta cancelada, y te decimos si puedes recuperar tu dinero.",
            "Solo tienes que traernos tu escritura de la hipoteca y nosotros nos encargamos del resto.",
            "Sin compromiso. Sin coste por la revision. Con total transparencia.",
            "Escribenos por privado o ven a vernos."
        ],
        "trans": {
            "Tienes una hipoteca? Podrias estar pagando de mas sin saberlo.": "Do you have a mortgage? You could be paying too much without knowing it.",
            "En muchas hipotecas se incluyen clausulas abusivas que afectan directamente a tu bolsillo y tu podrias reclamarlas.": "Many mortgages include abusive clauses that directly affect your pocket and you could claim them.",
            "Revisamos tus escrituras sin coste, incluso si ya esta cancelada, y te decimos si puedes recuperar tu dinero.": "We review your deeds at no cost, even if it is already canceled, and we tell you if you can recover your money.",
            "Solo tienes que traernos tu escritura de la hipoteca y nosotros nos encargamos del resto.": "You just have to bring us your mortgage deed and we take care of the rest.",
            "Sin compromiso. Sin coste por la revision. Con total transparencia.": "No obligation. No cost for the review. With total transparency.",
            "Escribenos por privado o ven a vernos.": "Write us privately or come see us.",
            "Siguenos en Redes": "Follow us on Social Media"
        }
    },
    {
        "slug": "asesoramiento-fiscal-especializado-empresas",
        "title": "Asesoramiento fiscal especializado para empresas y profesionales",
        "desc": "Le ofrecemos asesoramiento fiscal especializado para empresas y profesionales, ayudandole a tomar decisiones inteligentes.",
        "en_title": "Specialized tax advice for businesses and professionals",
        "body": [
            "Eres profesional o diriges una empresa? Es momento de optimizar tu negocio!",
            "Le ofrecemos asesoramiento fiscal especializado para empresas y profesionales, ayudandole a tomar decisiones inteligentes desde el area juridica.",
            "Trabajamos en la reestructuracion y eficiencia de actividad, para que su negocio crezca con bases solidas, organizadas y rentables.",
            "Si su empresa atraviesa problemas economicos coyunturales, le ayudamos en la reorganizacion para salir adelante con estrategias personalizadas, enfocadas en recuperar el equilibrio financiero y operativo.",
            "Mayor organizacion. Mas resultados. Soluciones para momentos dificiles. Diligencia en liquidaciones de impuestos.",
            "Consultenos sin compromiso y empiece a transformar su negocio desde hoy.",
            "Envienos un correo electronico o llamenos para concertar una reunion."
        ],
        "trans": {
            "Eres profesional o diriges una empresa? Es momento de optimizar tu negocio!": "Are you a professional or running a business? It's time to optimize your business!",
            "Le ofrecemos asesoramiento fiscal especializado para empresas y profesionales, ayudandole a tomar decisiones inteligentes desde el area juridica.": "We offer specialized tax advice for businesses and professionals, helping you make smart decisions from the legal area.",
            "Trabajamos en la reestructuracion y eficiencia de actividad, para que su negocio crezca con bases solidas, organizadas y rentables.": "We work on the restructuring and efficiency of activity, so that your business grows with solid, organized, and profitable foundations.",
            "Si su empresa atraviesa problemas economicos coyunturales, le ayudamos en la reorganizacion para salir adelante con estrategias personalizadas, enfocadas en recuperar el equilibrio financiero y operativo.": "If your company is going through cyclical economic problems, we help you in the reorganization to move forward with personalized strategies, focused on recovering financial and operational balance.",
            "Mayor organizacion. Mas resultados. Soluciones para momentos dificiles. Diligencia en liquidaciones de impuestos.": "Greater organization. More results. Solutions for difficult times. Diligence in tax settlements.",
            "Consultenos sin compromiso y empiece a transformar su negocio desde hoy.": "Consult us without obligation and start transforming your business today.",
            "Envienos un correo electronico o llamenos para concertar una reunion.": "Send us an email or call us to arrange a meeting.",
            "Siguenos en Redes": "Follow us on Social Media"
        }
    },
    {
        "slug": "redaccion-y-revision-de-contratos",
        "title": "Necesitas un contrato bien hecho? Nosotros lo hacemos a tu medida",
        "desc": "Te ayudamos a confeccionar contratos personalizados para que tus acuerdos esten bien claros y protegidos desde el inicio.",
        "en_title": "Do you need a well-made contract? We make it to measure",
        "body": [
            "Necesitas un contrato bien hecho? Nosotros lo hacemos a tu medida.",
            "Te ayudamos a confeccionar contratos personalizados para que tus acuerdos esten bien claros y protegidos desde el inicio. La seguridad en tu patrimonio empieza con seguridad juridica.",
            "Redactamos: Compraventas de muebles e inmuebles, Arrendamientos, Donaciones, Contratos de uso, Permutas, Mandatos.",
            "Ya firmaste un contrato? Tambien hacemos revision de contratos ya firmados, para explicarte sus consecuencias y como afrontarlas con la mayor garantia.",
            "Contactanos por mensaje o correo electronico. Seriedad, claridad y respaldo legal."
        ],
        "trans": {
            "Necesitas un contrato bien hecho? Nosotros lo hacemos a tu medida.": "Do you need a well-made contract? We make it to measure.",
            "Te ayudamos a confeccionar contratos personalizados para que tus acuerdos esten bien claros y protegidos desde el inicio. La seguridad en tu patrimonio empieza con seguridad juridica.": "We help you prepare personalized contracts so that your agreements are very clear and protected from the beginning. Security in your assets begins with legal certainty.",
            "Redactamos: Compraventas de muebles e inmuebles, Arrendamientos, Donaciones, Contratos de uso, Permutas, Mandatos.": "We draft: Sales of movable and immovable property, Leases, Donations, Contracts of use, Exchanges, Mandates.",
            "Ya firmaste un contrato? Tambien hacemos revision de contratos ya firmados, para explicarte sus consecuencias y como afrontarlas con la mayor garantia.": "Did you already sign a contract? We also review already signed contracts, to explain their consequences and how to face them with the greatest guarantee.",
            "Contactanos por mensaje o correo electronico. Seriedad, claridad y respaldo legal.": "Contact us by message or email. Seriousness, clarity, and legal backing.",
            "Siguenos en Redes": "Follow us on Social Media"
        }
    },
    {
        "slug": "conflicto-tribunal-supremo-constitucional",
        "title": "Choque de trenes entre el Tribunal Supremo y el Tribunal Constitucional",
        "desc": "En los ultimos meses, se ha intensificado un conflicto entre las mas altas esferas de la Magistratura espanola.",
        "en_title": "Train wreck between the Supreme Court and the Constitutional Court",
        "body": [
            "Choque de trenes entre el Tribunal Supremo y el Tribunal Constitucional.",
            "En los ultimos meses, se ha intensificado un conflicto entre las mas altas esferas de la Magistratura espanola entre el Tribunal Supremo (TS) y el Tribunal Constitucional (TC).",
            "El pasado verano el TC anulo varias condenas dictadas por el TS en el caso de los ERE de Andalucia contra varios politicos, una decision que muchos consideran mas politica que juridica ya que el TC se convirtio en revisor de una decision de nuestro alto Tribunal. Esto ha abierto una grieta en la relacion entre ambos Organos.",
            "Ahora, un recurso de inconstitucionalidad planteado por el TS ante el TC vuelve a poner a prueba las relaciones en otro asunto vinculados estrechamente con la politica.",
            "Ya se interpuso una querella ante el Tribunal Supremo contra el presidente del Tribunal Constitucional que fue inadmitida.",
            "A dia de hoy hay pendiente de resolverse otra querella presentada ante el TS, que acusa al presidente del TC de no haberse abstenido en la admision a tramite de un recurso presentado por fiscales sobre los que fue su superior jerarquico cuando desempenaba dicho cargo antes de convertirse en Magistrado del TC.",
            "Ademas, entra en juego un posible nuevo asunto: el Fiscal General del Estado podria pedir amparo al Constitucional para impedir que el Supremo acceda a sus dispositivos electronicos en el marco de su causa penal.",
            "Seguiremos atentamente la evolucion de los acontecimientos."
        ],
        "trans": {
            "Choque de trenes entre el Tribunal Supremo y el Tribunal Constitucional.": "Train wreck between the Supreme Court and the Constitutional Court.",
            "En los ultimos meses, se ha intensificado un conflicto entre las mas altas esferas de la Magistratura espanola entre el Tribunal Supremo (TS) y el Tribunal Constitucional (TC).": "In recent months, a conflict has intensified between the highest spheres of the Spanish Judiciary between the Supreme Court (TS) and the Constitutional Court (TC).",
            "El pasado verano el TC anulo varias condenas dictadas por el TS en el caso de los ERE de Andalucia contra varios politicos, una decision que muchos consideran mas politica que juridica ya que el TC se convirtio en revisor de una decision de nuestro alto Tribunal. Esto ha abierto una grieta en la relacion entre ambos Organos.": "Last summer the TC annulled several convictions handed down by the TS in the case of the ERE of Andalusia against several politicians, a decision that many consider more political than legal since the TC became a reviewer of a decision of our High Court. This has opened a rift in the relationship between both Bodies.",
            "Ahora, un recurso de inconstitucionalidad planteado por el TS ante el TC vuelve a poner a prueba las relaciones en otro asunto vinculados estrechamente con la politica.": "Now, an appeal of unconstitutionality raised by the TS before the TC once again tests relations in another matter closely linked to politics.",
            "Ya se interpuso una querella ante el Tribunal Supremo contra el presidente del Tribunal Constitucional que fue inadmitida.": "A complaint was already filed before the Supreme Court against the president of the Constitutional Court, which was dismissed.",
            "A dia de hoy hay pendiente de resolverse otra querella presentada ante el TS, que acusa al presidente del TC de no haberse abstenido en la admision a tramite de un recurso presentado por fiscales sobre los que fue su superior jerarquico cuando desempenaba dicho cargo antes de convertirse en Magistrado del TC.": "To date, there is another complaint pending resolution before the TS, which accuses the president of the TC of not having abstained in the admission for processing of an appeal filed by prosecutors over whom he was their hierarchical superior when he held said position before becoming a Magistrate of the TC.",
            "Ademas, entra en juego un posible nuevo asunto: el Fiscal General del Estado podria pedir amparo al Constitucional para impedir que el Supremo acceda a sus dispositivos electronicos en el marco de su causa penal.": "In addition, a possible new issue comes into play: the State Attorney General could ask for protection from the Constitutional Court to prevent the Supreme Court from accessing his electronic devices within the framework of his criminal case.",
            "Seguiremos atentamente la evolucion de los acontecimientos.": "We will closely follow the evolution of events.",
            "Siguenos en Redes": "Follow us on Social Media"
        }
    },
    {
        "slug": "testamento-derecho-sucesorio",
        "title": "Protege tu legado, asegura tu voluntad",
        "desc": "Redactar un testamento a medida no es solo un tramite, es un acto de prevision, de cuidado y de proteccion de tu patrimonio.",
        "en_title": "Protect your legacy, secure your will",
        "body": [
            "Protege tu legado, asegura tu voluntad.",
            "Redactar un testamento a medida no es solo un tramite, es un acto de prevision, de cuidado y de proteccion de tu patrimonio y tus seres queridos.",
            "Un buen testamento garantiza que el destino de tus bienes se cumpla como tu lo decides.",
            "Evaluamos contigo todas las posibilidades que ofrece el Derecho Sucesorio, para encontrar la formula adecuada para la situacion concreta.",
            "Abordamos las implicaciones fiscales desde el inicio, evitando sorpresas para tus herederos.",
            "Nos aseguramos de que se plasme correctamente en escritura publica.",
            "Con un testamento bien planteado salvaguardas la seguridad de tu patrimonio y tu tranquilidad.",
            "Con nuestro acompanamiento profesional, convertir un momento delicado en una decision bien tomada es posible."
        ],
        "trans": {
            "Protege tu legado, asegura tu voluntad.": "Protect your legacy, secure your will.",
            "Redactar un testamento a medida no es solo un tramite, es un acto de prevision, de cuidado y de proteccion de tu patrimonio y tus seres queridos.": "Drafting a custom will is not just a formality; it is an act of foresight, care, and protection of your assets and your loved ones.",
            "Un buen testamento garantiza que el destino de tus bienes se cumpla como tu lo decides.": "A good will guarantees that the destination of your assets is fulfilled as you decide.",
            "Evaluamos contigo todas las posibilidades que ofrece el Derecho Sucesorio, para encontrar la formula adecuada para la situacion concreta.": "We evaluate with you all the possibilities offered by Succession Law, to find the right formula for the specific situation.",
            "Abordamos las implicaciones fiscales desde el inicio, evitando sorpresas para tus herederos.": "We address the tax implications from the beginning, avoiding surprises for your heirs.",
            "Nos aseguramos de que se plasme correctamente en escritura publica.": "We ensure that it is correctly reflected in a public deed.",
            "Con un testamento bien planteado salvaguardas la seguridad de tu patrimonio y tu tranquilidad.": "With a well-planned will, you safeguard the security of your assets and your peace of mind.",
            "Con nuestro acompanamiento profesional, convertir un momento delicado en una decision bien tomada es posible.": "With our professional support, turning a delicate moment into a well-made decision is possible.",
            "Siguenos en Redes": "Follow us on Social Media"
        }
    },
    {
        "slug": "delito-descubrimiento-revelacion-secretos",
        "title": "Los delitos de descubrimiento y revelacion de secretos: Una realidad en auge",
        "desc": "El avance imparable de las nuevas tecnologias ha traido consigo una proliferacion de delitos que atentan contra la intimidad.",
        "en_title": "Crimes of discovery and revelation of secrets: A booming reality",
        "body": [
            "Los delitos de descubrimiento y revelacion de secretos: Una realidad en auge.",
            "El avance imparable de las nuevas tecnologias ha traido consigo una proliferacion de delitos que atentan contra la intimidad. Uno de los que mas crece: el descubrimiento y revelacion de secretos.",
            "Este delito, recogido en el Codigo Penal, se produce cuando alguien accede sin consentimiento a datos, conversaciones, imagenes o informacion privada de otra persona normalmente en el ambito intimo, familiar o laboral y, que puede llevar aparejada la difusion.",
            "Las penas para los condenados son: Penas de prision de 1 hasta 5 anos. Posibles indemnizaciones por danos y perjuicios ocasionados a la victima.",
            "En la ultima decada, las condenas por este tipo penal casi se han triplicado, reflejando su creciente incidencia."
        ],
        "trans": {
            "Los delitos de descubrimiento y revelacion de secretos: Una realidad en auge.": "The crimes of discovery and revelation of secrets: A booming reality.",
            "El avance imparable de las nuevas tecnologias ha traido consigo una proliferacion de delitos que atentan contra la intimidad. Uno de los que mas crece: el descubrimiento y revelacion de secretos.": "The unstoppable advance of new technologies has brought with it a proliferation of crimes against privacy. One of the fastest-growing: the discovery and revelation of secrets.",
            "Este delito, recogido en el Codigo Penal, se produce cuando alguien accede sin consentimiento a datos, conversaciones, imagenes o informacion privada de otra persona normalmente en el ambito intimo, familiar o laboral y, que puede llevar aparejada la difusion.": "This crime, included in the Penal Code, occurs when someone accesses data, conversations, images, or private information of another person without consent, normally in the intimate, family, or work environment, and which may entail dissemination.",
            "Las penas para los condenados son: Penas de prision de 1 hasta 5 anos. Posibles indemnizaciones por danos y perjuicios ocasionados a la victima.": "The penalties for those convicted are: Prison sentences of 1 to 5 years. Possible compensation for damages caused to the victim.",
            "En la ultima decada, las condenas por este tipo penal casi se han triplicado, reflejando su creciente incidencia.": "In the last decade, convictions for this type of crime have almost tripled, reflecting its growing incidence.",
            "Siguenos en Redes": "Follow us on Social Media"
        }
    },
    {
        "slug": "hallazgo-tesoro-codigo-civil",
        "title": "Que pasa si descubres un tesoro en Espana?",
        "desc": "El Codigo Civil espanol regula que ocurre cuando alguien encuentra un tesoro escondido.",
        "en_title": "What happens if you discover a treasure in Spain?",
        "body": [
            "Que pasa si descubres un tesoro en Espana?",
            "El Codigo Civil espanol regula que ocurre cuando alguien encuentra un tesoro escondido.",
            "Si el tesoro esta en tu terreno: El hallazgo te pertenece por completo.",
            "Y si lo encuentras en terreno ajeno? Si fue por casualidad, el valor se reparte 50/50 entre el descubridor y el dueno del terreno.",
            "Se considera tesoro, los depositos de dinero oculto e ignorado, alhajas u otros objetos preciosos.",
            "Este curioso detalle legal esta recogido en el Articulo 351 del Codigo Civil."
        ],
        "trans": {
            "Que pasa si descubres un tesoro en Espana?": "What happens if you discover a treasure in Spain?",
            "El Codigo Civil espanol regula que ocurre cuando alguien encuentra un tesoro escondido.": "The Spanish Civil Code regulates what happens when someone finds a hidden treasure.",
            "Si el tesoro esta en tu terreno: El hallazgo te pertenece por completo.": "If the treasure is on your land: The find belongs entirely to you.",
            "Y si lo encuentras en terreno ajeno? Si fue por casualidad, el valor se reparte 50/50 entre el descubridor y el dueno del terreno.": "And if you find it on someone else's land? If it was by chance, the value is split 50/50 between the discoverer and the landowner.",
            "Se considera tesoro, los depositos de dinero oculto e ignorado, alhajas u otros objetos preciosos.": "Deposits of hidden and ignored money, jewels, or other precious objects are considered treasure.",
            "Este curioso detalle legal esta recogido en el Articulo 351 del Codigo Civil.": "This curious legal detail is included in Article 351 of the Civil Code.",
            "Siguenos en Redes": "Follow us on Social Media"
        }
    },
    {
        "slug": "delitos-contra-la-salud-publica",
        "title": "Delitos contra la salud publica",
        "desc": "En Espana y en la Comunidad Valenciana, las condenas por delitos contra la salud publica se han mantenido estables.",
        "en_title": "Crimes against public health",
        "body": [
            "Delitos contra la salud publica.",
            "En Espana y en la Comunidad Valenciana, las condenas por delitos contra la salud publica se han mantenido estables en los ultimos 10 anos.",
            "Estos tipos se enjuician en el ambito penal de forma singular al resto de delitos. Se tiene en cuenta la sustancia incautada y el contexto que gira alrededor de los hechos ocurridos, la cantidad de la sustancia, la finalidad (consumo propio o trafico) y otros elementos clave.",
            "Ademas, el bien juridico protegido es un concepto abstracto que puede resultar ambiguo en su interpretacion siendo un arma de doble filo para todas las partes.",
            "Cada caso es unico, y las circunstancias concretas que rodean a los hechos son determinantes para lograr una sentencia mas o menos favorable para el acusado.",
            "El procedimiento penal en Espana goza de un alto grado de garantismo para el acusado, lo que puede ser una ventaja en la defensa, permitiendo explorar diversas vias legales para la proteccion de derechos. Las penas por la comision de este tipo de delitos en otros paises de la UE es mas severa que en el caso espanol.",
            "La contratacion de una defensa especializada puede marcar la diferencia."
        ],
        "trans": {
            "Delitos contra la salud publica.": "Crimes against public health.",
            "En Espana y en la Comunidad Valenciana, las condenas por delitos contra la salud publica se han mantenido estables en los ultimos 10 anos.": "In Spain and in the Valencian Community, convictions for crimes against public health have remained stable over the last 10 years.",
            "Estos tipos se enjuician en el ambito penal de forma singular al resto de delitos. Se tiene en cuenta la sustancia incautada y el contexto que gira alrededor de los hechos ocurridos, la cantidad de la sustancia, la finalidad (consumo propio o trafico) y otros elementos clave.": "These types are prosecuted in the criminal sphere in a unique way compared to the rest of the crimes. The seized substance, the context surrounding the events, the amount, the purpose (own consumption or trafficking) and other key elements are taken into account.",
            "Ademas, el bien juridico protegido es un concepto abstracto que puede resultar ambiguo en su interpretacion siendo un arma de doble filo para todas las partes.": "In addition, the protected legal right is an abstract concept that can be ambiguous in its interpretation, being a double-edged sword for all parties.",
            "Cada caso es unico, y las circunstancias concretas que rodean a los hechos son determinantes para lograr una sentencia mas o menos favorable para el acusado.": "Each case is unique, and the specific circumstances surrounding the facts are decisive in achieving a more or less favorable sentence for the accused.",
            "El procedimiento penal en Espana goza de un alto grado de garantismo para el acusado, lo que puede ser una ventaja en la defensa, permitiendo explorar diversas vias legales para la proteccion de derechos. Las penas por la comision de este tipo de delitos en otros paises de la UE es mas severa que en el caso espanol.": "Criminal proceedings in Spain enjoy a high degree of guarantees for the accused, which can be an advantage in the defense. Penalties for committing this type of crime in other EU countries are more severe than in the Spanish case.",
            "La contratacion de una defensa especializada puede marcar la diferencia.": "Hiring a specialized defense can make the difference.",
            "Siguenos en Redes": "Follow us on Social Media"
        }
    },
    {
        "slug": "estafa-bancaria-phishing",
        "title": "Has sido victima de una estafa bancaria por phishing? No estas indefenso",
        "desc": "Cada dia, miles de consumidores sufren fraudes por parte de delincuentes que se hacen pasar por su banco.",
        "en_title": "Have you been a victim of a banking phishing scam? You are not defenseless",
        "body": [
            "Has sido victima de una estafa bancaria por phishing? No estas indefenso.",
            "Cada dia, miles de consumidores sufren fraudes por parte de delincuentes que se hacen pasar por su banco. Pero si no se demuestra negligencia o temeridad por parte del consumidor, el banco tiene la obligacion de asumir la perdida economica.",
            "La ley protege al consumidor. En la mayoria de casos, cuando el fraude proviene de un tercero desconocido, el usuario NO debe cargar con las consecuencias financieras.",
            "Desde nuestro despacho de abogados te ayudamos a reclamar tu dinero y hacer valer tus derechos frente a la entidad bancaria.",
            "Escribenos por privado o agenda tu consulta gratuita.",
            "No dejes que el banco se lave las manos. Reclama lo que te corresponde."
        ],
        "trans": {
            "Has sido victima de una estafa bancaria por phishing? No estas indefenso.": "Have you been a victim of a banking phishing scam? You are not defenseless.",
            "Cada dia, miles de consumidores sufren fraudes por parte de delincuentes que se hacen pasar por su banco. Pero si no se demuestra negligencia o temeridad por parte del consumidor, el banco tiene la obligacion de asumir la perdida economica.": "Every day, thousands of consumers suffer frauds by criminals posing as their bank. But if negligence or recklessness on the part of the consumer is not proven, the bank has the obligation to assume the economic loss.",
            "La ley protege al consumidor. En la mayoria de casos, cuando el fraude proviene de un tercero desconocido, el usuario NO debe cargar con las consecuencias financieras.": "The law protects the consumer. In most cases, when the fraud comes from an unknown third party, the user MUST NOT bear the financial consequences.",
            "Desde nuestro despacho de abogados te ayudamos a reclamar tu dinero y hacer valer tus derechos frente a la entidad bancaria.": "From our law firm, we help you claim your money and assert your rights against the banking entity.",
            "Escribenos por privado o agenda tu consulta gratuita.": "Write us privately or schedule your free consultation.",
            "No dejes que el banco se lave las manos. Reclama lo que te corresponde.": "Don't let the bank wash its hands. Claim what belongs to you.",
            "Siguenos en Redes": "Follow us on Social Media"
        }
    },
    {
        "slug": "procedimiento-comprobacion-valores-hacienda",
        "title": "Te ha notificado Hacienda un procedimiento de comprobacion de valores?",
        "desc": "Tienes derecho a defenderte sin dejarte amedrentar por la Administracion.",
        "en_title": "Has the Treasury notified you of a value verification procedure?",
        "body": [
            "Te ha notificado Hacienda un procedimiento de comprobacion de valores? Tienes derecho a defenderte sin dejarte amedrentar por la Administracion.",
            "Este procedimiento lo inicia la Administracion Tributaria cuando considera, a su discrecion, que el valor declarado en una liquidacion de un tributo no se ajusta a lo que ellos estiman correcto. Por lo que, pueden exigir un pago adicional que quizas no corresponde.",
            "En nuestro despacho contamos con mas de 30 anos de experiencia defendiendo a contribuyentes como tu, tanto en via administrativa como judicial. Nuestros abogados especializados te asesoran desde el primer momento para proteger tus derechos y tu bolsillo.",
            "Si enfrentas una comprobacion de valores, no lo afrontes sin asesoramiento profesional. Una buena defensa puede marcar la diferencia."
        ],
        "trans": {
            "Te ha notificado Hacienda un procedimiento de comprobacion de valores? Tienes derecho a defenderte sin dejarte amedrentar por la Administracion.": "Has the Tax Agency notified you of a value verification procedure? You have the right to defend yourself without being intimidated by the Administration.",
            "Este procedimiento lo inicia la Administracion Tributaria cuando considera, a su discrecion, que el valor declarado en una liquidacion de un tributo no se ajusta a lo que ellos estiman correcto. Por lo que, pueden exigir un pago adicional que quizas no corresponde.": "This procedure is initiated by the Tax Administration when it considers, at its discretion, that the value declared in a tax settlement does not match what they consider correct. Therefore, they may require an additional payment that may not be due.",
            "En nuestro despacho contamos con mas de 30 anos de experiencia defendiendo a contribuyentes como tu, tanto en via administrativa como judicial. Nuestros abogados especializados te asesoran desde el primer momento para proteger tus derechos y tu bolsillo.": "In our firm we have over 30 years of experience defending taxpayers like you, both administratively and judicially. Our specialized lawyers advise you from the first moment to protect your rights and your pocket.",
            "Si enfrentas una comprobacion de valores, no lo afrontes sin asesoramiento profesional. Una buena defensa puede marcar la diferencia.": "If you face a value verification, do not face it without professional advice. A good defense can make a difference.",
            "Siguenos en Redes": "Follow us on Social Media"
        }
    },
    {
        "slug": "delito-apropiacion-indebida",
        "title": "Apropiacion indebida",
        "desc": "Este tipo penal requiere que el autor se quede con algo que debia devolver en virtud de cualquier titulo.",
        "en_title": "Misappropriation",
        "body": [
            "Apropiacion indebida.",
            "Este tipo penal requiere que el autor se quede con algo que debia devolver en virtud de cualquier titulo mediando o no confianza.",
            "Esta regulado en los articulos 253 y 254 del Codigo Penal, y las penas pueden alcanzar hasta 6 anos de prision, dependiendo de la gravedad del caso.",
            "Este delito se relaciona y puede confundirse en algunos supuestos con otros tipos penales como: Administracion desleal, Estafa.",
            "Si has sido victima de una apropiacion indebida o te acusan de este delito, es fundamental contar con asesoria legal especializada.",
            "Defendemos tus derechos con rigor y responsabilidad.",
            "Consulta sin compromiso."
        ],
        "trans": {
            "Apropiacion indebida.": "Misappropriation.",
            "Este tipo penal requiere que el autor se quede con algo que debia devolver en virtud de cualquier titulo mediando o no confianza.": "This criminal offense requires that the perpetrator keep something that they were supposed to return by virtue of any title, with or without trust.",
            "Esta regulado en los articulos 253 y 254 del Codigo Penal, y las penas pueden alcanzar hasta 6 anos de prision, dependiendo de la gravedad del caso.": "It is regulated in articles 253 and 254 of the Penal Code, and penalties can reach up to 6 years in prison, depending on the severity of the case.",
            "Este delito se relaciona y puede confundirse en algunos supuestos con otros tipos penales como: Administracion desleal, Estafa.": "This crime is related and can be confused in some cases with other criminal offenses such as: Unfair administration, Fraud.",
            "Si has sido victima de una apropiacion indebida o te acusan de este delito, es fundamental contar con asesoria legal especializada.": "If you have been a victim of misappropriation or are accused of this crime, it is essential to have specialized legal advice.",
            "Defendemos tus derechos con rigor y responsabilidad.": "We defend your rights with rigor and responsibility.",
            "Consulta sin compromiso.": "Consultation without obligation.",
            "Siguenos en Redes": "Follow us on Social Media"
        }
    },
    {
        "slug": "reclamacion-tarjetas-revolving-usura",
        "title": "Las tarjetas de credito revolving y condiciones usurarias",
        "desc": "Las tarjetas de credito revolving y otros productos financieros pueden esconder condiciones usurarias.",
        "en_title": "Revolving credit cards and usurious conditions",
        "body": [
            "Atencion consumidores!",
            "Las tarjetas de credito revolving y otros productos financieros pueden esconder condiciones usurarias muy costosas para el que las adquiere.",
            "Aunque las lineas de credito suelen ser de cuantia pequena, los intereses y comisiones se disparan, superando muchas veces los limites establecidos por la jurisprudencia. Esto puede hacer que el contrato sea nulo por usura, lo que te da derecho a reclamar lo que has pagado de mas.",
            "Estos productos con intereses desproporcionados provocan un efecto bola de nieve que es origen de multiples problemas: Primero afectan tu economia, luego tu entorno familiar, y finalmente tu salud mental y emocional.",
            "Si tienes una tarjeta revolving o cualquier producto con intereses desproporcionados, revisamos su legalidad. Puedes estar pagando mucho mas de lo justo.",
            "En nuestro despacho aconsejamos como actuar en estos asuntos para reclamar a bancos y entidades prestamistas. Recupera tu dinero con asesoria legal experta."
        ],
        "trans": {
            "Atencion consumidores!": "Attention consumers!",
            "Las tarjetas de credito revolving y otros productos financieros pueden esconder condiciones usurarias muy costosas para el que las adquiere.": "Revolving credit cards and other financial products can hide very costly usurious conditions for the purchaser.",
            "Aunque las lineas de credito suelen ser de cuantia pequena, los intereses y comisiones se disparan, superando muchas veces los limites establecidos por la jurisprudencia. Esto puede hacer que el contrato sea nulo por usura, lo que te da derecho a reclamar lo que has pagado de mas.": "Although credit lines are usually of small amounts, interest and commissions skyrocket, often exceeding the limits established by jurisprudence. This can make the contract null and void due to usury, giving you the right to claim what you have overpaid.",
            "Estos productos con intereses desproporcionados provocan un efecto bola de nieve que es origen de multiples problemas: Primero afectan tu economia, luego tu entorno familiar, y finalmente tu salud mental y emocional.": "These products with disproportionate interest cause a snowball effect that is the source of multiple problems: First they affect your economy, then your family environment, and finally your mental and emotional health.",
            "Si tienes una tarjeta revolving o cualquier producto con intereses desproporcionados, revisamos su legalidad. Puedes estar pagando mucho mas de lo justo.": "If you have a revolving card or any product with disproportionate interest, we will review its legality. You could be paying much more than is fair.",
            "En nuestro despacho aconsejamos como actuar en estos asuntos para reclamar a bancos y entidades prestamistas. Recupera tu dinero con asesoria legal experta.": "In our firm we advise how to act in these matters to claim against banks and lending entities. Recover your money with expert legal advice.",
            "Siguenos en Redes": "Follow us on Social Media"
        }
    },
    {
        "slug": "fiscal-general-estado-revelacion-secretos",
        "title": "Un lio en las altas esferas de la Fiscalia",
        "desc": "El Tribunal Supremo ha dictado auto de transformacion contra el Fiscal General del Estado.",
        "en_title": "A mess in the upper echelons of the Prosecutor's Office",
        "body": [
            "Un lio en las altas esferas de la Fiscalia.",
            "El Tribunal Supremo ha dictado auto de transformacion de diligencias previas en procedimiento abreviado contra el Fiscal General del Estado y la Fiscal Jefe Provincial de Madrid, investigados por un presunto delito de descubrimiento y revelacion de secretos. Un paso decisivo que sacude los cimientos del Ministerio Fiscal.",
            "Pero aqui viene el enredo...",
            "El articulo 145 del Estatuto del Ministerio Fiscal permite que el Fiscal General cese motivadamente a una fiscal si se dicta auto de apertura de juicio oral contra ella. Pero...",
            "Que pasa si ambos estan acusados en el mismo proceso? El Estatuto no contempla el cese del Fiscal General en estas circunstancias, por lo que podriamos presenciar como un Fiscal General acusado debe cesar a su subordinada tambien acusada. Una situacion tan absurda como grave.",
            "Pero hay mas: El Ministerio Fiscal esta personado como acusacion en esta causa penal. Es decir, una parte de la Fiscalia tiene que decidir ahora si acusa a su propio jefe.",
            "Se atrevevan a formular escrito de acusacion contra el Fiscal General del Estado? O veremos una maniobra evasiva ante el conflicto interno mas incomodo imaginable?",
            "Un caso sin precedentes. Un dilema institucional."
        ],
        "trans": {
            "Un lio en las altas esferas de la Fiscalia.": "A mess in the upper echelons of the Prosecutor's Office.",
            "El Tribunal Supremo ha dictado auto de transformacion de diligencias previas en procedimiento abreviado contra el Fiscal General del Estado y la Fiscal Jefe Provincial de Madrid, investigados por un presunto delito de descubrimiento y revelacion de secretos. Un paso decisivo que sacude los cimientos del Ministerio Fiscal.": "The Supreme Court has issued an order to transform preliminary proceedings into an abbreviated procedure against the State Attorney General and the Chief Provincial Prosecutor of Madrid, investigated for an alleged crime of discovery and revelation of secrets. A decisive step that shakes the foundations of the Public Prosecutor's Office.",
            "Pero aqui viene el enredo...": "But here comes the tangle...",
            "El articulo 145 del Estatuto del Ministerio Fiscal permite que el Fiscal General cese motivadamente a una fiscal si se dicta auto de apertura de juicio oral contra ella. Pero...": "Article 145 of the Statute of the Public Prosecutor's Office allows the Attorney General to dismiss a prosecutor if an order to open an oral trial is issued against her. But...",
            "Que pasa si ambos estan acusados en el mismo proceso? El Estatuto no contempla el cese del Fiscal General en estas circunstancias, por lo que podriamos presenciar como un Fiscal General acusado debe cesar a su subordinada tambien acusada. Una situacion tan absurda como grave.": "What happens if both are accused in the same process? The Statute does not contemplate the dismissal of the Attorney General in these circumstances, so we could witness how an accused Attorney General must dismiss his also accused subordinate. A situation as absurd as it is serious.",
            "Pero hay mas: El Ministerio Fiscal esta personado como acusacion en esta causa penal. Es decir, una parte de la Fiscalia tiene que decidir ahora si acusa a su propio jefe.": "But there's more: The Public Prosecutor's Office is appearing as prosecution in this criminal case. That is, a part of the Prosecutor's Office must now decide whether to accuse its own boss.",
            "Se atrevevan a formular escrito de acusacion contra el Fiscal General del Estado? O veremos una maniobra evasiva ante el conflicto interno mas incomodo imaginable?": "Will they dare to file an indictment against the State Attorney General? Or will we see an evasive maneuver in the face of the most uncomfortable internal conflict imaginable?",
            "Un caso sin precedentes. Un dilema institucional.": "An unprecedented case. An institutional dilemma.",
            "Siguenos en Redes": "Follow us on Social Media"
        }
    },
    {
        "slug": "complice-en-derecho-penal",
        "title": "El complice en el Derecho Penal",
        "desc": "En nuestro ordenamiento juridico, no solo el autor del delito puede ser castigado.",
        "en_title": "The accomplice in Criminal Law",
        "body": [
            "El complice en el Derecho Penal.",
            "En nuestro ordenamiento juridico, no solo el autor del delito puede ser castigado. Tambien lo sera quien coopera de forma secundaria en la comision del hecho delictivo: hablamos hoy del complice.",
            "Que dice el Codigo Penal? El articulo 29 del Codigo Penal define al complice como aquel que, sin ser autor, coopera a la ejecucion del hecho con actos anteriores o simultaneos.",
            "Diferencias clave con el autor: El complice no domina el hecho delictivo. Su participacion es accesoria y no imprescindible para que el delito se lleve a cabo. Su pena suele ser inferior a la del autor.",
            "Ejemplo practico: Si alguien proporciona informacion o materiales que facilitan un robo, pero no participa directamente en el, puede ser considerado complice y responder penalmente por ello."
        ],
        "trans": {
            "El complice en el Derecho Penal.": "The accomplice in Criminal Law.",
            "En nuestro ordenamiento juridico, no solo el autor del delito puede ser castigado. Tambien lo sera quien coopera de forma secundaria en la comision del hecho delictivo: hablamos hoy del complice.": "In our legal system, not only the perpetrator of the crime can be punished. Also, whoever cooperates in a secondary way in the commission of the criminal act will be punished: today we speak of the accomplice.",
            "Que dice el Codigo Penal? El articulo 29 del Codigo Penal define al complice como aquel que, sin ser autor, coopera a la ejecucion del hecho con actos anteriores o simultaneos.": "What does the Penal Code say? Article 29 of the Penal Code defines the accomplice as one who, without being an author, cooperates in the execution of the act with prior or simultaneous acts.",
            "Diferencias clave con el autor: El complice no domina el hecho delictivo. Su participacion es accesoria y no imprescindible para que el delito se lleve a cabo. Su pena suele ser inferior a la del autor.": "Key differences with the author: The accomplice does not dominate the criminal act. Their participation is accessory and not essential for the crime to be carried out. Their penalty is usually lower than that of the author.",
            "Ejemplo practico: Si alguien proporciona informacion o materiales que facilitan un robo, pero no participa directamente en el, puede ser considerado complice y responder penalmente por ello.": "Practical example: If someone provides information or materials that facilitate a robbery, but does not participate directly in it, they can be considered an accomplice and respond criminally for it.",
            "Siguenos en Redes": "Follow us on Social Media"
        }
    },
    {
        "slug": "concurso-acreedores-sin-masa",
        "title": "Concurso de acreedores sin masa",
        "desc": "Tienes deudas que no puedes pagar y ningun bien embargable? Existe una solucion legal rapida.",
        "en_title": "Bankruptcy without mass",
        "body": [
            "Tienes deudas que no puedes pagar y ningun bien embargable? Existe una solucion legal rapida: el concurso de acreedores sin masa.",
            "Este procedimiento judicial permite a personas fisicas y empresas obtener la exoneracion de sus deudas cuando no cuentan con bienes o derechos suficientes para hacer frente a sus obligaciones.",
            "En que consiste? Es un procedimiento agil y simplificado, destinado a quienes ya no tienen patrimonio embargable, pero necesitan una salida legal para empezar de nuevo.",
            "Tramitacion rapida. Ideal para situaciones de insolvencia total. Acceso a una segunda oportunidad real.",
            "Si te encuentras en esta situacion, preparamos solicitud de concurso y guiado durante todo el proceso judicial.",
            "Escribenos por mensaje directo. Primera consulta gratuita."
        ],
        "trans": {
            "Tienes deudas que no puedes pagar y ningun bien embargable? Existe una solucion legal rapida: el concurso de acreedores sin masa.": "Do you have debts that you cannot pay and no attachable assets? There is a quick legal solution: bankruptcy without mass.",
            "Este procedimiento judicial permite a personas fisicas y empresas obtener la exoneracion de sus deudas cuando no cuentan con bienes o derechos suficientes para hacer frente a sus obligaciones.": "This judicial procedure allows individuals and companies to obtain the exoneration of their debts when they do not have sufficient assets or rights to meet their obligations.",
            "En que consiste? Es un procedimiento agil y simplificado, destinado a quienes ya no tienen patrimonio embargable, pero necesitan una salida legal para empezar de nuevo.": "What does it consist of? It is an agile and simplified procedure, aimed at those who no longer have attachable assets, but need a legal way out to start over.",
            "Tramitacion rapida. Ideal para situaciones de insolvencia total. Acceso a una segunda oportunidad real.": "Fast processing. Ideal for situations of total insolvency. Access to a real second chance.",
            "Si te encuentras en esta situacion, preparamos solicitud de concurso y guiado durante todo el proceso judicial.": "If you are in this situation, we prepare bankruptcy requests and guidance throughout the judicial process.",
            "Escribenos por mensaje directo. Primera consulta gratuita.": "Write us by direct message. First consultation free.",
            "Siguenos en Redes": "Follow us on Social Media"
        }
    },
    {
        "slug": "adquisicion-terreno-aluvion-rios",
        "title": "Adquisicion de terreno por efecto del rio (Aluvion)",
        "desc": "El Codigo Civil, en su articulo 366, regula una interesante forma de adquirir terreno mediante el aluvion.",
        "en_title": "Acquisition of land by effect of the river (Alluvium)",
        "body": [
            "Adquisicion de terreno por efecto del rio.",
            'El Codigo Civil, en su articulo 366, regula una interesante forma de adquirir terreno: mediante el conocido en la practica como "aluvion".',
            "Se trata de la adquisicion gradual de tierra por parte de los propietarios de heredades colindantes con los rios, debido a la acumulacion paulatina de sedimentos que arrastra la corriente del agua.",
            "Que significa esto? Si el terreno esta junto a un rio y, con el tiempo, la corriente va depositando tierra y ese terreno se va extendiendo de manera natural y progresiva, ese nuevo terreno puede pasar a ser parte legal de la propiedad.",
            "Esta figura busca dar seguridad juridica sobre como se incorporan al dominio privado estos cambios naturales en el paisaje."
        ],
        "trans": {
            "Adquisicion de terreno por efecto del rio.": "Acquisition of land by effect of the river.",
            'El Codigo Civil, en su articulo 366, regula una interesante forma de adquirir terreno: mediante el conocido en la practica como "aluvion".': 'The Civil Code, in its article 366, regulates an interesting way of acquiring land: through what is known in practice as "alluvium".',
            "Se trata de la adquisicion gradual de tierra por parte de los propietarios de heredades colindantes con los rios, debido a la acumulacion paulatina de sedimentos que arrastra la corriente del agua.": "It is the gradual acquisition of land by the owners of estates adjacent to rivers, due to the gradual accumulation of sediments carried by the water current.",
            "Que significa esto? Si el terreno esta junto a un rio y, con el tiempo, la corriente va depositando tierra y ese terreno se va extendiendo de manera natural y progresiva, ese nuevo terreno puede pasar a ser parte legal de la propiedad.": "What does this mean? If the land is next to a river and, over time, the current deposits earth and that land extends naturally and progressively, that new land can legally become part of the property.",
            "Esta figura busca dar seguridad juridica sobre como se incorporan al dominio privado estos cambios naturales en el paisaje.": "This figure seeks to provide legal certainty on how these natural changes in the landscape are incorporated into the private domain.",
            "Siguenos en Redes": "Follow us on Social Media"
        }
    },
    {
        "slug": "viviendas-uso-turistico-comunidad-valenciana",
        "title": "Analisis sobre el futuro de la vivienda turistica en la Comunidad Valenciana",
        "desc": "Asistimos al curso organizado por la Universidad de Alicante sobre el nuevo escenario para las viviendas de uso turistico.",
        "en_title": "Analysis of the future of tourist housing in the Valencian Community",
        "body": [
            "Analisis sobre el futuro de la vivienda turistica en la Comunidad Valenciana.",
            "Asistimos al curso organizado por la Universidad de Alicante y celebrado en la sede del ICALI, titulado:",
            '"Nuevo escenario para las viviendas de uso turistico en la Comunitat Valenciana tras la entrada en vigor del Decreto Ley 9/2024".',
            "Unas jornadas de reflexion y analisis juridico en la que se abordaron los retos y oportunidades que plantea la nueva normativa, y que reune a expertos academicos y abogados especializados en la materia."
        ],
        "trans": {
            "Analisis sobre el futuro de la vivienda turistica en la Comunidad Valenciana.": "Analysis on the future of tourist housing in the Valencian Community.",
            "Asistimos al curso organizado por la Universidad de Alicante y celebrado en la sede del ICALI, titulado:": "We attended the course organized by the University of Alicante and held at the ICALI headquarters, entitled:",
            '"Nuevo escenario para las viviendas de uso turistico en la Comunitat Valenciana tras la entrada en vigor del Decreto Ley 9/2024".': '"New scenario for housing for tourist use in the Valencian Community after the entry into force of Decree Law 9/2024".',
            "Unas jornadas de reflexion y analisis juridico en la que se abordaron los retos y oportunidades que plantea la nueva normativa, y que reune a expertos academicos y abogados especializados en la materia.": "A conference of reflection and legal analysis in which the challenges and opportunities posed by the new regulations were addressed, bringing together academic experts and lawyers specialized in the matter.",
            "Siguenos en Redes": "Follow us on Social Media"
        }
    },
    {
        "slug": "diferencias-investigado-procesado-acusado",
        "title": "Diferencia conceptual entre ser investigado, procesado, acusado, condenado o absuelto",
        "desc": "Explicamos las diferencias en el sistema penal espanol entre ser investigado, procesado, acusado, condenado o absuelto.",
        "en_title": "Conceptual difference between being investigated, prosecuted, accused, convicted or acquitted",
        "body": [
            "Diferencia conceptual entre ser investigado, procesado, acusado, condenado o absuelto en el sistema penal espanol.",
            '1. Investigado: Es la persona sobre la que hay indicios de haber cometido un delito y esta siendo objeto de una investigacion judicial. Antiguo "imputado".',
            "2. Procesado: el Juzgado ha hallado indicios razonables de criminalidad tras la instruccion y dicta Auto de apertura de juicio oral.",
            "3. Acusado: Una vez se formula acusacion formal por cualquiera de las acusaciones personadas.",
            "4. Condenado: Tras el juicio, celebrado por Juzgado/Tribunal distinto al que ha celebrado la instruccion. Si se demuestra su culpabilidad, el Juzgado/Tribunal dicta una sentencia condenatoria.",
            "5. Absuelto: Si no se prueba la culpabilidad, el juzgado/Tribunal dicta sentencia absolutoria.",
            "Estar investigado o acusado no significa ser culpable."
        ],
        "trans": {
            "Diferencia conceptual entre ser investigado, procesado, acusado, condenado o absuelto en el sistema penal espanol.": "Conceptual difference between being investigated, prosecuted, accused, convicted or acquitted in the Spanish penal system.",
            '1. Investigado: Es la persona sobre la que hay indicios de haber cometido un delito y esta siendo objeto de una investigacion judicial. Antiguo "imputado".': '1. Investigated: This is the person about whom there are indications of having committed a crime and who is the subject of a judicial investigation. Formerly "imputed".',
            "2. Procesado: el Juzgado ha hallado indicios razonables de criminalidad tras la instruccion y dicta Auto de apertura de juicio oral.": "2. Prosecuted: the Court has found reasonable indications of criminality after the investigation and issues an Order to open an oral trial.",
            "3. Acusado: Una vez se formula acusacion formal por cualquiera de las acusaciones personadas.": "3. Accused: Once a formal accusation is formulated by any of the parties involved.",
            "4. Condenado: Tras el juicio, celebrado por Juzgado/Tribunal distinto al que ha celebrado la instruccion. Si se demuestra su culpabilidad, el Juzgado/Tribunal dicta una sentencia condenatoria.": "4. Convicted: After the trial, held by a Court different from the one that held the investigation. If their guilt is proven, the Court issues a guilty verdict.",
            "5. Absuelto: Si no se prueba la culpabilidad, el juzgado/Tribunal dicta sentencia absolutoria.": "5. Acquitted: If guilt is not proven, the Court issues an acquittal.",
            "Estar investigado o acusado no significa ser culpable.": "Being investigated or accused does not mean being guilty.",
            "Siguenos en Redes": "Follow us on Social Media"
        }
    },
    {
        "slug": "asesoramiento-aceptacion-herencia",
        "title": "Vas a aceptar una herencia? Antes de firmar, asesorate",
        "desc": "En la practica diaria es comun ver como muchos sucesores intentan ahorrar costes evitando contratar a un abogado experto.",
        "en_title": "Are you going to accept an inheritance? Before signing, get advice",
        "body": [
            "Vas a aceptar una herencia? Antes de firmar, asesorate.",
            "En la practica diaria es comun ver como muchos sucesores intentan ahorrar costes evitando contratar a un abogado experto en derecho sucesorio. Pero cuando descubren las consecuencias fiscales de haber aceptado una herencia sin planificacion, ya es demasiado tarde.",
            "Impuestos elevados, perdida de beneficios fiscales y decisiones irreversibles son solo algunas de las consecuencias que pueden surgir por no contar con el debido asesoramiento juridico y tributario.",
            "En nuestro despacho, te ayudamos a: Analizar la situacion sucesoria en detalle. Planificar a futuro. Optimizar la carga tributaria.",
            "Si estas por aceptar una herencia, no tomes decisiones sin consultar. Una consulta a tiempo puede significar un gran ahorro economico y evitarte disgustos.",
            "Contactanos y asesorate con profesionales de confianza."
        ],
        "trans": {
            "Vas a aceptar una herencia? Antes de firmar, asesorate.": "Are you going to accept an inheritance? Before signing, get advice.",
            "En la practica diaria es comun ver como muchos sucesores intentan ahorrar costes evitando contratar a un abogado experto en derecho sucesorio. Pero cuando descubren las consecuencias fiscales de haber aceptado una herencia sin planificacion, ya es demasiado tarde.": "In daily practice it is common to see how many successors try to save costs by avoiding hiring an expert lawyer in succession law. But when they discover the tax consequences of having accepted an inheritance without planning, it is already too late.",
            "Impuestos elevados, perdida de beneficios fiscales y decisiones irreversibles son solo algunas de las consecuencias que pueden surgir por no contar con el debido asesoramiento juridico y tributario.": "High taxes, loss of tax benefits, and irreversible decisions are just some of the consequences that can arise from not having proper legal and tax advice.",
            "En nuestro despacho, te ayudamos a: Analizar la situacion sucesoria en detalle. Planificar a futuro. Optimizar la carga tributaria.": "In our firm, we help you to: Analyze the succession situation in detail. Plan for the future. Optimize the tax burden.",
            "Si estas por aceptar una herencia, no tomes decisiones sin consultar. Una consulta a tiempo puede significar un gran ahorro economico y evitarte disgustos.": "If you are about to accept an inheritance, do not make decisions without consulting. A timely consultation can mean great financial savings and spare you trouble.",
            "Contactanos y asesorate con profesionales de confianza.": "Contact us and get advice from trusted professionals.",
            "Siguenos en Redes": "Follow us on Social Media"
        }
    }
]

# ─── BUILD EACH PAGE ───
count = 0
for art in articles:
    slug = art["slug"]
    folder = os.path.join(BASE, slug)
    os.makedirs(folder, exist_ok=True)
    fpath = os.path.join(folder, "index.html")

    # Build article body paragraphs
    paras = "\n".join(f'  <p class="mb-6">{p}</p>' for p in art["body"])

    # Build translation dict (include title + nav items)
    full_trans = dict(art["trans"])
    full_trans[art["title"]] = art["en_title"]
    full_trans["Servicios"] = "Services"
    full_trans["Contacto"] = "Contact"
    full_trans["Blog"] = "Blog"
    full_trans["Volver al Blog"] = "Back to Blog"
    full_trans["Ambito de Actuacion Legal en la Marina Baixa"] = "Legal Coverage Area in the Marina Baixa"

    trans_block = build_translation_script(full_trans)

    # Now build the full page using template structure
    # We take: HEAD (with modified meta) + NAV + HERO + CONTENT + FOOTER
    
    # --- HEAD ---
    head = tpl_head
    head = re.sub(r'<title>.*?</title>', f'<title>{art["title"]} | Blog Saval Garcia Abogados</title>', head)
    head = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{art["desc"]}">', head)
    head = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="https://savalgarciaabogados.es/blog/{slug}/">', head)
    head = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{art["title"]}">', head)
    head = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{art["desc"]}">', head)
    head = re.sub(r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="https://savalgarciaabogados.es/blog/{slug}/">', head)
    head = re.sub(r'<meta name="twitter:title" content="[^"]*">', f'<meta name="twitter:title" content="{art["title"]}">', head)
    head = re.sub(r'<meta name="twitter:description" content="[^"]*">', f'<meta name="twitter:description" content="{art["desc"]}">', head)

    # --- ARTICLE SECTION ---
    article_section = f"""
<!-- ══════════ ARTICLE HERO ══════════ -->
<section id="inicio" aria-label="Blog Article" class="relative pt-16 flex items-center" style="min-height: 25vh; background: var(--carbon);">
  <div class="relative z-20 px-[5vw] py-10 w-full max-w-7xl mx-auto">
    <div class="relative max-w-4xl">
      <a href="../index.html" class="text-[.62rem] font-medium tracking-[.22em] uppercase mb-6 inline-block transition-colors hover:text-white" style="color:var(--gold)">
        &#8592; Volver al Blog
      </a>
      <h1 class="a1 serif text-4xl md:text-5xl lg:text-6xl mb-6 leading-[1.1]" style="color:var(--sand)">{art["title"]}</h1>
    </div>
  </div>
</section>

<!-- ══════════ ARTICLE CONTENT ══════════ -->
<section class="py-10 px-[5vw] max-w-4xl mx-auto min-h-[50vh] text-base sm:text-lg font-light leading-[1.8]" style="background:var(--ivory);color:var(--carbon)">
{paras}

  <div class="mt-16 p-8 rounded-xl flex flex-col sm:flex-row items-center justify-between gap-6" style="border:1px solid rgba(15,28,53,.15)">
    <div>
      <p class="serif text-xl font-semibold mb-2" style="color:var(--carbon)">Necesitas asesoramiento legal?</p>
      <p class="text-sm font-light" style="color:var(--muted)">Contacta con nosotros para programar una cita en nuestro despacho.</p>
    </div>
    <a href="tel:+34614635342" class="flex-shrink-0 text-[.71rem] font-semibold tracking-[.12em] uppercase px-7 py-4 whitespace-nowrap rounded-md transition-transform hover:scale-105" style="background:var(--carbon);color:var(--sand)">
      Llamar ahora
    </a>
  </div>

{SOCIAL_IN_ARTICLE}
</section>
"""

    # --- FOOTER with social ---
    footer_block = f"""
<!-- ══════════ FOOTER ══════════ -->
<footer class="px-[5vw] py-12" style="background:#080f1e">
{SOCIAL_FOOTER}
  <!-- Local links for SEO -->
  <div class="max-w-7xl mx-auto mb-10 pb-8 border-b border-white/10 text-center sm:text-left">
    <p class="text-[.62rem] font-semibold tracking-[.2em] uppercase mb-4 text-white/40">Ambito de Actuacion Legal en la Marina Baixa</p>
    <div class="flex flex-wrap justify-center sm:justify-start gap-x-3 gap-y-2 text-[0.7rem] font-normal text-white/60">
      <a href="../../index.html" class="hover:text-[var(--gold)] transition-colors">Callosa d'en Sarria</a>
      <span class="text-white/20">·</span>
      <a href="../../abogados-la-nucia.html" class="hover:text-[var(--gold)] transition-colors">La Nucia</a>
      <span class="text-white/20">·</span>
      <a href="../../abogados-benidorm.html" class="hover:text-[var(--gold)] transition-colors">Benidorm</a>
      <span class="text-white/20">·</span>
      <a href="../../abogados-altea.html" class="hover:text-[var(--gold)] transition-colors">Altea</a>
      <span class="text-white/20">·</span>
      <a href="../../abogados-calpe.html" class="hover:text-[var(--gold)] transition-colors">Calpe</a>
      <span class="text-white/20">·</span>
      <a href="../../abogados-polop.html" class="hover:text-[var(--gold)] transition-colors">Polop</a>
      <span class="text-white/20">·</span>
      <a href="../../abogados-finestrat.html" class="hover:text-[var(--gold)] transition-colors">Finestrat</a>
      <span class="text-white/20">·</span>
      <a href="../../abogados-alfaz-del-pi.html" class="hover:text-[var(--gold)] transition-colors">Alfaz del Pi</a>
      <span class="text-white/20">·</span>
      <a href="../../abogados-la-vila-joiosa.html" class="hover:text-[var(--gold)] transition-colors">La Vila Joiosa</a>
      <span class="text-white/20">·</span>
      <a href="../../abogados-alicante.html" class="hover:text-[var(--gold)] transition-colors">Alicante</a>
    </div>
  </div>
  <div class="flex items-center justify-between flex-wrap gap-4">
    <div class="flex items-center gap-3">
      <div class="w-8 h-8 flex items-center justify-center" style="border:1px solid rgba(201,168,76,.35);background:rgba(255,255,255,.02)">
        <img src="../../logo.webp" alt="Logo Saval Garcia" class="w-full h-full object-cover">
      </div>
      <span class="serif text-[.82rem]" style="color:rgba(240,232,213,.75)">
        <b class="font-semibold" style="color:rgba(240,232,213,.95)">Saval Garcia</b> Abogados - Callosa d'en Sarria
      </span>
    </div>
    <div class="text-[.67rem] text-right" style="color:rgba(240,232,213,.55)">
      <p class="mb-1">2026 - C/ Ramon y Cajal, 14 - 03510 Callosa d'en Sarria - <span itemprop="addressRegion">Alicante</span></p>
      <p>
        <a href="../../politica-de-privacidad.html" class="hover:text-[var(--gold)] transition-colors">Politica de Privacidad</a>
        <span class="mx-2 opacity-50">|</span>
        <a href="../../aviso-legal.html" class="hover:text-[var(--gold)] transition-colors">Terminos y Condiciones</a>
      </p>
    </div>
  </div>
</footer>
</main>
"""

    # --- WhatsApp button ---
    wa_button = """
<!-- Boton Flotante de WhatsApp -->
<a href="https://wa.me/34614635342?text=Hola%2C%20quer%C3%ADa%20consultar%20un%20caso." 
   target="_blank" 
   rel="noopener" 
   class="fixed bottom-6 right-6 z-40 flex items-center justify-center w-14 h-14 rounded-full shadow-lg transition-transform hover:scale-110 active:scale-95 hover:shadow-2xl" 
   style="background:#25D366; color:white; border: 1.5px solid rgba(255,255,255,0.25);" 
   aria-label="Contactar por WhatsApp">
  <svg class="w-7 h-7" fill="currentColor" viewBox="0 0 24 24">
    <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/>
  </svg>
</a>
"""

    # --- Mobile menu script ---
    mobile_script = """
<script>
  /* Mobile menu logic for blog */
  (function(){
    const btn = document.getElementById('mobile-menu-btn');
    const nav = document.getElementById('mobile-nav');
    const burgerIcon = document.getElementById('hamburger-icon');
    const closeIcon = document.getElementById('close-icon');
    const links = document.querySelectorAll('.mob-link');
    if(!btn || !nav) return;
    function toggle() {
      const open = nav.classList.contains('active');
      if (open) {
        nav.classList.remove('active');
        burgerIcon.classList.remove('hidden');
        closeIcon.classList.add('hidden');
        document.body.style.overflow = '';
      } else {
        nav.classList.add('active');
        burgerIcon.classList.add('hidden');
        closeIcon.classList.remove('hidden');
        document.body.style.overflow = 'hidden';
      }
    }
    btn.addEventListener('click', toggle);
    links.forEach(l => {
      l.addEventListener('click', (e) => {
        const targetId = l.getAttribute('href');
        e.preventDefault();
        nav.classList.remove('active');
        burgerIcon.classList.remove('hidden');
        closeIcon.classList.add('hidden');
        document.body.style.overflow = '';
        if (targetId) {
          setTimeout(() => { window.location.href = targetId; }, 150);
        }
      });
    });
  })();
</script>
"""

    # Assemble full page
    full_page = head + "</head>\n<body>\n"
    full_page += '<div id="scroll-progress" aria-hidden="true"></div>\n'
    full_page += '<main id="main-content">\n'
    full_page += nav_block
    full_page += article_section
    full_page += footer_block
    full_page += wa_button
    full_page += trans_block
    full_page += mobile_script
    full_page += "</body>\n</html>\n"

    with open(fpath, "w", encoding="utf-8") as f:
        f.write(full_page)
    count += 1
    print(f"  [{count}/22] {slug}/index.html")

print(f"\nDone! Generated {count} blog article pages.")

# ─── Update blog/index.html posts array ───
idx_path = os.path.join(BASE, "index.html")
with open(idx_path, "r", encoding="utf-8") as f:
    idx = f.read()

# Check if posts already added (look for one of our slugs)
if "desahucio-grandes-tenedores" not in idx:
    # Find const posts = [...];
    m = re.search(r'(const posts\s*=\s*\[)(.*?)(\];)', idx, re.DOTALL)
    if m:
        old_posts = m.group(2).rstrip().rstrip(',')
        new_entries = ""
        for art in articles:
            new_entries += f"""
    {{
      title: "{art['title']}",
      excerpt: "{art['desc']}",
      link: "{art['slug']}/index.html"
    }},"""
        new_array = m.group(1) + old_posts + "," + new_entries + "\n  " + m.group(3)
        idx = idx[:m.start()] + new_array + idx[m.end():]
        with open(idx_path, "w", encoding="utf-8") as f:
            f.write(idx)
        print("Updated blog/index.html with 22 new posts in the array.")
    else:
        print("WARNING: Could not find posts array in blog/index.html")
else:
    print("Posts already present in blog/index.html, skipping.")

print("\nAll done!")
