Summary:        Libbpf library
Name:           libbpf
Version:        1.0.1
Release:        1%{?dist}
Group:          Development/System
Vendor:         VMware, Inc.
Distribution:   Photon
License:        GPL-2.1 OR BSD-2-Clause
URL:            https://github.com/libbpf/libbpf

Source0: https://github.com/libbpf/libbpf/archive/refs/tags/libbpf-%{version}.tar.gz
%define sha512 %{name}=2ee6d85c0a33f723e5b93ddddf97118e67754c9e44ca0449ceb49126820f89fea9ddc282a5add764dc4da090af6164cc6641b497489253d192ed01bc397df9be

BuildRequires:  elfutils-libelf-devel
BuildRequires:  elfutils-devel

Requires:       elfutils-libelf
Requires:       elfutils

%description
Library for loading eBPF programs and reading and manipulating eBPF objects from user-space

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}

%description    devel
The libbpf-devel package contains libraries header files for
developing applications that use libbpf.

%prep
%autosetup -p1

%build
%make_build -C ./src DESTDIR=%{buildroot} OBJDIR=%{_builddir} LIBDIR=%{_libdir} %{?_smp_mflags}

%install
%make_install -C ./src DESTDIR=%{buildroot} OBJDIR=%{_builddir} LIBDIR=%{_libdir} %{?_smp_mflags}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_libdir}/libbpf.so.*

%files devel
%defattr(-,root,root)
%{_libdir}/libbpf.so
%attr(0644,-,-) %{_includedir}/bpf/*
%attr(0644,-,-) %{_libdir}/libbpf.a
%attr(0644,-,-) %{_libdir}/pkgconfig/libbpf.pc

%changelog
* Fri Dec 02 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.0.1-1
- Upgrade to v1.0.1
* Wed Sep 28 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.0.0-1
- Upgrade to v1.0.0
* Mon Feb 21 2022 Mukul Sikka <msikka@vmware.com> 0.6.1-2
- Fix build error in aarch64 platform
* Wed Jan 12 2022 Susant Sahani <ssahani@vmware.com> 0.6.1-1
- Version Bump
* Thu Apr 29 2021 Gerrit Photon <photon-checkins@vmware.com> 0.3-1
- Automatic Version Bump
* Fri Oct 16 2020 Michelle Wang <michellew@vmware.com> 0.1.1-2
- Fix build error in aarch64 platform
* Mon Oct 05 2020 Gerrit Photon <photon-checkins@vmware.com> 0.1.1-1
- Automatic Version Bump
* Wed Sep 09 2020 Susant Sahani <ssahani@vmware.com>  0.1.0-1
- Initial release
