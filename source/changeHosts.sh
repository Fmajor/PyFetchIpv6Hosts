#!/bin/bash
echo "sudo mv /etc/hosts /etc/hosts.backupByPyFetchIpv6Hosts"
mv /etc/hosts /etc/hosts.backupByPyFetchIpv6Hosts
echo "sudo head -n 12 /etc/hosts.backupByPyFetchIpv6Hosts > /etc/hosts"
head -n 12 /etc/hosts.backupByPyFetchIpv6Hosts > /etc/hosts
echo "sudo cat ../hosts.bnu >> /etc/hosts"
cat ../hosts.bnu >> /etc/hosts
