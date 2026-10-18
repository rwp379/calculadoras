import os, html
BASE = os.environ.get("BASE", "/calculadoras")
SITE = "Calculadoras Úteis"
SITEURL = os.environ.get("SITEURL", "https://rwp379.github.io/calculadoras")
tools = [
 dict(slug="calculadora-de-tinta", title="Calculadora de Tinta: quantos litros comprar?", short="Tinta para parede",
  desc="Calcule quantos litros de tinta você precisa para pintar paredes, descontando portas e janelas.",
  fields=[("w","Largura da parede (m)",4),("h","Altura da parede (m)",2.7),("n","Número de paredes iguais",4),("o","Área de portas/janelas a descontar (m²)",3),("c","Demãos",2),("r","Rendimento da tinta (m²/L por demão)",10)],
  js="var a=(w*h*n-o);if(a<0)a=0;var l=a*c/r;return 'Área a pintar: '+f(a)+' m²<br>Tinta necessária: <b>'+f(l)+' litros</b><br>Sugestão: '+Math.ceil(l*1.1/3.6)+' lata(s) de 3,6 L (com 10% de margem)';",
  text="O rendimento varia por marca e superfície (em geral 8 a 12 m² por litro por demão; veja a embalagem). A calculadora multiplica a área líquida pelas demãos e divide pelo rendimento. A margem de 10% cobre perdas e retoques.",
  aff=("Rolos e pincéis para pintura","rolo-de-pintura")),
 dict(slug="calculadora-de-piso", title="Calculadora de Piso e Revestimento", short="Piso / revestimento",
  desc="Descubra quantos metros quadrados e caixas de piso comprar, incluindo a perda por corte.",
  fields=[("c","Comprimento do ambiente (m)",5),("l","Largura do ambiente (m)",4),("p","Perda por corte (%)",10),("cx","Metragem por caixa (m²)",2.5)],
  js="var a=c*l;var t=a*(1+p/100);return 'Área do ambiente: '+f(a)+' m²<br>Com perda: <b>'+f(t)+' m²</b><br>Caixas: <b>'+Math.ceil(t/cx)+'</b>';",
  text="Use 5% a 10% de perda para pisos retos e 15% para assentamento em diagonal ou ambientes com muitos recortes. Compre tudo do mesmo lote para evitar diferença de tom.",
  aff=("Ferramentas para assentar piso","kit-assentamento-piso")),
 dict(slug="calculadora-de-concreto", title="Calculadora de Concreto (volume e traço)", short="Concreto",
  desc="Calcule o volume de concreto de lajes, sapatas e pisos e a quantidade aproximada de cimento, areia e brita.",
  fields=[("c","Comprimento (m)",4),("l","Largura (m)",3),("e","Espessura (cm)",10)],
  js="var v=c*l*e/100;var m=v*1.05;return 'Volume: '+f(v)+' m³ (com 5% de folga: <b>'+f(m)+' m³</b>)<br>Traço 1:2:3 aproximado por m³: ~7 sacos de cimento de 50 kg, ~0,5 m³ de areia, ~0,8 m³ de brita.<br>Para seu volume: ~'+Math.ceil(m*7)+' sacos de cimento, '+f(m*0.5)+' m³ de areia, '+f(m*0.8)+' m³ de brita';",
  text="Os consumos de traço são estimativas usuais; o dimensionamento estrutural deve seguir projeto de um profissional habilitado. Esta ferramenta serve para estimar volume e compra de materiais.",
  aff=("Ferramentas para obra","carrinho-de-mao-obra")),
 dict(slug="calculadora-de-juros-compostos", title="Calculadora de Juros Compostos", short="Juros compostos",
  desc="Simule o crescimento de um investimento com juros compostos e aportes mensais.",
  fields=[("p","Valor inicial (R$)",1000),("a","Aporte mensal (R$)",200),("i","Taxa de juros ao mês (%)",1),("n","Prazo (meses)",24)],
  js="var s=p,t=i/100;for(var k=0;k<n;k++){s=s*(1+t)+a;}var inv=p+a*n;return 'Total investido: R$ '+f(inv)+'<br>Montante final: <b>R$ '+f(s)+'</b><br>Juros ganhos: R$ '+f(s-inv);",
  text="Fórmula: a cada mês o saldo recebe juros e depois o aporte é somado. É uma simulação matemática, não uma promessa de rendimento nem recomendação de investimento.",
  aff=None),
 dict(slug="calculadora-de-porcentagem", title="Calculadora de Porcentagem", short="Porcentagem",
  desc="Calcule quanto é X% de um valor, variação percentual e desconto de forma rápida.",
  fields=[("x","Percentual (%)",15),("y","Valor (R$ ou outro)",200),("a","Valor antigo (para variação)",80),("b","Valor novo (para variação)",100)],
  js="return x+'% de '+f(y)+' = <b>'+f(y*x/100)+'</b><br>'+f(y)+' com desconto de '+x+'% = '+f(y*(1-x/100))+'<br>'+f(y)+' com acréscimo de '+x+'% = '+f(y*(1+x/100))+'<br>Variação de '+f(a)+' para '+f(b)+': <b>'+f(a?(b-a)/a*100:0)+'%</b>';",
  text="Percentual de um valor = valor × percentual ÷ 100. Variação percentual = (novo − antigo) ÷ antigo × 100.",
  aff=None),
 dict(slug="calculadora-de-imc", title="Calculadora de IMC", short="IMC",
  desc="Calcule seu Índice de Massa Corporal e veja a classificação da OMS.",
  fields=[("m","Peso (kg)",70),("h","Altura (m)",1.75)],
  js="if(!h)return 'Informe a altura.';var v=m/(h*h);var c=v<18.5?'abaixo do peso':v<25?'peso normal':v<30?'sobrepeso':v<35?'obesidade grau I':v<40?'obesidade grau II':'obesidade grau III';return 'IMC: <b>'+f(v)+'</b> — '+c+'<br><small>Indicador de triagem; não substitui avaliação de um profissional de saúde.</small>';",
  text="IMC = peso ÷ altura². Classificação da OMS para adultos: abaixo de 18,5; 18,5–24,9 normal; 25–29,9 sobrepeso; 30 ou mais obesidade. Não considera massa muscular, idade ou sexo.",
  aff=None),
]
CSS = "body{font-family:system-ui,sans-serif;max-width:720px;margin:0 auto;padding:16px;line-height:1.5;color:#222}header a{font-weight:700;text-decoration:none;color:#0a58ca}label{display:block;margin:10px 0 2px}input{width:100%;padding:8px;font-size:16px;box-sizing:border-box}button{margin-top:14px;padding:10px 18px;font-size:16px;background:#0a58ca;color:#fff;border:0;border-radius:6px;cursor:pointer}#res{margin-top:16px;padding:14px;background:#eef4ff;border-radius:8px}footer{margin-top:40px;font-size:13px;color:#666}li{margin:6px 0}"

