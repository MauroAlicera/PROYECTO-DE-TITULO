import streamlit as st
from scraper import (scrapear_pagina,extraer_html,limpiar_body,split_dom_content)
from parse import parse_with_ollama

st.title("Web Scraper de farmacias ")

url = st.text_input("Ingresa el sitio de la farmacia:")

if st.button("Scrapear el sitio"):
    st.write("Scrapeando el sitio")

    # Extraer el contenido del sitio web
    resultado = scrapear_pagina(url)
    contenido_del_body = extraer_html(resultado)
    contenido_limpio = limpiar_body(contenido_del_body)

    # Almacenar el contenido del DOM en el estado de sesión de Streamlit
    st.session_state.dom_content = contenido_limpio

    # Mostrar el contenido del DOM en un cuadro de texto expandible
    with st.expander("Vista al  DOM Content"):
        st.text_area("DOM Content", contenido_limpio, height=300)


# Step 2: Ask Questions About the DOM Content
if "dom_content" in st.session_state:
    parse_description = st.text_area("Describe lo que quieres obtener ")

    if st.button("Parse Content"):
        if parse_description:
            st.write("Parsing the content...")

            # Parse the content with Ollama
            dom_chunks = split_dom_content(st.session_state.dom_content)
            parsed_result = parse_with_ollama(dom_chunks, parse_description)
            st.write(parsed_result)
            