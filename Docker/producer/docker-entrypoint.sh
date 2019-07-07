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

if ndn-repo-ng > /var/log/repo-ng.log; then
  echo "repo-ng started"
  sleep 2s
else
  echo "repo-ng failed to start"
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

for route in $routes; do
  if nfdc route add "$route" "$protocol"://"$gateway":6363; then
    echo "NDN route $route added"
  else
    echo "Failed to set $route route"
    exit
  fi
done

#if python3 /root/pid_server.py & > /var/log/pid_server.log; then
#  echo "PID server started"
#else
#  echo "PID server failed to start"
#fi
#
#if python3 /root/ndn_server.py & > /var/log/ndn_server.log; then
#  echo "NDN server started"
#else
#  echo "NDN server failed to start"
#fi

if [[ -f /var/log/nfd.log ]]; then
  echo "Starting /var/log/nfd.log tail + HTTP monitoring page (port $monitoring_port)"
  nfd-status-http-server -a 0.0.0.0 -p "$monitoring_port" &
  tail -f /var/log/nfd.log /var/log/repo-ng.log /var/log/pid_server.log /var/log/ndn_server.log
else
  echo "No NFD log found"
  exit
fi
