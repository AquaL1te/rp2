FROM fedora:30

MAINTAINER Kees de Jong "keesdejong@fedoraproject.org"

# Update system
RUN dnf -y update --refresh

# Install build dependencies
RUN dnf -y install gcc-g++ 
RUN dnf -y install sqlite-devel
RUN dnf -y install boost-devel
RUN dnf -y install openssl-devel
RUN dnf -y install doxygen
RUN dnf -y install graphviz
RUN dnf -y install python-sphinx
RUN dnf -y install libcap-devel
RUN dnf -y install libpcap-devel

# Install additional packages
RUN dnf -y install git

# Clone repos
WORKDIR /root
RUN git clone https://github.com/named-data/ndn-cxx
RUN git clone --recursive https://github.com/named-data/NFD
RUN git clone https://github.com/named-data/ndn-tools.git

# Build NDN-CXX from source
WORKDIR /root/ndn-cxx
RUN ./waf configure
RUN ./waf
RUN ./waf install
RUN ./waf docs
ENV PKG_CONFIG_PATH=/usr/local/lib64/pkgconfig
RUN echo "/usr/local/lib64" > /etc/ld.so.conf.d/ndn-cxx.conf
RUN ldconfig

# Build NFD from source
WORKDIR /root/NFD
RUN ./waf configure
RUN ./waf
RUN ./waf install
RUN ./waf docs
RUN ldconfig

# Build NDN-tools
WORKDIR /root/ndn-tools
RUN ./waf configure
RUN ./waf
RUN ./waf install
RUN ldconfig

# Clean up image
RUN dnf -y remove gcc-g++ 
RUN dnf -y remove sqlite-devel
RUN dnf -y remove boost-devel
RUN dnf -y remove openssl-devel
RUN dnf -y remove libcap-devel
RUN dnf -y remove libpcap-devel

# Dependencies for runtime
RUN dnf -y install boost

# For interactive troubleshooting
RUN dnf -y install vim
RUN dnf -y install iproute
RUN dnf -y install man
RUN mandb

# NDN customization
# TODO: Run NDN as non-root, binaries need special capabilities e.g. CAP_NET_ADMIN
#RUN useradd -rs /bin/false ndn
WORKDIR /root
RUN mkdir -vp /usr/local/etc/ndn/certs
RUN ndnsec-keygen /os3 | ndnsec-install-cert -
RUN ndnsec-cert-dump -i /os3 > /usr/local/etc/ndn/certs/os3.ndncert
COPY nfd.conf /usr/local/etc/ndn/nfd.conf
COPY nfd.conf.example /usr/local/etc/ndn/nfd.conf.example
COPY docker-entrypoint.sh /root/docker-entrypoint.sh

ENTRYPOINT /root/docker-entrypoint.sh
