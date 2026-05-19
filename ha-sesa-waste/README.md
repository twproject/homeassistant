# SESA Raccolta Rifiuti per Home Assistant

Integrazione custom per Home Assistant che legge il calendario raccolta rifiuti direttamente da `app.sesaeste.it` e lo integra nel calendario di Home Assistant.

## Funzioni

* Configurazione completamente da UI
* Caricamento live di:

  * Comuni
  * Vie/indirizzi
* Entità calendario Home Assistant native
* Sensori dedicati:

  * Raccolta oggi
  * Raccolta domani
* Download del calendario annuale completo
* Nessun polling continuo verso SESA
* Refresh manuale tramite service
* Supporto HACS (Custom Repository)
* Options Flow per cambiare Comune/Via senza reinstallare l'integrazione

---

# Screenshot

## Dashboard

* Sensori raccolta oggi/domani
* Calendario rifiuti integrato

## Calendario Home Assistant

Visualizzazione completa del calendario annuale direttamente nella vista calendario di Home Assistant.

---

# Installazione

## Metodo manuale

1. Scaricare la release
2. Estrarre la cartella:

```text
custom_components/sesa_waste
```

3. Copiarla dentro:

```text
/config/custom_components/
```

4. Riavviare Home Assistant

5. Aggiungere l'integrazione:

```text
Impostazioni → Dispositivi e Servizi → Aggiungi integrazione
```

6. Cercare:

```text
SESA Raccolta Rifiuti
```

---

## Installazione HACS

1. HACS → Integrations
2. Menu ⋮ → Custom repositories
3. Inserire:

```text
https://github.com/<TUO-USERNAME>/ha-sesa-waste
```

4. Categoria:

```text
Integration
```

5. Installare l'integrazione
6. Riavviare Home Assistant

---

# Entità create

## Sensori

### Raccolta oggi

```text
sensor.sesa_raccolta_oggi
```

Mostra il tipo di raccolta previsto per oggi.

---

### Raccolta domani

```text
sensor.sesa_raccolta_domani
```

Mostra il tipo di raccolta previsto per domani.

---

## Calendario

```text
calendar.sesa_calendario_rifiuti
```

Calendario annuale completo compatibile con:

* Vista calendario HA
* Automazioni calendar trigger
* Dashboard
* Reminder

---

# Service manuale

L'integrazione non interroga continuamente SESA.

Il calendario viene scaricato:

* all'avvio di Home Assistant
* al reload dell'integrazione
* al refresh manuale

## Refresh manuale

Developer Tools → Services:

```yaml
service: sesa_waste.aggiorna_calendario
```

Questo forza:

* nuova sessione PHP
* nuova registrazione UUID
* nuovo download calendario annuale

---

# Logging debug

Per debug avanzato:

```yaml
logger:
  default: info
  logs:
    custom_components.sesa_waste: debug
```

---

# Architettura tecnica

Il backend SESA richiede una sequenza specifica di chiamate:

1. Registrazione UUID
2. Inizializzazione sessione PHP
3. Apertura pagine setup indirizzo
4. Salvataggio impostazioni
5. Apertura homepage
6. Download calendario

L'integrazione replica il comportamento ufficiale dell'app Android.

---

# Note

* Nessuna API ufficiale pubblica disponibile
* Parsing HTML + endpoint AJAX
* Compatibile con i comuni supportati da SESA
* Testato su Home Assistant 2026.5+

---

# Disclaimer

Questo progetto non è affiliato ufficialmente a SESA.

Tutti i dati provengono da:

```text
https://app.sesaeste.it
```

---

# Licenza

MIT License

---

# Roadmap

## Possibili evoluzioni future

* notifiche native Home Assistant
* icone specifiche per tipo rifiuto
* cache persistente su disco
* localizzazione EN/IT completa
* ricerca inline/filterable per comuni e vie
* pubblicazione ufficiale HACS default

---

# Ringraziamenti

Sviluppato durante reverse engineering e testing live del backend SESA direttamente da Home Assistant 😄
