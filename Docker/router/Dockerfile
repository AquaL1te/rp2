FROM ndnbase

# NDN customization
# TODO: Run NDN as non-root, binaries need special capabilities e.g. CAP_NET_ADMIN
#RUN useradd -rs /bin/false ndn
RUN mkdir -vp /usr/local/etc/ndn/certs
RUN ndnsec-keygen /os3 | ndnsec-install-cert -
RUN ndnsec-cert-dump -i /os3 > /usr/local/etc/ndn/certs/os3.ndncert
COPY nfd.conf /usr/local/etc/ndn/nfd.conf
COPY nfd.conf.example /usr/local/etc/ndn/nfd.conf.example
COPY docker-entrypoint.sh /docker-entrypoint.sh

ENTRYPOINT /docker-entrypoint.sh
