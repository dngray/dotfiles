#bin/bash

pass=''
name=''

printf "\e[32mGenerate new Root CA key\e[0m\n"
openssl genrsa \
    -aes256 \
    -out "$name"Root.key \
    -passin pass:"${pass}" \
    4096

printf "\e[32mGenerate new "$name" Root cert\e[0m\n"
openssl req \
    -newkey rsa:4096 \
    -sha512 \
    -passin pass:"${pass}" \
    -x509 \
    -nodes \
    -keyout "$name"Root.pem \
    -new \
    -out "$name"Root.crt \
    -subj "/CN="$name" Root CA" \
    -days 3650

printf "\e[32mPrint "$name"Root key\e[0m\n"
openssl x509 \
    -text \
    -noout \
    -in "$name"Root.crt
