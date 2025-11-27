# ------------------------------------------------------------
# DASHBOARD KPI — SHOPONLINE ESPAÑA
# ------------------------------------------------------------

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ------------------------------------------------------------
# CARGA DE DATOS
# ------------------------------------------------------------
ventas_ecommerce = pd.read_csv("ventas_ecommerce_10000.csv")

# Transformaciones mínimas
ventas_ecommerce['Fecha'] = pd.to_datetime(ventas_ecommerce['Fecha'], errors='coerce')
ventas_ecommerce['Anio'] = ventas_ecommerce['Fecha'].dt.year
ventas_ecommerce['Mes'] = ventas_ecommerce['Fecha'].dt.month
ventas_ecommerce['Mes_Anio'] = ventas_ecommerce['Fecha'].dt.to_period('M').astype(str)
ventas_ecommerce['Valoracion_Categoria'] = ventas_ecommerce['Valoracion_Cliente'].astype("string").fillna("Sin valoración")

# ------------------------------------------------------------
# SIDEBAR
# ------------------------------------------------------------
st.sidebar.title("Dashboard — KPIs de Ventas")
st.sidebar.write("Proyecto: ShopOnline España")

kpi_seleccionado = st.sidebar.selectbox(
    "Seleccionar KPI:",
    [
        "1) Evolución de ventas",
        "2) Ventas por categoría",
        "3) Ticket medio",
        "4) Métodos de pago",
        "5) Ventas por región",
        "6) Valoraciones del cliente",
        "7) Tiempo de entrega",
    ],
)

# ------------------------------------------------------------
# KPI 1 — Evolución de ventas
# ------------------------------------------------------------
if kpi_seleccionado == "1) Evolución de ventas":
    st.title("📈 KPI 1 — Evolución de las Ventas")

    ventas_por_mes = (
        ventas_ecommerce
        .groupby("Mes_Anio", as_index=False)
        .agg(Total_Ventas_Netas=("Total_Neto", "sum"))
        .sort_values("Mes_Anio")
    )

    st.subheader("Tabla de ventas por mes")
    st.dataframe(ventas_por_mes)

    st.subheader("Gráfico de evolución mensual")
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(ventas_por_mes["Mes_Anio"], ventas_por_mes["Total_Ventas_Netas"], marker="o")
    plt.xticks(rotation=45)
    st.pyplot(fig)

    st.markdown(
        """
### 📝 Comentario profesional

**Contexto:** Permite evaluar la evolución temporal del negocio.  
**Cálculo:** Suma de `Total_Neto` agrupado por `Mes_Anio`.  
**Interpretación:** La serie revela picos de demanda y posibles campañas.  
**Insight:** Crecimientos marcados en determinados meses.  
**Relevancia:** Optimiza inventario, promociones y previsión de ventas.
"""
    )

# ------------------------------------------------------------
# KPI 2 — Ventas por categoría
# ------------------------------------------------------------
elif kpi_seleccionado == "2) Ventas por categoría":
    st.title("📦 KPI 2 — Ventas por Categoría")

    ventas_por_categoria = (
        ventas_ecommerce
        .groupby("Categoria_Producto", as_index=False)
        .agg(Total_Ventas_Netas=("Total_Neto", "sum"))
        .sort_values("Total_Ventas_Netas", ascending=False)
    )

    st.dataframe(ventas_por_categoria)

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(ventas_por_categoria["Categoria_Producto"], ventas_por_categoria["Total_Ventas_Netas"])
    plt.xticks(rotation=45)
    st.pyplot(fig)

    st.markdown(
        """
### 📝 Comentario profesional

**Contexto:** Ayuda a identificar qué líneas de producto son más rentables.  
**Cálculo:** Suma de ventas por `Categoria_Producto`.  
**Interpretación:** Las categorías top concentran gran parte de la facturación.  
**Insight:** Alta concentración del ingreso en 1–2 categorías.  
**Relevancia:** Guía decisiones de catálogo e inversión comercial.
"""
    )

# ------------------------------------------------------------
# KPI 3 — Ticket medio
# ------------------------------------------------------------
elif kpi_seleccionado == "3) Ticket medio":
    st.title("💶 KPI 3 — Ticket Medio")

    ticket_medio = ventas_ecommerce["Total_Neto"].mean()
    st.metric("Ticket medio (€)", f"{ticket_medio:,.2f}")

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.hist(ventas_ecommerce["Total_Neto"], bins=40)
    st.pyplot(fig)

    st.markdown(
        f"""
### 📝 Comentario profesional

**Contexto:** Evalúa el valor promedio por transacción.  
**Cálculo:** Media del campo `Total_Neto`.  
**Interpretación:** El ticket medio actual es **{ticket_medio:.2f} €**.  
**Insight:** Existen compras premium que elevan la media.  
**Relevancia:** Útil para estrategias de upselling y bundles.
"""
    )

