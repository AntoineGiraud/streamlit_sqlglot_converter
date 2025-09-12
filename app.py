import streamlit as st
from sqlglot import parse_one, dialects
from sqlglot.optimizer import optimize
from pathlib import Path

# Liste des dialectes disponibles (lowercase)
DIALECTS = sorted(dialect for dialect in dialects.DIALECTS)

st.set_page_config(page_title="SQL Dialect Converter", page_icon="🔄")
st.title("🔄 SQL Dialect Converter")

# Deux colonnes pour les sélecteurs
col1, col2 = st.columns(2)

with col1:
    default_src = DIALECTS.index("TSQL") if "TSQL" in DIALECTS else 1
    src_dialect = st.selectbox("Dialecte source", DIALECTS, index=default_src)

    # Checkbox pour activer/désactiver l'optimisation
    do_optimize = st.checkbox("Optimiser la requête avant conversion", value=False)

with col2:
    default_tgt = DIALECTS.index("DuckDB") if "DuckDB" in DIALECTS else 2
    tgt_dialect = st.selectbox("Dialecte cible", DIALECTS, index=default_tgt)

    if st.button("Charger la requête démo 📝"):
        demo_file = Path("demo_tsql.sql")
        if demo_file.exists():
            st.session_state.sql_input = demo_file.read_text(encoding="utf-8")
        else:
            st.error("Fichier demo_tsql.sql introuvable.")

# Zone de saisie SQL liée à session_state
sql_input = st.text_area("Collez votre SQL ici :", height=200, key="sql_input")


# Bouton de conversion
if st.button("Convertir 🚀") and sql_input.strip():
    # 1️⃣ Parse dans le dialecte source
    expr = parse_one(sql_input, read=src_dialect.lower())

    # 2️⃣ Optimisation si cochée
    if do_optimize:
        expr = optimize(expr)

    # 3️⃣ Génération SQL dans le dialecte cible + formatage
    formatted_sql = expr.sql(
        dialect=tgt_dialect.lower(),
        pretty=True,
        indent=4,
        normalize=True,
        normalize_functions="lower",
    )

    st.success("Conversion réussie ✅")
    st.code(formatted_sql, language="sql")
