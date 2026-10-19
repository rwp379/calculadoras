"""Gera o site estatico em docs/. Uso: python build.py"""
import os, html, json, shutil, datetime

BASE = os.environ.get("BASE", "/calculadoras")
SITEURL = os.environ.get("SITEURL", "https://rwp379.github.io/calculadoras")
SITE = "Calculadoras de Obra"
TAGLINE = "Calcule material de reforma e construção com memória de cálculo, lista de compras e fórmulas explicadas."
UPDATED = datetime.date.today().strftime("%d/%m/%Y")
OUT = "docs"
GSC = "lVqNX4_clxrA_3hEmZyA5nvMgk2JrCB1xlJymBVtD5Y"  # Google Search Console

# Cada ferramenta: campos (id, rotulo, padrao, passo, unidade) ou (id, rotulo, [opcoes], None, None);
# js recebe as variaveis dos campos e devolve {rows:[[rotulo, valor]], buy:[texto], warn:texto}.
TOOLS = [
dict(
 slug="calculadora-de-tinta",
 short="Tinta",
 title="Calculadora de Tinta: quantos litros e latas comprar",
 h1="Calculadora de tinta para paredes e tetos",
 desc="Calcule a área a pintar descontando portas e janelas, os litros de tinta por demão e a combinação mais econômica de latas de 18 L, 3,6 L e 900 ml.",
 fields=[
  ("perim", "Perímetro do cômodo (soma das paredes)", 14, 0.1, "m"),
  ("alt", "Pé-direito", 2.7, 0.05, "m"),
  ("teto", "Pintar o teto também?", [("0", "Não"), ("1", "Sim")], None, None),
  ("area_teto", "Área do teto (se for pintar)", 12, 0.1, "m²"),
  ("portas", "Portas (0,80 × 2,10 m)", 1, 1, "un"),
  ("janelas", "Janelas (1,20 × 1,00 m)", 1, 1, "un"),
  ("demaos", "Demãos", 2, 1, "un"),
  ("rend", "Rendimento por demão (confira a embalagem)", [("10", "Standard (≈ 10 m²/L)"), ("8", "Econômica (≈ 8 m²/L)"), ("13", "Premium (≈ 13 m²/L)")], None, None),
 ],
 js="""
var paredes = perim*alt;
var vaos = portas*0.8*2.1 + janelas*1.2*1.0;
var liq = Math.max(paredes - vaos, 0) + (teto==1 ? area_teto : 0);
var litros = liq*demaos/rend*1.10;
var combo = latas(litros);
return {rows:[
 ['Área bruta das paredes', f(paredes)+' m²'],
 ['Desconto de portas e janelas', '− '+f(vaos)+' m²'],
 ['Teto', teto==1 ? '+ '+f(area_teto)+' m²' : 'não incluído'],
 ['Área líquida a pintar', f(liq)+' m²'],
 ['Tinta necessária (com 10% de perda)', '<b>'+f(litros)+' L</b>']],
 buy:[combo, 'Selador ou fundo preparador se a parede for nova ou tiver reboco aparente', 'Rolo de lã, pincel, bandeja e fita crepe'],
 warn: liq<=0 ? 'Confira as medidas: a área líquida ficou zerada.' : ''};
""",
 extra_js="""
function latas(L){
 if(L<=0) return 'Nenhuma lata necessária';
 var best=null;
 for(var a=0;a<=Math.ceil(L/18)+1;a++){for(var b=0;b<=5;b++){for(var c=0;c<=4;c++){
  var v=a*18+b*3.6+c*0.9; if(v+1e-9<L) continue;
  var s=v*100+(a+b+c); if(!best||s<best.s) best={s:s,a:a,b:b,c:c,v:v};}}}
 var out=[];
 if(best.a) out.push(best.a+' × lata de 18 L');
 if(best.b) out.push(best.b+' × galão de 3,6 L');
 if(best.c) out.push(best.c+' × quarto de 900 ml');
 return out.join(' + ')+' (total de '+f(best.v)+' L)';
}
""",
 how=[
  "Some o comprimento de todas as paredes do cômodo (perímetro) e multiplique pelo pé-direito.",
  "Desconte os vãos: uma porta padrão tem cerca de 1,68 m² e uma janela de 1,20 × 1,00 m tem 1,2 m².",
  "Multiplique a área líquida pelo número de demãos e divida pelo rendimento da tinta.",
  "Acrescente 10% para perdas no rolo, na bandeja e em retoques.",
 ],
 example="Quarto de 3 × 4 m com pé-direito de 2,70 m: perímetro de 14 m e 37,8 m² de parede. Descontando uma porta (1,68 m²) e uma janela (1,2 m²), sobram 34,9 m². Com 2 demãos de tinta standard (10 m²/L): 34,9 × 2 ÷ 10 = 7,0 L, ou 7,7 L com a perda. A compra mais econômica é 2 galões de 3,6 L + 1 quarto de 900 ml.",
 formula="Litros = (perímetro × pé-direito − vãos + teto) × demãos ÷ rendimento × 1,10",
 faq=[
  ("Quantas demãos de tinta preciso?", "Em geral duas. Uma terceira costuma ser necessária ao trocar de uma cor escura para uma clara ou com tintas econômicas de baixa cobertura."),
  ("Qual o rendimento de uma lata de 18 litros?", "Depende da linha. Tintas econômicas rendem perto de 8 m² por litro por demão, e linhas premium podem passar de 12. O número exato está na embalagem; escolha a opção mais próxima no campo de rendimento."),
  ("Preciso de selador antes da tinta?", "Em reboco novo ou massa corrida, sim: o selador uniformiza a absorção e evita gastar tinta à toa. Em parede já pintada e em bom estado, normalmente não."),
  ("A calculadora considera a diluição?", "Não. A diluição recomendada pelo fabricante já está embutida no rendimento informado na embalagem."),
 ],
 related=["calculadora-de-reboco", "calculadora-de-alvenaria", "calculadora-de-piso"],
 aff=("Rolos e pincéis para pintura", "rolo-de-pintura-kit"),
),
dict(
 slug="calculadora-de-piso",
 short="Piso e rejunte",
 title="Calculadora de Piso: caixas, argamassa colante e rejunte",
 h1="Calculadora de piso e revestimento",
 desc="Calcule quantas caixas de piso comprar com a perda certa para o tipo de assentamento, além dos sacos de argamassa colante e quilos de rejunte.",
 fields=[
  ("comp", "Comprimento do ambiente", 4, 0.01, "m"),
  ("larg", "Largura do ambiente", 3, 0.01, "m"),
  ("pc", "Comprimento da peça", 60, 0.5, "cm"),
  ("pl", "Largura da peça", 60, 0.5, "cm"),
  ("esp", "Espessura da peça", 8, 0.5, "mm"),
  ("junta", "Largura da junta", 2, 0.5, "mm"),
  ("m2cx", "Metragem por caixa (veja a embalagem)", 2.16, 0.01, "m²"),
  ("tipo", "Tipo de assentamento", [("10", "Reto (≈ 10% de perda)"), ("15", "Diagonal ou muitos recortes (≈ 15%)")], None, None),
 ],
 js="""
var area = comp*larg;
var compra = area*(1+tipo/100);
var caixas = m2cx>0 ? Math.ceil(compra/m2cx) : 0;
var C=pc*10, L=pl*10;
var rej = (C>0&&L>0) ? (C+L)*esp*junta/(C*L)*1.58*area : 0;
var dupla = (pc*pl >= 900);
var arg = area*(dupla ? 8 : 5);
var sacos = Math.ceil(arg/20);
return {rows:[
 ['Área do ambiente', f(area)+' m²'],
 ['Área com perda ('+tipo+'%)', f(compra)+' m²'],
 ['Caixas de piso', '<b>'+caixas+' caixas</b> ('+f(caixas*m2cx)+' m²)'],
 ['Argamassa colante', f(arg)+' kg ('+(dupla?'colagem dupla, peça a partir de 30 × 30 cm':'colagem simples')+')'],
 ['Rejunte', '<b>'+f(rej)+' kg</b>']],
 buy:[caixas+' caixas de piso, todas do mesmo lote e tonalidade', sacos+' saco(s) de argamassa colante de 20 kg (tipo indicado pelo fabricante do piso)', Math.max(Math.ceil(rej),1)+' kg de rejunte', 'Espaçadores de '+f(junta)+' mm e niveladores se a peça for grande'],
 warn: m2cx<=0 ? 'Informe a metragem por caixa.' : ''};
""",
 how=[
  "Multiplique comprimento por largura para obter a área do ambiente.",
  "Acrescente a perda: cerca de 10% para assentamento reto e 15% para diagonal ou ambientes com muitos recortes.",
  "Divida pela metragem de cada caixa e arredonde para cima.",
  "Argamassa colante: cerca de 5 kg/m² em colagem simples e 8 kg/m² em colagem dupla, recomendada para peças a partir de 30 × 30 cm. Confira o consumo na embalagem.",
  "Rejunte: use a fórmula de consumo dos fabricantes, que depende do tamanho da peça, da espessura e da junta.",
 ],
 example="Sala de 4 × 3 m (12 m²) com porcelanato 60 × 60 cm, 8 mm de espessura e junta de 2 mm, em caixas de 2,16 m². Com 10% de perda são 13,2 m², ou 7 caixas. Argamassa em colagem dupla: 96 kg (5 sacos de 20 kg). Rejunte: (600 + 600) × 8 × 2 ÷ (600 × 600) × 1,58 × 12 ≈ 1,0 kg.",
 formula="Rejunte (kg) = (C + L) × E × J ÷ (C × L) × 1,58 × área   [C, L, E e J em mm; área em m²]",
 faq=[
  ("Quanto de piso a mais devo comprar?", "Entre 10% e 15% sobre a área. Guarde as peças que sobrarem: o mesmo lote raramente é encontrado depois para reparos."),
  ("O que é colagem dupla?", "É passar argamassa no contrapiso e também no verso da peça. Ela evita peças ocas e é recomendada para formatos grandes; siga a orientação do fabricante."),
  ("Qual argamassa usar: AC-I, AC-II ou AC-III?", "AC-I para áreas internas, AC-II para áreas externas e AC-III para porcelanatos grandes, piscinas e fachadas. A embalagem do piso costuma indicar o tipo."),
  ("Por que a junta influencia tanto o rejunte?", "O consumo é proporcional à largura e à profundidade da junta. Dobrar a junta dobra o rejunte."),
 ],
 related=["calculadora-de-contrapiso", "calculadora-de-tinta"],
 aff=("Niveladores e espaçadores para piso", "nivelador-de-piso-espacador"),
),
dict(
 slug="calculadora-de-concreto",
 short="Concreto",
 title="Calculadora de Concreto: volume, cimento, areia, brita e água",
 h1="Calculadora de concreto por traço",
 desc="Calcule o volume de concreto de pisos, calçadas, lajes e sapatas e a quantidade de sacos de cimento, areia, brita e água para o traço escolhido.",
 fields=[
  ("comp", "Comprimento", 4, 0.01, "m"),
  ("larg", "Largura", 3, 0.01, "m"),
  ("alt", "Espessura ou altura", 8, 0.5, "cm"),
  ("qtd", "Quantidade de peças iguais", 1, 1, "un"),
  ("traco", "Traço em volume (cimento : areia : brita)", [("1,2,3", "1 : 2 : 3 — uso geral (pisos, calçadas, pequenas peças)"), ("1,2.5,3.5", "1 : 2,5 : 3,5 — pisos e bases"), ("1,3,5", "1 : 3 : 5 — concreto magro, sem função estrutural")], None, None),
 ],
 js="""
var t = String(traco).split(',').map(Number);
var vol = comp*larg*alt/100*qtd;
var volP = vol*1.05;
var seco = volP*1.52;
var soma = t[0]+t[1]+t[2];
var vc = seco*t[0]/soma, va = seco*t[1]/soma, vb = seco*t[2]/soma;
var kg = vc*1400, sacos = Math.ceil(kg/50);
var agua = kg*0.55;
return {rows:[
 ['Volume geométrico', f(vol)+' m³'],
 ['Volume com 5% de perda', '<b>'+f(volP)+' m³</b>'],
 ['Cimento', '<b>'+sacos+' sacos de 50 kg</b> ('+f(kg)+' kg)'],
 ['Areia média', f(va)+' m³'],
 ['Brita 1', f(vb)+' m³'],
 ['Água (fator água/cimento ≈ 0,55)', f(agua)+' litros']],
 buy:[sacos+' sacos de cimento de 50 kg', f(va*1.1)+' m³ de areia média lavada (inclui 10% de inchamento)', f(vb)+' m³ de brita 1'],
 warn: volP>3 ? 'Acima de 3 m³ costuma compensar concreto usinado. Peça orçamento a uma concreteira.' : ''};
""",
 how=[
  "Calcule o volume: comprimento × largura × espessura (em metros) × número de peças.",
  "Acrescente 5% para perdas no transporte e no lançamento.",
  "Multiplique por 1,52, o fator usual que converte o volume de concreto pronto em volume de materiais secos (os grãos de areia e o cimento preenchem os vazios da brita).",
  "Divida esse volume seco na proporção do traço. O cimento é convertido em quilos pela massa unitária de cerca de 1.400 kg/m³.",
 ],
 example="Calçada de 4 × 3 m com 8 cm: 0,96 m³, ou 1,01 m³ com perda. Volume seco: 1,53 m³. No traço 1 : 2 : 3, o cimento é 1,53 ÷ 6 = 0,26 m³ ≈ 358 kg, ou 8 sacos de 50 kg; areia 0,51 m³; brita 0,77 m³; água por volta de 197 litros.",
 formula="Material = volume × 1,05 × 1,52 × (parte do material ÷ soma do traço);  cimento (kg) = volume de cimento × 1.400",
 faq=[
  ("Esta calculadora serve para dimensionar estrutura?", "Não. Ela estima material para compra. Lajes, vigas, pilares e fundações precisam de projeto e responsável técnico, que definem a resistência (fck), a armadura e o cobrimento."),
  ("Por que multiplicar por 1,52?", "Porque misturar areia, brita e cimento reduz o volume: parte do material preenche os vazios entre os grãos. O fator 1,52 é uma aproximação usual para concreto feito em obra."),
  ("Quanto concreto rende um saco de cimento?", "No traço 1 : 2 : 3, cerca de 0,14 m³ por saco de 50 kg, ou seja, perto de 7 sacos por metro cúbico."),
  ("Concreto feito em obra ou usinado?", "Para volumes pequenos, em obra. A partir de cerca de 3 m³, o usinado tende a sair mais barato e com resistência garantida."),
 ],
 related=["calculadora-de-contrapiso", "calculadora-de-alvenaria"],
 aff=("Betoneiras e carrinhos de mão", "betoneira-400-litros"),
),
dict(
 slug="calculadora-de-alvenaria",
 short="Tijolos e blocos",
 title="Calculadora de Tijolos e Blocos: quantidade por m² e argamassa",
 h1="Calculadora de tijolos e blocos para parede",
 desc="Calcule quantos blocos cerâmicos ou de concreto você precisa para levantar uma parede e o volume de argamassa de assentamento, descontando portas e janelas.",
 fields=[
  ("comp", "Comprimento total das paredes", 10, 0.01, "m"),
  ("alt", "Altura", 2.8, 0.01, "m"),
  ("vaos", "Área de portas e janelas a descontar", 3, 0.1, "m²"),
  ("bloco", "Tipo de bloco (largura × altura × comprimento)", [("14,19,29", "Cerâmico 14 × 19 × 29 cm"), ("9,19,19", "Cerâmico 9 × 19 × 19 cm"), ("14,19,39", "Concreto 14 × 19 × 39 cm"), ("19,19,39", "Concreto 19 × 19 × 39 cm")], None, None),
  ("junta", "Espessura da junta", 1, 0.1, "cm"),
 ],
 js="""
var b = String(bloco).split(',').map(Number);
var e=b[0]/100, h=b[1]/100, c=b[2]/100, j=junta/100;
var area = Math.max(comp*alt - vaos, 0);
var porM2 = 1/((c+j)*(h+j));
var blocos = Math.ceil(area*porM2*1.05);
var argM3 = area*(1 - porM2*c*h)*e*1.10;
return {rows:[
 ['Área líquida de parede', f(area)+' m²'],
 ['Blocos por m²', f(porM2)],
 ['Blocos (com 5% de quebra)', '<b>'+blocos+' unidades</b>'],
 ['Argamassa de assentamento', '<b>'+f(argM3)+' m³</b> (com 10% de perda)']],
 buy:[blocos+' blocos '+b[0]+' × '+b[1]+' × '+b[2]+' cm', f(argM3)+' m³ de argamassa de assentamento (pronta ou feita em obra)', 'Tela ou ferro-cabelo para amarração nos pilares, se houver estrutura de concreto'],
 warn: area<=0 ? 'A área líquida ficou zerada: confira os vãos.' : ''};
""",
 how=[
  "Calcule a área da parede (comprimento × altura) e desconte portas e janelas.",
  "Blocos por m² = 1 ÷ [(comprimento do bloco + junta) × (altura do bloco + junta)].",
  "Acrescente 5% para quebras e cortes.",
  "Argamassa: a parte da parede que não é ocupada pelas faces dos blocos, multiplicada pela largura do bloco, mais 10% de perda.",
 ],
 example="Paredes somando 10 m de comprimento e 2,80 m de altura, descontando 3 m² de vãos: 25 m². Com bloco cerâmico 14 × 19 × 29 cm e junta de 1 cm, são 1 ÷ (0,30 × 0,20) = 16,7 blocos/m², ou 438 blocos com a quebra. A argamassa fica em torno de 0,31 m³.",
 formula="Blocos/m² = 1 ÷ [(C + j) × (H + j)];  argamassa = área × (1 − blocos/m² × C × H) × largura do bloco × 1,10",
 faq=[
  ("Quantos tijolos de 9 furos vão em 1 m²?", "Com bloco 9 × 19 × 19 cm e junta de 1 cm, cerca de 25 unidades por m², sem contar a quebra."),
  ("Bloco cerâmico ou de concreto?", "O cerâmico é mais leve e costuma ser mais barato para vedação. O de concreto tem dimensões mais regulares e é usado também em alvenaria estrutural, que exige projeto específico."),
  ("Posso usar esta conta para alvenaria estrutural?", "Para estimar compra, sim. A definição de blocos, grauteamento e armaduras da alvenaria estrutural é do projeto."),
  ("Quanto de perda considerar?", "Entre 3% e 5% para blocos de boa qualidade e transporte cuidadoso; até 10% se houver muitos cortes."),
 ],
 related=["calculadora-de-reboco", "calculadora-de-concreto", "calculadora-de-tinta"],
 aff=("Colher de pedreiro e prumo", "colher-de-pedreiro-prumo"),
),
dict(
 slug="calculadora-de-reboco",
 short="Reboco",
 title="Calculadora de Reboco: cimento, cal, areia e chapisco por m²",
 h1="Calculadora de reboco (emboço e chapisco)",
 desc="Calcule a argamassa para rebocar paredes descontando portas e janelas, em uma ou nas duas faces: sacos de cimento, de cal e metros de areia do traço 1 : 2 : 8, ou sacos de argamassa pronta, com o chapisco incluído.",
 fields=[
  ("comp", "Comprimento total das paredes", 10, 0.01, "m"),
  ("alt", "Altura", 2.8, 0.01, "m"),
  ("vaos", "Área de portas e janelas a descontar", 3, 0.1, "m²"),
  ("faces", "Faces a revestir", [("1", "Uma face"), ("2", "As duas faces")], None, None),
  ("esp", "Espessura do emboço (massa única)", 2, 0.5, "cm"),
  ("tipo", "Argamassa", [("mista", "Feita em obra, traço 1 : 2 : 8 (cimento, cal e areia)"), ("pronta", "Industrializada, em sacos de 20 kg")], None, None),
  ("cons", "Consumo da argamassa industrializada (veja a embalagem)", 17, 0.5, "kg/m² por cm"),
  ("chap", "Incluir chapisco 1 : 3 (5 mm)?", [("1", "Sim"), ("0", "Não")], None, None),
  ("perda", "Perda de argamassa", 20, 1, "%"),
 ],
 js="""
var area = Math.max(comp*alt - vaos, 0)*faces;
var k = 1 + perda/100;
var vol = area*esp/100*k;
var rows = [['Área a revestir', f(area)+' m²'+(faces==2 ? ' (duas faces)' : '')]];
var buy = [], cim = 0;
if(tipo=='mista'){
 var c = vol*192.5, cal = vol*171.1, a = vol*1.14; cim += c;
 rows.push(['Argamassa 1 : 2 : 8 (com '+f(perda)+'% de perda)', '<b>'+f(vol)+' m³</b>']);
 rows.push(['Cimento do emboço', f(c)+' kg']);
 rows.push(['Cal hidratada', '<b>'+Math.ceil(cal/20)+' sacos de 20 kg</b> ('+f(cal)+' kg)']);
 rows.push(['Areia média', f(a)+' m³']);
 buy.push(Math.ceil(cal/20)+' sacos de cal hidratada CH-I de 20 kg', f(a)+' m³ de areia média');
} else {
 var kg = area*esp*cons*k;
 rows.push(['Argamassa industrializada (com '+f(perda)+'% de perda)', '<b>'+Math.ceil(kg/20)+' sacos de 20 kg</b> ('+f(kg)+' kg)']);
 buy.push(Math.ceil(kg/20)+' sacos de 20 kg de argamassa para reboco (mesma marca e lote)');
}
if(chap==1){
 var vc = area*0.005*k, cc = vc*478, ac = vc*1.06; cim += cc;
 rows.push(['Chapisco 1 : 3 (5 mm)', f(vc)+' m³: '+f(cc)+' kg de cimento e '+f(ac)+' m³ de areia']);
 buy.push(f(ac)+' m³ de areia grossa para o chapisco');
}
if(cim>0){
 rows.push(['Cimento total', '<b>'+Math.ceil(cim/50)+' sacos de 50 kg</b> ('+f(cim)+' kg)']);
 buy.unshift(Math.ceil(cim/50)+' sacos de cimento CP II de 50 kg');
}
buy.push('Régua de alumínio, desempenadeira e taliscas para manter o prumo');
return {rows:rows, buy:buy,
 warn: area<=0 ? 'A área ficou zerada: confira as medidas e os vãos.' : (esp<1 ? 'Emboço com menos de 1 cm raramente corrige o prumo da parede. Para apenas regularizar, avalie massa fina ou massa corrida.' : (esp>3 ? 'Acima de 3 cm, aplique em duas camadas, respeitando a cura entre elas, e avalie tela na argamassa. Espessura tão grande indica parede fora de prumo.' : ''))};
""",
 how=[
  "Calcule a área: comprimento total das paredes × altura, menos portas e janelas. Se for revestir os dois lados, multiplique por 2.",
  "Volume de argamassa = área × espessura (em metros) × (1 + perda). A perda em reboco é alta (material que cai e sobra na masseira); 20% é um valor prudente.",
  "Traço 1 : 2 : 8 feito em obra: cada m³ de argamassa consome cerca de 192,5 kg de cimento, 171,1 kg de cal hidratada e 1,14 m³ de areia média (coeficientes da composição SINAPI 87369).",
  "Argamassa industrializada: multiplique a área pela espessura em cm e pelo consumo da embalagem (em geral entre 16 e 20 kg/m² por cm).",
  "Chapisco 1 : 3 com 5 mm: cada m³ consome cerca de 478 kg de cimento e 1,06 m³ de areia (SINAPI 100467). Some esse cimento ao do emboço.",
 ],
 example="Paredes somando 10 m de comprimento e 2,80 m de altura, descontando 3 m² de portas e janelas: 25 m² em uma face. Emboço de 2 cm com 20% de perda: 25 × 0,02 × 1,20 = 0,60 m³ de argamassa 1 : 2 : 8, que pede 115,5 kg de cimento, 102,7 kg de cal (6 sacos de 20 kg) e 0,68 m³ de areia média. O chapisco de 5 mm soma 0,15 m³: 71,7 kg de cimento e 0,16 m³ de areia grossa. Cimento total: 187,2 kg, ou 4 sacos de 50 kg.",
 formula="Argamassa (m³) = (comprimento × altura − vãos) × faces × espessura × (1 + perda);  por m³ de 1 : 2 : 8: 192,5 kg de cimento, 171,1 kg de cal e 1,14 m³ de areia;  por m³ de chapisco 1 : 3: 478 kg de cimento e 1,06 m³ de areia",
 faq=[
  ("Qual a diferença entre chapisco, emboço e reboco?", "O chapisco é uma camada fina e áspera de cimento e areia que dá aderência. O emboço regulariza a parede e corrige o prumo. O reboco é o acabamento fino por cima. Hoje é comum fazer emboço e reboco numa camada só, a massa única, que é o que esta calculadora considera."),
  ("Qual a espessura certa do reboco?", "Em paredes internas, em geral entre 0,5 e 2 cm; em paredes externas, entre 2 e 3 cm. Espessuras maiores costumam indicar parede fora de prumo e devem ser aplicadas em camadas."),
  ("Quantos metros quadrados rende um saco de cimento no reboco?", "No traço 1 : 2 : 8 com 20% de perda, cerca de 11 m² com 2 cm de espessura e 14 m² com 1,5 cm. Rendimentos de 20 m² por saco só aparecem quando se ignora a perda ou se usa um traço mais fraco."),
  ("Para que serve a cal na argamassa?", "A cal deixa a massa mais plástica e fácil de aplicar, retém água durante a cura e reduz fissuras. Por isso o traço misto 1 : 2 : 8 é o mais usado em emboço de paredes."),
  ("Argamassa pronta ou feita em obra?", "A industrializada tem traço constante e dispensa o preparo, mas costuma custar mais por m². A feita em obra é mais barata em volumes grandes e exige dosagem cuidadosa. Use a opção do campo Argamassa para comparar as duas."),
 ],
 related=["calculadora-de-alvenaria", "calculadora-de-tinta"],
 aff=("Desempenadeiras e réguas de pedreiro", "desempenadeira-de-aco"),
),
dict(
 slug="calculadora-de-contrapiso",
 short="Contrapiso",
 title="Calculadora de Contrapiso: cimento e areia por m²",
 h1="Calculadora de contrapiso",
 desc="Calcule o volume de argamassa de contrapiso e quantos sacos de cimento e metros cúbicos de areia comprar, conforme a espessura e o traço.",
 fields=[
  ("area", "Área do piso", 20, 0.1, "m²"),
  ("esp", "Espessura média", 4, 0.5, "cm"),
  ("traco", "Traço em volume (cimento : areia)", [("1,4", "1 : 4 — uso residencial comum"), ("1,3", "1 : 3 — mais resistente"), ("1,5", "1 : 5 — áreas de pouco tráfego")], None, None),
 ],
 js="""
var t = String(traco).split(',').map(Number);
var vol = area*esp/100*1.05;
var seco = vol*1.30;
var vc = seco*t[0]/(t[0]+t[1]), va = seco*t[1]/(t[0]+t[1]);
var kg = vc*1400, sacos = Math.ceil(kg/50);
return {rows:[
 ['Volume de contrapiso (com 5% de perda)', '<b>'+f(vol)+' m³</b>'],
 ['Cimento', '<b>'+sacos+' sacos de 50 kg</b> ('+f(kg)+' kg)'],
 ['Areia média', f(va)+' m³'],
 ['Consumo de cimento por m²', area>0 ? f(kg/area)+' kg' : '—']],
 buy:[sacos+' sacos de cimento de 50 kg', f(va*1.1)+' m³ de areia média lavada (inclui inchamento)', 'Adesivo para chapisco ou ponte de aderência, se indicado pelo fabricante do piso'],
 warn: esp<3 ? 'Contrapisos com menos de 3 cm tendem a trincar e descolar; para espessuras tão pequenas, avalie argamassa autonivelante.' : (esp>6 ? 'Acima de 6 cm, avalie preencher parte da altura com concreto magro para economizar cimento.' : '')};
""",
 how=[
  "Multiplique a área pela espessura média em metros e acrescente 5% de perda.",
  "Multiplique por 1,30, fator usual para argamassa semisseca (o volume de materiais secos é maior que o volume final).",
  "Divida na proporção do traço; o cimento vira quilos pela massa unitária de cerca de 1.400 kg/m³.",
 ],
 example="Piso de 20 m² com 4 cm de contrapiso: 0,84 m³ com perda. Volume seco: 1,09 m³. No traço 1 : 4, cimento = 1,09 ÷ 5 = 0,22 m³ ≈ 306 kg, ou 7 sacos de 50 kg; areia 0,87 m³.",
 formula="Material = área × espessura × 1,05 × 1,30 × (parte do material ÷ soma do traço)",
 faq=[
  ("Qual a espessura ideal de contrapiso?", "Entre 3 e 5 cm é o mais comum em residências. Menos que isso trinca com facilidade; muito mais encarece e pesa sobre a laje."),
  ("Quanto tempo esperar para assentar o piso?", "Em geral de 7 a 14 dias de cura para argamassa convencional. Siga a orientação do fabricante da argamassa colante e do piso."),
  ("Contrapiso precisa de cal?", "Não é obrigatório. O contrapiso comum usa cimento e areia em consistência semisseca, conhecida como farofa."),
 ],
 related=["calculadora-de-piso", "calculadora-de-concreto"],
 aff=("Régua de alumínio e desempenadeira", "regua-de-aluminio-pedreiro"),
),
]

