Summary:        GD is an open source code library for the dynamic creation of images by programmers.
Name:           libgd
Version:        2.2.5
Release:        10%{?dist}
License:        MIT
URL:            https://libgd.github.io/
Group:          System/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/libgd/libgd/releases/download/gd-%{version}/%{name}-%{version}.tar.xz
%define sha1    libgd=b777b005c401b6fa310ccf09eeb29f6c6e17ab2c
Source1:        %{name}-tests.tar.gz
%define sha1    libgd-tests=86e16395e4dc7de3e8c471f8675c7403dda33aea
Patch0:         CVE-2018-1000222.patch
Patch1:         libgd-CVE-2019-6978.patch
Patch2:         libgd-CVE-2019-6977.patch
Patch3:         libgd-CVE-2018-14553.patch
Patch4:         libgd-CVE-2017-6363.patch
Patch5:         libgd-CVE-2019-11038.patch
Patch6:         libgd-CVE-2019-11038-testcase.patch
Patch7:         libgd-CVE-2021-38115.patch
Patch8:         libgd-CVE-2021-40145.patch
BuildRequires:  libjpeg-turbo-devel
BuildRequires:  libpng-devel
BuildRequires:  libwebp-devel
BuildRequires:  libtiff-devel
Requires:       libpng
Requires:       libwebp
Requires:       libtiff
Requires:       libjpeg-turbo
Provides:       pkgconfig(libgd)
%description
GD is an open source code library for the dynamic creation of images by programmers.

GD is written in C, and "wrappers" are available for Perl, PHP and other languages. GD can read and write many different image formats. GD is commonly used to generate charts, graphics, thumbnails, and most anything else, on the fly.
%package    devel
Summary:    Header and development files
Requires:   %{name} = %{version}-%{release}
%description    devel
Header & Development files
%prep
%autosetup -N -a0
tar xf %{SOURCE1} --no-same-owner
cp libgd-tests/bug00383.gd tests/gd/
cp libgd-tests/bug00383.gd2 tests/gd2/
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1

%build
# To use the system installed automake latest version instead of given version in source
autoreconf -fi
%configure --with-webp --with-tiff --with-jpeg --with-png --disable-werror --disable-static
make %{?_smp_mflags}
%install
%make_install

%check
make %{?_smp_mflags} -k check

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/libgd.so.*
%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.la
%{_libdir}/libgd.so
%{_libdir}/pkgconfig/*

%changelog
*   Mon Mar 21 2022 Harinadh D <hdommaraju@vmware.com>  2.2.5-10
-   Version bump up to use libtiff 4.3.0
*   Wed Sep 08 2021 Nitesh Kumar <kunitesh@vmware.com>  2.2.5-9
-   Fix for CVE-2021-40145
*   Thu Aug 26 2021 Nitesh Kumar <kunitesh@vmware.com>  2.2.5-8
-   Fix for CVE-2021-38115
*   Mon Nov 02 2020 Piyush Gupta <gpiyush@vmware.com>  2.2.5-7
-   Fix for CVE-2019-11038
*   Tue Mar 10 2020 Ankit Jain <ankitja@vmware.com>  2.2.5-6
-   Fix for CVE-2017-6363
*   Tue Feb 18 2020 Ankit Jain <ankitja@vmware.com>  2.2.5-5
-   Fix for CVE-2018-14553
*   Tue Feb 19 2019 Ankit Jain <ankitja@vmware.com>  2.2.5-4
-   Fix for CVE-2019-6977
*   Wed Jan 30 2019 Ankit Jain <ankitja@vmware.com>  2.2.5-3
-   Fix for CVE-2019-6978
*   Fri Nov 02 2018 Ankit Jain <ankitja@vmware.com>  2.2.5-2
-   Fix for CVE-2018-1000222
*   Tue Oct 10 2017 Alexey Makhalov <amakhalov@vmware.com> 2.2.5-1
-   Updated to version 2.2.5 to address CVE-2017-6362
*   Tue Jan 31 2017 Xiaolin Li <xiaolinl@vmware.com> 2.2.4-1
-   Updated to version 2.2.4.
*   Wed Jan 18 2017 Kumar Kaushik <kaushikk@vmware.com>  2.2.3-3
-   Fix for CVE-2016-8670
*   Fri Oct 07 2016 Anish Swaminathan <anishs@vmware.com>  2.2.3-2
-   Fix for CVE-2016-7568
*   Thu Jul 28 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 2.2.3-1
-   Initial version
