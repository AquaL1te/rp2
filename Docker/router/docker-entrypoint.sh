#!/bin/bash

echo "Hostname: $HOSTNAME"

if nfd-start > /var/log/nfd.log; then
  echo "NFD started"
  sleep 2s
fi

if nfdc face create udp://$HOSTNAME/os3; then
  echo "NFD face created"
  sleep 2s
  nfdc face list
else
  echo "NFD face creation failed"
  exit
fi

if nfdc route add /os3 udp://$HOSTNAME/os3; then
  echo "NFD route added"
  sleep 2s
  nfdc route list
else
  echo "NFD route creation failed"
  exit
fi

if [[ -f /var/log/nfd.log ]]; then
  echo "Tailing NFD log"
  tail -f /var/log/nfd.log
else
  echo "No NFD log found"
  exit
fi
