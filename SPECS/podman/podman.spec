%global dnsnamevers 1.3.1

Summary:        A tool to manage Pods, Containers and Container Images
Name:           podman
Version:        4.3.0
Release:        3%{?dist}
License:        ASL 2.0
URL:            https://github.com/containers/podman
Group:          Podman
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/containers/podman/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512 %{name}=b5b70e83a67ccfea149cb7df87a452d51fbb5e87ab3d1c6b4f623ba0f8f8a25442cee6ae8b8d31ea844f08c3ea4962e865ddb90e61c185dfad29d3b23aa8338f

Source1: https://github.com/containers/dnsname/archive/refs/tags/dnsname-%{dnsnamevers}.tar.gz
%define sha512 dnsname=ebebbe62394b981e86cd21fa8b92639a6d67e007a18c576ffdbac8067084a4cffdc9d077213bf7c9ee1e2731c7d69e4d4c02465f2340556c8723b6e302238aad

Source2: https://github.com/containers/gvisor-tap-vsock/archive/refs/tags/gvisor-tap-vsock-fdc231ae7b8fe1aec4cf0b8777274fa21b70d789.tar.gz
%define sha512 gvisor-tap-vsock=eedc553378abdb4a2aff3ba10e77c52c8cdec0de67ad70dc69e418255b0f78663271ac0ac3f3a887bc5fd0871309b5c9769c92c26b894d836dcf6e7385836abf

BuildRequires:  gcc
BuildRequires:  glibc-devel
BuildRequires:  libgpg-error-devel
BuildRequires:  shadow-tools
BuildRequires:  pkg-config
BuildRequires:  make
BuildRequires:  systemd-devel
BuildRequires:  containers-common
BuildRequires:  go-md2man
BuildRequires:  go
BuildRequires:  git
BuildRequires:  libassuan-devel
BuildRequires:  gpgme-devel
BuildRequires:  btrfs-progs-devel
BuildRequires:  device-mapper-devel
BuildRequires:  libseccomp-devel
BuildRequires:  libselinux-devel

Provides:       pkgconfig(devmapper)

Requires:       libassuan
Requires:       gpgme
Requires:       cni
Requires:       conmon
Requires:       containers-common
Requires:       iptables
Requires:       shadow
Requires:       slirp4netns

%description
%{name} is a daemonless, open source, Linux native tool designed to make it easy to find, run, build,
share and deploy applications using OCI Containers and Container Images.

%package tests
Summary: Tests for %{name}
Requires: bats
Requires: jq

%description tests
This package contains system tests for %{name}

%package remote
Summary: (Experimental) Remote client for managing %{name} containers

%description remote
Remote client to connect with a %{name} client for managing %{name} containers. This experimental
remote client is under heavy development. Please do not run %{name}-remote in production.

%package plugins
Summary: Plugins for %{name}
Requires: dnsmasq
Recommends: %{name}-gvproxy = %{version}-%{release}

%description plugins
This plugin sets up the use of dnsmasq on a given CNI network so that Pods can resolve each other by name.
Each CNI network will have its own dnsmasq instance.

%package gvproxy
Summary: Go replacement for libslirp and VPNKit

%description gvproxy
A replacement for libslirp and VPNKit, written in pure Go. It is based on the network stack of gVisor.
Compared to libslirp, gvisor-tap-vsock brings a configurable DNS server and dynamic port forwarding.

%prep
%autosetup -Sgit -n %{name}-%{version}
tar xf %{SOURCE1} --no-same-owner
tar xf %{SOURCE2} --no-same-owner

%build
#build podman
export BUILDTAGS="seccomp exclude_graphdriver_devicemapper $(hack/btrfs_installed_tag.sh) $(hack/btrfs_tag.sh) $(hack/libdm_tag.sh) $(hack/selinux_tag.sh) $(hack/systemd_tag.sh) $(hack/libsubid_tag.sh)"
%make_build

#build plugin
pushd dnsname-%{dnsnamevers}
%make_build
popd

#build gvproxy
pushd gvisor-tap-vsock
%make_build
popd

%install
#install podman
export PREFIX=%{_prefix}

%make_install %{?_smp_mflags} LIBEXECDIR=%{_libexecdir} \
     install.bin install.man install.systemd install.completions \
     install.remote install.modules-load

install -d -p %{buildroot}%{_datadir}/%{name}/test/system
cp -pav test/system %{buildroot}%{_datadir}/%{name}/test/

# Exclude podman-remote man pages from main package
rm -f podman.file-list
for file in $(find %{buildroot}%{_mandir}/man[15] -type f | sed "s,%{buildroot},," | grep -v -e remote); do
  echo "$file*" >> podman.file-list
done

#install plugin
pushd dnsname-%{dnsnamevers}
%make_install %{?_smp_mflags}
popd

#install gvproxy
pushd gvisor-tap-vsock
install -dp %{buildroot}%{_libexecdir}/%{name}
install -p -m0755 bin/gvproxy %{buildroot}%{_libexecdir}/%{name}
popd

rm -rf %{buildroot}%{_datadir}/zsh \
       %{buildroot}%{_datadir}/fish

%files -f %{name}.file-list
%defattr(-,root,root)
%license LICENSE
%doc README.md CONTRIBUTING.md install.md transfer.md
%{_bindir}/%{name}
%dir %{_libexecdir}/%{name}
%{_libexecdir}/%{name}/rootlessport
%{_datadir}/bash-completion/completions/%{name}
%{_unitdir}/%{name}*
%{_userunitdir}/%{name}*
%{_tmpfilesdir}/%{name}.conf
%{_modulesloaddir}/%{name}-iptables.conf

%files remote
%defattr(-,root,root)
%license LICENSE
%{_bindir}/%{name}-remote
%{_mandir}/man1/%{name}-remote*.*
%{_datadir}/bash-completion/completions/%{name}-remote

%files tests
%defattr(-,root,root)
%license LICENSE
%{_datadir}/%{name}/test

%files plugins
%defattr(-,root,root)
%license dnsname-%{dnsnamevers}/LICENSE
%doc dnsname-%{dnsnamevers}/{README.md,README_PODMAN.md}
%dir %{_libexecdir}/cni
%{_libexecdir}/cni/dnsname

%files gvproxy
%defattr(-,root,root)
%license gvisor-tap-vsock/LICENSE
%doc gvisor-tap-vsock/README.md
%dir %{_libexecdir}/%{name}
%{_libexecdir}/%{name}/gvproxy

%changelog
* Thu Nov 24 2022 Shreenidhi Shedi <sshedi@vmware.com> 4.3.0-3
- Bump version as a part of cni upgrade
* Mon Nov 21 2022 Piyush Gupta <gpiyush@vmware.com> 4.3.0-2
- Bump up version to compile with new go
* Wed Nov 2 2022 Gerrit Photon <photon-checkins@vmware.com> 4.3.0-1
- Automatic Version Bump
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 4.2.1-2
- Bump up version to compile with new go
* Thu Oct 06 2022 Gerrit Photon <photon-checkins@vmware.com> 4.2.1-1
- Automatic Version Bump
* Fri Sep 02 2022 Nitesh Kumar <kunitesh@vmware.com> 4.2.0-1
- Initial version
