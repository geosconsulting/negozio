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

def calcola_prezzo_finale(prezzo_totale: float, numero_componenti: int,
                          iva_percentuale: float,
                          margine_percentuale: float) -> dict:
    """
    Calcola il prezzo finale con IVA e margine di guadagno
    
    Args:
        prezzo_totale: Prezzo totale del lotto in euro
        numero_componenti: Numero di componenti nel lotto
        iva_percentuale: Percentuale IVA (10 o 22)
        margine_percentuale: Percentuale margine di guadagno
    
    Returns:
        Dizionario con tutti i calcoli
    """
    # Calcola prezzo unitario
    prezzo_unitario = prezzo_totale / numero_componenti
    
    # Calcola IVA sul prezzo unitario
    importo_iva_unitario = prezzo_unitario * (iva_percentuale / 100)
    prezzo_unitario_con_iva = prezzo_unitario + importo_iva_unitario
    
    # Calcola margine sul prezzo unitario con IVA
    importo_margine_unitario = prezzo_unitario_con_iva * (margine_percentuale / 100)
    prezzo_finale_unitario = prezzo_unitario_con_iva + importo_margine_unitario
    
    return {
        'prezzo_totale': prezzo_totale,
        'numero_componenti': numero_componenti,
        'prezzo_unitario': prezzo_unitario,
        'iva_percentuale': iva_percentuale,
        'importo_iva_unitario': importo_iva_unitario,
        'prezzo_unitario_con_iva': prezzo_unitario_con_iva,
        'margine_percentuale': margine_percentuale,
        'importo_margine_unitario': importo_margine_unitario,
        'prezzo_finale_unitario': prezzo_finale_unitario,
        # Totali per l'intero lotto
        'totale_iva': importo_iva_unitario * numero_componenti,
        'totale_con_iva': prezzo_unitario_con_iva * numero_componenti,
        'totale_margine': importo_margine_unitario * numero_componenti,
        'totale_finale': prezzo_finale_unitario * numero_componenti
    }

def calcola_elasticita(p_old, q_old, p_new, q_new):
    """
    Calcola l'elasticità della domanda al prezzo.
    Formula: (ΔQ / Q_mid) / (ΔP / P_mid)
    """
    if p_old == p_new or q_old == q_new:
        return 0.0
    
    delta_q = q_new - q_old
    q_mid = (q_new + q_old) / 2
    pct_delta_q = delta_q / q_mid
    
    delta_p = p_new - p_old
    p_mid = (p_new + p_old) / 2
    pct_delta_p = delta_p / p_mid
    
    return round(pct_delta_q / pct_delta_p, 2)

def stima_domanda_lineare(p_old, q_old, p_new, q_new):
    """
    Stima la curva di domanda Q = a - bP
    Returns: (a, b)
    """
    if p_new == p_old:
        raise ValueError("I prezzi devono essere diversi per stimare la domanda")
        
    b = (q_new - q_old) / (p_new - p_old) # Slope (negative for normal goods)
    a = q_old - b * p_old                 # Intercept
    
    return a, b

def ottimizza_prezzo(costo, p_old, q_old, p_new, q_new):
    """
    Calcola il prezzo ottimale per massimizzare il profitto.
    Profitto = (P - Costo) * (a - bP)
    Derivata = a + b*Costo - 2bP = 0
    P_opt = (a + b*Costo) / 2b
    """
    try:
        a, b = stima_domanda_lineare(p_old, q_old, p_new, q_new)
        
        # Il valore di b calcolato è la pendenza (negativa per beni normali)
        # Q = a + bP  (dove b < 0)
        # Profitto = (P - C) * (a + bP) = aP + bP^2 - aC - bPC
        # dProfitto/dP = a + 2bP - bC = 0
        # 2bP = bC - a
        # P = (bC - a) / 2b = C/2 - a/2b
        
        # Esempio test: P=100 Q=100, P=110 Q=80
        # b = -20/10 = -2
        # a = 100 - (-2)*100 = 300
        # Q = 300 - 2P
        # Costo = 50
        # P_opt = (-2*50 - 300) / (2*-2) = (-100 - 300) / -4 = -400 / -4 = 100
        
        p_opt = (b * costo - a) / (2 * b)
        
        # Calcolo proiezioni
        q_opt = a + b * p_opt
        profitto_opt = (p_opt - costo) * q_opt
        ricavo_opt = p_opt * q_opt
        
        elasticita = calcola_elasticita(p_old, q_old, p_new, q_new)
        
        return {
            'prezzo_ottimale': round(p_opt, 2),
            'quantita_stimata': round(q_opt, 1),
            'profitto_stimato': round(profitto_opt, 2),
            'ricavo_stimato': round(ricavo_opt, 2),
            'elasticita': elasticita,
            'domanda_a': round(a, 2),
            'domanda_b': round(b, 2)
        }
    except ValueError as e:
        return {'error': str(e)}
