#bin/bash

pass=''
name=''
C=''
ST=''

domain=""
subDomains=( ".$domain" )

mkdir -p "$domain"
openssl genrsa \
    -out ./$domain/$domain.pem \ 4096

printf "\e[32mCreating %s certificate request \e[0m\n" "$domain"
openssl req \
    -new \
    -sha512 \
    -key ./"$domain"/"$domain".pem \
    -subj "/C="$C"/ST="$ST"/O="$name" Network, Inc./CN=$domain" \
    -out ./"$domain"/"$domain".csr \
    -reqexts SAN \
    -extensions SAN \
    -config <(cat /etc/ssl/openssl.cnf \
        <(printf -v joined 'DNS:%s,' "${subDomains[@]}"; printf "%s%s\n[SAN]\nsubjectAltName=${joined%,} ")) \

printf "\e[32mSigning certificate request %s x509 key\e[0m\n" "$domain"
openssl x509 \
    -req \
    -in ./"$domain"/"$domain".csr \
    -CA "$name"Root.crt \
    -CAkey "$name"Root.pem \
    -CAcreateserial \
    -out ./"$domain"/"$domain".crt \
    -days 3650 \
    -sha512 \
    -extensions v3_ext \
    -extensions SAN \
    -extfile <(cat /etc/ssl/openssl.cnf \
        <(printf -v joined 'DNS:%s,' "${subDomains[@]}"; printf "%s%s\n[SAN]\nsubjectAltName=${joined%,} ")) \
