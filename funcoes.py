import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import square, sawtooth
import pandas as pd

def gerarSenoide(offset, amp, fs, tf, f):
    t = np.linspace(0, tf, int(fs * tf))
    seno = offset + amp * np.sin(2 * np.pi * f * t)
    df_seno = pd.DataFrame({'t': t, 'sinal': seno})
    return df_seno

def gerarQuadrada(offset, amp, fs, tf, f):
    t = np.linspace(0, tf, int(fs * tf))
    quadrada = offset + amp * square(2 * np.pi * f * t)
    df_quadrada = pd.DataFrame({'t': t, 'sinal': quadrada})
    return df_quadrada

def gerarTriangular(offset, amp, fs, tf, f):
    t = np.linspace(0, tf, int(fs * tf))
    triangular = offset + amp * sawtooth(2 * np.pi * f * t, width=0.5)  # width=0.5 → forma triangular simétrica
    df_triangular = pd.DataFrame({'t': t, 'sinal': triangular})
    return df_triangular

def gerarSinalAleatorio(offset, amp, fs, tf, distribuicao):
    t = np.linspace(0, tf, int(fs * tf))

    if distribuicao == 'normal':
        sinal = np.random.normal(0, 1, size=t.shape)
    elif distribuicao == 'uniforme':
        sinal = np.random.uniform(-1, 1, size=t.shape)
    elif distribuicao == 'binomial':
        sinal = np.random.binomial(n=1, p=0.5, size=t.shape) * 2 - 1  # Resultado: -1 ou +1

    sinal = offset + amp * sinal
    df_sinal_aleatorio = pd.DataFrame({'t': t, 'sinal': sinal})
    return df_sinal_aleatorio

def adicionarRuido (df_sinal, snr_dB):
    t = df_sinal['t']
    sinal = df_sinal['sinal']

    noise_power = np.var(sinal) / (10**(snr_dB / 10))
    ruido = np.random.normal(0, np.sqrt(noise_power), size = sinal.shape)
    
    sinal_com_ruido = sinal + ruido
    df_sinal_com_ruido = pd.DataFrame({'t': t, 'sinal': sinal_com_ruido})
    return df_sinal_com_ruido

def adicionarTendencia (df_sinal, tipo):
    t = df_sinal['t']
    sinal = df_sinal['sinal']

    if tipo == 'linear':
        tendencia = 0.5 * t 
    elif tipo == 'quadratica':
        tendencia = 0.1 * t**2 

    sinal_com_tendencia = sinal + tendencia
    df_com_tendencia = pd.DataFrame({'t': t, 'sinal': sinal_com_tendencia})
    return df_com_tendencia

def adicionarDescontinuidade(df_sinal, t_quebra, valor_salto):
    t = df_sinal['t']
    sinal = df_sinal['sinal'].copy()

    sinal[t >= t_quebra] += valor_salto
    df_descontinuidade = pd.DataFrame({'t': t, 'sinal': sinal})
    return df_descontinuidade

def adicionarMudancaBrusca(df_sinal, t_mudanca, novo_amp):
    t = df_sinal['t']
    sinal = df_sinal['sinal'].copy()

    # Calcula fator de escala para simular nova amplitude
    max_antigo = np.max(np.abs(sinal[t < t_mudanca]))
    fator = novo_amp / max_antigo if max_antigo != 0 else 1

    # Aplica a nova amplitude a partir do tempo t_mudanca
    sinal[t >= t_mudanca] *= fator

    df_mudanca = pd.DataFrame({'t': t, 'sinal': sinal})
    return df_mudanca
