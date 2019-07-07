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

if nfdc face create "$protocol"4://"$gateway":6363; then
  echo "Default NDN gateway interface set"
else
  echo "Failed to set default NDN gateway interface"
  exit
fi

if [[ -n "$routes" ]]; then
  for route in $routes; do
    if nfdc route add "$route" "$protocol"://"$gateway":6363; then
      echo "NDN route $route added"
    else
      echo "Failed to set $route route"
      exit
    fi
  done
fi

if [[ -f /var/log/nfd.log ]]; then
  echo "Starting /var/log/nfd.log tail + HTTP monitoring page (port $monitoring_port)"
  nfd-status-http-server -a 0.0.0.0 -p "$monitoring_port" &
  tail -f /var/log/nfd.log
else
  echo "No NFD log found"
  exit
fi
