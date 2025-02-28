Name:           python3-wheel
Version:        0.37.1
Release:        1%{?dist}
Summary:        A built-package format for Python
License:        MIT
URL:            https://pypi.org/project/wheel
Source0:        https://github.com/pypa/wheel/archive/%{version}.tar.gz#/wheel-%{version}.tar.gz
%define sha512  wheel=c977a740c17abd1fa4b4c2382a33f3ff887baa4231c36990d988cb8531496074e39744786ef6ac0da9c9af4977bce5b2da145377a3ac15eea918f8125bff66ec
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

Requires:       python3
Provides:       python%{python3_version}dist(wheel) = %{version}-%{release}
%description
This library is the reference implementation of the Python wheel packaging standard, as defined in PEP 427.
It has two different roles. Firstly a setuptools extension for building wheels that provides the bdist_wheel setuptools command
Secondly, a command line tool for working with wheel files

%prep
%autosetup -p1 -n wheel-%{version}

%build
%py3_build

%install
%py3_install

%if %{with check}
%check
python3 setup.py test
%endif

%files
%defattr(-,root,root,-)
%{_bindir}/wheel
%{python3_sitelib}/*
%doc README.rst
%license LICENSE.txt

%changelog
* Mon Oct 10 2022 Prashant S Chauhan <psinghchauha@vmware.com> 0.37.1-1
- Initial Build
