# -*- coding: utf-8 -*-
"""
Dialogapp - Ecoruta Conectada / AMAZONIA VIVA 360
Hackathon Colombia 5.0 (MinTIC) - Leticia, Amazonas
"""

import os
import urllib.parse
import unicodedata
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Dialogapp · Ecoruta", page_icon="🌿", layout="wide", initial_sidebar_state="expanded")

# MANIFIESTO PWA PARA INSTALACIÓN EN ANDROID E iOS
PWA_HEADER = """
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="Dialogapp">
<link rel="apple-touch-icon" href="https://img.icons8.com/emoji/192/leaf-fluttering-in-wind.png">
<link rel="manifest" href="data:application/manifest+json,{
  'name': 'Dialogapp — Ecoruta Conectada',
  'short_name': 'Dialogapp',
  'start_url': '/',
  'display': 'standalone',
  'background_color': '#f2f7f4',
  'theme_color': '#007f5f',
  'icons': [{
    'src': 'https://img.icons8.com/emoji/192/leaf-fluttering-in-wind.png',
    'sizes': '192x192',
    'type': 'image/png'
  }]
}">
"""
st.markdown(PWA_HEADER, unsafe_allow_html=True)

# Inicialización segura de variables
if 'paso_plan' not in st.session_state: st.session_state.paso_plan = 1
if 'reserva' not in st.session_state: st.session_state.reserva = {}
if 'ir_a_pago_directo' not in st.session_state: st.session_state.ir_a_pago_directo = False
if 'acts_elegidas' not in st.session_state: st.session_state.acts_elegidas = []
if 'comidas_elegidas' not in st.session_state: st.session_state.comidas_elegidas = []

def cop(v): return "$" + format(int(v), ",").replace(",", ".")
def norm(t):
    t = unicodedata.normalize("NFD", t.strip().lower())
    return "".join(c for c in t if unicodedata.category(c) != "Mn")

def qr_url(data, size=220):
    dato = urllib.parse.quote(data)
    return f"https://api.qrserver.com/v1/create-qr-code/?size={size}x{size}&margin=8&data={dato}"

def cargar_img(base_name, fallback_url):
    for ext in ['.jpg', '.png', '.jpeg', '.JPG', '.PNG', '.JPEG']:
        path = f"assets/{base_name}{ext}"
        if os.path.exists(path): return path
    return fallback_url

# CSS Y SCRIPTS DE CONTROL DE SCROLL Y ALTO CONTRASTE
CSS_Y_SCROLL = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap');

