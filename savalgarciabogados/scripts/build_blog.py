import sys, re, os

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Extract from start to the end of mobile menu
# Mobile menu ends at <!-- ══════════ HERO ══════════ -->
header_match = re.search(r'(.*?)(?=<!-- ══════════ HERO ══════════ -->)', html, re.DOTALL)
if not header_match:
    print('Could not find header in index.html')
    sys.exit(1)

header_content = header_match.group(1)

# Fix paths for blog index (which is one level deep)
blog_head = header_content.replace('href="favicon', 'href="../favicon')
blog_head = blog_head.replace('href="apple-touch', 'href="../apple-touch')
blog_head = blog_head.replace('href="site.webmanifest"', 'href="../site.webmanifest"')
blog_head = blog_head.replace('src="logo.jpg"', 'src="../logo.jpg"')
blog_head = blog_head.replace('href="#', 'href="/#')

blog_html = blog_head + '''
<!-- ══════════ BLOG HERO ══════════ -->
<section id="inicio" aria-label="Blog — Saval García Abogados" class="relative pt-16 flex items-center" style="min-height: 50vh;">
  <div class="absolute inset-0 bg-gradient-to-r from-[var(--carbon)] via-[var(--carbon)]/80 md:via-[var(--carbon)]/40 to-transparent"></div>
  <div class="absolute inset-0 bg-gradient-to-t from-[var(--carbon)] via-transparent to-transparent"></div>
  <div class="relative z-20 px-[5vw] py-[8vw] w-full max-w-7xl mx-auto">
    <div class="relative max-w-3xl">
      <p class="a1 text-[.62rem] font-medium tracking-[.22em] uppercase mb-8" style="color:var(--gold)">
        Saval García Abogados · Desde 1989
      </p>
      <h1 class="a2 serif font-normal leading-[1.04] mb-7" style="color:var(--sand);font-size:clamp(3rem,5vw,5.5rem)">
        Blog
      </h1>
      <p class="a3 text-base sm:text-lg font-light leading-[1.8] mb-10 text-white/70">
        Encuentre artículos, actualidad jurídica y noticias sobre nuestros servicios.
      </p>
    </div>
  </div>
</section>

<!-- ══════════ BLOG POSTS ══════════ -->
<section class="py-24 px-[5vw] max-w-5xl mx-auto min-h-[50vh]" style="background:var(--ivory)">
  <div class="mb-12">
    <input type="text" id="search" placeholder="Buscar artículos..." class="w-full p-4 rounded-lg focus:outline-none focus:ring-2 focus:ring-[var(--gold)] transition-shadow" style="background:var(--sand);color:var(--carbon);border:1px solid rgba(15,28,53,0.1);" />
  </div>
  <ul id="posts" class="space-y-6">
    <!-- Posts will be injected here -->
  </ul>
</section>

<script>
  const posts = [
    { title: "Campaña de la Renta 2025: Información y servicios de gestión", slug: "campana-de-la-renta-2025", excerpt: "Todo lo que necesita saber sobre la campaña de IRPF 2025 y cómo podemos ayudarle a presentar su declaración sin errores." }
  ];
  const postsContainer = document.getElementById('posts');
  const render = (list) => {
    postsContainer.innerHTML = '';
    if(list.length === 0) {
      postsContainer.innerHTML = '<li class="p-6 rounded-xl text-center" style="background:var(--sand);color:var(--muted);">No se encontraron artículos.</li>';
      return;
    }
    list.forEach(p => {
      const li = document.createElement('li');
      li.className = 'sv p-6 sm:p-8 rounded-xl transition-all duration-300';
      li.innerHTML = `
        <div class="sv-b w-5 h-px mb-4" style="background:rgba(15,28,53,.18)"></div>
        <a href="${p.slug}/" class="block group">
          <h3 class="serif text-2xl sm:text-3xl font-semibold mb-3 transition-colors group-hover:text-[var(--gold)]" style="color:var(--carbon)">${p.title}</h3>
          <p class="text-sm font-light leading-[1.75] mb-6" style="color:var(--muted)">${p.excerpt}</p>
          <span class="text-[.65rem] font-semibold tracking-[.12em] uppercase inline-block transition-colors pb-px" style="color:var(--gold);border-bottom:1px solid var(--gold)">Leer artículo →</span>
        </a>
      `;
      postsContainer.appendChild(li);
    });
  };
  render(posts);
  document.getElementById('search').addEventListener('input', (e) => {
    const query = e.target.value.toLowerCase();
    const filtered = posts.filter(p => p.title.toLowerCase().includes(query) || p.excerpt.toLowerCase().includes(query));
    render(filtered);
  });
</script>

<!-- ══════════ FOOTER ══════════ -->
<footer style="background:var(--carbon);color:rgba(240,232,213,.5);padding:5rem 5vw">
  <div class="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-6">
    <div class="text-center md:text-left">
      <p class="serif text-2xl font-normal mb-2" style="color:var(--sand)">Saval García</p>
      <p class="text-[.65rem] font-medium tracking-[.15em] uppercase" style="color:var(--gold)">Abogados</p>
    </div>
    <div class="text-center md:text-right text-xs font-light leading-[1.8]">
      <p>C/ Ramón y Cajal, 14, 1º · 03510 Callosa d'en Sarrià, Alicante</p>
      <p class="mt-1">© 2026 Saval García Abogados · Todos los derechos reservados</p>
    </div>
  </div>
</footer>
</main>
</body>
</html>
'''