# ------------------------------------------------------------
# KPI 4 — Métodos de pago
# ------------------------------------------------------------
elif kpi_seleccionado == "4) Métodos de pago":
    st.title("💳 KPI 4 — Métodos de Pago")

    metodos_pago = (
        ventas_ecommerce
        .groupby("Metodo_Pago", as_index=False)
        .agg(Cantidad=("Metodo_Pago", "count"))
        .sort_values("Cantidad", ascending=False)
    )

    st.dataframe(metodos_pago)

    etiquetas = [
        f"{row.Metodo_Pago}\n{row.Cantidad / metodos_pago['Cantidad'].sum():.1%}"
        for _, row in metodos_pago.iterrows()
    ]

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(metodos_pago["Cantidad"], labels=etiquetas, startangle=90)
    st.pyplot(fig)

    st.markdown(
        """
### 📝 Comentario profesional

**Contexto:** Evalúa la experiencia de checkout y fricción de pago.  
**Cálculo:** Conteo de `Metodo_Pago` por transacción.  
**Interpretación:** Un método de pago suele dominar el proceso.  
**Insight:** Dependencia elevada de un único método.  
**Relevancia:** Sugiere expandir alternativas para optimizar conversión.
"""
    )

# ------------------------------------------------------------
# KPI 5 — Ventas por región
# ------------------------------------------------------------
elif kpi_seleccionado == "5) Ventas por región":
    st.title("🗺️ KPI 5 — Ventas por Región")

    ventas_por_region = (
        ventas_ecommerce
        .groupby("Region", as_index=False)
        .agg(Total_Ventas_Netas=("Total_Neto", "sum"))
        .sort_values("Total_Ventas_Netas", ascending=False)
    )

    st.dataframe(ventas_por_region)

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.barh(ventas_por_region["Region"], ventas_por_region["Total_Ventas_Netas"])
    ax.invert_yaxis()
    st.pyplot(fig)

    st.markdown(
        """
### 📝 Comentario profesional

**Contexto:** Permite detectar mercados fuertes y zonas de oportunidad.  
**Cálculo:** Suma de ventas por `Region`.  
**Interpretación:** Algunas regiones concentran mayor facturación.  
**Insight:** Alta concentración geográfica del negocio.  
**Relevancia:** Optimiza logística, campañas y distribución de stock.
"""
    )

# ------------------------------------------------------------
# KPI 6 — Valoraciones del cliente
# ------------------------------------------------------------
elif kpi_seleccionado == "6) Valoraciones del cliente":
    st.title("⭐ KPI 6 — Valoraciones del Cliente")

    valoraciones = ventas_ecommerce["Valoracion_Categoria"].value_counts()

    st.dataframe(valoraciones)

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(valoraciones.index, valoraciones.values)
    plt.xticks(rotation=45)
    st.pyplot(fig)

    st.markdown(
        """
### 📝 Comentario profesional

**Contexto:** Mide satisfacción post-compra y calidad del servicio.  
**Cálculo:** Conteo de `Valoracion_Cliente` (incluye nulos).  
**Interpretación:** Suelen predominar valoraciones altas; “Sin valoración” sigue siendo relevante.  
**Insight:** Alto nivel de satisfacción general.  
**Relevancia:** Guía mejoras de retención y feedback del cliente.
"""
    )

# ------------------------------------------------------------
# KPI 7 — Tiempo de entrega
# ------------------------------------------------------------
elif kpi_seleccionado == "7) Tiempo de entrega":
    st.title("🚚 KPI 7 — Tiempo de Entrega")

    tiempos_validos = ventas_ecommerce[~ventas_ecommerce["Tiempo_Entrega_Dias"].isna()]

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.hist(tiempos_validos["Tiempo_Entrega_Dias"], bins=30)
    st.pyplot(fig)

    st.write("Pedidos sin dato de entrega:", ventas_ecommerce["Tiempo_Entrega_Dias"].isna().sum())

    st.markdown(
        """
### 📝 Comentario profesional

**Contexto:** Impacta en satisfacción y repetición de compra.  
**Cálculo:** Histograma de tiempos válidos (`Tiempo_Entrega_Dias`).  
**Interpretación:** La mayoría de entregas suele concentrarse en pocos días.  
**Insight:** La variabilidad evidencia oportunidades de optimización.  
**Relevancia:** Identifica cuellos de botella logísticos.
"""
    )
