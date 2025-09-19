#!/usr/bin/env bash
set -euo pipefail

# Configure UFW to play nicely with Docker by adjusting forward policy
# and adding permissive forward rules for docker0 and bridge interfaces.
#
# Usage: sudo ./scripts/configure_ufw_for_docker.sh

require_root() {
  if [[ "${EUID}" -ne 0 ]]; then
    echo "This script must be run as root (use sudo)." >&2
    exit 1
  fi
}

backup_file() {
  local file="$1"
  if [[ -f "$file" ]]; then
    cp -a "$file" "${file}.bak.$(date +%Y%m%d%H%M%S)"
  fi
}

ensure_line_in_file() {
  local line="$1"
  local file="$2"
  grep -Fqx "$line" "$file" || echo "$line" >> "$file"
}

require_root

echo "Backing up UFW configuration files..."
backup_file /etc/default/ufw
backup_file /etc/ufw/after.rules

echo "Setting DEFAULT_FORWARD_POLICY=\"ACCEPT\" in /etc/default/ufw ..."
sed -i 's/^#*\s*DEFAULT_FORWARD_POLICY\s*=.*/DEFAULT_FORWARD_POLICY="ACCEPT"/' /etc/default/ufw

DOCKER_UFW_BLOCK_START="# BEGIN UFW-DOCKER"
DOCKER_UFW_BLOCK_END="# END UFW-DOCKER"

if ! grep -q "${DOCKER_UFW_BLOCK_START}" /etc/ufw/after.rules; then
  echo "Adding Docker forward allowances to /etc/ufw/after.rules ..."
  cat >> /etc/ufw/after.rules <<'RULES'
# BEGIN UFW-DOCKER
# Allow forwarding for Docker bridge and networks. This prevents UFW from breaking container traffic.
*filter
:ufw-user-forward - [0:0]
# Establish related connections first
-A ufw-user-forward -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT
# Permit traffic to/from docker0
-A ufw-user-forward -i docker0 -j ACCEPT
-A ufw-user-forward -o docker0 -j ACCEPT
# Permit traffic to/from user-defined bridge networks (br-*)
-A ufw-user-forward -i br-+ -j ACCEPT
-A ufw-user-forward -o br-+ -j ACCEPT
# Optionally, permit to/from common Docker subnet range (172.16.0.0/12)
-A ufw-user-forward -s 172.16.0.0/12 -j ACCEPT
-A ufw-user-forward -d 172.16.0.0/12 -j ACCEPT
COMMIT

# NAT is generally handled by Docker. If you truly need UFW to handle NAT,
# uncomment the following block and adjust the outbound interface as needed.
#
# *nat
# :POSTROUTING ACCEPT [0:0]
# -A POSTROUTING -s 172.16.0.0/12 ! -o docker0 -j MASQUERADE
# COMMIT
# END UFW-DOCKER
RULES
else
  echo "UFW-DOCKER rules already present. Skipping insertion."
fi

echo "Reloading UFW..."
ufw reload || true
echo "Done. Verify with: ufw status verbose && cat /etc/ufw/after.rules | sed -n '/BEGIN UFW-DOCKER/,/END UFW-DOCKER/p'"

