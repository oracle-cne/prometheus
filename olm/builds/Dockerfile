FROM container-registry.oracle.com/os/oraclelinux:8
COPY rpms /tmp/
RUN dnf install -y /tmp/*.rpm &&\
    dnf clean all &&\
    rm -rf /var/cache/yum/* /tmp/*.rpm

FROM container-registry.oracle.com/os/oraclelinux:8-slim

COPY --from=0 /usr/share/licenses/prometheus /usr/share/licenses/prometheus
COPY --from=0 /bin/prometheus /bin/prometheus
COPY --from=0 /bin/promtool /bin/promtool
COPY --from=0 /etc/prometheus /etc/prometheus
COPY LICENSE THIRD_PARTY_LICENSES.txt NOTICE olm/SECURITY.md /usr/share/licenses/
RUN ln -s /etc/prometheus/ &&\
    mkdir -p /prometheus &&\
    chown -R nobody:nobody etc/prometheus /prometheus &&\
    test -d /LICENSES || ln -s /usr/share/licenses /LICENSES

RUN microdnf update -y && \
    microdnf clean all && \
    rm -rf /var/cache/yum/*

USER       nobody
EXPOSE     9090
VOLUME     [ "/prometheus" ]
WORKDIR    /prometheus
ENTRYPOINT [ "/bin/prometheus" ]
CMD        [ "--config.file=/etc/prometheus/prometheus.yml", \
             "--storage.tsdb.path=/prometheus", \
             "--web.console.libraries=/usr/share/prometheus/console_libraries", \
             "--web.console.templates=/usr/share/prometheus/consoles" ]
