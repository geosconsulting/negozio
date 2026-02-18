#!/usr/bin/env python3
"""
Calcolatore IVA e Margini di Guadagno
Utilizza Click per interfaccia a riga di comando interattiva
"""

import click
from typing import List


from margini_modulo_wrong import calcola_prezzo_finale


def stampa_risultato(risultato: dict):
    """Stampa i risultati del calcolo in formato leggibile"""
    if risultato['numero_componenti'] > 1:
        # Mostra calcolo per lotti
        click.echo(f"\n{'='*60}")
        click.echo(f"💼 LOTTO ({risultato['numero_componenti']} componenti)")
        click.echo(f"Costo totale lotto:    €{risultato['prezzo_totale']:>10.2f}")
        click.echo(f"Costo unitario:        €{risultato['prezzo_unitario']:>10.2f}")
        click.echo(f"{'='*60}")
        click.echo(f"📦 CALCOLO UNITARIO")
        click.echo(f"Prezzo unitario:       €{risultato['prezzo_unitario']:>10.2f}")
        click.echo(f"IVA ({risultato['iva_percentuale']:>2.0f}%):             €{risultato['importo_iva_unitario']:>10.2f}")
        click.echo(f"Prezzo con IVA:        €{risultato['prezzo_unitario_con_iva']:>10.2f}")
        click.echo(f"Margine ({risultato['margine_percentuale']:>2.0f}%):          €{risultato['importo_margine_unitario']:>10.2f}")
        click.echo(f"{'='*60}")
        click.echo(f"💰 PREZZO FINALE UNITARIO: €{risultato['prezzo_finale_unitario']:>10.2f}")
        click.echo(f"{'='*60}")
        click.echo(f"🔢 TOTALI LOTTO COMPLETO")
        click.echo(f"Ricavo totale:         €{risultato['totale_finale']:>10.2f}")
        click.echo(f"Guadagno totale:       €{risultato['totale_finale'] - risultato['totale_con_iva']:>10.2f}")
        click.echo(f"{'='*60}")
    else:
        # Mostra calcolo singolo (compatibilità con versione precedente)
        click.echo(f"\n{'='*50}")
        click.echo(f"Prezzo base:        €{risultato['prezzo_unitario']:>10.2f}")
        click.echo(f"IVA ({risultato['iva_percentuale']:>2.0f}%):          €{risultato['importo_iva_unitario']:>10.2f}")
        click.echo(f"Prezzo con IVA:     €{risultato['prezzo_unitario_con_iva']:>10.2f}")
        click.echo(f"Margine ({risultato['margine_percentuale']:>2.0f}%):       €{risultato['importo_margine_unitario']:>10.2f}")
        click.echo(f"{'='*50}")
        click.echo(f"PREZZO FINALE:      €{risultato['prezzo_finale_unitario']:>10.2f}")
        click.echo(f"{'='*50}")


def elabora_margini(prezzo_totale: float, componenti: int, iva: float, margini: List[float]):
    """Elabora lo stesso prezzo con diversi margini e stampa i risultati"""
    if componenti > 1:
        prezzo_unitario = prezzo_totale / componenti
        click.echo(f"\n🧮 Elaborando lotto €{prezzo_totale:.2f} ({componenti} pz, €{prezzo_unitario:.2f}/pz) con IVA {iva}% e {len(margini)} margini diversi")
    else:
        click.echo(f"\n🧮 Elaborando prezzo €{prezzo_totale:.2f} con IVA {iva}% e {len(margini)} margini diversi")
    
    risultati = []
    
    for i, margine in enumerate(margini, 1):
        click.echo(f"\n--- Margine {i}: {margine}% ---")
        risultato = calcola_prezzo_finale(prezzo_totale, componenti, iva, margine)
        stampa_risultato(risultato)
        risultati.append(risultato)
    
    # Tabella comparativa se ci sono più margini
    if len(margini) > 1:
        if componenti > 1:
            click.echo(f"\n{'📊 CONFRONTO MARGINI (UNITARIO) 📊':=^80}")
            #click.echo(f"{'Margine':<10} {'Prezzo unitario':<15} {'Guadagno unit.':<15} {'Ricavo totale':<15} {'Diff.'}")
            #click.echo("=" * 80)
            click.echo(f"{'Margine':<10} {'Prezzo unitario':<15} {'Guadagno unit.':<15} {'Guadagno totale':<17} {'Ricavo totale':<15} {'Diff.'}")
            click.echo("=" * 80)
            
            primo_prezzo = risultati[0]['prezzo_finale_unitario']
            
            for risultato in risultati:
                margine = risultato['margine_percentuale']
                prezzo_unitario = risultato['prezzo_finale_unitario']
                guadagno_unitario = prezzo_unitario - risultato['prezzo_unitario_con_iva']
                guadagno_totale = guadagno_unitario * risultato['numero_componenti']
                ricavo_totale = risultato['totale_finale']                
                diff_primo = prezzo_unitario - primo_prezzo
                
                #click.echo(f"{margine:>6.0f}%    €{prezzo_unitario:>10.2f}     €{guadagno_unitario:>10.2f}      €{ricavo_totale:>10.2f}     {diff_primo:+.2f}€")
                click.echo(f"{margine:>6.0f}%    €{prezzo_unitario:>10.2f}     €{guadagno_unitario:>10.2f}      €{guadagno_totale:>12.2f}      €{ricavo_totale:>10.2f}     {diff_primo:+.2f}€")
        else:
            click.echo(f"\n{'📊 CONFRONTO MARGINI 📊':=^70}")
            click.echo(f"{'Margine':<10} {'Prezzo finale':<15} {'Guadagno totale':<15} {'Diff. dal primo'}")
            click.echo("=" * 70)
            
            primo_prezzo = risultati[0]['prezzo_finale_unitario']
            
            for risultato in risultati:
                margine = risultato['margine_percentuale']
                prezzo_finale = risultato['prezzo_finale_unitario']
                guadagno_totale = prezzo_finale - risultato['prezzo_unitario_con_iva']
                diff_primo = prezzo_finale - primo_prezzo
                
                click.echo(f"{margine:>6.0f}%    €{prezzo_finale:>10.2f}     €{guadagno_totale:>10.2f}      {diff_primo:+.2f}€")
        
        click.echo("=" * 80 if componenti > 1 else "=" * 70)


