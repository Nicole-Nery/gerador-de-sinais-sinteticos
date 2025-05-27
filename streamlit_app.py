import streamlit as st
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from functions import * 

st.set_page_config('Signal Generator', layout='wide')
st.title("Synthetic Signal Generator")

st.sidebar.header("Signal Settings")
signal_type = st.sidebar.selectbox("Waveform", ["Sinusoidal", "Square", "Triangular", "Random"])

# Common parameters
with st.sidebar:
    with st.expander("Basic parameters"):
        fs = st.slider("Sample rate (Hz)", 10, 1000, 100, step=1)
        duration = st.slider("Signal duration (s)", 1, 10, 5, step=1)
        offset = st.slider("Offset", -10.0, 10.0, 0.0, step=0.5)
        amplitude = st.slider("Amplitude", 0.1, 10.0, 1.0, step=0.1)
        frequency = st.slider("Frequency (Hz)", 0.1, 50.0, 1.0, step=0.1)

        # Signal generation
        if signal_type == "Sinusoidal":
            df = generateSine(offset, amplitude, fs, duration, frequency)
        elif signal_type == "Square":
            df = generateSquare(offset, amplitude, fs, duration, frequency)
        elif signal_type == "Triangular":
            df = generateTriangle(offset, amplitude, fs, duration, frequency)
        elif signal_type == "Random":
            distribution = st.selectbox("Distribution", ["normal", "uniform", "binomial"])
            df = generateRandomSignal(offset, amplitude, fs, duration, distribution)

with st.sidebar:
    with st.expander("Additional effects"):
        add_noise = st.checkbox("Add noise")
        add_trend = st.checkbox("Add trend")
        add_discontinuity = st.checkbox("Add discontinuity")
        add_sudden_change = st.checkbox("Sudden amplitude change")

        # Extra parameters
        if add_noise:
            snr = st.slider("SNR (dB)", 0, 50, 20, step=1)
            df = addNoise(df, snr)

        if add_trend:
            trend_type = st.selectbox("Trend type", ["linear", "quadratic"])
            df = addTrend(df, trend_type)

        if add_discontinuity:
            break_time = st.slider("Discontinuity time (s)", 0.0, float(duration), 2.0)
            jump_value = st.slider("Jump value", -10.0, 10.0, 2.0)
            df = addDiscontinuity(df, break_time, jump_value)

        if add_sudden_change:
            change_time = st.slider("Time of change (s)", 0.0, float(duration), 2.0)
            new_amp = st.slider("New amplitude", 0.1, 10.0, 2.0, step=0.1)
            df = addSuddenChange(df, change_time, new_amp)

# Plotting the signal
fig = go.Figure()
fig.add_trace(go.Scatter(x=df['t'], y=df['signal'], mode='lines', name=signal_type))
fig.update_layout(
    xaxis_title="Time (s)",
    yaxis_title="Amplitude",
    template="plotly_white",
    height=300
)
st.plotly_chart(fig, use_container_width=True)

st.subheader("Gramian Angular Field")
fig, axes = plt.subplots(1, 2, figsize=(9, 4))

# GASF image
im = axes[0].imshow(applyGAF(df, 'summation'), cmap='rainbow', origin='lower')
axes[0].set_title('Gramian Angular Summation Field')
fig.colorbar(im, ax=axes[0], fraction=0.046, pad=0.04)

# GADF image
im = axes[1].imshow(applyGAF(df, 'difference'), cmap='rainbow', origin='lower')
axes[1].set_title('Gramian Angular Difference Field')
fig.colorbar(im, ax=axes[1], fraction=0.046, pad=0.04)

plt.tight_layout()
st.pyplot(fig)
