#!/bin/bash
echo "mv /etc/hosts /etc/hosts.backupByPyFetchIpv6Hosts"
mv /etc/hosts /etc/hosts.backupByPyFetchIpv6Hosts
echo "head -n 12 /etc/hosts.backupByPyFetchIpv6Hosts > /etc/hosts"
head -n 12 /etc/hosts.backupByPyFetchIpv6Hosts > /etc/hosts
echo "cat ../hosts.bnu >> /etc/hosts"
cat ../hosts.bnu >> /etc/hosts
