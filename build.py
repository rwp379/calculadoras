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
 dict(slug="calculadora-de-tijolos", title="Calculadora de Tijolos e Blocos por m²", short="Tijolos / blocos",
  desc="Calcule quantos tijolos ou blocos comprar para uma parede, com junta de argamassa e perda.",
  fields=[("c","Comprimento da parede (m)",5),("h","Altura da parede (m)",2.8),("o","Aberturas a descontar (m²)",2),("bl","Comprimento do bloco (cm)",19),("bh","Altura do bloco (cm)",19),("j","Espessura da junta (cm)",1),("p","Perda (%)",5)],
  js="var a=c*h-o;if(a<0)a=0;var u=1/(((bl+j)/100)*((bh+j)/100));var t=a*u*(1+p/100);return 'Área da parede: '+f(a)+' m²<br>Blocos por m²: '+f(u)+'<br>Total com perda: <b>'+Math.ceil(t)+' unidades</b>';",
  text="Blocos por m² = 1 ÷ [(comprimento + junta) × (altura + junta)], com medidas em metros. Para bloco cerâmico 9×19×19 cm com junta de 1 cm, são cerca de 25 por m². Use 5% a 10% de perda para quebras.",
  aff=("Ferramentas de pedreiro","colher-de-pedreiro")),
 dict(slug="calculadora-de-reboco", title="Calculadora de Argamassa de Reboco", short="Reboco / argamassa",
  desc="Estime o volume de argamassa e a quantidade de cimento, cal e areia para rebocar paredes.",
  fields=[("a","Área a rebocar (m²)",30),("e","Espessura média (cm)",2),("p","Perda (%)",10)],
  js="var v=a*e/100*(1+p/100);return 'Volume de argamassa: <b>'+f(v)+' m³</b><br>Traço 1:2:8 (cimento:cal:areia) aproximado por m³: ~3,6 sacos de cimento de 50 kg, ~7 sacos de cal de 20 kg, ~1,2 m³ de areia.<br>Para seu volume: ~'+Math.ceil(v*3.6)+' sacos de cimento, ~'+Math.ceil(v*7)+' sacos de cal, '+f(v*1.2)+' m³ de areia';",
  text="Volume = área × espessura. Reboco interno costuma ter 1,5 a 2 cm e externo 2 a 3 cm. Os consumos de traço são estimativas usuais e variam com a umidade da areia e o tipo de material; argamassa industrializada traz o rendimento na embalagem.",
  aff=("Desempenadeiras e ferramentas de reboco","desempenadeira")),
 dict(slug="calculadora-de-contrapiso", title="Calculadora de Contrapiso", short="Contrapiso",
  desc="Calcule o volume de argamassa de contrapiso e os sacos de cimento e areia necessários.",
  fields=[("c","Comprimento (m)",5),("l","Largura (m)",4),("e","Espessura (cm)",4),("p","Perda (%)",5)],
  js="var v=c*l*e/100*(1+p/100);return 'Área: '+f(c*l)+' m²<br>Volume: <b>'+f(v)+' m³</b><br>Traço 1:4 aproximado por m³: ~6,5 sacos de cimento de 50 kg e ~1,1 m³ de areia.<br>Para seu volume: ~'+Math.ceil(v*6.5)+' sacos de cimento e '+f(v*1.1)+' m³ de areia';",
  text="O contrapiso costuma ter de 3 a 5 cm de espessura. Volume = área × espessura. Os consumos são estimativas usuais para traço 1:4 (cimento:areia) e variam conforme os materiais.",
  aff=("Réguas e níveis para contrapiso","regua-de-aluminio-pedreiro")),
 dict(slug="calculadora-de-telhas", title="Calculadora de Telhas para Telhado", short="Telhas",
  desc="Calcule a área do telhado considerando a inclinação e quantas telhas comprar.",
  fields=[("c","Comprimento da projeção do telhado (m)",10),("l","Largura da projeção do telhado (m)",8),("i","Inclinação (%)",30),("t","Telhas por m² (veja o fabricante)",16),("p","Perda (%)",5)],
  js="var fc=Math.sqrt(1+Math.pow(i/100,2));var a=c*l*fc;return 'Fator de inclinação: '+f(fc)+'<br>Área real do telhado: <b>'+f(a)+' m²</b><br>Telhas: <b>'+Math.ceil(a*t*(1+p/100))+' unidades</b>';",
  text="A área real é a área em planta multiplicada pelo fator de inclinação √(1 + i²), com i em decimal. Telhas cerâmicas tipo romana ficam em torno de 16 por m² e as francesas em torno de 15; confirme no fabricante.",
  aff=("Ferramentas para telhado","ferramentas-telhado")),
 dict(slug="calculadora-de-juros-simples", title="Calculadora de Juros Simples", short="Juros simples",
  desc="Calcule juros simples e o montante final a partir do capital, taxa e prazo.",
  fields=[("p","Capital (R$)",1000),("i","Taxa de juros ao mês (%)",2),("n","Prazo (meses)",6)],
  js="var j=p*i/100*n;return 'Juros: <b>R$ '+f(j)+'</b><br>Montante: <b>R$ '+f(p+j)+'</b>';",
  text="Juros simples: J = C × i × t, e montante M = C + J. Diferente dos juros compostos, os juros não incidem sobre os juros já acumulados.",
  aff=None),
 dict(slug="calculadora-de-financiamento", title="Calculadora de Financiamento (Tabela Price)", short="Financiamento / parcelas",
  desc="Simule o valor da parcela de um empréstimo ou financiamento pela Tabela Price.",
  fields=[("v","Valor financiado (R$)",20000),("i","Taxa de juros ao mês (%)",1.5),("n","Número de parcelas",36)],
  js="if(n<=0)return 'Informe as parcelas.';var t=i/100;var pm=t?v*t/(1-Math.pow(1+t,-n)):v/n;return 'Parcela: <b>R$ '+f(pm)+'</b><br>Total pago: R$ '+f(pm*n)+'<br>Juros totais: R$ '+f(pm*n-v);",
  text="Na Tabela Price as parcelas são fixas: PMT = PV × i ÷ (1 − (1 + i)^−n). A simulação não inclui tarifas, seguros e IOF, que entram no Custo Efetivo Total (CET) informado pelo banco.",
  aff=None),
 dict(slug="calculadora-regra-de-tres", title="Calculadora de Regra de Três", short="Regra de três",
  desc="Resolva regra de três simples direta ou inversa em segundos.",
  fields=[("a","A",2),("b","B (corresponde a A)",10),("c","C",5)],
  js="if(!a)return 'A não pode ser zero.';return 'Direta (A está para B assim como C está para X): X = <b>'+f(b*c/a)+'</b><br>Inversa: X = <b>'+(c?f(a*b/c):'—')+'</b>';",
  text="Regra de três direta: X = B × C ÷ A (as grandezas crescem juntas). Inversa: X = A × B ÷ C (quando uma cresce, a outra diminui, como velocidade e tempo).",
  aff=None),
 dict(slug="calculadora-de-consumo-de-energia", title="Calculadora de Consumo de Energia", short="Consumo de energia",
  desc="Calcule quantos kWh um aparelho consome por mês e quanto ele custa na conta de luz.",
  fields=[("pw","Potência do aparelho (W)",1500),("hd","Horas de uso por dia",1),("d","Dias de uso no mês",30),("t","Tarifa (R$/kWh, veja sua conta)",0.9)],
  js="var k=pw*hd*d/1000;return 'Consumo: <b>'+f(k)+' kWh/mês</b><br>Custo estimado: <b>R$ '+f(k*t)+'</b> por mês';",
  text="Consumo (kWh) = potência (W) × horas de uso × dias ÷ 1000. Use a tarifa com impostos que aparece na sua conta de luz; bandeiras tarifárias podem mudar o valor no mês.",
  aff=("Medidores de consumo de energia (tomada)","medidor-consumo-energia-tomada")),
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
w("index.html", page(SITE + " — ferramentas gratuitas", f'<h1>{SITE}</h1><p>Ferramentas gratuitas em português para obra, finanças e dia a dia.</p><ul>{lst}</ul>', "Calculadoras gratuitas em português: " + ", ".join(t["short"].lower() for t in tools) + ".", SITEURL + "/"))
w("sobre.html", page("Sobre | " + SITE, "<h1>Sobre</h1><p>Site de calculadoras gratuitas. Os textos e ferramentas são criados com auxílio de inteligência artificial. Os resultados são estimativas e não substituem orientação profissional.</p>", "Sobre o site", SITEURL + "/sobre.html"))
w("privacidade.html", page("Privacidade | " + SITE, "<h1>Política de privacidade</h1><p>Os cálculos são feitos no seu navegador; os valores digitados não são enviados a nenhum servidor. Futuramente o site poderá exibir anúncios (Google AdSense) e links de afiliados, que podem usar cookies de terceiros conforme as políticas desses serviços.</p>", "Política de privacidade", SITEURL + "/privacidade.html"))
urls += ["sobre.html", "privacidade.html"]
w("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + "".join(f"<url><loc>{SITEURL}/{u}</loc></url>" for u in urls) + "</urlset>")
w("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {SITEURL}/sitemap.xml\n")
