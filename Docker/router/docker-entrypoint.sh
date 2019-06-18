#!/bin/bash

echo "Hostname: $HOSTNAME"

if nfd-start > /var/log/nfd.log; then
  echo "NFD started"
  sleep 2s
else
  echo "NFD failed to start"
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
