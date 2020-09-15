#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests

Summary:	IPython kernel for Jupyter
Summary(pl.UTF-8):	Jądro IPythona dla Jupytera
Name:		python3-ipykernel
Version:	5.3.4
Release:	1
License:	BSD
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/ipykernel/
Source0:	https://files.pythonhosted.org/packages/source/i/ipykernel/ipykernel-%{version}.tar.gz
# Source0-md5:	d9ad6a4a4235940d65300e33f541edf5
URL:		https://pypi.org/project/ipykernel/
BuildRequires:	python3-jupyter_client
BuildRequires:	python3-modules >= 1:3.5
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-flaky
BuildRequires:	python3-ipython >= 5.0.0
BuildRequires:	python3-nose
BuildRequires:	python3-pytest
BuildRequires:	python3-pytest-cov
BuildRequires:	python3-traitlets >= 4.1.0
BuildRequires:	python3-tornado >= 4.2
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-sphinxcontrib_github_alt
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.5
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package provides the IPython kernel for Jupyter.

%description -l pl.UTF-8
Ten pakiet dostarcza jądro IPythona dla Jupytera.

%package apidocs
Summary:	API documentation for Python ipykernel module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona ipykernel
Group:		Documentation

%description apidocs
API documentation for Python ipykernel module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona ipykernel.

%prep
%setup -q -n ipykernel-%{version}

%build
%py3_build

%if %{with tests}
PYTHONPATH=$(pwd) \
%{__python3} -m pytest ipykernel
%endif

%if %{with doc}
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

install -d $RPM_BUILD_ROOT%{_examplesdir}/python3-ipykernel-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/python3-ipykernel-%{version}
find $RPM_BUILD_ROOT%{_examplesdir}/python3-ipykernel-%{version} -name '*.py' \
	| xargs sed -i '1s|/usr/bin/env python|%{__python3}|'

%{__rm} -r $RPM_BUILD_ROOT%{py3_sitescriptdir}/ipykernel/tests \
	$RPM_BUILD_ROOT%{py3_sitescriptdir}/ipykernel/inprocess/tests

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc COPYING.md README.md
%{py3_sitescriptdir}/ipykernel
%{py3_sitescriptdir}/ipykernel_launcher.py
%{py3_sitescriptdir}/__pycache__/ipykernel_launcher.cpython-*.py[co]
%{py3_sitescriptdir}/ipykernel-%{version}-py*.egg-info
%dir %{_datadir}/jupyter
%dir %{_datadir}/jupyter/kernels
%{_datadir}/jupyter/kernels/python3
%{_examplesdir}/python3-ipykernel-%{version}

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,*.html,*.js}
%endif
