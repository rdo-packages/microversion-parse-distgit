# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif
%global pyver_bin python%{pyver}
%global pyver_sitelib %{expand:%{python%{pyver}_sitelib}}
%global pyver_install %{expand:%{py%{pyver}_install}}
%global pyver_build %{expand:%{py%{pyver}_build}}
# End of macros for py2/py3 compatibility
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global pypi_name microversion_parse
%global pkg_name microversion-parse

%global common_desc \
A simple parser for OpenStack microversion headers

Name:           python-%{pkg_name}
Version:        0.2.1
Release:        1%{?dist}
Summary:        OpenStack microversion header parser

License:        ASL 2.0
URL:            http://www.openstack.org/
Source0:        https://tarballs.openstack.org/%{pkg_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch


%description
%{common_desc}

%package -n     python%{pyver}-%{pkg_name}
Summary:        OpenStack microversion header parser
%{?python_provide:%python_provide python%{pyver}-%{pkg_name}}

BuildRequires:  python%{pyver}-devel
BuildRequires:  python%{pyver}-setuptools
BuildRequires:  python%{pyver}-pbr
BuildRequires:  python%{pyver}-sphinx
# Required for testing and documentation generation
BuildRequires:  python%{pyver}-gabbi
BuildRequires:  python%{pyver}-hacking
BuildRequires:  python%{pyver}-oslo-sphinx
BuildRequires:  python%{pyver}-testrepository
BuildRequires:  python%{pyver}-testtools
BuildRequires:  python%{pyver}-webob

Requires:       python%{pyver}-webob

%description -n python%{pyver}-%{pkg_name}
%{common_desc}

%package -n python-%{pkg_name}-doc
Summary:        microversion_parse documentation
%description -n python-%{pkg_name}-doc
Documentation for microversion_parse

%prep
%autosetup -n %{pypi_name}-%{upstream_version}
# Let RPM handle the requirements
rm -f {test-,}requirements.txt

%build
%{pyver_build}

# generate html docs
sphinx-build-%{pyver} doc/source html
# remove the sphinx-build-%{pyver} leftovers
rm -rf html/.{doctrees,buildinfo}

%install
%{pyver_install}

%check
%{pyver_bin} setup.py test


%files -n python%{pyver}-%{pkg_name}
%doc README.rst
%license LICENSE
%{pyver_sitelib}/%{pypi_name}
%{pyver_sitelib}/%{pypi_name}-*.egg-info

%files -n python-%{pkg_name}-doc
%doc html
%license LICENSE

%changelog
* Fri Sep 20 2019 RDO <dev@lists.rdoproject.org> 0.2.1-1
- Update to 0.2.1

