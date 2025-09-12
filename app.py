import streamlit as st
from sqlglot import parse_one, dialects
from sqlglot.optimizer import optimize

# Liste des dialectes disponibles (lowercase)
DIALECTS = sorted(dialect for dialect in dialects.DIALECTS)

st.set_page_config(page_title="SQL Dialect Converter", page_icon="🔄")
st.title("🔄 SQL Dialect Converter + Optimizer")

# Sélecteurs de dialectes
default_src = DIALECTS.index("TSQL") if "TSQL" in DIALECTS else 0
default_tgt = DIALECTS.index("DuckDB") if "DuckDB" in DIALECTS else 0

src_dialect = st.selectbox("Dialecte source", DIALECTS, index=default_src)
tgt_dialect = st.selectbox("Dialecte cible", DIALECTS, index=default_tgt)

# Zone de saisie SQL
sql_input = st.text_area("Collez votre SQL ici :", height=200)

if st.button("Convertir et Optimiser 🚀"):
    if sql_input.strip():
        try:
            # 1️⃣ Parse dans le dialecte source
            expr = parse_one(sql_input, read=src_dialect.lower())

            # 2️⃣ Optimisation de l'AST
            # optimized_expr = optimize(expr)

            # 3️⃣ Génération SQL dans le dialecte cible + formatage
            formatted_sql = expr.sql(
                dialect=tgt_dialect.lower(),
                pretty=True,
                indent=4,
                normalize=True,
                normalize_functions="lower",
            )

            st.success("Conversion et optimisation réussies ✅")
            st.code(formatted_sql, language="sql")

        except Exception as e:
            st.error(f"Erreur lors de la conversion : {e}")
    else:
        st.warning("Veuillez coller du SQL à convertir.")