%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%if 0%{?fedora}
%global with_python3 1
%endif

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

%package -n     python2-%{pkg_name}
Summary:        OpenStack microversion header parser
%{?python_provide:%python_provide python2-%{pkg_name}}

BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
BuildRequires:  python2-pbr
BuildRequires:  python2-sphinx
# Required for testing and documentation generation
BuildRequires:  python2-gabbi
BuildRequires:  python2-hacking
BuildRequires:  python2-oslo-sphinx
BuildRequires:  python2-testrepository
BuildRequires:  python2-testtools
%if 0%{?fedora} || 0%{?rhel} > 7
BuildRequires:  python2-webob
Requires:       python2-webob
%else
BuildRequires:  python-webob
Requires:       python-webob
%endif

%description -n python2-%{pkg_name}
%{common_desc}

%if 0%{?with_python3}
%package -n     python3-%{pkg_name}
Summary:        OpenStack microversion header parser
%{?python_provide:%python_provide python3-%{pkg_name}}

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pbr
BuildRequires:  python3-sphinx
# Required for testing and documentation generation
BuildRequires:  python3-gabbi
BuildRequires:  python3-hacking
BuildRequires:  python3-oslo-sphinx
BuildRequires:  python3-testrepository
BuildRequires:  python3-testtools
BuildRequires:  python3-webob
Requires:       python3-webob
%description -n python3-%{pkg_name}
%{common_desc}
%endif

%package -n python-%{pkg_name}-doc
Summary:        microversion_parse documentation
%description -n python-%{pkg_name}-doc
Documentation for microversion_parse

%prep
%autosetup -n %{pypi_name}-%{upstream_version}
# Let RPM handle the requirements
rm -f {test-,}requirements.txt

%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

# generate html docs
sphinx-build doc/source html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}

%install
%if 0%{?with_python3}
%py3_install
%endif
%py2_install

%check
%if 0%{?with_python3}
%{__python3} setup.py test
rm -rf .testrepository
%endif
%{__python2} setup.py test


%files -n python2-%{pkg_name}
%doc README.rst
%license LICENSE
%{python2_sitelib}/%{pypi_name}
%{python2_sitelib}/%{pypi_name}-*.egg-info

%if 0%{?with_python3}
%files -n python3-%{pkg_name}
%doc README.rst
%license LICENSE
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-*.egg-info
%endif

%files -n python-%{pkg_name}-doc
%doc html
%license LICENSE

%changelog
* Thu Aug 16 2018 RDO <dev@lists.rdoproject.org> 0.2.1-1
- Update to 0.2.1

