# Base OS
FROM tomcat:8.5.4-jre8

# Install wget
RUN apt-get update
RUN apt-get install wget

WORKDIR /root

# Download dhis2 war
ARG DHIS2_VERSION=2.24
RUN wget "https://www.dhis2.org/download/releases/${DHIS2_VERSION}/dhis.war"

COPY ./hibernate.properties /opt/dhis2/config/hibernate.properties
RUN cp ./dhis.war /usr/local/tomcat/webapps/ROOT.war

RUN echo "export JAVA_OPTS=$JAVA_OPTS\nexport DHIS2_HOME='/opt/dhis2/config'" >> /usr/local/tomcat/bin/setenv.sh
COPY ./wait-for-it.sh ./wait-for-it.sh