%global debug_package %{nil}

Summary:        Ultra fast JSON encoder and decoder written in pure C
Name:           python3-ujson
Version:        5.4.0
Release:        1%{?dist}
Group:          Development/Tools
License:        BSD
Vendor:         VMware, Inc.
Distribution:   Photon

URL:            https://pypi.org/project/ujson
Source0:        https://files.pythonhosted.org/packages/fb/94/44fbbb059fe5d295f1f73e731a0b9c2e1b5073c2c6b58bb9c068715e9b72/ujson-%{version}.tar.gz
%define sha512  ujson=9622e872391d5467455b32e324d7b680487664ca486bfc56ba8c3969853e5db94725cd45e81b535dca80af4a3c718af171ce7adb6dcb9b98a37a8068824f89c6

BuildRequires:  double-conversion-devel
BuildRequires:  python3-devel
BuildRequires:  python3-pytest
BuildRequires:  python3-setuptools
BuildRequires:  python3-pip

Requires:       python3

%description
UltraJSON is an ultra fast JSON encoder and decoder written in pure C with bindings for Python.

%prep
%autosetup -p1 -n ujson-%{version}

%build
python3 -m pip wheel --disable-pip-version-check --verbose .

%install
python3 -m pip install --root %{buildroot} --prefix %{_prefix} --disable-pip-version-check --verbose .

%check
%pytest -v

%files
%defattr(-,root,root)
%license LICENSE.txt
%doc README.md
%{python3_sitearch}/ujson-%{version}.dist-info/
%{python3_sitearch}/ujson*.so

%changelog
* Thu Sep 1 2022 Nitesh Kumar <kunitesh@vmware.com> - 5.4.0-1
- Initial version, Needed by python3-pydantic