def valida_iva(iva: float) -> bool:
    """Valida che l'IVA sia 10 o 22 percento"""
    return iva in [10.0, 22.0]


def parse_margini(input_margini: str) -> List[float]:
    """
    Converte l'input dell'utente in una lista di margini
    Supporta sia singoli valori che liste separate da virgola
    """
    try:
        # Rimuove spazi e divide per virgola
        margini_str = [m.strip() for m in input_margini.split(',')]
        margini = [float(m) for m in margini_str if m]
        
        # Verifica che tutti i margini siano positivi
        if not all(m >= 0 for m in margini):
            raise ValueError("Tutti i margini devono essere maggiori o uguali a 0")
        
        # Avviso per margini molto alti
        if any(m > 90 for m in margini):
            if not click.confirm(f"⚠️  Alcuni margini sono molto alti (>90%). Continuare?"):
                raise click.Abort()
            
        return margini
    except ValueError as e:
        raise click.BadParameter(f"Errore nei margini inseriti: {e}")


@click.command()
@click.option('--debug', is_flag=True, help='Abilita modalità debug')
def main(debug):
    """
    🧮 Calcolatore IVA e Margini di Guadagno
    
    Calcola prezzi finali applicando IVA (10% o 22%) e uno o più margini di guadagno.
    Supporta il calcolo per lotti con più componenti (es. 54€ per 6 pacchi di caffè).
    Permette di confrontare lo stesso prezzo con margini diversi.
    """
    click.echo("🧮 Benvenuto nel Calcolatore IVA e Margini!")
    click.echo("=" * 50)
    
    while True:
        try:
            # Input prezzo totale
            prezzo_totale = click.prompt(
                "💰 Prezzo totale del lotto (€)", 
                type=click.FloatRange(min=0.01),
                show_default=False
            )

            # Input sconto opzionale
            sconto = click.prompt(
                    "💸 Sconto sul prezzo totale (%) [premi invio per nessuno]",
                    type=click.FloatRange(min=0, max=100),
                    default=0.0,
                    show_default=True
                )
            if sconto > 0:
                prezzo_totale = prezzo_totale * (1 - sconto / 100)
                click.echo(f"   → Prezzo totale scontato: €{prezzo_totale:.2f} (-{sconto:.1f}%)")
            
            # Input numero componenti
            componenti = click.prompt(
                "📦 Numero di componenti nel lotto",
                type=click.IntRange(min=1),
                default=1,
                show_default=True
            )
            
            # Mostra prezzo unitario se ci sono più componenti
            if componenti > 1:
                prezzo_unitario = prezzo_totale / componenti
                click.echo(f"   → Prezzo unitario: €{prezzo_unitario:.2f}")
            
            if debug:
                click.echo(f"Debug: Prezzo totale: €{prezzo_totale:.2f}, Componenti: {componenti}")
            
            # Input IVA
            iva = click.prompt(
                "📋 Percentuale IVA", 
                type=click.Choice(['10', '22']),
                default='22',
                show_choices=True
            )
            iva = float(iva)
            
            # Input margini
            click.echo("\n📈 Inserisci i margini di guadagno:")
            click.echo("• Un singolo margine: es. 25")
            click.echo("• Più margini separati da virgola: es. 33, 35, 38")
            
            # input_margini = click.prompt("Margini (%)", type=str)
            # margini = parse_margini(input_margini)
            default_margini = "33, 35, 38"
            input_margini = click.prompt(
                "Margini (%)",
                type=str,
                default=default_margini,
                show_default=True
            )
            margini = parse_margini(input_margini)
            if not margini:
                raise click.BadParameter("Devi inserire almeno un margine di guadagno")
            click.echo(f"Margini inseriti: {', '.join(map(str, margini))}%")            
            if debug:
                click.echo(f"Debug: Margini parsati: {margini}")
            
            # Elaborazione
            elabora_margini(prezzo_totale, componenti, iva, margini)
            
            # Continuare?
            click.echo("\n" + "="*50)
            continua = click.confirm("Vuoi effettuare un altro calcolo?", default=True)
            
            if not continua:
                click.echo("\n👋 Grazie per aver usato il calcolatore!")
                break
                
        except click.Abort:
            click.echo("\n\n👋 Operazione annullata. Arrivederci!")
            break
        except Exception as e:
            click.echo(f"\n❌ Errore: {e}", err=True)
            if debug:
                import traceback
                click.echo(traceback.format_exc(), err=True)
            
            continua = click.confirm("\nVuoi riprovare?", default=True)
            if not continua:
                break


if __name__ == '__main__':
    main()