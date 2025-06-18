#!/usr/bin/env bash
# wait-for-it.sh

# ეს სკრიპტი ელოდება სერვისის გაშვებას კონკრეტულ პორტზე. (This script waits for a service to be up on a given port.)

host="$1"
port="$2"
shift 2
cmd="$@"

echo "Waiting for $host:$port to be available..."

while ! nc -z "$host" "$port"; do
  sleep 0.1
done

echo "$host:$port is available. Executing command..."
exec $cmd