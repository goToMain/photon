Summary:        X11 libXtst runtime library.
Name:           libXtst
Version:        1.2.3
Release:        1%{?dist}
License:        MIT
URL:            http://www.x.org
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://ftp.x.org/pub/individual/lib/%{name}-%{version}.tar.bz2
%define sha512 %{name}=6f6741fd3596775eaa056465319f78c29c91b3893a851a4899df651a2023a4d762497b112a33d7d3e8865fe85d173d03e4b49daef76a66af1ae1eaab82a12765

BuildRequires:  libXi-devel
BuildRequires:  proto

Requires:       libXi
Requires:       libXext
Requires:       libX11

%description
The X11 libXtst runtime library.

%package        devel
Summary:        Header and development files
Requires:       %{name} = %{version}-%{release}
Requires:       libXi-devel

%description    devel
It contains the libraries and header files to create applications

%prep
%autosetup

%build
%configure
%make_build

%install
%make_install %{?_smp_mflags}

%ldconfig_scriptlets

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig
%{_libdir}/*.a
%{_datadir}/*

%changelog
* Fri Aug 19 2022 Shivani Agarwal <shivania2@vmware.com> 1.2.3-1
- Upgrade version 1.2.3
* Tue May 19 2015 Alexey Makhalov <amakhalov@vmware.com> 1.2.2-1
- initial version
