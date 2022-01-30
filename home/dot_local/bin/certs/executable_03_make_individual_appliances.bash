#bin/bash

pass=''
name=''
C=''
ST=''

domain=""
subDomains=( ".$domain" )

for c in "${subDomains[@]}"; do
mkdir -p "${c}"
openssl genrsa \
    -out ./"${c}"/"${c}".pem \ 4096
done

for c in "${subDomains[@]}"; do
printf "\e[32mCreating %s certificate request \e[0m\n" "$c"
openssl req \
    -new \
    -sha512 \
    -key ./"${c}"/"${c}".pem \
    -subj "/C="$C"/ST="$ST"/O="$name" Network, Inc./CN=${c}" \
    -out ./"${c}"/"${c}".csr \
    -reqexts SAN \
    -extensions SAN \
    -config <(cat /etc/ssl/openssl.cnf ; printf "[SAN]\nsubjectAltName=DNS:%s" "$c")
done

printf "\e[32mSigning certificate request %s x509 key\e[0m\n" "$c"
for c in "${subDomains[@]}"; do
openssl x509 \
    -req \
    -in ./"${c}"/"${c}".csr \
    -CA "$name"Root.crt \
    -CAkey "$name"Root.pem \
    -CAcreateserial \
    -out ./"${c}"/"${c}".crt \
    -days 3650 \
    -sha512 \
    -extensions v3_ext \
    -extensions SAN \
    -extfile <(cat /etc/ssl/openssl.cnf ; printf "[SAN]\nsubjectAltName=DNS:%s" "$c")
done

for c in "${subDomains[@]}"; do
    openssl dhparam -check -text -5 4096 > "${c}".dh
done