html, body, [class*="css"], [data-testid="stMarkdownContainer"] {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

.stApp { background-color: #f2f7f4 !important; }

p, span, label, h1, h2, h3, h4, h5, h6, [data-testid="stWidgetLabel"] p, [data-testid="stMarkdownContainer"] p {
    color: #112a12 !important;
    font-weight: 700 !important;
}

[data-testid="stSidebar"] {
    background-color: #ffffff !important;
    border-right: 2px solid #2b9348 !important;
}

[data-testid="stSidebar"] p, [data-testid="stSidebar"] label, [data-testid="stSidebar"] span {
    color: #112a12 !important;
    font-weight: 700 !important;
}

.hero-vivid {
    background: linear-gradient(135deg, #007f5f, #2b9348);
    border-radius: 20px;
    padding: 25px;
    color: #ffffff !important;
    margin-bottom: 20px;
}

.hero-vivid h1, .hero-vivid p {
    color: #ffffff !important;
}

.card-bright {
    background: #ffffff !important;
    border-radius: 16px !important;
    padding: 20px !important;
    margin-bottom: 18px !important;
    border: 1px solid #d8f3dc !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.04) !important;
}

div.stButton > button {
    background: linear-gradient(135deg, #2b9348, #007f5f) !important;
    color: #ffffff !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    width: 100% !important;
}

.err-msg {
    color: #d90429 !important;
    font-size: 0.85rem;
    font-weight: bold;
}

/* TARJETA TRADUCTOR MULTILINGÜE - ALTO CONTRASTE */
.trans-card {
    background-color: #e8f5e9 !important;
    border-left: 5px solid #2b9348 !important;
    padding: 18px !important;
    border-radius: 12px !important;
    margin-top: 15px !important;
    color: #112a12 !important;
}
.trans-card p, .trans-card h4, .trans-card li {
    color: #112a12 !important;
}
</style>

<script>
    function irArriba() {
        var el = window.parent.document.querySelector('[data-testid="stAppViewContainer"]');
        if (el) { el.scrollTop = 0; }
        window.parent.scrollTo(0, 0);
    }
    setTimeout(irArriba, 10);
    setTimeout(irArriba, 100);
</script>
<div id="inicio_pagina"></div>
"""
st.markdown(CSS_Y_SCROLL, unsafe_allow_html=True)

# ------------------------------------------------------------------
# DICCIONARIO MULTILINGÜE Y RESPUESTAS DE LA SABEDORA
# ------------------------------------------------------------------
UI_TEXT = {
    "Español": {
        "title": "🌿 Dialogapp — Ecoruta Conectada", "sub": "Conecta con comunidades indígenas del Trapecio Amazónico sin intermediarios.",
        "nav1": "🛠️ Diseña Tu Ecoruta", "nav2": "🗣️ Traductor & IA", "nav3": "🍫 Ruta Cacao EUDR", "nav4": "🎫 Reservas & QR",
        "lbl_lang": "Idioma / Language:", "lbl_profile": "Perfil del Turista:", "lbl_offline": "⚡ Modo Offline PWA", "lbl_scan": "📱 Escanea o haz clic para abrir la App:",
        "prof_normal": "Normal", "prof_acad": "Académico", "prof_adv": "Aventura", "prof_well": "Bienestar",
        "step": "Paso {} de 4", "btn_next": "Siguiente ➡️", "btn_prev": "⬅️ Anterior", "btn_pay": "💳 IR A RESERVA Y PAGO 🚀", "btn_back": "⬅️ Volver",
        "p1_title": "Paso 1: ¿Con quién viajas?", "gopts": ["Solo (1 pers)", "Pareja (2-3 pers)", "Familia (4-8 pers)", "Grupo (9+ pers)"],
        "lbl_grupo": "Tipo de grupo:", "lbl_pers": "Número exacto:", "lbl_nights": "Noches de hospedaje:",
        "p2_title": "Paso 2: Actividades y Alojamiento", "lbl_rec": "Recomendadas para tu perfil", "lbl_all_acts": "Todas las actividades",
        "msg_acad": "🎓 Perfil Académico Activo: Priorizando talleres etnobotánicos, ciencia y cultura.",
        "msg_adv": "🧗 Perfil Aventura Activo: Priorizando exploración y deportes en el territorio.",
        "msg_well": "🧘 Perfil Bienestar Activo: Priorizando descanso, arte y espiritualidad.",
        "lbl_aloj": "Selecciona tu estancia:", "aloj_none": "Sin Alojamiento",
        "p3_title": "Paso 3: Comida y Pasajeros", "lbl_food_sec": "🍲 Gastronomía y Bebidas Ancestrales",
        "lbl_pass_list": "Registro de Pasajeros", "lbl_pass": "Pasajero", "lbl_name": "Nombre Completo *", "lbl_age": "Edad *", "lbl_doc": "Documento ID *",
        "lbl_alg": "Alergias", "alg_opts": ["Ninguna", "Mariscos / Pescados", "Picaduras de insectos", "Polen / Polvo", "Lácteos / Gluten", "Medicamentos"],
        "lbl_cond": "Condición Física", "cond_opts": ["Sin restricciones", "Dificultad para caminar", "Asma / Respiratorio", "Embarazo"],
        "err_req": "⚠️ Campo obligatorio", "err_form": "❌ Completa los campos obligatorios en rojo.", "lbl_ins": "Seguro Médico Rescate Amazónico",
        "p4_title": "Paso 4: Resumen y Finanzas", "lbl_total": "Total Reserva", "lbl_com": "80% Pago Directo al Emprendedor Indígena", "lbl_emp": "20% Operación Tecnológica Dialogapp",
        "lbl_group_res": "Grupo", "lbl_nights_res": "Noches", "lbl_aloj_res": "Alojamiento",
        "gw_title": "💳 Pasarela de Pago", "gw_method": "Método de Pago", "gw_opts": ["Tarjeta de Crédito", "PSE / Banco Local", "Nequi / Daviplata", "Efectivo"],
        "gw_name": "Nombre Titular *", "gw_doc": "Documento Titular *", "gw_card": "Número Tarjeta *", "gw_exp": "Exp (MM/AA)", "gw_cvv": "CVV (3 dígitos) *",
        "gw_term": "Acepto Políticas de Seguridad y Tratamiento de Datos.", "btn_conf": "💳 CONFIRMAR RESERVA", "msg_succ": "🎉 ¡Reserva Confirmada Exitosamente!", 
        "qr_tit": "🎟️ Pase Digital Biocultural", "lbl_holder": "Titular", "msg_no_book": "No hay reservas activas en este momento.",
        "eudr_title": "🍫 Ruta Cacao EUDR — Vitrina de Comercio Justo", "eudr_sub": "Trazabilidad satelital y certificación de Cero Deforestación (Normativa Europea EUDR)",
        "col_lote": "Lote de Cacao", "col_gps": "Coordenadas GPS", "col_eudr": "Cumplimiento EUDR", "lbl_ok": "✅ Verificado Cero Deforestación",
        "ai_title": "🤖 Sabedora — IA Biocultural Inteligente", "ai_input": "Pregúntale a la Sabedora (ej: hola, gracias, agua, comer, cacao, salud):",
        "ai_resp_hola": "👋 ¡Hola! En la Amazonía te recibimos con los brazos abiertos y alegría. Pregúntame sobre saludos, agua, comida, cacao o cultura.",
        "ai_resp_gracias": "🙏 'Gracias' se expresa con el corazón y profundo respeto por la tierra que nos hospeda y alimenta.",
        "ai_resp_agua": "💧 El agua es sagrada y dadora de vida. En las comunidades usamos sistemas de filtración natural y protección de fuentes.",
        "ai_resp_food": "🍲 Puedes degustar Pescado Moqueado en hoja de Bijao, Pirarucú con Fariña, Patarashca y jugos naturales de Açaí y Copoazú.",
        "ai_resp_cacao": "🍫 Proceso del Cacao: 1. Cosecha manual de la mazorca madura en la chagra. 2. Extracción de granos y fermentación en cajones de madera noble. 3. Secado artesanal al sol. 4. Transformación en chocolate fino de aroma con trazabilidad por GPS y Cero Deforestación (EUDR).",
        "ai_resp_bano": "💧 Los baños ecológicos y secos están disponibles en cada comunidad, respetando el río y el ecosistema.",
        "ai_resp_salud": "🌿 La medicina tradicional se basa en plantas sagradas y saberes de los abuelos. Contamos con seguro médico de rescate integrado.",
        "ai_resp_def": "💡 Te escucho. Puedes consultarme sobre saludos, gracias, agua, qué comer, cacao, baños o salud ancestral.",
        "ai_trans_title": "🗣️ Soberanía Lingüística — Traducción en Lenguas Amazónicas & Globales:"
    },
    "English": {
        "title": "🌿 Dialogapp — Connected Eco-Route", "sub": "Connect directly with indigenous communities in the Amazon without intermediaries.",
        "nav1": "🛠️ Design Eco-Route", "nav2": "🗣️ Translator & AI", "nav3": "🍫 EUDR Cocoa", "nav4": "🎫 Bookings & QR",
        "lbl_lang": "Language:", "lbl_profile": "Tourist Profile:", "lbl_offline": "⚡ Offline PWA Mode", "lbl_scan": "📱 Scan or click to open the App:",
        "prof_normal": "Normal", "prof_acad": "Academic", "prof_adv": "Adventure", "prof_well": "Wellness",
        "step": "Step {} of 4", "btn_next": "Next ➡️", "btn_prev": "⬅️️ Previous", "btn_pay": "💳 PROCEED TO CHECKOUT 🚀", "btn_back": "⬅️ Back",
        "p1_title": "Step 1: Who is traveling?", "gopts": ["Solo (1 pers)", "Couple (2-3 pers)", "Family (4-8 pers)", "Group (9+ pers)"],
        "lbl_grupo": "Group type:", "lbl_pers": "Exact number:", "lbl_nights": "Nights of stay:",
        "p2_title": "Step 2: Activities & Accommodation", "lbl_rec": "Recommended for your profile", "lbl_all_acts": "All activities",
        "msg_acad": "🎓 Academic Profile Active: Prioritizing ethnobotanical workshops, science and culture.",
        "msg_adv": "🧗 Adventure Profile Active: Prioritizing exploration and outdoor sports.",
        "msg_well": "🧘 Wellness Profile Active: Prioritizing rest, art and spirituality.",
        "lbl_aloj": "Select accommodation:", "aloj_none": "No Accommodation",
        "p3_title": "Step 3: Food & Passengers", "lbl_food_sec": "🍲 Ancestral Cuisine & Native Drinks",
        "lbl_pass_list": "Passenger Registry", "lbl_pass": "Passenger", "lbl_name": "Full Name *", "lbl_age": "Age *", "lbl_doc": "ID Document *",
        "lbl_alg": "Allergies", "alg_opts": ["None", "Seafood / Fish", "Insect bites", "Pollen / Dust", "Dairy / Gluten", "Medications"],
        "lbl_cond": "Physical Condition", "cond_opts": ["No restrictions", "Walking difficulty", "Asthma", "Pregnancy"],
        "err_req": "⚠️ Required field", "err_form": "❌ Complete required fields in red.", "lbl_ins": "Amazon Rescue Medical Insurance",
        "p4_title": "Step 4: Summary & Finance", "lbl_total": "Total Booking", "lbl_com": "80% Direct Payment to Indigenous Entrepreneur", "lbl_emp": "20% Dialogapp Operations",
        "lbl_group_res": "Group", "lbl_nights_res": "Nights", "lbl_aloj_res": "Accommodation",
        "gw_title": "💳 Payment Gateway", "gw_method": "Payment Method", "gw_opts": ["Credit Card", "Local Bank Transfer", "Mobile Wallet", "Cash"],
        "gw_name": "Cardholder Name *", "gw_doc": "Cardholder ID *", "gw_card": "Card Number *", "gw_exp": "Exp (MM/YY)", "gw_cvv": "CVV (3 digits) *",
        "gw_term": "I accept Data and Safety Policies.", "btn_conf": "💳 CONFIRM BOOKING", "msg_succ": "🎉 Booking Successfully Confirmed!", 
        "qr_tit": "🎟️️ Biocultural Digital Pass", "lbl_holder": "Cardholder", "msg_no_book": "No active bookings at the moment.",
        "eudr_title": "🍫 EUDR Cocoa Route — Fair Trade Showcase", "eudr_sub": "Satellite traceability and Zero Deforestation certification (EUDR)",
        "col_lote": "Cocoa Lot", "col_gps": "GPS Coordinates", "col_eudr": "EUDR Compliance", "lbl_ok": "✅ Verified Zero Deforestation",
        "ai_title": "🤖 Elder — Smart Biocultural AI", "ai_input": "Ask the Elder (e.g. hello, thanks, water, food, cacao, health):",
        "ai_resp_hola": "👋 Hello! In the Amazon we welcome you with respect and joy. Ask me about greetings, water, food, or cacao.",
        "ai_resp_gracias": "🙏 'Thank you' is expressed with the heart and deep respect for the land that hosts us.",
        "ai_resp_agua": "💧 Water is sacred. Communities use natural filtration systems and protected sources.",
        "ai_resp_food": "🍲 You can taste Smoked Fish in Bijao Leaf, Pirarucu with Fariña, and natural Açaí juice.",
        "ai_resp_cacao": "🍫 Cocoa Process: 1. Manual harvest of ripe pods. 2. Fermentation in wooden boxes. 3. Sun drying. 4. Crafting fine aroma chocolate with GPS traceability and Zero Deforestation (EUDR).",
        "ai_resp_bano": "💧 Ecological dry toilets are available in each community.",
        "ai_resp_salud": "🌿 Traditional medicine relies on sacred plants and elder wisdom. Rescue insurance is included.",
        "ai_resp_def": "💡 I am listening. Ask me about greetings, thanks, water, food, cacao, or health.",
        "ai_trans_title": "🗣️ Linguistic Sovereignty — Amazonian & Global Translation:"
    },
    "Português": {
        "title": "🌿 Dialogapp — Ecorrota", "sub": "Conecte-se diretamente com comunidades indígenas sem intermediários.",
        "nav1": "🛠 Desenhar Ecorrota", "nav2": "🗣 Tradutor e IA", "nav3": "🍫 Cacau EUDR", "nav4": "🎫 Reservas e QR",
        "lbl_lang": "Idioma:", "lbl_profile": "Perfil do Turista:", "lbl_offline": "⚡ Modo Offline", "lbl_scan": "📱 Escaneie ou clique para abrir o App:",
        "prof_normal": "Normal", "prof_acad": "Académico", "prof_adv": "Aventura", "prof_well": "Bem-estar",
        "step": "Passo {} de 4", "btn_next": "Próximo ➡️", "btn_prev": "⬅️ Anterior", "btn_pay": "💳 IR PARA PAGAMENTO 🚀", "btn_back": "⬅️ Voltar",
        "p1_title": "Passo 1: Com quem você viaja?", "gopts": ["Sozinho (1 pers)", "Casal (2-3 pers)", "Família (4-8 pers)", "Grupo (9+ pers)"],
        "lbl_grupo": "Tipo de grupo:", "lbl_pers": "Número exato:", "lbl_nights": "Noites de estadia:",
        "p2_title": "Passo 2: Atividades e Hospedagem", "lbl_rec": "Recomendadas para o seu perfil", "lbl_all_acts": "Todas as atividades",
        "msg_acad": "🎓 Perfil Académico Ativo: Priorizando oficinas etnobotânicas, ciência e cultura.",
        "msg_adv": "🧗 Perfil Aventura Ativo: Priorizando exploração e esportes.",
        "msg_well": "🧘 Perfil Bem-estar Ativo: Priorizando descanso, arte e espiritualidade.",
        "lbl_aloj": "Selecione hospedagem:", "aloj_none": "Sem Hospedagem",
        "p3_title": "Passo 3: Comida e Passageiros", "lbl_food_sec": "🍲 Gastronomia Ancestral e Bebidas Nativas",
        "lbl_pass_list": "Registro de Passageiros", "lbl_pass": "Passageiro", "lbl_name": "Nome Completo *", "lbl_age": "Idade *", "lbl_doc": "Documento ID *",
        "lbl_alg": "Alergias", "alg_opts": ["Nenhuma", "Frutos do mar / Peixe", "Picadas de insetos", "Pólen / Poeira", "Laticínios / Glúten", "Medicamentos"],
        "lbl_cond": "Condição Física", "cond_opts": ["Sem restrições", "Dificuldade para andar", "Asma", "Gravidez"],
        "err_req": "⚠️ Campo obrigatório", "err_form": "❌ Preencha os campos obrigatórios em vermelho.", "lbl_ins": "Seguro Médico de Resgate",
        "p4_title": "Passo 4: Resumo e Finanças", "lbl_total": "Total Reserva", "lbl_com": "80% Pagamento Direto ao Empreendedor Indígena", "lbl_emp": "20% Operações Dialogapp",
        "lbl_group_res": "Grupo", "lbl_nights_res": "Noites", "lbl_aloj_res": "Hospedagem",
        "gw_title": "💳 Gateway de Pagamento", "gw_method": "Método de Pagamento", "gw_opts": ["Cartão de Crédito", "Transferência Bancária", "Carteira Digital", "Dinheiro"],
        "gw_name": "Nome Titular *", "gw_doc": "Documento Titular *", "gw_card": "Número do Cartão *", "gw_exp": "Exp (MM/AA)", "gw_cvv": "CVV (3 dígitos) *",
        "gw_term": "Aceito as Políticas de Dados.", "btn_conf": "💳 CONFIRMAR RESERVA", "msg_succ": "🎉 Reserva Confirmada com Sucesso!", 
        "qr_tit": "🎟️ Passe Digital Biocultural", "lbl_holder": "Titular", "msg_no_book": "Nenhuma reserva ativa no momento.",
        "eudr_title": "🍫 Rota do Cacau EUDR — Vitrine de Comércio Justo", "eudr_sub": "Rastreabilidade via satélite e certificação de Zero Desmatamento (EUDR)",
        "col_lote": "Lote Cacau", "col_gps": "Coordenadas GPS", "col_eudr": "Conformidade EUDR", "lbl_ok": "✅ Verificado Zero Desmatamento",
        "ai_title": "🤖 Sabedora — IA Biocultural Inteligente", "ai_input": "Pergunte à Sabedora (ex: olá, obrigado, água, comer, cacau, saúde):",
        "ai_resp_hola": "👋 Olá! Na Amazônia recebemos você com respeito e alegria. Pergunte-me sobre cumprimentos, água, comida ou cacau.",
        "ai_resp_gracias": "🙏 'Obrigado' é expresso com o coração e profundo respeito pela terra que nos acolhe.",
        "ai_resp_agua": "💧 A água é sagrada. Nas comunidades usamos sistemas de filtragem natural.",
        "ai_resp_food": "🍲 Você pode provar Peixe Moqueado, Pirarucu com Farinha e suco de Açaí.",
        "ai_resp_cacao": "🍫 Processo do Cacau: 1. Colheita manual. 2. Fermentação em caixas de madeira. 3. Secagem ao sol. 4. Transformação em chocolate fino com rastreabilidade GPS e Zero Desmatamento (EUDR).",
        "ai_resp_bano": "💧 Banheiros ecológicos secos estão disponíveis em cada comunidade.",
        "ai_resp_salud": "🌿 A medicina tradicional baseia-se em plantas sagradas. Seguro de resgate integrado.",
        "ai_resp_def": "💡 Ouço você. Pergunte-me sobre cumprimentos, obrigado, água, comida, cacau ou saúde.",
        "ai_trans_title": "🗣️ Soberania Linguística — Tradução em Línguas Amazônicas & Globais:"
    },
    "Français": {
        "title": "🌿 Dialogapp — Écoroute", "sub": "Connectez-vous avec les communautés autochtones sans intermédiaires.",
        "nav1": "🛠 Créer Écoroute", "nav2": "🗣 Traducteur et IA", "nav3": "🍫 Cacao EUDR", "nav4": "🎫 Réservations et QR",
        "lbl_lang": "Langue:", "lbl_profile": "Profil Touriste:", "lbl_offline": "⚡ Mode Hors Ligne", "lbl_scan": "📱 Scannez ou cliquez pour ouvrir l'App:",
        "prof_normal": "Normal", "prof_acad": "Académique", "prof_adv": "Aventura", "prof_well": "Bien-être",
        "step": "Étape {} sur 4", "btn_next": "Suivant ➡️", "btn_prev": "⬅ Précédent", "btn_pay": "💳 PROCÉDER AU PAIEMENT 🚀", "btn_back": "⬅️ Retour",
        "p1_title": "Étape 1: Avec qui voyagez-vous?", "gopts": ["Solo (1 pers)", "Couple (2-3 pers)", "Famille (4-8 pers)", "Groupe (9+ pers)"],
        "lbl_grupo": "Type de groupe:", "lbl_pers": "Nombre exact:", "lbl_nights": "Nuits de séjour:",
        "p2_title": "Étape 2: Activités et Hébergement", "lbl_rec": "Recommandé pour votre profil", "lbl_all_acts": "Toutes les activités",
        "msg_acad": "🎓 Profil Académique Actif: Ateliers ethnobotaniques, science et culture priorisés.",
        "msg_adv": "🧗 Profil Aventure Actif: Exploration et sports de plein air priorisés.",
        "msg_well": "🧘 Profil Bien-être Actif: Repos, art et spiritualité priorisés.",
        "lbl_aloj": "Sélectionnez hébergement:", "aloj_none": "Sans Hébergement",
        "p3_title": "Étape 3: Nourriture et Passagers", "lbl_food_sec": "🍲 Gastronomie Ancestrale et Boissons Natives",
        "lbl_pass_list": "Registre des Passagers", "lbl_pass": "Passager", "lbl_name": "Nom Complet *", "lbl_age": "Âge *", "lbl_doc": "Document ID *",
        "lbl_alg": "Allergies", "alg_opts": ["Aucune", "Fruits de mer / Poisson", "Piqûres d'insectes", "Pollen / Poussière", "Laitiers / Gluten", "Médicaments"],
        "lbl_cond": "Condition Physique", "cond_opts": ["Sans restriction", "Difficulté à marcher", "Asthme", "Grossesse"],
        "err_req": "⚠️ Champ obligatoire", "err_form": "❌ Remplissez les champs obligatoires en rouge.", "lbl_ins": "Assurance Médicale de Secours",
        "p4_title": "Étape 4: Résumé et Finances", "lbl_total": "Total Réservation", "lbl_com": "80% Paiement Direct à l'Entrepreneur Autochtone", "lbl_emp": "20% Opérations Dialogapp",
        "lbl_group_res": "Groupe", "lbl_nights_res": "Nuits", "lbl_aloj_res": "Hébergement",
        "gw_title": "💳 Passerelle de Paiement", "gw_method": "Méthode de Paiement", "gw_opts": ["Carte de Crédit", "Virement Bancaire", "Portefeuille Mobile", "Espèces"],
        "gw_name": "Nom Titulaire *", "gw_doc": "ID Titulaire *", "gw_card": "Numéro Carte *", "gw_exp": "Exp (MM/AA)", "gw_cvv": "CVV (3 chiffres) *",
        "gw_term": "J'accepte les politiques de données.", "btn_conf": "💳 CONFIRMER RÉSERVATION", "msg_succ": "🎉 Réservation Confirmée avec Succès!", 
        "qr_tit": "🎟️ Pass Numérique Bioculturel", "lbl_holder": "Titular", "msg_no_book": "Aucune réservation active pour le moment.",
        "eudr_title": "🍫 Route du Cacao EUDR — Vitrine de Commerce Équitable", "eudr_sub": "Traçabilité satellite et certification Zéro Déforestation (EUDR)",
        "col_lote": "Lot de Cacao", "col_gps": "Coordenadas GPS", "col_eudr": "Conformité EUDR", "lbl_ok": "✅ Vérifié Zéro Déforestation",
        "ai_title": "🤖 Aîné — IA Bioculturelle Intelligente", "ai_input": "Posez votre question à l'Aîné (ex: bonjour, merci, eau, manger, cacao):",
        "ai_resp_hola": "👋 Bonjour ! En Amazonie, nous vous accueillons avec joie. Posez vos questions sur les salutations, l'eau, la nourriture ou le cacao.",
        "ai_resp_gracias": "🙏 'Merci' s'exprime avec le cœur et le respect de la terre qui nous accueille.",
        "ai_resp_agua": "💧 L'eau est sacrée. Les communautés utilisent des systèmes de filtration naturelle.",
        "ai_resp_food": "🍲 Vous pouvez goûter le Poisson Moqueado, le Pirarucu et les jus d'Açaí.",
        "ai_resp_cacao": "🍫 Processus du Cacao : 1. Récolte manuelle. 2. Fermentation en caisses de bois. 3. Séchage au soleil. 4. Transformation en chocolat fin avec traçabilité GPS et Zéro Déforestation (EUDR).",
        "ai_resp_bano": "💧 Des toilettes écologiques sèches sont disponibles dans chaque communauté.",
        "ai_resp_salud": "🌿 La médecine traditionnelle repose sur les plantes sacrées. Assurance secours incluse.",
        "ai_resp_def": "💡 Je vous écoute. Posez-moi des questions sur les salutations, merci, l'eau, le cacao ou la santé.",
        "ai_trans_title": "🗣️ Souveraineté Linguistique — Traduction en Langues Amazoniennes & Globales:"
    }
}

# GLOSARIO NATIVO AMAZÓNICO AMPLIADO
GLOSARIO_NATIVO = {
    "saludo": {
        "Tikuna": "Naneé (Hola / Buen día)",
        "Cocama": "Maé (Saludo tradicional)",
        "Huitoto": "Jigüi (Buenos días / Vida)",
        "Español": "¿Cómo se saluda en la comunidad?",
        "English": "How do you say hello in the community?",
        "Português": "Como se cumprimenta na comunidade?",
        "Français": "Comment salue-t-on dans la communauté ?"
    },
    "gracias": {
        "Tikuna": "Dëga (Agradecimiento profundo)",
        "Cocama": "Tupana (Gracias / Bendición)",
        "Huitoto": "Jimeke (Agradecimiento al territorio)",
        "Español": "Muchas gracias por el recibimiento",
        "English": "Thank you very much for the welcome",
        "Português": "Muito obrigado pela recepção",
        "Français": "Merci beaucoup pour l'accueil"
    },
    "agua": {
        "Tikuna": "Üi (Agua del río sagrado)",
        "Cocama": "Yacu (Agua / Río Amazonas)",
        "Huitoto": "Meni (Fluido vital de la selva)",
        "Español": "¿Dónde hay agua potable o del río?",
        "English": "Where is drinking water or river water?",
        "Português": "Onde há água potável ou do rio?",
        "Français": "Où y a-t-il de l'eau potable ou de rivière ?"
    },
    "comida": {
        "Tikuna": "Aï (Alimento / Pescado del río)",
        "Cocama": "Ura (Alimento tradicional)",
        "Huitoto": "Jigüi (Sustento de la chagra)",
        "Español": "¿Dónde puedo degustar la gastronomía ancestral?",
        "English": "Where can I taste ancestral cuisine?",
        "Português": "Onde posso provar a gastronomia ancestral?",
        "Français": "Où puis-je goûter la cuisine ancestrale ?"
    },
    "cacao": {
        "Tikuna": "Kakuu (Cacao nativo amazónico)",
        "Cocama": "Cacao sacha (Cacao de monte)",
        "Huitoto": "IINi (Fruto y pensamiento de cacao)",
        "Español": "¿Cómo se procesa y verifica el cacao sin deforestación (EUDR)?",
        "English": "How is zero-deforestation cocoa processed and verified (EUDR)?",
        "Português": "Como é processado e verificado o cacau sem desmatamento (EUDR)?",
        "Français": "Comment traite-t-on et vérifie-t-on le cacao zéro déforestation (EUDR) ?"
    },
    "salud": {
        "Tikuna": "Pea (Bienestar y armonía en la comunidad)",
        "Cocama": "Causana (Salud y vida en equilibrio)",
        "Huitoto": "Jima (Sanación física y espiritual)",
        "Español": "¿Qué hacer en caso de requerir asistencia médica o rescate?",
        "English": "How is emergency medical assistance handled?",
        "Português": "O que fazer em caso de assistência médica?",
        "Français": "Que faire en cas de besoin d'assistance médicale ?"
    }
}

DATA_ACTS = {
    "a1": {"cat": "Académico", "price": 25000, "img": "nocturna", "n": {"Español": "Caminata Nocturna con Sabedor", "English": "Night Walk with Elder", "Português": "Caminhada Noturna com Sabedor", "Français": "Marche Nocturne avec Aîné"}},
    "a2": {"cat": "Académico", "price": 25000, "img": "cacao", "n": {"Español": "Taller de Cacao Ancestral", "English": "Ancestral Cocoa Workshop", "Português": "Oficina de Cacau Ancestral", "Français": "Atelier Cacao Ancestral"}},
    "a3": {"cat": "Académico", "price": 30000, "img": "chagra", "n": {"Español": "Siembra en la Chagra", "English": "Farming in Chagra", "Português": "Plantio na Chagra", "Français": "Agriculture dans la Chagra"}},
    "a4": {"cat": "Académico", "price": 15000, "img": "maloca_dia", "n": {"Español": "Estancia de Día en Maloca", "English": "Day Stay in Maloca", "Português": "Estadia de Dia na Maloca", "Français": "Séjour de Jour en Maloca"}},
    "a5": {"cat": "Aventura", "price": 35000, "img": "canopy", "n": {"Español": "Canopy y Arbolismo", "English": "Tree Canopy Zipline", "Português": "Canopy em Árvores", "Français": "Canopée et Tyrolienne"}},
    "a6": {"cat": "Aventura", "price": 30000, "img": "kayak", "n": {"Español": "Travesía Kayak por Lagos", "English": "Kayak Journey through Lakes", "Português": "Passeio de Caiaque", "Français": "Excursion en Kayak"}},
    "a7": {"cat": "Aventura", "price": 28000, "img": "pesca", "n": {"Español": "Pesca Artesanal Nocturna", "English": "Artisanal Night Fishing", "Português": "Pesca Artesanal Noturna", "Français": "Pêche Artisanale Nocturne"}},
    "a8": {"cat": "Bienestar", "price": 20000, "img": "artesania", "n": {"Español": "Taller de Cerámica", "English": "Pottery Workshop", "Português": "Oficina de Cerâmica", "Français": "Atelier de Poterie"}},
    "a9": {"cat": "Bienestar", "price": 32000, "img": "delfines", "n": {"Español": "Avistamiento Delfines Rosados", "English": "Pink Dolphin Watching", "Português": "Observação de Botos Cor-de-rosa", "Français": "Observation de Dauphins Roses"}}
}

DATA_ALOJ = {
    "h1": {"price": 45000, "img": "cabana", "n": {"Español": "Cabaña Tradicional", "English": "Traditional Cabin", "Português": "Cabana Tradicional", "Français": "Cabane Traditionnelle"}},
    "h2": {"price": 60000, "img": "arbol", "n": {"Español": "Cabaña en el Árbol", "English": "Treehouse", "Português": "Casa na Árvore", "Français": "Cabane dans les Arbres"}},
    "h3": {"price": 20000, "img": "hamaca", "n": {"Español": "Maloca / Hamacas", "English": "Maloca / Hammocks", "Português": "Maloca / Redes", "Français": "Maloca / Hamacs"}}
}

DATA_FOOD = {
    "f1": {"price": 22000, "img": "moqueado", "n": {"Español": "Pescado Moqueado en Bijao", "English": "Smoked Fish in Bijao Leaf", "Português": "Peixe Moqueado na Folha", "Français": "Poisson Fumé en Feuille"}},
    "f2": {"price": 25000, "img": "pirarucu", "n": {"Español": "Pirarucú con Fariña", "English": "Pirarucu with Fariña", "Português": "Pirarucu com Farinha", "Français": "Pirarucu et Fariña"}},
    "f3": {"price": 28000, "img": "patarashca", "n": {"Español": "Patarashca Tradicional", "English": "Traditional Patarashca", "Português": "Patarashca Tradicional", "Français": "Patarashca Traditionnelle"}},
    "b1": {"price": 6000, "img": "acai", "n": {"Español": "Jugo Natural de Açaí", "English": "Natural Açaí Juice", "Português": "Suco Natural de Açaí", "Français": "Jus Naturel d'Açaí"}},
    "b2": {"price": 7000, "img": "camucamu", "n": {"Español": "Bebida Ancestral Camu-Camu", "English": "Ancestral Camu-Camu Drink", "Português": "Bebida de Camu-Camu", "Français": "Boisson Camu-Camu"}},
    "p1": {"price": 8000, "img": "casabe", "n": {"Español": "Casabe Dulce con Miel", "English": "Sweet Casabe with Honey", "Português": "Beiju Doce com Mel", "Français": "Casabe Doux au Miel"}},
    "p2": {"price": 10000, "img": "mousse", "n": {"Español": "Mousse de Copoazú", "English": "Copoazu Mousse", "Português": "Mousse de Cupuaçu", "Français": "Mousse Copoazu"}}
}

# ------------------------------------------------------------------
# URL BASE DE LA APLICACIÓN
# ------------------------------------------------------------------
APP_URL = "http://localhost:8501"

# ------------------------------------------------------------------
# BARRA LATERAL (SIDEBAR CON QR CLICLEABLE Y FUNCIONAL)
# ------------------------------------------------------------------
with st.sidebar:
    lang_sel = st.selectbox("🌍 Select Language / Idioma", ["Español", "English", "Português", "Français"])
    t = UI_TEXT[lang_sel]
    
    pagina = st.radio("Navegación:", [t["nav1"], t["nav2"], t["nav3"], t["nav4"]])
    st.markdown("---")
    
    prof_opts = [t["prof_normal"], t["prof_acad"], t["prof_adv"], t["prof_well"]]
    prof_map = {t["prof_normal"]: "Normal", t["prof_acad"]: "Académico", t["prof_adv"]: "Aventura", t["prof_well"]: "Bienestar"}
    prof_sel = st.selectbox(t["lbl_profile"], prof_opts)
    perfil_interno = prof_map[prof_sel]
    
    st.toggle(t["lbl_offline"], value=False)
    st.markdown("---")
    
    # QR Interactivo clicleable en la barra lateral con enlace directo
    qr_img_src = qr_url(APP_URL, 150)
    st.markdown(f"""
        <div style="text-align: center;">
            <a href="{APP_URL}" target="_blank" title="Haz clic para abrir la App">
                <img src="{qr_img_src}" alt="QR Code App" style="border-radius: 8px; border: 2px solid #2b9348;">
            </a>
            <br><br>
            <a href="{APP_URL}" target="_blank" style="color: #2b9348; font-weight: 700; text-decoration: underline; font-size: 0.9rem;">
                🔗 Abrir Aplicación Directamente
            </a>
        </div>
    """, unsafe_allow_html=True)
    st.caption(t["lbl_scan"])

# ==================================================================
# MÓDULO 1: DISEÑADOR PASO A PASO
# ==================================================================
if pagina == t["nav1"]:
    st.markdown(f'<div class="hero-vivid"><h1>{t["title"]}</h1><p>{t["sub"]}</p></div>', unsafe_allow_html=True)
    
    paso = st.session_state.paso_plan
    st.progress(paso / 4, text=t["step"].format(paso))

    # PASO 1
    if paso == 1 and not st.session_state.ir_a_pago_directo:
        st.markdown('<div class="card-bright">', unsafe_allow_html=True)
        st.subheader(t["p1_title"])
        
        idx_g = st.session_state.get("idx_g", 0)
        sel_g = st.radio(t["lbl_grupo"], t["gopts"], index=idx_g, horizontal=True)
        st.session_state.idx_g = t["gopts"].index(sel_g)
        
        num_p = st.number_input(t["lbl_pers"], min_value=1, max_value=30, value=st.session_state.get("num_p", 1))
        st.session_state.num_p = num_p
        
        num_n = st.slider(t["lbl_nights"], 0, 7, st.session_state.get("num_n", 1))
        st.session_state.num_n = num_n
        
        st.markdown('</div>', unsafe_allow_html=True)
        if st.button(t["btn_next"], key="btn_next_p1"): 
            st.session_state.paso_plan = 2
            st.rerun()

    # PASO 2: ACTIVIDADES Y ALOJAMIENTO CON PRECIO VISIBLE
    elif paso == 2 and not st.session_state.ir_a_pago_directo:
        c_top1, c_top2 = st.columns(2)
        if c_top1.button(t["btn_prev"], key="p2_top_prev"): st.session_state.paso_plan = 1; st.rerun()
        if c_top2.button(t["btn_next"], key="p2_top_next"): st.session_state.paso_plan = 3; st.rerun()

        st.markdown('<div class="card-bright">', unsafe_allow_html=True)
        st.subheader(t["p2_title"])

        if perfil_interno == "Académico": st.success(t["msg_acad"])
        elif perfil_interno == "Aventura": st.success(t["msg_adv"])
        elif perfil_interno == "Bienestar": st.success(t["msg_well"])

        st.markdown(f"#### {t['lbl_all_acts']}")

        items_act = list(DATA_ACTS.items())
        if perfil_interno != "Normal":
            items_act.sort(key=lambda x: 0 if x[1]['cat'] == perfil_interno else 1)

        for k, v in items_act:
            es_rec = (v['cat'] == perfil_interno)
            badge = f"⭐ [{v['cat'].upper()}]" if es_rec else ""
            c_i, c_t = st.columns([1, 2.5])
            with c_i: 
                st.image(cargar_img(v['img'], "https://picsum.photos/600/400"), width=200)
            with c_t:
                nom_a = v['n'][lang_sel]
                chk = st.checkbox(f"**{nom_a}** — {cop(v['price'])} {badge}", value=(k in st.session_state.acts_elegidas), key=f"chk_a_{k}")
                if chk and k not in st.session_state.acts_elegidas: st.session_state.acts_elegidas.append(k)
                if not chk and k in st.session_state.acts_elegidas: st.session_state.acts_elegidas.remove(k)
            st.markdown("---")

        st.markdown(f"#### {t['lbl_aloj']}")
        opts_a = [f"{v['n'][lang_sel]} — {cop(v['price'])}" for v in DATA_ALOJ.values()] + [t["aloj_none"]]
        idx_aloj = st.session_state.get("idx_aloj", 0)
        sel_aloj = st.radio("", opts_a, index=idx_aloj)
        st.session_state.idx_aloj = opts_a.index(sel_aloj)

        st.markdown('</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        if c1.button(t["btn_prev"], key="p2_bot_prev"): st.session_state.paso_plan = 1; st.rerun()
        if c2.button(t["btn_next"], key="p2_bot_next"): st.session_state.paso_plan = 3; st.rerun()

    # PASO 3: GASTRONOMÍA Y PASAJEROS
    elif paso == 3 and not st.session_state.ir_a_pago_directo:
        c_top1, c_top2 = st.columns(2)
        if c_top1.button(t["btn_prev"], key="p3_top_prev"): st.session_state.paso_plan = 2; st.rerun()

        st.markdown('<div class="card-bright">', unsafe_allow_html=True)
        st.subheader(t["p3_title"])
        st.markdown(f"### {t['lbl_food_sec']}")

        for k, v in DATA_FOOD.items():
            c_i, c_t = st.columns([1, 3])
            with c_i: st.image(cargar_img(v['img'], "https://picsum.photos/600/400"), width=140)
            with c_t:
                chk = st.checkbox(f"**{v['n'][lang_sel]}** — {cop(v['price'])}", value=(k in st.session_state.comidas_elegidas), key=f"chk_f_{k}")
                if chk and k not in st.session_state.comidas_elegidas: st.session_state.comidas_elegidas.append(k)
                if not chk and k in st.session_state.comidas_elegidas: st.session_state.comidas_elegidas.remove(k)

        st.markdown("---")
        st.markdown(f"### 📋 {t['lbl_pass_list']}")
        cant_p = st.session_state.num_p
        hay_error = False
        pasajeros = []

        for i in range(cant_p):
            st.write(f"#### {t['lbl_pass']} {i+1}")
            c1, c2, c3 = st.columns([2, 1, 1.5])
            with c1:
                p_nom = st.text_input(f"{t['lbl_name']}", value="" if f"p_nom_{i}" not in st.session_state else st.session_state[f"p_nom_{i}"], key=f"p_nom_{i}")
                if not p_nom.strip(): st.markdown(f'<div class="err-msg">{t["err_req"]}</div>', unsafe_allow_html=True); hay_error = True
            with c2: 
                p_ed = st.number_input(f"{t['lbl_age']}", min_value=1, value=25, key=f"p_ed_{i}")
            with c3:
                p_doc = st.text_input(f"{t['lbl_doc']}", value="" if f"p_doc_{i}" not in st.session_state else st.session_state[f"p_doc_{i}"], key=f"p_doc_{i}")
                if not p_doc.strip(): st.markdown(f'<div class="err-msg">{t["err_req"]}</div>', unsafe_allow_html=True); hay_error = True
            
            p_alg = st.selectbox(t["lbl_alg"], t["alg_opts"], key=f"p_alg_{i}")
            p_cond = st.selectbox(t["lbl_cond"], t["cond_opts"], key=f"p_cond_{i}")
            pasajeros.append({"nom": p_nom, "ed": p_ed, "doc": p_doc, "alg": p_alg, "cond": p_cond})

        costo_seg = 30000 * cant_p
        st.info(f"🛡️️ **{t['lbl_ins']}:** {cop(costo_seg)}")

        st.session_state.pasajeros_temp = pasajeros
        st.session_state.costo_seg_temp = costo_seg
        st.markdown('</div>', unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        if c1.button(t["btn_prev"], key="p3_bot_prev"): st.session_state.paso_plan = 2; st.rerun()
        if c2.button(t["btn_next"], key="p3_bot_next"):
            if hay_error: st.error(t["err_form"])
            else: st.session_state.paso_plan = 4; st.rerun()

    # PASO 4: RESUMEN Y FINANZAS
    elif paso == 4 and not st.session_state.ir_a_pago_directo:
        st.markdown('<div class="card-bright">', unsafe_allow_html=True)
        st.subheader(t["p4_title"])
        
        cant_p = st.session_state.num_p
        noches = st.session_state.num_n
        
        tot_acts = sum(DATA_ACTS[k]['price'] for k in st.session_state.acts_elegidas) * cant_p
        
        aloj_k = list(DATA_ALOJ.keys())[st.session_state.idx_aloj] if st.session_state.idx_aloj < len(DATA_ALOJ) else None
        tot_aloj = DATA_ALOJ[aloj_k]['price'] * noches if aloj_k else 0
        aloj_nom = DATA_ALOJ[aloj_k]['n'][lang_sel] if aloj_k else t["aloj_none"]
        
        tot_food = sum(DATA_FOOD[k]['price'] for k in st.session_state.comidas_elegidas) * cant_p
        tot_seg = st.session_state.costo_seg_temp
        
        total_gen = tot_acts + tot_aloj + tot_food + tot_seg
        
        st.write(f"**{t['lbl_group_res']}:** {t['gopts'][st.session_state.idx_g]} | **{t['lbl_nights_res']}:** {noches}")
        st.write(f"**{t['lbl_aloj_res']}:** {aloj_nom}")
        
        for p in st.session_state.pasajeros_temp:
            st.caption(f"👤 {p['nom']} - {p['doc']} ({t['lbl_alg']}: {p['alg']} | {p['cond']})")

        st.markdown(f"### 💵 {t['lbl_total']}: {cop(total_gen)}")
        st.success(f"🌱 {t['lbl_com']}: {cop(total_gen*0.8)}")
        st.info(f"⚙️ {t['lbl_emp']}: {cop(total_gen*0.2)}")
        st.markdown('</div>', unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        if c1.button(t["btn_prev"], key="p4_bot_prev"): st.session_state.paso_plan = 3; st.rerun()
        if c2.button(t["btn_pay"], key="p4_bot_pay"):
            st.session_state.reserva = {"total": total_gen, "titular": st.session_state.pasajeros_temp[0]['nom']}
            st.session_state.ir_a_pago_directo = True
            st.rerun()

    # PASARELA DE PAGO DIRECTA (CVV ESTRICTO DE 3 DÍGITOS)
    if st.session_state.ir_a_pago_directo:
        st.markdown('<div class="card-bright">', unsafe_allow_html=True)
        st.subheader(t["gw_title"])
        with st.form("form_pago"):
            st.selectbox(t["gw_method"], t["gw_opts"])
            st.text_input(t["gw_name"])
            st.text_input(t["gw_doc"])
            st.text_input(t["gw_card"])
            c1, c2 = st.columns(2)
            c1.text_input(t["gw_exp"])
            cvv_input = c2.text_input(t["gw_cvv"], max_chars=3, placeholder="123")
            chk = st.checkbox(t["gw_term"], value=True)
            
            submitted = st.form_submit_button(t["btn_conf"])
            if submitted:
                if not chk: 
                    st.error(t["err_req"])
                elif len(cvv_input) != 3 or not cvv_input.isdigit():
                    st.error("⚠️ El CVV debe contener exactamente 3 números.")
                else:
                    st.balloons()
                    st.success(t["msg_succ"])
                    # QR interactivo de éxito de reserva
                    st.markdown(f"""
                        <div style="text-align: center; margin-top: 15px;">
                            <a href="{APP_URL}" target="_blank">
                                <img src="{qr_url("RESERVA_EXITOSA", 200)}" alt="QR Reserva" style="border-radius: 8px; border: 2px solid #2b9348;">
                            </a>
                            <br>
                            <a href="{APP_URL}" target="_blank" style="color: #2b9348; font-weight: bold; text-decoration: underline;">🔗 Abrir Pase Digital en la App</a>
                        </div>
                    """, unsafe_allow_html=True)
                    
        st.markdown('</div>', unsafe_allow_html=True)
        if st.button(t["btn_back"], key="gw_bot_back"): 
            st.session_state.ir_a_pago_directo = False
            st.session_state.paso_plan = 1
            st.rerun()

# ==================================================================
# MÓDULOS SECUNDARIOS (TRADUCTOR, IA INTELIGENTE, EUDR, QR)
# ==================================================================
elif pagina == t["nav2"]:
    st.markdown('<div class="card-bright">', unsafe_allow_html=True)
    st.title(t["ai_title"])
    ui_q = st.text_input(t["ai_input"])
    
    if ui_q:
        q_low = norm(ui_q)
        clave_encontrada = None
        
        if any(w in q_low for w in ["hola", "saludos", "buenas", "hi", "bonjour", "oi"]):
            resp = t["ai_resp_hola"]
            clave_encontrada = "saludo"
        elif any(w in q_low for w in ["gracias", "thank", "obrigado", "merci"]):
            resp = t["ai_resp_gracias"]
            clave_encontrada = "gracias"
        elif any(w in q_low for w in ["agua", "water", "eau", "hidrat"]):
            resp = t["ai_resp_agua"]
            clave_encontrada = "agua"
        elif any(w in q_low for w in ["comer", "comida", "hambre", "food", "manger", "pescado", "jugo", "comidas", "aliment", "plato", "gastronomia"]):
            clave_encontrada = "comida"
            resp = t["ai_resp_food"]
        elif any(w in q_low for w in ["cacao", "chocolate", "eudr", "trazabilidad", "lote", "gps", "proceso"]):
            clave_encontrada = "cacao"
            resp = t["ai_resp_cacao"]
        elif any(w in q_low for w in ["bano", "banos", "toilet", "restroom", "wc", "ducha"]):
            clave_encontrada = "bano"
            resp = t["ai_resp_bano"]
        elif any(w in q_low for w in ["salud", "medico", "seguro", "rescate", "hospital", "enfermo"]):
            clave_encontrada = "salud"
            resp = t["ai_resp_salud"]
        else:
            resp = t["ai_resp_def"]
            clave_encontrada = None
        
        st.info(resp)
        
        if clave_encontrada and clave_encontrada in GLOSARIO_NATIVO:
            item = GLOSARIO_NATIVO[clave_encontrada]
            st.markdown(f'''
            <div class="trans-card">
                <h4>{t["ai_trans_title"]} ({clave_encontrada.upper()})</h4>
                <p>🌿 <b>Tikuna:</b> {item["Tikuna"]}</p>
                <p>🌿 <b>Cocama:</b> {item["Cocama"]}</p>
                <p>🌿 <b>Huitoto:</b> {item["Huitoto"]}</p>
                <hr style="border: 0; border-top: 1px solid #2b9348; margin: 10px 0;">
                <p>1. <b>Español:</b> {item["Español"]}</p>
                <p>2. <b>English:</b> {item["English"]}</p>
                <p>3. <b>Português:</b> {item["Português"]}</p>
                <p>4. <b>Français:</b> {item["Français"]}</p>
            </div>
            ''', unsafe_allow_html=True)
        else:
            st.markdown(f'''
            <div class="trans-card">
                <h4>{t["ai_trans_title"]}</h4>
                <p>🌿 <b>Tikuna:</b> Nana kuu... (Saber biocultural verificado)</p>
                <p>🌿 <b>Cocama:</b> Iara yacu... (Traducción comunitaria)</p>
                <p>🌿 <b>Huitoto:</b> Jigüi uima... (Pensamiento ancestral)</p>
                <hr style="border: 0; border-top: 1px solid #2b9348; margin: 10px 0;">
                <p>1. <b>Español:</b> ¿Dónde puedo encontrar el servicio / espacio más cercano?</p>
                <p>2. <b>English:</b> Where can I find the nearest facility?</p>
                <p>3. <b>Português:</b> Onde posso encontrar o local mais próximo?</p>
                <p>4. <b>Français:</b> Où puis-je trouver l'espace le plus proche ?</p>
            </div>
            ''', unsafe_allow_html=True)
        
    st.markdown('</div>', unsafe_allow_html=True)

# MÓDULO 3: RUTA CACAO EUDR VISUAL
elif pagina == t["nav3"]:
    st.markdown(f'<div class="hero-vivid"><h1>{t["eudr_title"]}</h1><p>{t["eudr_sub"]}</p></div>', unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown('<div class="card-bright">', unsafe_allow_html=True)
        st.image(cargar_img("cacao", "https://picsum.photos/600/400"), width=350)
        st.subheader("🍫 Lote de Cacao Ancestral — AMZ-001")
        st.write("**Productor:** Asociación de Familias Indígenas Tikuna")
        st.write("**Coordenadas GPS:** `-3.77, -70.38`")
        st.success("✅ Certificado EUDR: Cero Deforestación Verificada por Satélite")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with c2:
        st.markdown('<div class="card-bright">', unsafe_allow_html=True)
        st.image(cargar_img("cacao", "https://picsum.photos/600/400"), width=350)
        st.subheader("🍫 Lote de Cacao Fino de Aroma — AMZ-002")
        st.write("**Productor:** Colectivo Agroecológico Huitoto")
        st.write("**Coordenadas GPS:** `-4.20, -69.94`")
        st.success("✅ Certificado EUDR: Cultivado bajo sombra en Chagra Nativa")
        st.markdown('</div>', unsafe_allow_html=True)

elif pagina == t["nav4"]:
    st.markdown('<div class="card-bright">', unsafe_allow_html=True)
    st.title(t["nav4"])
    res = st.session_state.reserva
    if res:
        st.success(t["msg_succ"])
        st.write(f"**{t['lbl_holder']}:** {res['titular']} | **Total:** {cop(res['total'])}")
        # QR Interactivo de Reserva Activa
        st.markdown(f"""
            <div style="text-align: center; margin-top: 15px;">
                <a href="{APP_URL}" target="_blank">
                    <img src="{qr_url("PASE_DIGITAL_OK", 200)}" alt="QR Pase Digital" style="border-radius: 8px; border: 2px solid #2b9348;">
                </a>
                <br>
                <a href="{APP_URL}" target="_blank" style="color: #2b9348; font-weight: bold; text-decoration: underline;">🔗 Abrir Enlace del Pase Digital</a>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.warning(t["msg_no_book"])
    st.markdown('</div>', unsafe_allow_html=True)