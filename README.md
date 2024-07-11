# Tesi small watering

## Hardware
1. Provare sensori (verificare che non si influenzano a vicenda)
2. Predisporre "impianto elettrico" breadboard
3. Comunicazione bidirezionale Raspberry - Arduino.


## Software

### Collection (Arduino)
1. Sampling sensori (<b>definire frequenza  di campionamento</b>)
2. Invio dati Arduino -> Raspberry
    - JSON
            - {timestamp: 1720684942,
            ges_10_10: 56,
            ...,
            ges_30_30: 100
           }

### Processing (Raspberry)g
1. Per ogni .JSON, salvarlo su storage
2. Per ogni .JSON effettuare interpolazione bilineare con <b>granularità 5 cm</b> e salvare dati su storage.

#### Nice to have
 - Salvare i dati su un DB

### Exploitation

#### Interfaccia grafica

Applicazione in Java/Python
<b>Due</b> grafici:
1. Valori singoli sensori
2. Matrice interpolata

#### Prescrittivo

<b>TO BE DEFINED</b>

Considerazioni su algoritmo prescrittivo as-is:
- Senza rilevare la quantità irrigata in questo scenario, il PID non funzia;
- Semplice sistema a soglia?


# TODOLIST
- Compra relè
