FROM fedora:30 AS ndn-base-image

MAINTAINER Kees de Jong "keesdejong@fedoraproject.org"

ENV PKG_CONFIG_PATH=/usr/local/lib64/pkgconfig

RUN dnf -y update --refresh; \
  dnf -y install \
    boost-devel \
    doxygen \
    gcc-g++ \
    git \
    graphviz \
    libcap-devel \
    libpcap-devel \
    openssl-devel \
    python-sphinx \
    sqlite-devel; \
  cd /root; \
  git clone https://github.com/named-data/ndn-cxx; \
  cd /root/ndn-cxx; \
  ./waf configure --with-examples --with-tests; \
  ./waf; \
  ./waf install; \
  ./waf docs; \
  echo "/usr/local/lib64" > /etc/ld.so.conf.d/ndn-cxx.conf; \
  ldconfig; \
  cd /root; \
  git clone https://github.com/named-data/ndn-tools.git; \
  cd /root/ndn-tools; \
  ./waf configure; \
  ./waf; \
  ./waf install; \
  ldconfig; \
  cd /root; \
  git clone --recursive https://github.com/named-data/NFD; \
  cd /root/NFD; \
  ./waf configure; \
  ./waf; \
  ./waf install; \
  ./waf docs; \
  ldconfig; \
  cd /root; \
  git clone https://github.com/named-data/ndn-traffic-generator.git; \
  cd /root/ndn-traffic-generator; \
  ./waf configure; \
  ./waf; \
  ./waf install; \
  ldconfig

# Copy consumer and producer scripts
COPY pid_client.py /root/pid_client.py
COPY ndn_client.py /root/ndn_client.py
COPY pid_server.py /root/pid_server.py
COPY ndn_server.py /root/ndn_server.py

# For interactive troubleshooting
RUN dnf -y install iproute man vim; \
  mandb

# Needed for python
RUN dnf -y install python3-urllib3

WORKDIR /root
