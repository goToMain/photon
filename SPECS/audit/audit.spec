%define with_golang 0

Summary:        Kernel Audit Tool
Name:           audit
Version:        3.0.9
Release:        1%{?dist}
License:        GPLv2+
Group:          System Environment/Security
URL:            http://people.redhat.com/sgrubb/audit
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        http://people.redhat.com/sgrubb/audit/%{name}-%{version}.tar.gz
%define sha512  %{name}=5219eb0b41746eca3406008a97731c0083e7be50ec88563a39537de22cb69fe88490f5fe5a11535930f360b11a62538e2ff6cbe39e059cd760038363954ef4d6

BuildRequires:  krb5-devel
BuildRequires:  openldap
BuildRequires:  tcp_wrappers-devel
BuildRequires:  libcap-ng-devel
BuildRequires:  swig
BuildRequires:  e2fsprogs-devel
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  systemd-devel

%if 0%{?with_golang}
BuildRequires:  go
%endif

Requires:       systemd
Requires:       krb5
Requires:       openldap
Requires:       tcp_wrappers
Requires:       libcap-ng
Requires:       gawk

%description
The audit package contains the user space utilities for
storing and searching the audit records generate by
the audit subsystem in the Linux 2.6 kernel.

%package        devel
Summary:        The libraries and header files needed for audit development.
Requires:       %{name} = %{version}-%{release}

%description    devel
The libraries and header files needed for audit development.

%package  -n    python3-audit
Summary:        Python3 bindings for libaudit
License:        LGPLv2+
Requires:       %{name} = %{version}-%{release}
Requires:       python3

%description -n python3-audit
The python3-audit package contains the python2 bindings for libaudit
and libauparse.

%prep
%autosetup -p1

%build
%configure \
    $(test %{_host} != %{_build} && echo "--with-sysroot=/target-%{_arch}") \
    --exec_prefix=%{_usr} \
    --with-python3=yes \
    --with-libwrap \
    --enable-gssapi-krb5=yes \
    --with-libcap-ng=yes \
    --with-aarch64 \
    --enable-zos-remote \
%if 0%{?with_golang}
    --with-golang \
%endif
    --enable-systemd \
    --disable-static

%make_build

%install
mkdir -p %{buildroot}/{etc/audispd/plugins.d,etc/audit/rules.d}
mkdir -p %{buildroot}/%{_var}/opt/audit/log
mkdir -p %{buildroot}/%{_var}/log
mkdir -p %{buildroot}/%{_var}/spool/audit
ln -sfv %{_var}/opt/audit/log %{buildroot}/%{_var}/log/audit
%make_install

install -vdm755 %{buildroot}%{_libdir}/systemd/system-preset
echo "disable auditd.service" > %{buildroot}%{_libdir}/systemd/system-preset/50-auditd.preset

%check
make %{?_smp_mflags} check

%post
/sbin/ldconfig
%systemd_post  auditd.service

%postun
/sbin/ldconfig
%systemd_postun_with_restart auditd.service

%preun
%systemd_preun auditd.service

