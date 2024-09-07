#!/bin/bash

# Avviare socat in background
socat -d -d PTY,link=/tmp/ttyV0,raw,echo=0 PTY,link=/tmp/ttyV1,raw,echo=0 &

# Memorizzare l'ID di processo (PID) di socat
SOCAT_PID=$!
echo "socat avviato con PID $SOCAT_PID"

# Attendere che i dispositivi PTY siano pronti
echo "Aspettando che socat sia pronto..."
while [ ! -e /tmp/ttyV0 ] || [ ! -e /tmp/ttyV1 ]; do
    sleep 0.5
done
echo "socat è pronto."

# Caricare manualmente le variabili d'ambiente dal file .env
export $(grep -v '^#' ~/Work/small_watering/dashboard/.env | xargs)

# Verifica che le variabili siano state caricate (opzionale)
echo "SERIAL_PORT=$SERIAL_PORT"
echo "SERIAL_BAUDRATE=$SERIAL_BAUDRATE"

# Entrare nella directory del simulatore e avviarlo in background
cd ~/Work/small_watering/moisture_sensor_simulator/.venv/bin
./python ../../moisture_sensor_simulator.py &
echo "Simulatore avviato in background"

# Entrare nella directory del dashboard e avviarlo
cd ~/Work/small_watering/dashboard/.venv/bin
./python ../../main.py

