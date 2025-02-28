%define apuver 1

Summary:    The Apache Portable Runtime Utility Library
Name:       apr-util
Version:    1.6.1
Release:    6%{?dist}
License:    Apache License 2.0
URL:        https://apr.apache.org
Group:      System Environment/Libraries
Vendor:     VMware, Inc.
Distribution: Photon

Source0:    http://archive.apache.org/dist/apr/%{name}-%{version}.tar.gz
%define sha512  %{name}=84da76e9b64da2de0996d4d6f3ab3f23db3724eb6352d218e0e8196bcc0b0a5d4fe791f41b4cc350ce3d04cce3bb3cf8bfb513d777d0cd030928368e6b55a536

BuildRequires:   apr-devel
BuildRequires:   sqlite-devel
BuildRequires:   openssl-devel
BuildRequires:   nss-devel
BuildRequires:   expat-devel
BuildRequires:   openldap
BuildRequires:   postgresql-devel >= 10.5

Requires:   apr
Requires:   openssl
Requires:   expat
Requires:   nss

%description
The Apache Portable Runtime Utility Library.

%package devel
Group: Development/Libraries
Summary: APR utility library development kit
Requires: apr-devel
Requires: expat-devel
Requires: %{name} = %{version}-%{release}
%description devel
This package provides the support files which can be used to
build applications using the APR utility library.

%package ldap
Group: Development/Libraries
Summary: APR utility library LDAP support
Requires: %{name} = %{version}-%{release}
Requires: openldap

%description ldap
This package provides the LDAP support for the %{name}.

%package pgsql
Group: Development/Libraries
Summary: APR utility library PostgreSQL DBD driver
Requires: %{name} = %{version}-%{release}
Requires: postgresql >= 10.5

%description pgsql
This package provides the PostgreSQL driver for the %{name} DBD (database abstraction) interface.

%package sqlite
Group: Development/Libraries
Summary: APR utility library SQLite DBD driver.
Requires: %{name} = %{version}-%{release}

%description sqlite
This package provides the SQLite driver for the %{name} DBD
(database abstraction) interface.

%prep
%autosetup -p1

%build
%configure --with-apr=%{_prefix} \
        --with-ldap \
        --without-gdbm \
        --with-sqlite3 \
        --with-pgsql \
        --without-sqlite2 \
        --with-openssl=%{_prefix} \
        --with-nss \
        --with-crypto

%make_build

%install
%make_install %{?_smp_mflags}

%if 0%{?with_check}
%check
# make doesn't support _smp_mflags
make check
%endif

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/aprutil.exp
%{_libdir}/libaprutil-%{apuver}.so.*
%{_libdir}/%{name}-%{apuver}/apr_crypto_nss*
%{_libdir}/%{name}-%{apuver}/apr_crypto_openssl*
%exclude %dir %{_libdir}/debug

%files devel
%defattr(-,root,root)
%{_libdir}/libaprutil-%{apuver}.*a
%{_libdir}/libaprutil-%{apuver}.so
%{_bindir}/*
%{_includedir}/*
%{_libdir}/pkgconfig/%{name}-%{apuver}.pc

%files ldap
%defattr(-,root,root,-)
%{_libdir}/%{name}-%{apuver}/apr_ldap*

%files pgsql
%defattr(-,root,root,-)
%{_libdir}/%{name}-%{apuver}/apr_dbd_pgsql*

%files sqlite
%defattr(-,root,root,-)
%{_libdir}/%{name}-%{apuver}/apr_dbd_sqlite*

%changelog
* Sat Jul 30 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.6.1-6
- Bump version as a part of sqlite upgrade
* Mon Feb 28 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.6.1-5
- Fix binary path
* Wed Aug 04 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.6.1-4
- Bump up release for openssl
* Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.6.1-3
- openssl 1.1.1
* Fri Sep 21 2018 Dweep Advani <dadvani@vmware.com> 1.6.1-2
- Consuming postgresql 10.5
* Tue Sep 18 2018 Ankit Jain <ankitja@vmware.com> 1.6.1-1
- Updated to version 1.6.1
* Mon Sep 18 2017 Rui Gu <ruig@vmware.com> 1.5.4-12
- Disable smp_flag on make check because of race condition
* Thu Jul 6 2017 Divya Thaluru <dthaluru@vmware.com> 1.5.4-11
- Added build requires on postgresql-devel
* Wed May 10 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.5.4-10
- Add missing Requires.
* Tue Apr 18 2017 Alexey Makhalov <amakhalov@vmware.com> 1.5.4-9
- Add expat-devel build deps otherwise it builds expat from its source tree
* Fri Nov 18 2016 Alexey Makhalov <amakhalov@vmware.com> 1.5.4-8
- Add sqlite-devel build deps
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.5.4-7
- GA - Bump release of all rpms
* Wed Apr 13 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.5.4-6
- remove libexpat files
* Tue Sep 22 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.5.4-5
- Updated build-requires after creating devel package for apr.
* Wed Sep 16 2015 Xiaolin Li <xiaolinl@vmware.com> 1.5.4-4
- Seperate Separate apr-util to apr-util, apr-util-devel, aprutil-ldap, apr-util-pgsql, and apr-utilsqlite.
* Wed Jul 15 2015 Sarah Choi <sarahc@vmware.com> 1.5.4-4
- Use apuver(=1) instead of version for mesos
* Mon Jul 13 2015 Alexey Makhalov <amakhalov@vmware.com> 1.5.2-3
- Exclude /usr/lib/debug
* Wed Jul 01 2015 Touseef Liaqat <tliaqat@vmware.com> 1.5.2-2
- Fix tags and paths.
* Wed May 20 2015 Touseef Liaqat <tliaqat@vmware.com> 1.5.4-1
- Initial build. First version
