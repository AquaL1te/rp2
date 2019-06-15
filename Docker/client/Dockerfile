FROM ubuntu:18.04

MAINTAINER Kees de Jong "kees.dejong@os3.nl"

ENV DEBIAN_FRONTEND=noninteractive
RUN export LC_ALL="en_US.UTF-8"

# Install NDN-CXX packages
RUN apt-get update && apt-get -y upgrade
RUN apt-get -y install software-properties-common
RUN add-apt-repository ppa:named-data/ppa
RUN apt-get update
RUN apt-get -y install nfd
RUN apt-get -y install ndn-tools

# Install additional packages
RUN apt-get -y install vim