CSS = """
:root{--bg:#f7f6f2;--card:#fff;--ink:#1d2321;--muted:#5b6461;--line:#e3e1da;--accent:#b4501a;--accent-ink:#fff;--soft:#fbeee5;--warn:#7a4f00;--warn-bg:#fff4d6}
@media (prefers-color-scheme:dark){:root{--bg:#141716;--card:#1d2120;--ink:#e9ece9;--muted:#a3aba7;--line:#2e3432;--accent:#f08a4b;--accent-ink:#1b0f07;--soft:#2a211b;--warn:#f1c76b;--warn-bg:#2b2412}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
a{color:var(--accent)}
.wrap{max-width:880px;margin:0 auto;padding:0 16px}
header.top{border-bottom:1px solid var(--line);background:var(--card)}
header.top .wrap{display:flex;align-items:center;gap:8px 20px;min-height:56px;flex-wrap:wrap;padding-top:8px;padding-bottom:8px}
.brand{font-weight:800;text-decoration:none;color:var(--ink);letter-spacing:-.01em}
.brand span{color:var(--accent)}
nav.tools{display:flex;gap:4px 14px;flex-wrap:wrap;font-size:14px}
nav.tools a{color:var(--muted);text-decoration:none}nav.tools a:hover{color:var(--accent)}
h1{font-size:clamp(26px,4.5vw,36px);line-height:1.15;margin:28px 0 8px;letter-spacing:-.02em}
h2{font-size:21px;margin:36px 0 10px}
.lead{color:var(--muted);margin:0 0 20px;max-width:65ch}
.calc{display:grid;grid-template-columns:1fr 1fr;gap:20px;align-items:start}
@media (max-width:720px){.calc{grid-template-columns:1fr}}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:18px}
label{display:block;font-size:14px;color:var(--muted);margin:12px 0 4px}
form label:first-child{margin-top:0}
.inp{display:flex;align-items:center;border:1px solid var(--line);border-radius:8px;background:var(--bg)}
.inp input,select{width:100%;border:0;background:transparent;color:var(--ink);font:inherit;padding:9px 10px;outline:none;min-width:0}
select{border:1px solid var(--line);border-radius:8px;background:var(--bg)}
.inp:focus-within,select:focus{outline:2px solid var(--accent);outline-offset:1px}
.inp em{font-style:normal;color:var(--muted);padding:0 10px;font-size:14px;white-space:nowrap}
.res h3{margin:0 0 8px;font-size:13px;color:var(--muted);font-weight:700;text-transform:uppercase;letter-spacing:.06em}
table{width:100%;border-collapse:collapse;font-size:15px}
td{padding:7px 0;border-bottom:1px solid var(--line);vertical-align:top}td:last-child{text-align:right;padding-left:12px}
.buy{background:var(--soft);border-radius:10px;padding:12px 14px;margin-top:14px}
.buy ul{margin:6px 0 0;padding-left:20px}
.warn{background:var(--warn-bg);color:var(--warn);border-radius:8px;padding:10px 12px;margin-top:12px;font-size:14px}
.warn:empty{display:none}
button.copy{margin-top:10px;background:var(--accent);color:var(--accent-ink);border:0;border-radius:8px;padding:8px 14px;font:inherit;font-weight:600;cursor:pointer}
ol.steps li{margin:6px 0}
.formula{font-family:ui-monospace,Consolas,monospace;background:var(--card);border:1px solid var(--line);border-radius:8px;padding:10px 12px;font-size:14px;overflow-x:auto}
details{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:10px 14px;margin:8px 0}
summary{cursor:pointer;font-weight:600}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:14px;margin-top:16px}
a.card{display:block;text-decoration:none;color:var(--ink)}
a.card:hover{border-color:var(--accent)}
a.card b{display:block;margin-bottom:4px}a.card small{color:var(--muted)}
.note{font-size:14px;color:var(--muted)}
footer{margin-top:48px;padding-top:16px;padding-bottom:24px;border-top:1px solid var(--line);font-size:14px;color:var(--muted)}
"""

