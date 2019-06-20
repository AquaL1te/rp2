#!/bin/bash

echo "Hostname: $HOSTNAME"
echo "Gateway: $gateway"

if nfd-start > /var/log/nfd.log; then
  echo "NFD started"
  sleep 2s
else
  echo "NFD failed to start"
  exit
fi

if nfdc face create udp4://"$gateway":6363; then
  echo "Default NDN gateway set"
  sleep 2s
else
  echo "Failed to set default NDN gateway"
  exit
fi

if nfdc route add /example udp://"$gateway":6363; then
  echo "Default NDN gateway set"
  sleep 2s
else
  echo "Failed to set default NDN gateway"
  exit
fi

if [[ -f /var/log/nfd.log ]]; then
  echo "Starting /var/log/nfd.log tail + HTTP monitoring page (port 8080)"
  nfd-status-http-server -a 0.0.0.0 &
  tail -f /var/log/nfd.log
else
  echo "No NFD log found"
  exit
fi
