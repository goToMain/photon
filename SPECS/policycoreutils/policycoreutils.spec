Summary:        SELinux policy core utilities
Name:           policycoreutils
Version:        3.3
Release:        1%{?dist}
License:        Public Domain
Group:          System Environment/Libraries
Url:            https://github.com/SELinuxProject/selinux/wiki
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://github.com/SELinuxProject/selinux/releases/download/%{version}/%{name}-%{version}.tar.gz
%define sha512  %{name}=db658990355f99a8e43f53d20cc67bf9e557b0a7837d1927c80f325b7f93ad47876382278a980b818484d6e31712a9b03e279f947ebc88c4be60a9f395607f98

BuildRequires:  libsemanage-devel = %{version}

Requires:       libsemanage = %{version}

%description
policycoreutils contains the policy core utilities that are required for
basic operation of a SELinux system.

%prep
%autosetup -p1

%build
make %{?_smp_mflags}

%install
make DESTDIR="%{buildroot}" LIBDIR="%{_libdir}" SHLIBDIR="%{_lib}" \
     BINDIR="%{_bindir}" SBINDIR="%{_sbindir}" %{?_smp_mflags} install

rm -rf %{buildroot}%{_datadir}/locale \
       %{buildroot}%{_mandir}/ru

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_sbindir}/*
%{_libexecdir}/*
%{_sysconfdir}/sestatus.conf
%{_datadir}/bash-completion/*
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man8/*

%changelog
* Fri Apr 08 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.3-1
- Upgrade v3.3
* Fri Sep 03 2021 Vikash Bansal <bvikas@vmware.com> 3.2-1
- Update to version 3.2
* Thu Jul 23 2020 Gerrit Photon <photon-checkins@vmware.com> 3.1-1
- Automatic Version Bump
* Sat Apr 18 2020 Alexey Makhalov <amakhalov@vmware.com> 3.0-1
- Initial build.
