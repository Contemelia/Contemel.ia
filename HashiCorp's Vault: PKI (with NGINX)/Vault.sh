#!/bin/bash

# Read user input
read -p "Enter domain name: " domain
read -p "Enter sub-domain name: " subdomain
read -p "Enter root CA directory name: " rootDir
read -p "Enter intermediate CA directory name: " intermediateDir
read -p "Enter role name: " roleName
read -p "Enter the maximum TTL for the root CA (in hours): " rootMTTL
read -p "Enter the maximum TTL for the intermediate CA (in hours): " intermediateMTTL
read -p "Enter the duration of validity for the certificate (in hours): " certificateDuration
read -p "Enter directory name to store certificates: " certDir

# Start Vault in development mode
vault server -dev &
sleep 1s;
read -p "Enter the token: " vaultToken

# Set environment variables for Vault CLI
export VAULT_ADDR=http://127.0.0.1:8200
export VAULT_TOKEN=${vaultToken}

# Create a root CA
vault secrets enable -path=${rootDir} -description="Root CA" pki
vault write ${rootDir}/root/generate/internal common_name="${domain} Root CA" ttl="${rootMTTL}h"
vault write ${rootDir}/config/urls issuing_certificates="${VAULT_ADDR}/v1/${rootDir}/ca" crl_distribution_points="${VAULT_ADDR}/v1/${rootDir}/crl"

# Create an intermediate CA
vault secrets enable -path=${intermediateDir} -description="Intermediate CA" pki
vault secrets tune -max-lease-ttl=${intermediateMTTL}h ${intermediateDir}
vault write -format=json ${intermediateDir}/intermediate/generate/internal common_name="${subdomain}.${domain} Intermediate CA" | jq -r '.data.csr' > intermediate.csr
vault write -format=json ${rootDir}/root/sign-intermediate csr=@intermediate.csr format="pem_bundle" | jq -r '.data.certificate' > signed_intermediate.crt
vault write ${intermediateDir}/intermediate/set-signed certificate=@signed_intermediate.crt

# Create a role for the subdomain
vault write ${intermediateDir}/roles/${roleName} allowed_domains="${domain}" allow_subdomains=true


# Issue certificate for the sub-domain

# vault write -format=json ${intermediateDir}/issue/${roleName} common_name="${subdomain}.${domain}" ttl="24h" | jq -r '.data.certificate' > ${certDir}/${subdomain}_certificate.crt
# vault write -format=json ${intermediateDir}/issue/${roleName} common_name="${subdomain}.${domain}" ttl="24h" | jq -r '.data.private_key' > ${certDir}/${subdomain}_private_key.key
# vault write -format=json ${intermediateDir}/issue/${roleName} common_name="${subdomain}.${domain}" ttl="24h" | jq -r '.data.issuing_ca' > ${certDir}/${subdomain}_issuing_ca.crt

response=$(vault write -format=json ${intermediateDir}/issue/${roleName} common_name="${subdomain}.${domain}" ttl="${certificateDuration}h")
echo ${response} >> ${certDir}/${subdomain}_domain_certificate.json
# echo ${response} | jq -r '.data.certificate' >> ${certDir}/${subdomain}_certificate.crt
# echo "$response" | jq -r '.data.private_key' >> ${certDir}/${subdomain}_private_key.key
# echo "$response" | jq -r '.data.issuing_ca' >> ${certDir}/${subdomain}_issuing_ca.crt


# Display the generated root and intermediate CA paths
echo "Root CA path: ${rootDir}"
echo "Intermediate CA path: ${intermediateDir}"
echo "Certificate, private key, and issuing CA are stored in ${certDir}"