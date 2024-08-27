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

# Entrare nella directory del simulatore e avviarlo in background
cd ~/arduino/small_watering/moisture_sensor_simulator/.venv/bin
./python ../../moisture_sensor_simulator.py &
echo "Simulatore avviato in background"
