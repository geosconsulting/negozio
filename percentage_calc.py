def calcola_incremento_percentuale(valore_iniziale, valore_finale):
    """
    Calcola l'incremento percentuale tra due valori.
    
    Args:
        valore_iniziale: Il valore di partenza
        valore_finale: Il valore di arrivo
    
    Returns:
        float: L'incremento percentuale
    """
    if valore_iniziale == 0:
        raise ValueError("Il valore iniziale non può essere zero")
    
    differenza = valore_finale - valore_iniziale
    incremento_percentuale = (differenza / valore_iniziale) * 100
    
    return incremento_percentuale


# Esempio di utilizzo
valore_iniziale = 14.44
valore_finale = 14.94

incremento = calcola_incremento_percentuale(valore_iniziale, valore_finale)

print(f"Valore iniziale: {valore_iniziale}")
print(f"Valore finale: {valore_finale}")
print(f"Differenza: {valore_finale - valore_iniziale:.2f}")
print(f"Incremento percentuale: {incremento:.2f}%")

# Caso con decremento
print("\n--- Esempio con decremento ---")
valore_iniziale2 = 20.00
valore_finale2 = 18.50

incremento2 = calcola_incremento_percentuale(valore_iniziale2, valore_finale2)
print(f"Da {valore_iniziale2} a {valore_finale2}: {incremento2:.2f}%")

# Versione interattiva con loop continuo
print("\n--- Calcolo personalizzato (continuo) ---")
print("Digita 'esci' o 'quit' in qualsiasi momento per terminare\n")

while True:
    try:
        # Input valore iniziale
        val_iniz_input = input("Inserisci il valore iniziale: ").strip().lower()
        if val_iniz_input in ['esci', 'quit', 'exit', 'q']:
            print("Arrivederci!")
            break
        
        val_iniz = float(val_iniz_input)
        
        # Input valore finale
        val_fin_input = input("Inserisci il valore finale: ").strip().lower()
        if val_fin_input in ['esci', 'quit', 'exit', 'q']:
            print("Arrivederci!")
            break
        
        val_fin = float(val_fin_input)
        
        # Calcolo
        risultato = calcola_incremento_percentuale(val_iniz, val_fin)
        differenza = val_fin - val_iniz
        
        print(f"\n{'='*50}")
        print(f"Valore iniziale: {val_iniz}")
        print(f"Valore finale: {val_fin}")
        print(f"Differenza assoluta: {differenza:+.2f}")
        
        if risultato > 0:
            print(f"✓ Incremento del {risultato:.2f}%")
        elif risultato < 0:
            print(f"✓ Decremento del {abs(risultato):.2f}%")
        else:
            print("✓ Nessuna variazione (0%)")
        
        print(f"{'='*50}\n")
        
    except ValueError as e:
        if "could not convert" in str(e):
            print("⚠ Errore: Inserisci un numero valido\n")
        else:
            print(f"⚠ Errore: {e}\n")
    except Exception as e:
        print(f"⚠ Errore imprevisto: {e}\n")