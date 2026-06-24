from scapy.all import rdpcap, TCP
import sys

def analisar_pcap(arquivo_pcap):
    print(f"Analisando: {arquivo_pcap}\n")
    pacotes = rdpcap(arquivo_pcap)
    
    tempo_anterior = None
    contador = 1

    print("Pacote | Tamanho | Delta T (Segundos)")
    print("-" * 40)

    for pacote in pacotes:
        # Filtra pacotes TCP que contêm payload (geralmente as teclas enviadas)
        # O tamanho do payload no SSH para uma tecla geralmente é bem pequeno e padronizado
        if pacote.haslayer(TCP) and len(pacote[TCP].payload) > 0:
            tempo_atual = pacote.time
            tamanho = len(pacote[TCP].payload)
            
            if tempo_anterior is not None:
                delta_t = tempo_atual - tempo_anterior
                # Filtramos deltas muito grandes para focar na rajada de digitação
                if delta_t < 2.0: 
                    print(f"{contador:02d}     | {tamanho:03d}     | {delta_t:.4f}")
                    contador += 1
            
            tempo_anterior = tempo_atual

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python analyze_timing.py <arquivo.pcap>")
    else:
        analisar_pcap(sys.argv[1])
