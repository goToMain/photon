Summary:        The Sysstat package contains utilities to monitor system performance and usage activity
Name:           sysstat
Version:        12.6.0
Release:        1%{?dist}
License:        GPLv2
URL:            http://sebastien.godard.pagesperso-orange.fr/
Group:          Development/Debuggers
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://perso.wanadoo.fr/sebastien.godard/%{name}-%{version}.tar.xz
%define sha512  sysstat=e85e4e46e9218ee3263cc287a7664997a8a71a5be0bef080b7930b83b94ce1b3b488acc399b5b981591cf1c4ff56b660b7aa0de8ba81306766f2bb30e136f348
Patch0:         sysstat.sysconfig.in.patch
BuildRequires:  cronie
Requires:       cronie

%description
The Sysstat package contains utilities to monitor system performance and usage activity. Sysstat contains the sar utility, common to many commercial Unixes, and tools you can schedule via cron to collect and historize performance and activity data.

%prep
%autosetup -p1

%build
%configure \
            --enable-install-cron \
            --enable-copy-only \
            --disable-file-attr \
            sa_lib_dir=%{_libdir}/sa \
            --disable-stripping
make %{?_smp_mflags}

%install
make install %{?_smp_mflags}
mkdir -p %{buildroot}/usr/lib/systemd/system/
install -D -m 0644 %{_builddir}/%{name}-%{version}/sysstat.service %{buildroot}/usr/lib/systemd/system/
install -D -m 0644 %{_builddir}/%{name}-%{version}/cron/sysstat-summary.timer %{buildroot}/usr/lib/systemd/system/
install -D -m 0644 %{_builddir}/%{name}-%{version}/cron/sysstat-summary.service %{buildroot}/usr/lib/systemd/system/
install -D -m 0644 %{_builddir}/%{name}-%{version}/cron/sysstat-collect.timer %{buildroot}/usr/lib/systemd/system/
install -D -m 0644 %{_builddir}/%{name}-%{version}/cron/sysstat-collect.service %{buildroot}/usr/lib/systemd/system/

%find_lang %{name}

%check
make test %{?_smp_mflags}

%clean
rm -rf %{buildroot}/*

%files -f %{name}.lang
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/sysconfig/*
%config(noreplace) %{_sysconfdir}/cron.d/*
%exclude %{_sysconfdir}/rc.d/init.d/sysstat
%{_bindir}/*
%{_libdir}/sa/*
%{_datadir}/doc/%{name}-%{version}/*
%{_mandir}/man*/*
%{_libdir}/systemd/system/*

%changelog
*   Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 12.6.0-1
-   Automatic Version Bump
*   Tue Apr 19 2022 Gerrit Photon <photon-checkins@vmware.com> 12.5.6-1
-   Automatic Version Bump
*   Mon Jul 27 2020 Gerrit Photon <photon-checkins@vmware.com> 12.4.0-1
-   Automatic Version Bump
*   Mon Dec 16 2019 Shreyas B. <shreyasb@vmware.com> 12.2.0-1
-   Update to 12.2.0 & fix CVE-2019-19725.
*   Wed Nov 20 2019 Shreyas B. <shreyasb@vmware.com> 12.1.6-2
-   Fix System Config Issue get SAR logs - Bug 2460236
*   Wed Oct 09 2019 Shreyas B. <shreyasb@vmware.com> 12.1.6-1
-   Update to 12.1.6 to fix CVE-2019-16167.
*   Thu Jan 03 2019 Keerthana K <keerthanak@vmware.com> 12.1.2-1
-   Update to 12.1.2 to fix CVEs.
*   Mon Sep 17 2018 Tapas Kundu <tkundu@vmware.com> 12.0.1-1
-   Updated to 12.0.1 release
*   Thu Apr 27 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 11.4.3-2
-   Ensure debuginfo
*   Tue Apr 11 2017 Vinay Kulkarni <kulkarniv@vmware.com> 11.4.3-1
-   Update to version 11.4.3
*   Thu Jan 05 2017 Xiaolin Li <xiaolinl@vmware.com> 11.4.2-1
-   Updated to version 11.4.2 and enable install cron.
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 11.2.0-3
-   GA - Bump release of all rpms
*   Wed May 4 2016 Divya Thaluru <dthaluru@vmware.com> 11.2.0-2
-   Adding systemd service file
*   Wed Jan 20 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 11.2.0-1
-   Update to 11.2.0-1.
*   Mon Nov 30 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 11.1.8-1
-   Initial build.  First version.