os.makedirs('blog', exist_ok=True)
with open('blog/index.html', 'w', encoding='utf-8') as f:
    f.write(blog_html)


# Now create the article
article_head = header_content.replace('href="favicon', 'href="../../favicon')
article_head = article_head.replace('href="apple-touch', 'href="../../apple-touch')
article_head = article_head.replace('href="site.webmanifest"', 'href="../../site.webmanifest"')
article_head = article_head.replace('src="logo.jpg"', 'src="../../logo.jpg"')
article_head = article_head.replace('href="#', 'href="/#')

article_html = article_head + '''
<!-- ══════════ ARTICLE HERO ══════════ -->
<section id="inicio" aria-label="Blog Article" class="relative pt-16 flex items-center" style="min-height: 40vh;">
  <div class="absolute inset-0 bg-gradient-to-r from-[var(--carbon)] via-[var(--carbon)]/80 md:via-[var(--carbon)]/40 to-transparent"></div>
  <div class="absolute inset-0 bg-gradient-to-t from-[var(--carbon)] via-transparent to-transparent"></div>
  <div class="relative z-20 px-[5vw] py-[8vw] w-full max-w-7xl mx-auto">
    <div class="relative max-w-4xl">
      <a href="/blog/" class="text-[.62rem] font-medium tracking-[.22em] uppercase mb-6 inline-block transition-colors hover:text-white" style="color:var(--gold)">
        ← Volver al Blog
      </a>
      <h1 class="a2 serif font-normal leading-[1.04] mb-7" style="color:var(--sand);font-size:clamp(2.5rem,4vw,4.5rem)">
        Campaña de la Renta 2025: Información y servicios de gestión
      </h1>
    </div>
  </div>
</section>

<!-- ══════════ ARTICLE CONTENT ══════════ -->
<section class="py-20 px-[5vw] max-w-4xl mx-auto min-h-[50vh] text-base sm:text-lg font-light leading-[1.8]" style="background:var(--ivory);color:var(--carbon)">
  
  <p class="mb-6">Desde el pasado 8 de abril, la campaña del Impuesto sobre la Renta de las Personas Físicas (IRPF) correspondiente al ejercicio 2025 ya está abierta.</p>
  
  <p class="mb-6">Si necesita ayuda para realizar su declaración, nuestro equipo se encarga de todo el proceso de liquidación de forma rápida, clara y sin complicaciones. Contar con asesoramiento profesional le permite evitar errores, ahorrar tiempo y asegurarse de que su renta sea presentada correctamente ante la Agencia Tributaria.</p>
  
  <hr class="my-12 border-t" style="border-color:rgba(15,28,53,0.1)" />
  
  <h2 class="serif text-3xl font-semibold mb-6" style="color:var(--carbon)">2025 Tax Return Campaign: Information and Management Services</h2>
  
  <p class="mb-6">The 2025 Personal Income Tax (IRPF) campaign has been open since April 8.</p>
  
  <p class="mb-6">If you require assistance with your tax return, we handle the entire filing process for you, ensuring it is done quickly, clearly, and hassle-free. Professional tax advisory helps you avoid errors, save time, and ensure that your tax return is filed correctly.</p>

  <div class="mt-16 p-8 rounded-xl flex flex-col sm:flex-row items-center justify-between gap-6" style="border:1px solid rgba(15,28,53,.15)">
    <div>
      <p class="serif text-xl font-semibold mb-2" style="color:var(--carbon)">¿Necesita gestionar su declaración de la renta?</p>
      <p class="text-sm font-light" style="color:var(--muted)">Contacte con nosotros para programar una cita en nuestro despacho.</p>
    </div>
    <a href="tel:+34614635342" class="flex-shrink-0 text-[.71rem] font-semibold tracking-[.12em] uppercase px-7 py-4 whitespace-nowrap rounded-md transition-transform hover:scale-105" style="background:var(--carbon);color:var(--sand)">
      Llamar ahora
    </a>
  </div>
</section>

<!-- ══════════ FOOTER ══════════ -->
<footer style="background:var(--carbon);color:rgba(240,232,213,.5);padding:5rem 5vw">
  <div class="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-6">
    <div class="text-center md:text-left">
      <p class="serif text-2xl font-normal mb-2" style="color:var(--sand)">Saval García</p>
      <p class="text-[.65rem] font-medium tracking-[.15em] uppercase" style="color:var(--gold)">Abogados</p>
    </div>
    <div class="text-center md:text-right text-xs font-light leading-[1.8]">
      <p>C/ Ramón y Cajal, 14, 1º · 03510 Callosa d'en Sarrià, Alicante</p>
      <p class="mt-1">© 2026 Saval García Abogados · Todos los derechos reservados</p>
    </div>
  </div>
</footer>
</main>
</body>
</html>
'''

os.makedirs('blog/campana-de-la-renta-2025', exist_ok=True)
with open('blog/campana-de-la-renta-2025/index.html', 'w', encoding='utf-8') as f:
    f.write(article_html)

print("Blog pages generated successfully!")
