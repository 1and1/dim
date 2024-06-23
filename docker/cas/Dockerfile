FROM eclipse-temurin:11-alpine AS buildwar
RUN cd /tmp \
  && apk update \
  && apk upgrade \
  && apk add --no-cache git \
  && git clone -b 6.6 --single-branch https://github.com/ahettlin/cas-overlay-template-ldap.git cas-overlay \
  && mkdir -p /tmp/cas-overlay/src/main/webapp

WORKDIR /tmp/cas-overlay
COPY src/ /tmp/cas-overlay/src
RUN  ./gradlew clean build

FROM eclipse-temurin:11-alpine

RUN mkdir /etc/cas

WORKDIR /root
COPY --from=buildwar /tmp/cas-overlay/build/libs/cas.war .

ARG LDAP_PORT
ARG LDAP_ADMIN_PASSWORD

COPY ./config-build /etc/cas/config

WORKDIR /etc/cas/config

EXPOSE 8443
CMD [ "java", "-jar", "/root/cas.war", "-Dcas.log.level=debug" ]
