FROM alpine:3.14

RUN apk add --no-cache curl jq

# download Vault
ENV VAULT_VERSION 1.13.1

RUN curl -sSL https://releases.hashicorp.com/vault/${VAULT_VERSION}/vault_${VAULT_VERSION}_linux_amd64.zip -o vault.zip \
  && unzip vault.zip \
  && mv vault /usr/bin/ \
  && rm vault.zip

# add your script
COPY vault_init.sh /usr/bin/vault_init.sh
RUN chmod +x /usr/bin/vault_init.sh

ENTRYPOINT ["/usr/bin/vault_init.sh"]