def page(t, body, desc, canon):
    return (f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{html.escape(t)}</title><meta name="description" content="{html.escape(desc)}"><link rel="canonical" href="{canon}"><style>{CSS}</style></head>'
            f'<body><header><a href="{BASE}/">{SITE}</a></header>{body}<footer>Resultados são estimativas para fins informativos. '
            f'<a href="{BASE}/sobre.html">Sobre</a> · <a href="{BASE}/privacidade.html">Privacidade</a></footer></body></html>')

def w(name, s):
    open("docs/" + name, "w", encoding="utf-8").write(s)

os.makedirs("docs", exist_ok=True)
urls = [""]
for t in tools:
    fl = "".join(f'<label for="{k}">{html.escape(lb)}</label><input id="{k}" type="number" step="any" value="{v}">' for k, lb, v in t["fields"])
    assigns = "".join(f'var {k}=parseFloat(document.getElementById("{k}").value)||0;' for k, _, _ in t["fields"])
    aff = ""
    if t["aff"]:
        aff = f'<h2>Materiais úteis</h2><p><a rel="sponsored noopener" href="https://lista.mercadolivre.com.br/{t["aff"][1]}">{t["aff"][0]} no Mercado Livre</a></p>'
    script = ('<script>function f(x){return x.toLocaleString("pt-BR",{maximumFractionDigits:2})}function calc(){' + assigns +
              'document.getElementById("res").innerHTML=(function(){' + t["js"] + '})();return false}</script>')
    body = (f'<h1>{html.escape(t["title"])}</h1><p>{html.escape(t["desc"])}</p><form onsubmit="return calc()">{fl}<button>Calcular</button></form>'
            f'<div id="res" aria-live="polite">Preencha os valores e clique em Calcular.</div><h2>Como funciona</h2><p>{html.escape(t["text"])}</p>{aff}{script}')
    w(t["slug"] + ".html", page(t["title"] + " | " + SITE, body, t["desc"], f'{SITEURL}/{t["slug"]}.html'))
    urls.append(t["slug"] + ".html")
lst = "".join(f'<li><a href="{BASE}/{t["slug"]}.html">{t["short"]}</a> — {html.escape(t["desc"])}</li>' for t in tools)
w("index.html", page(SITE + " — ferramentas gratuitas", f'<h1>{SITE}</h1><p>Ferramentas gratuitas em português para obra, finanças e dia a dia.</p><ul>{lst}</ul>', "Calculadoras gratuitas: tinta, piso, concreto, juros compostos, porcentagem e IMC.", SITEURL + "/"))
w("sobre.html", page("Sobre | " + SITE, "<h1>Sobre</h1><p>Site de calculadoras gratuitas. Os textos e ferramentas são criados com auxílio de inteligência artificial. Os resultados são estimativas e não substituem orientação profissional.</p>", "Sobre o site", SITEURL + "/sobre.html"))
w("privacidade.html", page("Privacidade | " + SITE, "<h1>Política de privacidade</h1><p>Os cálculos são feitos no seu navegador; os valores digitados não são enviados a nenhum servidor. Futuramente o site poderá exibir anúncios (Google AdSense) e links de afiliados, que podem usar cookies de terceiros conforme as políticas desses serviços.</p>", "Política de privacidade", SITEURL + "/privacidade.html"))
urls += ["sobre.html", "privacidade.html"]
w("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + "".join(f"<url><loc>{SITEURL}/{u}</loc></url>" for u in urls) + "</urlset>")
w("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {SITEURL}/sitemap.xml\n")
