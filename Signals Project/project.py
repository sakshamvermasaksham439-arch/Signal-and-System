
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import signal

# ---------------------------------
# PAGE CONFIGURATION
# ---------------------------------
st.set_page_config(
    page_title="Interactive Signal Generator",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Interactive Signal Generator")
st.markdown(
    "### Signal and Systems Laboratory"
)
st.write(
    "Generate, modify and visualize different "
    "signals interactively."
)

# ---------------------------------
# SIDEBAR CONTROLS
# ---------------------------------
st.sidebar.header("⚙️ Signal Configuration")

signal_type = st.sidebar.selectbox(
    "Select Signal Type",
    [
        "Sine",
        "Cosine",
        "Unit Step",
        "Unit Impulse",
        "Ramp",
        "Exponential",
        "Square",
        "Triangular",
        "Sawtooth"
    ]
)

signal_mode = st.sidebar.radio(
    "Signal Representation",
    ["Continuous Time", "Discrete Time"]
)

amplitude = st.sidebar.slider(
    "Amplitude (A)", 0.1, 10.0, 1.0, 0.1
)

frequency = st.sidebar.slider(
    "Frequency (Hz)", 0.1, 10.0, 1.0, 0.1
)

phase = st.sidebar.slider(
    "Phase (Radians)", -np.pi, np.pi, 0.0
)

time_shift = st.sidebar.slider(
    "Time Shift", -5.0, 5.0, 0.0, 0.1
)

time_scale = st.sidebar.slider(
    "Time Scaling", 0.1, 5.0, 1.0, 0.1
)

duration = st.sidebar.slider(
    "Time Duration", 1, 10, 5
)

# ---------------------------------
# GENERATE TIME AXIS
# ---------------------------------
if signal_mode == "Continuous Time":
    t = np.linspace(
        -duration,
        duration,
        2000
    )
    dt = t[1] - t[0]
else:
    t = np.arange(
        -duration * 10,
        duration * 10 + 1
    )
    dt = 1.0

# Apply time shifting and scaling
transformed_t = time_scale * (t - time_shift)

# ---------------------------------
# SIGNAL GENERATION
# ---------------------------------
def generate_signal(name, x, A, f, p, dt, mode):

    if name == "Sine":
        y = A * np.sin(2 * np.pi * f * x + p)

    elif name == "Cosine":
        y = A * np.cos(2 * np.pi * f * x + p)

    elif name == "Unit Step":
        y = A * np.where(x >= 0, 1, 0)

    elif name == "Unit Impulse":
        if mode == "Discrete Time":
            y = A * np.where(np.isclose(x, 0), 1, 0)
        else:
            # Rectangular approximation of a unit-area impulse
            y = A * np.where(
                np.abs(x) <= dt / 2,
                1 / dt,
                0
            )

    elif name == "Ramp":
        y = A * np.maximum(x, 0)

    elif name == "Exponential":
        y = A * np.exp(-f * x)

    elif name == "Square":
        y = A * signal.square(
            2 * np.pi * f * x + p
        )

    elif name == "Triangular":
        y = A * signal.sawtooth(
            2 * np.pi * f * x + p,
            width=0.5
        )

    elif name == "Sawtooth":
        y = A * signal.sawtooth(
            2 * np.pi * f * x + p
        )

    return y


# Generate output
y = generate_signal(
    signal_type,
    transformed_t,
    amplitude,
    frequency,
    phase,
    dt,
    signal_mode
)

# ---------------------------------
# DISPLAY SIGNAL INFORMATION
# ---------------------------------
st.subheader("Signal Information")

col1, col2, col3 = st.columns(3)

col1.metric("Signal Type", signal_type)
col2.metric("Amplitude", amplitude)
col3.metric("Frequency", f"{frequency} Hz")

# ---------------------------------
# PLOT SIGNAL
# ---------------------------------
st.subheader("📈 Signal Visualization")

fig, ax = plt.subplots(figsize=(12, 5))

if signal_mode == "Discrete Time":
    ax.stem(
        t,
        y,
        linefmt="b-",
        markerfmt="bo",
        basefmt="k-"
    )
    ax.set_xlabel("Discrete Time (n)")
else:
    ax.plot(
        t,
        y,
        linewidth=2
    )
    ax.set_xlabel("Continuous Time (t)")

ax.set_ylabel("Amplitude")
ax.set_title(
    signal_type + " Signal"
)

ax.grid(True, alpha=0.3)
ax.axhline(0, color="black", linewidth=0.8)
ax.axvline(0, color="black", linewidth=0.8)

st.pyplot(fig)
plt.close(fig)

# ---------------------------------
# SIGNAL DATA TABLE
# ---------------------------------
st.subheader("📋 Generated Signal Data")

df = pd.DataFrame({
    "Time": t,
    "Transformed Time": transformed_t,
    "Amplitude": y
})

st.dataframe(
    df.head(20),
    use_container_width=True
)

# ---------------------------------
# DOWNLOAD CSV
# ---------------------------------
csv_data = df.to_csv(index=False)

st.download_button(
    label="⬇️ Download Signal Data (CSV)",
    data=csv_data,
    file_name="generated_signal.csv",
    mime="text/csv"
)

# ---------------------------------
# SIGNAL EQUATIONS
# ---------------------------------
st.subheader("📚 Mathematical Representation")

equations = {
    "Sine": "x(t) = A sin(2πft + φ)",
    "Cosine": "x(t) = A cos(2πft + φ)",
    "Unit Step": "u(t) = 1 for t ≥ 0, otherwise 0",
    "Unit Impulse": "δ(t): unit-area impulse approximation",
    "Ramp": "r(t) = t u(t)",
    "Exponential": "x(t) = A e^(-ft)",
    "Square": "x(t) = A square(2πft + φ)",
    "Triangular": "x(t) = A triangular(2πft + φ)",
    "Sawtooth": "x(t) = A sawtooth(2πft + φ)"
}

st.info(equations[signal_type])

st.markdown("---")
st.markdown(
    "**Signal and Systems Project | Python | NumPy | SciPy | Matplotlib | Streamlit**"
)