COMMON_JS = """
function f(x){return Number(x).toLocaleString('pt-BR',{maximumFractionDigits:2})}
function run(){
 var v={};document.querySelectorAll('[data-k]').forEach(function(el){v[el.dataset.k]=el.tagName==='SELECT'?el.value:(parseFloat(el.value)||0);});
 var r=calc(v);
 document.getElementById('rows').innerHTML=r.rows.map(function(x){return '<tr><td>'+x[0]+'</td><td>'+x[1]+'</td></tr>'}).join('');
 document.getElementById('buy').innerHTML=r.buy.map(function(x){return '<li>'+x+'</li>'}).join('');
 document.getElementById('warn').textContent=r.warn||'';
}
function copyList(){var t=Array.from(document.querySelectorAll('#buy li')).map(function(li){return '- '+li.textContent}).join('\\n');
 if(navigator.clipboard){navigator.clipboard.writeText(t).then(function(){var b=document.getElementById('cp');b.textContent='Copiado!';setTimeout(function(){b.textContent='Copiar lista de compras'},1500)})}}
document.addEventListener('input',run);document.addEventListener('change',run);
"""


def esc(s):
    return html.escape(str(s))


def nav():
    return "".join(f'<a href="{BASE}/{t["slug"]}.html">{esc(t["short"])}</a>' for t in TOOLS)


