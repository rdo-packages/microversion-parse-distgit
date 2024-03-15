%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0xbba3b1e67a7303dd1769d34595bf2e4d09004514
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
# we are excluding some BRs from automatic generator
%global excluded_brs doc8 bandit pre-commit hacking flake8-import-order

%global pypi_name microversion_parse
%global pkg_name microversion-parse

%global common_desc \
A simple parser for OpenStack microversion headers

Name:           python-%{pkg_name}
Version:        1.0.1
Release:        2%{?dist}
Summary:        OpenStack microversion header parser

License:        Apache-2.0
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

BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros

%description -n python3-%{pkg_name}
%{common_desc}

%package -n python-%{pkg_name}-doc
Summary:        microversion_parse documentation
%description -n python-%{pkg_name}-doc
Documentation for microversion_parse

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{pypi_name}-%{upstream_version}

sed -i /^[[:space:]]*-c{env:.*_CONSTRAINTS_FILE.*/d tox.ini
sed -i "s/^deps = -c{env:.*_CONSTRAINTS_FILE.*/deps =/" tox.ini
sed -i /^minversion.*/d tox.ini
sed -i /^requires.*virtualenv.*/d tox.ini
sed -i '/sphinx-build/ s/-W//' tox.ini

# Exclude some bad-known BRs
for pkg in %{excluded_brs};do
  for reqfile in doc/requirements.txt test-requirements.txt; do
    if [ -f $reqfile ]; then
      sed -i /^${pkg}.*/d $reqfile
    fi
  done
done

%generate_buildrequires
%pyproject_buildrequires -t -e %{default_toxenv},docs


%build
%pyproject_wheel

# generate html docs
%tox -e docs
# remove the sphinx-build-3 leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}

%install
%pyproject_install

%check
%tox -e %{default_toxenv}


%files -n python3-%{pkg_name}
%doc README.rst
%license LICENSE
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-*.dist-info

%files -n python-%{pkg_name}-doc
%doc doc/build/html
%license LICENSE

%changelog
* Fri Mar 15 2024 RDO <dev@lists.rdoproject.org> 1.0.1-2
- Rebuild 1.0.1 in Caracal

