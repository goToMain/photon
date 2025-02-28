%ifarch aarch64
%global gohostarch      arm64
%else
%global gohostarch      amd64
%endif

Summary:        Configures network interfaces in cloud enviroment
Name:           cloud-network-setup
Version:        0.2.1
Release:        4%{?dist}
License:        Apache-2.0
URL:            https://github.com/vmware/%{name}/archive/refs/tags/v%{version}.tar.gz
Source0:        https://github.com/vmware/%{name}/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512  %{name}=dc610c2fc491ee4d5e40fd7097c25d9b0f8a03fd88066bf57d1483a2dfa7b322d75dc10bd7a269fbabb36cbe056c2f222c464fd4a57296cc7331292d224f43e8
Group:          Networking
Vendor:         VMware, Inc.
Distribution:   Photon

BuildRequires:  go
BuildRequires:  systemd-rpm-macros

Requires:  systemd

%global debug_package %{nil}

%description
cloud-network configures network in cloud environment. In cloud environment
instances are set public IPs and private IPs. If more than one private IP is
configured then except the IP which is provided by DHCP others can't be fetched
and configured. This project is adopting towards cloud network environment such
as Azure, GCP and Amazon EC2.

%prep -p exit
%autosetup -p1 -n %{name}-%{version}

%build
export ARCH=%{gohostarch}
export VERSION=%{version}
export PKG=github.com/%{name}/%{name}
export GOARCH=${ARCH}
export GOHOSTARCH=${ARCH}
export GOOS=linux
export GOHOSTOS=linux
export GOROOT=/usr/lib/golang
export GOPATH=/usr/share/gocode
export GOBIN=/usr/share/gocode/bin
export PATH=$PATH:$GOBIN

mkdir -p ${GOPATH}/src/${PKG}
cp -rf . ${GOPATH}/src/${PKG}
pushd ${GOPATH}/src/${PKG}

go build -o bin/cloud-network ./cmd/cloud-network
go build -o bin/cnctl ./cmd/cnctl

popd

%install
install -m 755 -d %{buildroot}%{_bindir}
install -m 755 -d %{buildroot}%{_sysconfdir}/cloud-network
install -m 755 -d %{buildroot}%{_unitdir}

install -pm 755 -t %{buildroot}%{_bindir} ${GOPATH}/src/github.com/%{name}/%{name}/bin/cloud-network
install -pm 755 -t %{buildroot}%{_bindir} ${GOPATH}/src/github.com/%{name}/%{name}/bin/cnctl

install -pm 755 -t %{buildroot}%{_sysconfdir}/cloud-network ${GOPATH}/src/github.com/%{name}/%{name}/distribution/cloud-network.toml
install -pm 755 -t %{buildroot}%{_unitdir}/ ${GOPATH}/src/github.com/%{name}/%{name}/distribution/cloud-network.service

%clean
rm -rf %{buildroot}/*

%pre
if ! getent group cloud-network >/dev/null 2>&1; then
    /usr/sbin/groupadd -g 89 cloud-network
fi

if ! getent passwd cloud-network >/dev/null 2>&1 ; then
    /usr/sbin/useradd -g 89 -u 89 -r -s /sbin/nologin cloud-network >/dev/null 2>&1 || exit 1
fi

%post
%systemd_post cloud-network.service

%preun
%systemd_preun cloud-network.service

%postun
%systemd_postun_with_restart cloud-network.service

%files
%defattr(-,root,root)
%{_bindir}/cloud-network
%{_bindir}/cnctl
%{_sysconfdir}/cloud-network/cloud-network.toml
%{_unitdir}/cloud-network.service

%changelog
* Mon Nov 21 2022 Piyush Gupta <gpiyush@vmware.com> 0.2.1-4
- Bump up version to compile with new go
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 0.2.1-3
- Bump up version to compile with new go
* Fri Jun 17 2022 Piyush Gupta <gpiyush@vmware.com> 0.2.1-2
- Bump up version to compile with new go
* Thu Mar 03 2022 Susant Sahani <ssahani@vmware.com> 0.2.1-1
- Version bump.
* Sun Feb 13 2022 Susant Sahani <ssahani@vmware.com> 0.2-1
- Version bump.
* Wed Jun 30 2021 Susant Sahani <ssahani@vmware.com> 0.1-1
- Initial rpm release.
