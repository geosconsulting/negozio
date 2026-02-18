import os

def leggi_file_acquisto(nome_file):
    dati = []
    totale_scatole = 0
    totale_spesa = 0.0
    
    with open(nome_file, 'r', encoding='utf-8') as f:
        for riga in f:
            riga = riga.strip()
            if not riga: # Salta le righe vuote
                continue
                
            parti = riga.split()
            if len(parti) >= 3:
                try:
                    miscela = parti[0]
                    scatole = int(parti[1])
                    # Rimuove € e converte virgola in punto
                    prezzo_pulito = parti[2].replace('€', '').replace(',', '.').strip()
                    prezzo_totale = float(prezzo_pulito)
                    
                    dati.append({
                        "miscela": miscela,
                        "scatole": scatole,
                        "prezzo_totale": prezzo_totale
                    })
                    totale_scatole += scatole
                    totale_spesa += prezzo_totale
                except ValueError:
                    print(f"Attenzione: Riga ignorata in {nome_file} (formato errato): {riga}")
                    continue
                
    return dati, totale_scatole, totale_spesa

def leggi_file_sconto(nome_file):
    sconto_totale = 0.0
    with open(nome_file, 'r', encoding='utf-8') as f:
        for riga in f:
            riga = riga.strip()
            if not riga:
                continue
                
            parti = riga.split()
            if len(parti) >= 2:
                try:
                    valore_pulito = parti[1].replace('€', '').replace(',', '.').strip()
                    sconto_totale += float(valore_pulito)
                except ValueError:
                    print(f"Attenzione: Riga ignorata in {nome_file}: {riga}")
                    continue
    return sconto_totale

# Configurazione File
file_acquisto = 'acquisto.txt'
file_sconto = 'sconto.txt'

try:
    lista_miscele, tot_scatole, tot_spesa = leggi_file_acquisto(file_acquisto)
    valore_sconto_totale = leggi_file_sconto(file_sconto)

    # Verifica se sono stati caricati dati per evitare la divisione per zero
    if tot_spesa == 0:
        print("Errore: La spesa totale è zero. Verifica che 'acquisto.txt' contenga i dati correttamente.")
    else:
        rapporto_sconto = valore_sconto_totale / tot_spesa

        print(f"--- RIEPILOGO CARICAMENTO ---")
        print(f"Totale Scatole caricate: {tot_scatole}")
        print(f"Spesa Totale calcolata: {tot_spesa:.2f} €")
        print(f"Sconto Totale calcolato: {valore_sconto_totale:.2f} €")
        print(f"Percentuale Sconto: {rapporto_sconto * 100:.2f}%\n")

        header = f"{'Miscela':<10} | {'Scatole':<8} | {'P. Lordo/Scat':<15} | {'Sconto Pro-Rata':<15} | {'P. Netto/Scat':<15}"
        print(header)
        print("-" * len(header))

        for m in lista_miscele:
            p_lordo_unit = m['prezzo_totale'] / m['scatole']
            sconto_su_miscela = m['prezzo_totale'] * rapporto_sconto
            p_netto_unit = (m['prezzo_totale'] - sconto_su_miscela) / m['scatole']
            
            print(f"{m['miscela'].capitalize():<10} | {m['scatole']:<8} | {p_lordo_unit:>12.2f} € | {sconto_su_miscela:>12.2f} € | {p_netto_unit:>12.2f} €")

except FileNotFoundError:
    print(f"Errore: File non trovati. Assicurati che siano in: {os.getcwd()}")
except Exception as e:
    print(f"Si è verificato un errore: {e}")