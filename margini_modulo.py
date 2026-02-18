# margini_modulo.py

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
