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
        signal = np.random.normal(0, 1, size=t.shape) # Mean = 0 and Standard Deviation = 1
    elif distribution == 'uniform':
        signal = np.random.uniform(-1, 1, size=t.shape) # Values are uniformly distributed between -1 and 1, 
                                                        # meaning every number in this interval has the same probability of being chosen
    elif distribution == 'binomial':        
        signal = np.random.binomial(n=1, p=0.5, size=t.shape) * 2 - 1   # n=1 means one trial per example
                                                                        # p=0.5 means a 50% chance of getting a 1 (success)
                                                                        # The result is then transformed to -1 or 1 by (0 or 1)*2-1
    signal = offset + amp * signal
    df_signal_aleatorio = pd.DataFrame({'t': t, 'signal': signal})
    return df_signal_aleatorio

def addNoise (df_signal, snr_dB):
    t = df_signal['t']
    signal = df_signal['signal']

    # Calculate the noise power needed to achieve the desired Signal-to-Noise Ratio (SNR)
    # SNR (in linear scale) = signal_power / noise_power
    # signal_power is estimated using the variance of the signal
    # Rearranged to: noise_power = signal_power / SNR
    # Since SNR is given in dB, convert it to linear scale using 10^(SNR_dB / 10)
    noise_power = np.var(signal) / (10**(snr_dB / 10))

    noise = np.random.normal(0, np.sqrt(noise_power), size=signal.shape) # White Gaussian noise (Mean = 0, Standard Deviation = sqrt(noise_power))
                                                                         # This gives noise with the power that matches the desired SNR
    signal_with_noise = signal + noise
    df_signal_with_noise = pd.DataFrame({'t': t, 'signal': signal_with_noise}) 
    return df_signal_with_noise

def addTrend (df_signal, tipo):
    t = df_signal['t']
    signal = df_signal['signal']

    if tipo == 'linear':
        tendencia = 1 * t 
    elif tipo == 'quadractic':
        tendencia = 0.5 * t**2 

    signal_with_tendencia = signal + tendencia
    df_with_tendencia = pd.DataFrame({'t': t, 'signal': signal_with_tendencia})
    return df_with_tendencia

def addDiscontinuity(df_signal, t_jump, jump_value):
    t = df_signal['t']
    signal = df_signal['signal'].copy()

    # Adds a jump (discontinuity) in the signal from time t_jump onward
    signal[t >= t_jump] += jump_value
    df_discontinuity = pd.DataFrame({'t': t, 'signal': signal})
    return df_discontinuity

def addSuddenChange(df_signal, t_change, new_amp):
    t = df_signal['t']
    signal = df_signal['signal'].copy()

    # Calculates the amplitude before the change, to scale the rest of the signal
    old_max = np.max(np.abs(signal[t < t_change]))
    factor = new_amp / old_max if old_max != 0 else 1

    # Applies the scaling factor to the signal from t_change onward
    signal[t >= t_change] *= factor

    df_mudanca = pd.DataFrame({'t': t, 'signal': signal})
    return df_mudanca

def applyGAF(df, chosen_method='summation'):
    signal = df['signal']
    
    # Reshapes the signal to the format expected by the GAF transformer (1 sample, many time points)
    X = np.array(signal).reshape(1, -1) 

    gaf = GramianAngularField(method=chosen_method)
    X_gaf = gaf.fit_transform(X)
    return X_gaf[0] 