def page(title, desc, canon, body, jsonld=None):
    ld = f'<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>' if jsonld else ""
    return (f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<meta name="google-site-verification" content="{GSC}">'
            f'<title>{esc(title)}</title><meta name="description" content="{esc(desc)}">'
            f'<link rel="canonical" href="{canon}"><meta property="og:title" content="{esc(title)}">'
            f'<meta property="og:description" content="{esc(desc)}"><meta property="og:type" content="website">'
            f'<style>{CSS}</style>{ld}</head><body>'
            f'<header class="top"><div class="wrap"><a class="brand" href="{BASE}/">Calculadoras <span>de Obra</span></a>'
            f'<nav class="tools" aria-label="Calculadoras">{nav()}</nav></div></header>'
            f'<main class="wrap">{body}</main>'
            f'<footer class="wrap">Os resultados são estimativas para compra de material e não substituem projeto nem orientação de profissional habilitado. '
            f'Atualizado em {UPDATED}. <a href="{BASE}/sobre.html">Sobre</a> · <a href="{BASE}/privacidade.html">Privacidade</a></footer>'
            f'</body></html>')


def field_html(k, label, default, step, unit):
    if isinstance(default, list):
        opts = "".join(f'<option value="{esc(v)}">{esc(t)}</option>' for v, t in default)
        return f'<label for="{k}">{esc(label)}</label><select id="{k}" data-k="{k}">{opts}</select>'
    return (f'<label for="{k}">{esc(label)}</label><div class="inp"><input id="{k}" data-k="{k}" type="number" inputmode="decimal" '
            f'min="0" step="{step}" value="{default}"><em>{esc(unit)}</em></div>')


