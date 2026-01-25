#!/bin/sh

for host in $HOSTS_WITH_SELF_SIGNED_CERTS; do
if [ ! -e /certs/$host.crt ]; then
mkcert -cert-file /certs/$host.crt -key-file /certs/$host.key $host
fi
done
