import streamlit as st
import plotly.graph_objects as go
from funcoes import *

st.set_page_config('Gerador de Sinais', layout='wide')
st.title("Gerador de Sinais Sintéticos")

st.sidebar.header("Configurações do sinal")
tipo_sinal = st.sidebar.selectbox("Tipo de sinal", ["Senoidal", "Quadrada", "Triangular", "Aleatório"])

# Parâmetros comuns
with st.sidebar:
    with st.expander("Parâmetros básicos"):
        offset = st.slider("Offset", -10.0, 10.0, 0.0, step=0.5)
        amplitude = st.slider("Amplitude", 0.1, 10.0, 1.0, step=0.1)
        frequencia = st.slider("Frequência (Hz)", 0.1, 50.0, 1.0, step=0.1)
        fs = st.slider("Frequência de amostragem (Hz)", 10, 1000, 100, step=1)
        duracao = st.slider("Duração do sinal (s)", 1, 10, 5, step=1)

        # Geração do sinal base
        if tipo_sinal == "Senoidal":
            df = gerarSenoide(offset, amplitude, fs, duracao, frequencia)
        elif tipo_sinal == "Quadrada":
            df = gerarQuadrada(offset, amplitude, fs, duracao, frequencia)
        elif tipo_sinal == "Triangular":
            df = gerarTriangular(offset, amplitude, fs, duracao, frequencia)
        elif tipo_sinal == "Aleatório":
            distribuicao = st.selectbox("Distribuição", ["normal", "uniforme", "binomial"])
            df = gerarSinalAleatorio(offset, amplitude, fs, duracao, distribuicao)

with st.sidebar:
    with st.expander("Efeitos adicionais"):
        adicionar_ruido = st.checkbox("Ruído")
        adicionar_tendencia = st.checkbox("Tendência")
        adicionar_descont = st.checkbox("Descontinuidade")
        adicionar_mudanca = st.checkbox("Mudança brusca de amplitude")

        # Parâmetros extras
        if adicionar_ruido:
            snr = st.slider("SNR (dB)", 0, 50, 20, step=1)
            df = adicionarRuido(df, snr)

        if adicionar_tendencia:
            tipo_tend = st.selectbox("Tipo de tendência", ["linear", "quadratica"])
            df = adicionarTendencia(df, tipo_tend)

        if adicionar_descont:
            t_quebra = st.slider("Tempo de descontinuidade (s)", 0.0, float(duracao), 2.0)
            salto = st.slider("Valor do salto", -10.0, 10.0, 2.0)
            df = adicionarDescontinuidade(df, t_quebra, salto)

        if adicionar_mudanca:
            t_mudanca = st.slider("Tempo da mudança (s)", 0.0, float(duracao), 2.0)
            nova_amp = st.slider("Nova amplitude", 0.1, 10.0, 2.0, step=0.1)
            df = adicionarMudancaBrusca(df, t_mudanca, nova_amp)

# Plot
fig = go.Figure()
fig.add_trace(go.Scatter(x=df['t'], y=df['sinal'], mode='lines', name=tipo_sinal))
fig.update_layout(
    xaxis_title="Tempo (s)",
    yaxis_title="Amplitude",
    template="plotly_white"
)
st.plotly_chart(fig, use_container_width=True)

st.subheader("Gramian Angular Field")
fig, axes = plt.subplots (1, 2, figsize =(10, 5))

# Imagem GASF
im = axes[0].imshow(aplicarGAF(df, 'summation'), cmap='rainbow', origin='lower')
axes[0].set_title('Gramian Angular Summation Field')
fig.colorbar(im, ax=axes[0], fraction=0.046, pad=0.04)

# Imagem GADF
im = axes[1].imshow(aplicarGAF(df, 'difference'), cmap='rainbow', origin='lower')
axes[1].set_title('Gramian Angular Difference Field')
fig.colorbar(im, ax=axes[1], fraction=0.046, pad=0.04)

plt.tight_layout()
st.pyplot(fig)