%files
%defattr(-,root,root)
%{_bindir}/*
%{_sbindir}/*
%{_libdir}/*.so.*
%{_unitdir}/auditd.service
%{_presetdir}/50-auditd.preset
%{_libexecdir}/*
%{_mandir}/man5/*
%{_mandir}/man7/*
%{_mandir}/man8/*
%dir %{_var}/opt/audit/log
%{_var}/log/audit
%{_var}/spool/audit
%attr(750,root,root) %dir %{_sysconfdir}/audit
%attr(750,root,root) %dir %{_sysconfdir}/audit/rules.d

%attr(750,root,root) %dir %{_sysconfdir}/audispd
%attr(750,root,root) %dir %{_sysconfdir}/audispd/plugins.d
%config(noreplace) %attr(640,root,root) %{_sysconfdir}/audit/auditd.conf
%config(noreplace) %attr(640,root,root) %{_sysconfdir}/audit/audisp-remote.conf
%config(noreplace) %attr(640,root,root) %{_sysconfdir}/audit/zos-remote.conf
%config(noreplace) %attr(640,root,root) %{_sysconfdir}/audit/plugins.d/*.conf
%ghost %config(noreplace) %attr(640,root,root) %{_sysconfdir}/audit/rules.d/audit.rules
%ghost %config(noreplace) %attr(640,root,root) %{_sysconfdir}/audit/audit.rules
%ghost %config(noreplace) %attr(640,root,root) %{_sysconfdir}/audit/audit-stop.rules
%ghost %config(noreplace) %attr(640,root,root) %{_datadir}/audit/sample-rules/*.rules
%ghost %config(noreplace) %attr(640,root,root) %{_datadir}/audit/sample-rules/README-rules
%config(noreplace) %attr(640,root,root) %{_sysconfdir}/libaudit.conf

%files devel
%defattr(-,root,root)
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%if 0%{?with_golang}
%{_libdir}/golang/*
%endif
%{_includedir}/*.h
%{_mandir}/man3/*
%{_datadir}/aclocal/audit.m4

%files -n python3-audit
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Thu Dec 01 2022 Harinadh D <hdommaraju@vmware.com> 3.0.9-1
- Version update
* Mon Nov 21 2022 Piyush Gupta <gpiyush@vmware.com> 3.0.8-5
- Bump up version to compile with new go
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 3.0.8-4
- Bump up version to compile with new go
* Sun Aug 07 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.0.8-3
- Remove .la files
* Fri Jun 17 2022 Piyush Gupta <gpiyush@vmware.com> 3.0.8-2
- Bump up version to compile with new go
* Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 3.0.8-1
- Automatic Version Bump
* Fri Jun 11 2021 Piyush Gupta <gpiyush@vmware.com> 3.0.1-2
- Bump up version to compile with new go
* Mon Apr 12 2021 Gerrit Photon <photon-checkins@vmware.com> 3.0.1-1
- Automatic Version Bump
* Fri Feb 05 2021 Harinadh D <hdommaraju@vmware.com> 2.8.5-6
- Bump up version to compile with new go
* Thu Jan 21 2021 Alexey Makhalov <amakhalov@vmware.com> 2.8.5-5
- GCC-10 support
* Fri Jan 15 2021 Piyush Gupta<gpiyush@vmware.com> 2.8.5-4
- Bump up version to compile with new go
* Mon Jun 22 2020 Tapas Kundu <tkundu@vmware.com> 2.8.5-3
- Mass removal python2
* Tue Nov 26 2019 Alexey Makhalov <amakhalov@vmware.com> 2.8.5-2
- Cross compilation support.
- Do not use BuildRequires in subpackages.
- Disable golang dependency.
* Thu Oct 17 2019 Shreyas B <shreyasb@vmware.com> 2.8.5-1
- Updated to version 2.8.5.
* Mon Sep 3 2018 Keerthana K <keerthanak@vmware.com> 2.8.4-1
- Updated to version 2.8.4.
* Thu Dec 28 2017 Divya Thaluru <dthaluru@vmware.com>  2.7.5-4
- Fixed the log file directory structure
* Thu Jun 29 2017 Divya Thaluru <dthaluru@vmware.com>  2.7.5-3
- Disabled audit service by default
* Thu May 18 2017 Xiaolin Li <xiaolinl@vmware.com> 2.7.5-2
- Move python2 requires to python subpackage and added python3.
* Fri Apr 14 2017 Alexey Makhalov <amakhalov@vmware.com> 2.7.5-1
- Version update.
* Wed Dec 07 2016 Xiaolin Li <xiaolinl@vmware.com> 2.5-7
- Moved man3 to devel subpackage.
* Thu Nov 24 2016 Alexey Makhalov <amakhalov@vmware.com> 2.5-6
- Required krb5-devel.
* Fri Jul 22 2016 Xiaolin Li <xiaolinl@vmware.com> 2.5-5
- Add gawk requirement.
* Thu May 26 2016 Divya Thaluru <dthaluru@vmware.com>  2.5-4
- Fixed logic to restart the active services after upgrade
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.5-3
- GA - Bump release of all rpms
* Tue May 3 2016 Divya Thaluru <dthaluru@vmware.com>  2.5-2
- Fixing spec file to handle rpm upgrade scenario correctly
* Tue Feb 23 2016 Anish Swaminathan <anishs@vmware.com>  2.5-1
- Upgrade to 2.5
* Fri Jan 29 2016 Anish Swaminathan <anishs@vmware.com>  2.4.4-4
- Add directories for auditd service.
* Tue Jan 12 2016 Anish Swaminathan <anishs@vmware.com>  2.4.4-3
- Change config file attributes.
* Wed Dec 09 2015 Anish Swaminathan <anishs@vmware.com> 2.4.4-2
- Add systemd requirement.
* Fri Aug 28 2015 Divya Thaluru <dthaluru@vmware.com> 2.4.4-1
- Initial version
