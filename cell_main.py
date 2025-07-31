import streamlit as st
import pandas as pd
import random

# ------------------- Config -------------------
st.set_page_config(
    page_title="Battery Dashboard",
    page_icon="🔋",
    layout="wide"
)

st.markdown("""
    <h1 style='text-align: center; color: #4CAF50;'>🔋 Battery Cell Monitoring Dashboard</h1>
    <p style='text-align: center;'>Real-time simulated data with interactive controls and insights.</p>
""", unsafe_allow_html=True)

# ------------------- Sidebar Input -------------------
st.sidebar.header("🧪 Configure Cells")

# Predefined cell types
available_cell_types = ["LFP", "NMC", "NCA", "LMO", "LTO", "NiMH", "Lead-Acid"]

cell_selection = []
for i in range(8):
    selected = st.sidebar.selectbox(f"Select type for Cell {i+1}", options=[""] + available_cell_types, key=f"cell_{i}")
    if selected:
        cell_selection.append(selected.lower())

# Remove empty or duplicate cells
cell_selection = list(dict.fromkeys([c for c in cell_selection if c.strip() != ""]))

if st.sidebar.button("🚀 Generate Dashboard"):
    if not cell_selection:
        st.warning("⚠️ Please select at least one valid cell type.")
    else:
        # ------------------- Generate Data -------------------
        cell_data = []
        for idx, cell_type in enumerate(cell_selection, start=1):
            voltage = 3.2 if cell_type == "lfp" else 3.6
            current = round(random.uniform(0.5, 5.0), 2)
            temp = round(random.uniform(25, 40), 1)
            capacity = round(voltage * current, 2)

            cell_data.append({
                "Cell ID": f"Cell_{idx}",
                "Type": cell_type.upper(),
                "🔋 Voltage (V)": voltage,
                "⚡ Current (A)": current,
                "🌡️ Temp (°C)": temp,
                "⚙️ Capacity (Wh)": capacity
            })

        df = pd.DataFrame(cell_data)

        # ------------------- Metrics -------------------
        st.markdown("## 📊 Key Metrics Overview")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("🔋 Avg Voltage", f"{df['🔋 Voltage (V)'].mean():.2f} V")
        col2.metric("⚡ Avg Current", f"{df['⚡ Current (A)'].mean():.2f} A")
        col3.metric("🌡️ Avg Temp", f"{df['🌡️ Temp (°C)'].mean():.1f} °C")
        col4.metric("⚙️ Total Capacity", f"{df['⚙️ Capacity (Wh)'].sum():.2f} Wh")

        # ------------------- Data Table -------------------
        st.markdown("## 📋 Detailed Cell Data")
        st.dataframe(df, use_container_width=True)

        # ------------------- Charts -------------------
        st.markdown("## 📈 Visual Insights")
        chart1, chart2 = st.columns(2)

        with chart1:
            st.subheader("🌡️ Temperature by Cell")
            st.bar_chart(df.set_index("Cell ID")["🌡️ Temp (°C)"])

        with chart2:
            st.subheader("⚙️ Capacity Distribution")
            st.bar_chart(df.set_index("Cell ID")["⚙️ Capacity (Wh)"])

        # ------------------- Download -------------------
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name="battery_cell_data.csv",
            mime='text/csv'
        )

        st.success("✅ Dashboard generated successfully!")

else:
    st.info("ℹ️ Select cell types from the sidebar and click 'Generate Dashboard' to begin.")

