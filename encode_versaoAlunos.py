#importe as bibliotecas
import sys
import numpy as np
import sounddevice as sd
from suaBibSignal import signalMeu
import matplotlib.pyplot as plt
import soundfile as sf
from funcoes_LPF import filtro, LPF
from scipy import signal as sg

def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)

#converte intensidade em Db, caso queiram ...
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)

def main():
    print("Inicializando encoder")
    
    #declare um objeto da classe da sua biblioteca de apoio (cedida) 
    s = signalMeu()

    #declare uma variavel com a frequencia de amostragem, sendo 44100
    freq_amostragem = 44100

    audio, sample_rate = sf.read("output.wav")

    maior_0 = max(audio[:,0])
    menor_0 = abs(min(audio[:,0]))
    maior_0_final = max([maior_0, menor_0])

    maior_1 = max(audio[:,1])
    menor_1 = abs(min(audio[:,1]))
    maior_1_final = max([maior_1, menor_1])

    max_freq = max([maior_0_final, maior_1_final])

    novo_audio = audio / max_freq

    plt.figure()
    plt.plot(range(len(novo_audio[:,0])), novo_audio[:,0])
    plt.title("Gráfico 1. Audio normalizado X tempo")
    plt.show()

    audio_filtrado = LPF(novo_audio[:,0], 4000, 44100)

    plt.figure()
    plt.plot(range(len(audio_filtrado)), audio_filtrado)
    plt.title("Gráfico 2. Audio filtrado X tempo")
    plt.show()

    s.plotFFT(audio_filtrado, 44100, "Gráfico 3. audio filtrado X frquencia")
    plt.show()

    audio_portadora = s.generateSin(14000, 1, 5, 44100)[1]

    audio_final = audio_filtrado * audio_portadora

    plt.figure()
    plt.plot(range(len(audio_final)), audio_final)
    plt.title("Gráfico 4. Audio modulado X tempo")
    plt.show()

    s.plotFFT(audio_final, 44100, "Gráfico 5. Audio modulado X frequencia")
    plt.show()

    #sd.play(audio_final, freq_amostragem)
    #sd.wait()

    audio_demodulado = audio_final * audio_portadora

    s.plotFFT(audio_demodulado, 44100, "Gráfico 6. Audio demodulado X frequencia")
    plt.show()

    audio_demodulado_filtrado = LPF(audio_demodulado, 4000, 44100)

    s.plotFFT(audio_demodulado_filtrado, 44100, "Gráfico 7. Audio demodulado e filtrado X frequencia")
    plt.show()

    sd.play(audio_demodulado_filtrado, 44100)
    sd.wait()

    #gere duas senoides para cada frequencia da tabela DTMF ! Canal x e canal y 
    #use para isso sua biblioteca (cedida)
    '''
    sin_audio = s.generateSin(14000, 1, len(audio_filtrado)/44100, 44100)
    
    # Plotando X
    plt.figure(figsize=(8,8))
    plt.grid()
    plt.title("Curva senóide X")
    l = [0, 0.01, -1, 1]
    plt.axis(l)
    plt.plot(sin_x[0], sin_x[1])
    plt.show()

    # Plotando Y
    plt.figure(figsize=(8,8))
    plt.grid()
    plt.title("Curva senóide Y")
    l = [0, 0.01, -1, 1]
    plt.axis(l)
    plt.plot(sin_y[0], sin_y[1])
    plt.show()

    #nao aceite outro valor de entrada.
    print("Gerando Tom referente ao símbolo : {}".format(ton_escolhido))
    
    #construa o sinal a ser reproduzido. nao se esqueca de que é a soma das senoides
    tempo = sin_x[0]
    soma_senoides = sin_x[1] + sin_y[1]

    # Plotando soma
    plt.figure(figsize=(8,8))
    plt.grid()
    plt.title("Soma senóides")
    l = [0, 0.01, -1, 1]
    plt.axis(l)
    plt.plot(tempo, soma_senoides)
    plt.show()
    
    tone = soma_senoides
    # reproduz o som
    sd.play(tone, freq_amostragem)

    # aguarda fim do audio
    sd.wait()
'''
if __name__ == "__main__":
    main()
