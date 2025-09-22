
%if 0%{?with_debug}
# https://bugzilla.redhat.com/show_bug.cgi?id=995136#c12
%global _dwz_low_mem_die_limit 0
%else
%global debug_package   %{nil}
%endif

%global _buildhost	build-ol%{?oraclelinux}-%{?_arch}.oracle.com

%global build_dir	src/github.com/prometheus/prometheus

Name:          	prometheus
Version:       	3.6.0
Release:        1%{?dist}
Summary:        Systems and service monitoring
License:        Apache-2.0
Group:          System/Management
Url:            https://github.com/prometheus/prometheus
Source:         %{name}-%{version}.tar.bz2
Vendor:	        Oracle America
BuildRequires:  golang
BuildRequires:  nodejs >= 22
BuildRequires:  npm >= 10
BuildRequires:  yarnpkg
BuildRequires:  bzip2
%if %{?oraclelinux} == 9
Patch0:         package.json.patch
%endif

%description
Prometheus, a Cloud Native Computing Foundation project, is a systems and service monitoring system.
It collects metrics from configured targets at given intervals, evaluates rule expressions,
displays the results, and can trigger alerts if some condition is observed to be true.

%prep
%setup -q -n %{name}-%{version}
%if %{?oraclelinux} == 9
%patch0
%endif
mkdir -p %{build_dir}
mv $(ls | grep -v "^src$") %{build_dir}
mv .promu.yml %{build_dir}

%build
export GOPATH=$(pwd)/Godeps/_workspace
pushd %{build_dir}
#%if %{minor_version} >= 31
#NPM_CONFIG_PREFIX=~/.npm-global
#npm install --global --unsafe-perm lezer-generator typescript
#%endif
npm version
node --version
yarn --version
go version
make build
popd

%install
pushd %{build_dir}
install -m 755 -d %{buildroot}/bin
install -p -m 755 -t %{buildroot}/bin prometheus
install -p -m 755 -t %{buildroot}/bin promtool
install -m 755 -d %{buildroot}/etc/prometheus/
install -p -m 644 -t %{buildroot}/etc/prometheus/ documentation/examples/prometheus.yml

popd
mv %{build_dir}/LICENSE .
mv %{build_dir}/THIRD_PARTY_LICENSES.txt .
mv %{build_dir}/NOTICE .
mv %{build_dir}/olm/SECURITY.md .

%files
%license LICENSE THIRD_PARTY_LICENSES.txt NOTICE SECURITY.md
/bin/prometheus
/bin/promtool
/etc/prometheus/prometheus.yml

%changelog
* Mon Sep 22 2025 Olcne-Builder Jenkins <olcne-builder_us@oracle.com> - 3.6.0-1
- Added Oracle Specific Build Files for prometheus
