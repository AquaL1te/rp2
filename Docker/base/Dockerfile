FROM fedora:30 AS firstfrom

MAINTAINER Kees de Jong "keesdejong@fedoraproject.org"

ENV PKG_CONFIG_PATH=/usr/local/lib64/pkgconfig

RUN dnf -y update --refresh; \
  dnf -y install \
    boost \
    boost-devel \
    doxygen \
    gcc-g++ \
    git \
    graphviz \
    iproute \
    libcap-devel \
    libpcap-devel \
    man \
    openssl-devel \
    python-sphinx \
    sqlite-devel \
    vim; \
  mandb; \
  mkdir -p /ndn; \
  cd /ndn; \
  git clone https://github.com/named-data/ndn-cxx; \
  cd /ndn/ndn-cxx; \
  ./waf configure; \
  ./waf; \
  ./waf install; \
  ./waf docs; \
  echo "/usr/local/lib64" > /etc/ld.so.conf.d/ndn-cxx.conf; \
  ldconfig; \
  cd /ndn; \
  git clone https://github.com/named-data/ndn-tools.git; \
  cd /ndn/ndn-tools; \
  ./waf configure; \
  ./waf; \
  ./waf install; \
  ldconfig; \
  cd /ndn; \
  git clone --recursive https://github.com/named-data/NFD; \
  cd /ndn/NFD; \
  ./waf configure; \
  ./waf; \
  ./waf install; \
  ./waf docs; \
  ldconfig;

WORKDIR /root

# doing RUN dnf -y remove,
# actually makes the image larger, since you add an extra layer
# you should do a second FROM, something like:

# FROM alpine # or any other base
# COPY --from=firstfrom /ndn /ndn

# as shown in https://github.com/svlentink/www/blob/master/Dockerfile
