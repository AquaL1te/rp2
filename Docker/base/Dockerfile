FROM fedora:30 AS ndnbase

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
  ./waf configure; \
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

# For interactive troubleshooting
RUN dnf -y install iproute man vim; \
  mandb

WORKDIR /root
