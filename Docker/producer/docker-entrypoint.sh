#!/bin/bash

echo "Hostname: $HOSTNAME"

if nfd-start > /var/log/nfd.log; then
  echo "NFD started"
  sleep 2s
else
  echo "NFD failed to start"
  exit
fi

if ndn-repo-ng > /var/log/repo-ng.log; then
  echo "repo-ng started"
  sleep 2s
else
  echo "repo-ng failed to start"
fi

if [[ -f /var/log/nfd.log ]]; then
  echo "Starting /var/log/nfd.log tail + HTTP monitoring page (port $monitoring_port)"
  nfd-status-http-server -a 0.0.0.0 -p "$monitoring_port" &
  tail -f /var/log/nfd.log /var/log/repo-ng.log
else
  echo "No NFD log found"
  exit
fi
