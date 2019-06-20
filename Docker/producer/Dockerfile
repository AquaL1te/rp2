FROM ndnbase

# Install repo-ng
RUN dnf -y install sqlite3 libsqlite3-dev; \
  git clone https://github.com/named-data/repo-ng.git; \
  cd repo-ng; \
  ./waf configure --with-tests; \
  ./waf; \
  ./waf install; \
  ldconfig; \
  cp /usr/local/etc/ndn/repo-ng.conf.sample /usr/local/etc/ndn/repo-ng.conf; \
  mkdir -vp /var/db/ndn-repo-ng

# NDN customization
# TODO: Run NDN as non-root, binaries need special capabilities e.g. CAP_NET_ADMIN
# TODO: Make use of KSK
#RUN useradd -rs /bin/false ndn
#RUN mkdir -vp /usr/local/etc/ndn/certs
#RUN ndnsec-keygen /os3 | ndnsec-install-cert -
#RUN ndnsec-cert-dump -i /os3 > /usr/local/etc/ndn/certs/os3.ndncert
COPY nfd.conf /usr/local/etc/ndn/nfd.conf
COPY ndn-traffic-server.conf /usr/local/etc/ndn/ndn-traffic-server.conf
COPY docker-entrypoint.sh /root/docker-entrypoint.sh

ENTRYPOINT /root/docker-entrypoint.sh
