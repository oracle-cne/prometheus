FROM container-registry.oracle.com/os/oraclelinux:9 AS builder

RUN dnf config-manager --enable ol9_codeready_builder && \
    dnf -y install git make golang hostname bzip2 && \
    curl -fsSL https://rpm.nodesource.com/setup_22.x | bash - && \
    dnf install -y nodejs && \
    go version

# Copy the contents of the repository
COPY . /workspace/go/src/github.com/oracle-cne/prometheus

ENV GOPATH=/workspace/go CGO_ENABLED=0
ENV GOPATH_SRC=$GOPATH/src/github.com/oracle-cne/prometheus
WORKDIR /workspace/go/src/github.com/oracle-cne/prometheus

RUN git config --global --add safe.directory $(pwd) && \
    sh olm/go-build.sh

FROM container-registry.oracle.com/os/oraclelinux:9-slim

COPY --from=builder /workspace/go/src/github.com/oracle-cne/prometheus/bin/prometheus /bin/prometheus
COPY --from=0 /bin/promtool /bin/promtool
COPY --from=0 /etc/prometheus /etc/prometheus
COPY LICENSE THIRD_PARTY_LICENSES.txt NOTICE olm/SECURITY.md /usr/share/licenses/prometheus/
RUN ln -s /etc/prometheus/ &&\
    mkdir -p /prometheus &&\
    chown -R nobody:nobody etc/prometheus /prometheus &&\
    test -d /LICENSES || ln -s /usr/share/licenses /LICENSES

RUN microdnf update -y && \
    microdnf clean all

USER       nobody
EXPOSE     9090
VOLUME     [ "/prometheus" ]
WORKDIR    /prometheus
ENTRYPOINT [ "/bin/prometheus" ]
CMD        [ "--config.file=/etc/prometheus/prometheus.yml", \
             "--storage.tsdb.path=/prometheus", \
             "--web.console.libraries=/usr/share/prometheus/console_libraries", \
             "--web.console.templates=/usr/share/prometheus/consoles" ]
