def calcola_prezzo_vendita(costo_netto, margine_percent, iva_percent):
    """
    Da costo e margine, calcola PV netto/lordo (originale).
    """
    margine_dec = margine_percent / 100
    pv_netto = costo_netto / (1 - margine_dec)
    pv_lordo = pv_netto * (1 + iva_percent / 100)
    iva_amount = pv_lordo - pv_netto
    return {
        'prezzo_vendita_netto': round(pv_netto, 2),
        'prezzo_vendita_lordo': round(pv_lordo, 2),
        'iva_amount': round(iva_amount, 2),
        'margine_percentuale': round(margine_percent, 2)
    }

def calcola_margine(costo_netto, pv_netto, iva_percent):
    """
    Da prezzi netti, calcola margine % e dettagli.
    """
    margine = (pv_netto - costo_netto) / pv_netto * 100
    pv_lordo = pv_netto * (1 + iva_percent / 100)
    iva_amount = pv_lordo - pv_netto
    profitto_assoluto = pv_netto - costo_netto
    return {
        'margine_percentuale': round(margine, 2),
        'prezzo_vendita_lordo': round(pv_lordo, 2),
        'iva_amount': round(iva_amount, 2),
        'profitto_assoluto': round(profitto_assoluto, 2)
    }

def calcola_da_lordo(pv_lordo, iva_percent):
    """Scorporo IVA da PV_lordo."""
    return round(pv_lordo / (1 + iva_percent / 100), 2)

def markup_da_margine(margine_percent):
    """Markup equivalente."""
    return round((margine_percent / (100 - margine_percent)) * 100, 2)

def rotazione(vendite_annue, stock_medio):
    """Rotazione merci."""
    return round(vendite_annue / stock_medio, 1)

# LOOP PRINCIPALE con uscita
print("=== CALCOLATORE MARGINI PER CAFFÈ E CAPSULE ===")
print("Target: 33-40% su PV netto. IVA caffè 22%, solubili 10%.\n")

while True:
    tipo = input("Tipo prodotto (1: Caffè 22%, 2: Non caffè 10%, 0: Esci): ").strip()
    if tipo == '0':
        print("Arrivederci!")
        break
    iva = 22 if tipo == '1' else 10
    print(f"IVA: {iva}% selezionata.")
    
    while True:  # Sottomenu calcoli
        scelta = input("\nCalcolo (1:Margine da prezzi, 2:PV da margine, 3:Scorporo IVA, 4:Markup, 5:Rotazione, 0:Menu tipo): ").strip()
        if scelta == '0':
            break  # Torna a selezione tipo
        elif scelta == '1':
            costo = float(input("  Costo netto fornitore (€/unità): "))
            pv_net = float(input("  PV netto proposto (€/unità): "))
            print("Risultati:", calcola_margine(costo, pv_net, iva))
        elif scelta == '2':
            costo = float(input("  Costo netto fornitore (€/unità): "))
            margine = float(input("  Margine desiderato % (33-40): "))
            print("Prezzi suggeriti:", calcola_prezzo_vendita(costo, margine, iva))
        elif scelta == '3':
            pv_lordo = float(input("  PV lordo cliente (€/unità): "))
            print("PV netto:", calcola_da_lordo(pv_lordo, iva), "€")
        elif scelta == '4':
            margine = float(input("  Margine % desiderato: "))
            print("Markup sul costo:", markup_da_margine(margine), "%")
        elif scelta == '5':
            vend = float(input("  Vendite annue (unità): "))
            stock = float(input("  Stock medio (unità): "))
            print("Rotazione:", f"{rotazione(vend, stock)}x/anno")
        else:
            print("Opzione non valida.")

print("Sessione chiusa.")
