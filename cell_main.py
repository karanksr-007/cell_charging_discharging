import streamlit as st
import pandas as pd
import random
import time

# ------------------- ⚙️ Page Config -------------------
st.set_page_config(
    page_title="Battery Monitoring Suite",
    page_icon="🔋",
    layout="wide"
)

# Predefined cell types
AVAILABLE_CELL_TYPES = ["LFP", "NMC", "NCA", "LMO", "LTO", "NiMH", "Lead-Acid"]

# Battery operating modes
OPERATING_MODES = ["Idle", "Charging", "Discharging"]

# ------------------- Helper Functions -------------------

def generate_cell_data(cell_selection, mode):
    data = []
    for idx, cell_type in enumerate(cell_selection, start=1):
        voltage_base = 3.2 if cell_type == "lfp" else 3.6
        if mode == "Charging":
            voltage = round(random.uniform(voltage_base + 0.1, voltage_base + 0.5), 2)
            current = round(random.uniform(1.0, 5.0), 2)
        elif mode == "Discharging":
            voltage = round(random.uniform(voltage_base - 0.5, voltage_base - 0.1), 2)
            current = round(random.uniform(0.5, 3.0), 2)
        else:
            voltage = round(random.uniform(voltage_base - 0.05, voltage_base + 0.05), 2)
            current = 0.0
        
        temp = round(random.uniform(25, 40), 1)
        capacity = round(voltage * current, 2)

        data.append({
            "Cell ID": f"Cell_{idx}",
            "Type": cell_type.upper(),
            "Mode": mode,
            "🔋 Voltage (V)": voltage,
            "⚡ Current (A)": current,
            "🌡️ Temp (°C)": temp,
            "⚙️ Capacity (Wh)": capacity
        })
    return pd.DataFrame(data)

def show_metrics(df):
    st.markdown("## 📊 Key Metrics Overview")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🔋 Avg Voltage", f"{df['🔋 Voltage (V)'].mean():.2f} V")
    col2.metric("⚡ Avg Current", f"{df['⚡ Current (A)'].mean():.2f} A")
    col3.metric("🌡️ Avg Temp", f"{df['🌡️ Temp (°C)'].mean():.1f} °C")
    col4.metric("⚙️ Total Capacity", f"{df['⚙️ Capacity (Wh)'].sum():.2f} Wh")

def show_data_table(df):
    st.markdown("## 📋 Detailed Cell Data")
    st.dataframe(df, use_container_width=True)

def show_charts(df):
    st.markdown("## 📈 Visual Insights")
    chart1, chart2 = st.columns(2)

    with chart1:
        st.subheader("🌡️ Temperature by Cell")
        st.bar_chart(df.set_index("Cell ID")["🌡️ Temp (°C)"])

    with chart2:
        st.subheader("⚙️ Capacity Distribution")
        st.bar_chart(df.set_index("Cell ID")["⚙️ Capacity (Wh)"])

def download_csv(df):
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name="battery_cell_data.csv",
        mime="text/csv"
    )

# ------------------- Section: Dashboard -------------------
def dashboard():
    st.header("🔋 Battery Dashboard")
    st.markdown("Configure your battery cells and operation mode below:")

    with st.form("dashboard_form"):
        col1, col2 = st.columns([1, 2])

        with col1:
            num_cells = st.number_input("Number of Cells", min_value=1, max_value=20, value=4, step=1,
                                        help="Select how many battery cells to simulate.")

        with col2:
            operation_mode = st.selectbox("Operation Mode", OPERATING_MODES, index=0,
                                          help="Select the battery operation mode.")

        cell_types = []
        for i in range(num_cells):
            cell_type = st.selectbox(f"Cell {i+1} Type", options=AVAILABLE_CELL_TYPES, key=f"cell_type_{i}")
            cell_types.append(cell_type.lower())

        submitted = st.form_submit_button("Generate Dashboard")

    if submitted:
        if not cell_types or len(cell_types) == 0:
            st.warning("⚠️ Please select at least one cell type.")
            return
        
        df = generate_cell_data(cell_types, operation_mode)
        show_metrics(df)
        show_data_table(df)
        show_charts(df)
        download_csv(df)
        st.success("✅ Dashboard generated successfully!")
    else:
        st.info("ℹ️ Fill out the form above and submit to generate the dashboard.")

# ------------------- Section: Task Manager -------------------
def task_manager():
    st.header("🛠️ Task Manager")
    st.write("Simulate and manage battery tasks.")

    task = st.selectbox("Select Task", ["Start Charging", "Start Discharging", "Set Idle", "Perform Maintenance"])
    duration = st.slider("Task Duration (minutes)", 1, 120, 30)
    st.write(f"Task `{task}` scheduled for {duration} minutes.")

    if st.button("Execute Task"):
        with st.spinner(f"Executing task: {task} for {duration} minutes..."):
            time.sleep(2)
        st.success(f"Task `{task}` executed successfully!")

# ------------------- Section: Real-time Application -------------------
def realtime_application():
    st.header("⏱️ Real-time Battery Monitoring")

    st.write("Simulating live data stream with periodic updates...")

    cell_selection = ["lfp", "nmc", "nca"]

    mode = st.selectbox("Select Operating Mode", OPERATING_MODES, index=0)

    if st.button("Start Real-time Monitoring"):
        placeholder = st.empty()
        for _ in range(20):
            df = generate_cell_data(cell_selection, mode)
            with placeholder.container():
                show_metrics(df)
                show_data_table(df)
                show_charts(df)
                time.sleep(1)

        st.success("Real-time monitoring session completed.")

# ------------------- Section: Performance & Graphs -------------------
def performance_and_graphs():
    st.header("📈 Performance & Graphs")

    st.write("Analyze battery performance over time or under different modes.")

    modes = OPERATING_MODES
    records = []

    for mode in modes:
        for t in range(10):
            cell_selection = ["lfp", "nmc", "nca"]
            df = generate_cell_data(cell_selection, mode)
            avg_voltage = df["🔋 Voltage (V)"].mean()
            avg_current = df["⚡ Current (A)"].mean()
            avg_temp = df["🌡️ Temp (°C)"].mean()
            total_capacity = df["⚙️ Capacity (Wh)"].sum()
            records.append({
                "Time": t,
                "Mode": mode,
                "Avg Voltage": avg_voltage,
                "Avg Current": avg_current,
                "Avg Temp": avg_temp,
                "Total Capacity": total_capacity
            })

    perf_df = pd.DataFrame(records)

    metric = st.selectbox("Select metric to visualize:", ["Avg Voltage", "Avg Current", "Avg Temp", "Total Capacity"])

    st.line_chart(data=perf_df, x="Time", y=metric, color="Mode")

    st.markdown("### Detailed Data")
    st.dataframe(perf_df)

    download_csv(perf_df)

# ------------------- 🚀 Main -------------------
def main():
    # Only one sidebar radio with unique key
    section = st.sidebar.radio(
        "Navigate to:",
        ["Dashboard", "Task Manager", "Real-time Application", "Performance & Graphs"],
        key="sidebar_navigation"  # Unique key added here
    )

    if section == "Dashboard":
        dashboard()
    elif section == "Task Manager":
        task_manager()
    elif section == "Real-time Application":
        realtime_application()
    elif section == "Performance & Graphs":
        performance_and_graphs()

if __name__ == "__main__":
    main()