def tool_page(t):
    fields = "".join(field_html(*fl) for fl in t["fields"])
    unpack = "".join(f"var {fl[0]}=v.{fl[0]};" for fl in t["fields"])
    script = f"<script>{COMMON_JS}{t.get('extra_js', '')}function calc(v){{{unpack}{t['js']}}}run();</script>"
    steps = "".join(f"<li>{esc(s)}</li>" for s in t["how"])
    faq = "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in t["faq"])
    rel = "".join(
        f'<a class="card" href="{BASE}/{r["slug"]}.html"><b>{esc(r["short"])}</b><small>{esc(r["desc"])}</small></a>'
        for r in TOOLS if r["slug"] in t["related"])
    aff = ""
    if t.get("aff"):
        aff = (f'<p class="note">Ferramentas úteis: <a rel="sponsored nofollow noopener" target="_blank" '
               f'href="https://lista.mercadolivre.com.br/{t["aff"][1]}">{esc(t["aff"][0])} no Mercado Livre</a>.</p>')
    body = (f'<h1>{esc(t["h1"])}</h1><p class="lead">{esc(t["desc"])}</p>'
            f'<section class="calc"><form class="card" onsubmit="return false">{fields}</form>'
            f'<div class="card res" aria-live="polite"><h3>Resultado</h3><table><tbody id="rows"></tbody></table>'
            f'<div class="buy"><b>Lista de compras</b><ul id="buy"></ul></div>'
            f'<button class="copy" id="cp" type="button" onclick="copyList()">Copiar lista de compras</button>'
            f'<div class="warn" id="warn"></div></div></section>'
            f'<h2>Como calcular, passo a passo</h2><ol class="steps">{steps}</ol>'
            f'<h2>Exemplo resolvido</h2><p>{esc(t["example"])}</p>'
            f'<h2>Fórmula usada</h2><div class="formula">{esc(t["formula"])}</div>'
            f'<h2>Perguntas frequentes</h2>{faq}{aff}'
            f'<h2>Calculadoras relacionadas</h2><div class="grid">{rel}</div>{script}')
    ld = {"@context": "https://schema.org", "@type": "FAQPage",
          "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in t["faq"]]}
    return page(t["title"], t["desc"], f'{SITEURL}/{t["slug"]}.html', body, ld)


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)

    def w(name, s):
        with open(os.path.join(OUT, name), "w", encoding="utf-8") as fh:
            fh.write(s)

    for t in TOOLS:
        w(t["slug"] + ".html", tool_page(t))
    cards = "".join(f'<a class="card" href="{BASE}/{t["slug"]}.html"><b>{esc(t["short"])}</b><small>{esc(t["desc"])}</small></a>' for t in TOOLS)
    w("index.html", page(f"{SITE}: material de reforma e construção", TAGLINE, SITEURL + "/",
        f'<h1>{SITE}</h1><p class="lead">{esc(TAGLINE)} Gratuito, sem cadastro, e os cálculos ficam no seu navegador.</p><div class="grid">{cards}</div>'))
    w("sobre.html", page(f"Sobre | {SITE}", "Sobre o site Calculadoras de Obra", SITEURL + "/sobre.html",
        "<h1>Sobre</h1><p>Calculadoras de Obra reúne ferramentas gratuitas para estimar material de reforma e construção, sempre com a fórmula e um exemplo resolvido, para que você entenda e confira o resultado.</p>"
        "<p>Os textos e as ferramentas são produzidos com auxílio de inteligência artificial, a partir de regras de cálculo usuais na construção civil. Os resultados são estimativas para compra e não substituem projeto nem responsável técnico.</p>"))
    w("privacidade.html", page(f"Privacidade | {SITE}", "Política de privacidade", SITEURL + "/privacidade.html",
        "<h1>Política de privacidade</h1><p>Os cálculos são feitos no seu navegador: os valores digitados não são enviados a nenhum servidor e não coletamos dados pessoais.</p>"
        "<p>O site pode exibir anúncios do Google AdSense e links de afiliados (por exemplo, Mercado Livre e Amazon). Esses serviços podem usar cookies conforme as próprias políticas. Ao comprar por um link de afiliado, o site pode receber uma comissão, sem custo extra para você.</p>"))
    urls = [""] + [t["slug"] + ".html" for t in TOOLS] + ["sobre.html", "privacidade.html"]
    w("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
      + "".join(f"<url><loc>{SITEURL}/{u}</loc></url>" for u in urls) + "</urlset>")
    w("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {SITEURL}/sitemap.xml\n")
    w(".nojekyll", "")


if __name__ == "__main__":
    main()
