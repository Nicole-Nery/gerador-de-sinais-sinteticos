import numpy as np
from scipy.signal import square, sawtooth
import pandas as pd
from pyts.image import GramianAngularField

def generateSine(offset, amp, fs, tf, f):
    t = np.linspace(0, tf, int(fs * tf))
    sine = offset + amp * np.sin(2 * np.pi * f * t)
    df_sine = pd.DataFrame({'t': t, 'signal': sine})
    return df_sine

def generateSquare(offset, amp, fs, tf, f):
    t = np.linspace(0, tf, int(fs * tf))
    square_wave = offset + amp * square(2 * np.pi * f * t)
    df_square = pd.DataFrame({'t': t, 'signal': square_wave})
    return df_square

def generateTriangle(offset, amp, fs, tf, f):
    t = np.linspace(0, tf, int(fs * tf))
    triangular = offset + amp * sawtooth(2 * np.pi * f * t, width=0.5) 
    df_triangular = pd.DataFrame({'t': t, 'signal': triangular})
    return df_triangular

def generateRandomSignal(offset, amp, fs, tf, distribution):
    t = np.linspace(0, tf, int(fs * tf))

    if distribution == 'normal':
        signal = np.random.normal(0, 1, size=t.shape)
    elif distribution == 'uniform':
        signal = np.random.uniform(-1, 1, size=t.shape)
    elif distribution == 'binomial':
        signal = np.random.binomial(n=1, p=0.5, size=t.shape) * 2 - 1  

    signal = offset + amp * signal
    df_signal_aleatorio = pd.DataFrame({'t': t, 'signal': signal})
    return df_signal_aleatorio

def addNoise (df_signal, snr_dB):
    t = df_signal['t']
    signal = df_signal['signal']

    noise_power = np.var(signal) / (10**(snr_dB / 10))
    noise = np.random.normal(0, np.sqrt(noise_power), size = signal.shape)
    
    signal_com_noise = signal + noise
    df_signal_com_noise = pd.DataFrame({'t': t, 'signal': signal_com_noise})
    return df_signal_com_noise

def addTrend (df_signal, tipo):
    t = df_signal['t']
    signal = df_signal['signal']

    if tipo == 'linear':
        tendencia = 0.5 * t 
    elif tipo == 'quadractic':
        tendencia = 0.1 * t**2 

    signal_com_tendencia = signal + tendencia
    df_com_tendencia = pd.DataFrame({'t': t, 'signal': signal_com_tendencia})
    return df_com_tendencia

def addDiscontinuity(df_signal, t_quebra, valor_salto):
    t = df_signal['t']
    signal = df_signal['signal'].copy()

    signal[t >= t_quebra] += valor_salto
    df_discontinuity = pd.DataFrame({'t': t, 'signal': signal})
    return df_discontinuity

def addSuddenChange(df_signal, t_change, new_amp):
    t = df_signal['t']
    signal = df_signal['signal'].copy()

    old_max = np.max(np.abs(signal[t < t_change]))
    factor = new_amp / old_max if old_max != 0 else 1

    signal[t >= t_change] *= factor

    df_mudanca = pd.DataFrame({'t': t, 'signal': signal})
    return df_mudanca

def applyGAF(df, chosen_method='summation'):
    signal = df['signal']
    
    X = np.array(signal).reshape(1, -1) 

    gaf = GramianAngularField(method=chosen_method)
    X_gaf = gaf.fit_transform(X)
    return X_gaf[0] 
