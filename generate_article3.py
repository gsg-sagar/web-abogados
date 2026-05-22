import os

source_path = 'C:/Users/USUARIO/Documents/savalgarciabogados/blog/la-terceria-de-dominio/index.html'
dest_dir = 'C:/Users/USUARIO/Documents/savalgarciabogados/blog/contrato-de-opcion-de-compra'
dest_path = os.path.join(dest_dir, 'index.html')

os.makedirs(dest_dir, exist_ok=True)

with open(source_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Replace titles
html = html.replace('La tercería de dominio', 'Contrato de opción de compra: una oportunidad para comprar con más tiempo')
html = html.replace('Third-Party Ownership Claim (Tercería de dominio)', 'Purchase Option Agreement: an opportunity to buy with more time')

# Replace content section start
content_start_marker = '<!-- ══════════ ARTICLE CONTENT ══════════ -->'
content_start = html.find(content_start_marker)
footer_start_marker = '<!-- ══════════ FOOTER ══════════ -->'
footer_start = html.find(footer_start_marker)

top_part = html[:content_start]
footer_part = html[footer_start:]

article_html = f'''{content_start_marker}
<section class="py-10 px-[5vw] max-w-4xl mx-auto min-h-[50vh] text-base sm:text-lg font-light leading-[1.8]" style="background:var(--ivory);color:var(--carbon)">
  
  <p class="mb-6">La opción de compra es un acuerdo por el que el propietario concede a otra persona el derecho a comprar un inmueble dentro de un plazo determinado y por un precio previamente fijado. Este tipo de contrato se utiliza con frecuencia cuando el comprador no dispone en ese momento de todos los recursos económicos para adquirir el inmueble. De esta forma, el optante obtiene tiempo para reunir financiación para posteriormente ejecutar la compra.</p>
  
  <p class="mb-6">Algunas características importantes:</p>
  <ul class="list-disc pl-6 mb-6 space-y-2">
    <li>Otorga un derecho exclusivo de compra durante un plazo determinado.</li>
    <li>El precio de la vivienda queda fijado desde el inicio.</li>
    <li>Puede inscribirse en el Registro de la Propiedad.</li>
    <li>Posible combinación con un contrato de arrendamiento.</li>
    <li>Puede incluirse una cláusula de elevación a público unilateralmente, que permite al optante formalizar la compraventa en escritura pública sin la firma del propietario para ejercitar la opción.</li>
  </ul>
  
  <figure class="my-12">
    <img src="../opcioncompra.webp" alt="Contrato de opción de compra" class="w-full rounded-xl shadow-lg" style="border: 1px solid rgba(15,28,53,0.05);" />
    <figcaption class="text-sm mt-3 text-center" style="color:var(--muted)">Asegure su compra con tiempo.</figcaption>
  </figure>
  
  <hr class="my-12 border-t" style="border-color:rgba(15,28,53,0.1)" />
  
  <h2 class="serif text-3xl font-semibold mb-6" style="color:var(--carbon)">Purchase Option Agreement: an opportunity to buy with more time</h2>
  
  <p class="mb-6">A purchase option agreement is an arrangement whereby the owner grants another person the right to buy a property within a specified period and at a previously agreed price. This type of contract is often used when the buyer does not have sufficient financial resources at that moment to acquire the property. In this way, the option holder gains time to secure financing and later proceed with the purchase.</p>
  
  <p class="mb-6">Some key features:</p>
  <ul class="list-disc pl-6 mb-6 space-y-2">
    <li>It grants an exclusive right to purchase for a specified period.</li>
    <li>The purchase price of the property is fixed from the outset.</li>
    <li>It may be registered with the Land Registry.</li>
    <li>It can be combined with a lease agreement.</li>
    <li>It may include a unilateral clause allowing the agreement to be formalised in a public deed, enabling the option holder to formalise the sale before a notary without the owner’s signature once the option is exercised.</li>
  </ul>
</section>

'''

with open(dest_path, 'w', encoding='utf-8') as f:
    f.write(top_part + article_html + footer_part)
