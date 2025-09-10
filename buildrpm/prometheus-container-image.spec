
%global debug_package     %{nil}
%{!?registry: %global registry container-registry.oracle.com/olcne}

%global _buildhost  build-ol%{?oraclelinux}-%{?_arch}.oracle.com
%global _name	    prometheus

Name:               %{_name}-container-image
Version:            3.5.0
Release:            1%{?dist}
Summary:            Oracle Linux base prometheus docker image
License:            UPL
Source:             %{name}-%{version}.tar.bz2
Url:                https://github.com/prometheus/prometheus
Vendor:             Oracle America

%description
Prometheus, a Cloud Native Computing Foundation project, is a systems and service monitoring system.
It collects metrics from configured targets at given intervals, evaluates rule expressions,
displays the results, and can trigger alerts if some condition is observed to be true.

%prep
%setup -n %{name}-%{version}

%build
%global rpm_name %{_name}-%{version}-%{release}.%{_build_arch}
yum clean all
yumdownloader --destdir=${PWD}/rpms %{rpm_name}

%__rm .dockerignore
%global docker_tag %{registry}/%{_name}:v%{version}
docker build --pull \
    --build-arg https_proxy=${https_proxy} \
    -t %{docker_tag} -f \
    ./olm/builds/Dockerfile .
docker save -o %{_name}.tar %{docker_tag}

%install
%__install -D -m 644 %{_name}.tar %{buildroot}/usr/local/share/olcne/%{_name}.tar

%files
%license LICENSE THIRD_PARTY_LICENSES.txt NOTICE olm/SECURITY.md
/usr/local/share/olcne/prometheus.tar

%clean

%changelog
* Wed Sep 10 2025 Olcne-Builder Jenkins <olcne-builder_us@oracle.com> - 3.5.0-1
- Added Oracle Specific Build Files for prometheus-container-image
