import streamlit as st
import plotly.graph_objects as go
from funcoes import *

st.set_page_config(page_icon='🔊', page_title='Gerador de sinais', layout='wide')
st.title("Gerador de sinais sintéticos")

# Parâmetros comuns
col1, col2, col3 = st.columns(3)
with col1:
    fs = st.number_input("Frequência de amostragem (Hz)", value=1000)
with col2:
    tf = st.number_input("Tempo de duração (s)", value=2.0)
with col3:
    offset = st.number_input("Offset", value=0.0)

# Escolha do tipo de sinal
tipo = st.selectbox("Tipo de sinal", ["Senoide", "Quadrada", "Triangular", "Aleatório"])

amp = st.slider("Amplitude", 0.1, 5.0, 1.0)
f = st.slider("Frequência (Hz)", 1, 50, 5) if tipo != "Aleatório" else None

# Geração do sinal base
if tipo == "Senoide":
    df = gerarSenoide(offset, amp, fs, tf, f)
elif tipo == "Quadrada":
    df = gerarQuadrada(offset, amp, fs, tf, f)
elif tipo == "Triangular":
    df = gerarTriangular(offset, amp, fs, tf, f)
elif tipo == "Aleatório":
    dist = st.selectbox("Distribuição aleatória", ["normal", "uniforme", "binomial"])
    df = gerarSinalAleatorio(offset, amp, fs, tf, dist)

sinais = [("Sinal base", df['t'], df['sinal'])]

# Efeitos adicionais
st.subheader("⚙️ Efeitos adicionais")

col1, col2, col3 = st.columns(3)

with col1:
    aplicar_ruido = st.checkbox("Ruído")
    if aplicar_ruido:
        snr = st.slider("SNR (dB)", 0, 40, 10)
        df_ruido = adicionarRuido(df, snr)
        sinais.append(("Com Ruído", df_ruido['t'], df_ruido['sinal_com_ruido']))

with col2:
    aplicar_tend = st.checkbox("Tendência")
    if aplicar_tend:
        tipo_tend = st.selectbox("Tipo de tendência", ["linear", "quadratica"])
        df_tend = adicionarTendencia(df, tipo_tend)
        sinais.append((f"Tendência {tipo_tend}", df_tend['t'], df_tend[f'sinal_com_tendencia']))

with col3:
    aplicar_mudanca = st.checkbox("Mudança brusca")
    if aplicar_mudanca:
        t_m = st.slider("Tempo da mudança", 0.1, tf, tf/2.0)
        novo_amp = st.slider("Nova amplitude após mudança", 0.1, 5.0, 2.0)
        df_mudanca = adicionarMudancaBrusca(df, t_m, novo_amp)
        sinais.append(("Mudança brusca", df_mudanca['t'], df_mudanca['sinal_com_mudanca']))

# Descontinuidade
aplicar_desc = st.checkbox("Adicionar descontinuidade")
if aplicar_desc:
    t_quebra = st.slider("Tempo da quebra", 0.1, tf, tf/2.0)
    salto = st.slider("Valor do salto", -5.0, 5.0, 1.0)
    df_desc = adicionarDescontinuidade(df, t_quebra, salto)
    sinais.append(("Descontinuidade", df_desc['t'], df_desc['sinal_descont']))

# Plot
st.subheader("📈 Visualização dos sinais")

fig = go.Figure()

for nome, t, y in sinais:
    fig.add_trace(go.Scatter(x=t, y=y, mode='lines', name=nome))

fig.update_layout(
    title="Sinais gerados",
    xaxis_title="Tempo (s)",
    yaxis_title="Amplitude",
    template="plotly_white",
    height=500,
    margin=dict(l=40, r=40, t=60, b=40)
)

st.plotly_chart(fig, use_container_width=True)

# Exportação
st.subheader("💾 Exportar sinal base")
csv = df.to_csv(index=False).encode('utf-8')
st.download_button("Baixar CSV do sinal base", data=csv, file_name="sinal_base.csv", mime="text/csv")
