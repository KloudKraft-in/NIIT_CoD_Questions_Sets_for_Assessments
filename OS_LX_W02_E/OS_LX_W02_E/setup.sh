#!/usr/bin/env bash
# ==============================================================================
# OS_LX_W02_E Lab Setup: Seed /var/log/syslog with simulated incident outage logs
# ==============================================================================
set -e

echo "[SETUP] Configuring /var/log/syslog for incident window isolation lab..."

sudo mkdir -p /var/log

sudo tee /var/log/syslog > /dev/null << 'EOF'
Oct 27 13:45:10 web-srv01 systemd[1]: Started Daily apt upgrade and clean activities.
Oct 27 13:58:20 web-srv01 app[1042]: INFO Health check responding OK on port 8080
Oct 27 14:02:15 web-srv01 app[1042]: ERROR Database connection failure from 192.168.1.105
Oct 27 14:05:32 web-srv01 app[1042]: TIMEOUT Upstream gateway response timeout for client 10.0.0.45
Oct 27 14:08:19 web-srv01 app[1042]: ERROR Failed to authenticate user session from 172.16.0.88
Oct 27 14:12:44 web-srv01 app[1042]: TIMEOUT Request timeout from 192.168.1.105
Oct 27 14:14:50 web-srv01 app[1042]: ERROR Critical thread pool exhaustion caused by 10.0.0.45
Oct 27 14:18:05 web-srv01 app[1042]: INFO Service stabilized, normal latency restored
Oct 27 14:25:30 web-srv01 systemd[1]: Session 3 logged out.
EOF

sudo chmod 644 /var/log/syslog

echo "[SETUP] /var/log/syslog successfully initialized!"
echo "[SETUP] Sample incident data between 14:00:00 and 14:15:00 is ready for querying."

