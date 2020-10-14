%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global pypi_name microversion_parse
%global pkg_name microversion-parse

%global common_desc \
A simple parser for OpenStack microversion headers

Name:           python-%{pkg_name}
Version:        XXX
Release:        XXX
Summary:        OpenStack microversion header parser

License:        ASL 2.0
URL:            http://www.openstack.org/
Source0:        https://tarballs.openstack.org/%{pkg_name}/%{pypi_name}-%{version}.tar.gz
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.openstack.org/%{pkg_name}/%{pypi_name}-%{version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif
BuildArch:      noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
BuildRequires:  openstack-macros
%endif


%description
%{common_desc}

%package -n     python3-%{pkg_name}
Summary:        OpenStack microversion header parser
%{?python_provide:%python_provide python3-%{pkg_name}}

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pbr
# Required for testing and documentation generation
BuildRequires:  python3-gabbi
BuildRequires:  python3-hacking
BuildRequires:  python3-testrepository
BuildRequires:  python3-testtools
BuildRequires:  python3-webob

Requires:       python3-webob

%description -n python3-%{pkg_name}
%{common_desc}

%package -n python-%{pkg_name}-doc
Summary:        microversion_parse documentation
BuildRequires:  python3-sphinx
BuildRequires:  python3-openstackdocstheme
%description -n python-%{pkg_name}-doc
Documentation for microversion_parse

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{pypi_name}-%{upstream_version}
# Let RPM handle the requirements
rm -f {test-,}requirements.txt

%build
%{py3_build}

# generate html docs
sphinx-build-3 doc/source html
# remove the sphinx-build-3 leftovers
rm -rf html/.{doctrees,buildinfo}

%install
%{py3_install}

%check
%{__python3} setup.py test


%files -n python3-%{pkg_name}
%doc README.rst
%license LICENSE
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-*.egg-info

%files -n python-%{pkg_name}-doc
%doc html
%license LICENSE

%changelog
