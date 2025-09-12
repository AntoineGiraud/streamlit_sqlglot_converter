import streamlit as st
from sqlglot import parse_one, dialects
from sqlglot.optimizer import optimize
from pathlib import Path

# List of available dialects (lowercase)
DIALECTS = sorted(dialect for dialect in dialects.DIALECTS)
DIALECTS_lower = [dialect.lower() for dialect in DIALECTS]

st.set_page_config(page_title="SQLGlot Dialect Converter", page_icon="🔄")
st.title("🔄 SQLGlot Dialect Converter")

st.info("[SQLGlot](https://github.com/tobymao/sqlglot) is a SQL parsing, conversion, and optimization.")

# Two columns for the selectors
col1, col2 = st.columns(2)

with col1:
    src_dialect = st.selectbox("Source dialect", DIALECTS, index=DIALECTS_lower.index("tsql"))

    # Checkbox to enable/disable optimization
    do_optimize = st.checkbox("Optimize query before conversion", value=False)

with col2:
    tgt_dialect = st.selectbox("Target dialect", DIALECTS, index=DIALECTS_lower.index("duckdb"))

    col2_1, col2_2 = st.columns([6, 4])
    with col2_1:
        if st.button("📝 Load demo query"):
            demo_file = Path("demo_tsql.sql")
            if demo_file.exists():
                st.session_state.sql_input = demo_file.read_text(encoding="utf-8")
            else:
                st.error("demo_tsql.sql file not found.")
    with col2_2:
        if st.button("🗑️ Clear query"):
            st.session_state.sql_input = ""


# SQL input area linked to session_state
sql_input = st.text_area("Paste your SQL here:", height=200, key="sql_input")

# Conversion button
if st.button("Convert 🚀", type="primary") and sql_input.strip():
    # 1️⃣ Parse in the source dialect
    expr = parse_one(sql_input, read=src_dialect.lower())

    # 2️⃣ Optimize if checked
    if do_optimize:
        expr = optimize(expr)

    # 3️⃣ Generate SQL in the target dialect + formatting
    formatted_sql = expr.sql(
        dialect=tgt_dialect.lower(),
        pretty=True,
        indent=4,
        normalize=True,
        normalize_functions="lower",
    )

    st.success("Conversion successful ✅")
    st.code(formatted_sql, language="sql")
