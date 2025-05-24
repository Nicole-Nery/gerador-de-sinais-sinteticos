import streamlit as st
import plotly.graph_objects as go
from funcoes import *

st.set_page_config('Gerador de Sinais', layout='wide')
st.title("Gerador de Sinais Sintéticos")

st.sidebar.header("Configuração do sinal")
tipo_sinal = st.sidebar.selectbox("Tipo de sinal", ["Senoidal", "Quadrada", "Triangular", "Aleatório"])

# Parâmetros comuns
offset = st.sidebar.slider("Offset", -10.0, 10.0, 0.0, step=0.5)
amplitude = st.sidebar.slider("Amplitude", 0.1, 10.0, 1.0, step=0.1)
frequencia = st.sidebar.slider("Frequência (Hz)", 0.1, 50.0, 1.0, step=0.1)
fs = st.sidebar.slider("Frequência de amostragem (Hz)", 10, 1000, 100, step=1)
duracao = st.sidebar.slider("Duração do sinal (s)", 1, 10, 5, step=1)

# Geração do sinal base
if tipo_sinal == "Senoidal":
    df = gerarSenoide(offset, amplitude, fs, duracao, frequencia)
elif tipo_sinal == "Quadrada":
    df = gerarQuadrada(offset, amplitude, fs, duracao, frequencia)
elif tipo_sinal == "Triangular":
    df = gerarTriangular(offset, amplitude, fs, duracao, frequencia)
elif tipo_sinal == "Aleatório":
    distribuicao = st.sidebar.selectbox("Distribuição", ["normal", "uniforme", "binomial"])
    df = gerarSinalAleatorio(offset, amplitude, fs, duracao, distribuicao)

# Efeitos adicionais
st.sidebar.subheader("Efeitos adicionais")
adicionar_ruido = st.sidebar.checkbox("Ruído")
adicionar_tendencia = st.sidebar.checkbox("Tendência")
adicionar_descont = st.sidebar.checkbox("Descontinuidade")
adicionar_mudanca = st.sidebar.checkbox("Mudança brusca de amplitude")

# Parâmetros extras
if adicionar_ruido:
    snr = st.sidebar.slider("SNR (dB)", 0, 50, 20, step=1)
    df = adicionarRuido(df, snr)

if adicionar_tendencia:
    tipo_tend = st.sidebar.selectbox("Tipo de tendência", ["linear", "quadratica"])
    df = adicionarTendencia(df, tipo_tend)

if adicionar_descont:
    t_quebra = st.sidebar.slider("Tempo de descontinuidade (s)", 0.0, float(duracao), 2.0)
    salto = st.sidebar.slider("Valor do salto", -10.0, 10.0, 2.0)
    df = adicionarDescontinuidade(df, t_quebra, salto)

if adicionar_mudanca:
    t_mudanca = st.sidebar.slider("Tempo da mudança (s)", 0.0, float(duracao), 2.0)
    nova_amp = st.sidebar.slider("Nova amplitude", 0.1, 10.0, 2.0, step=0.1)
    df = adicionarMudancaBrusca(df, t_mudanca, nova_amp)

# Plot
fig = go.Figure()
fig.add_trace(go.Scatter(x=df['t'], y=df['sinal'], mode='lines', name=tipo_sinal))
fig.update_layout(
    title="Sinal gerado",
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
