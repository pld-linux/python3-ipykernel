#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests

Summary:	IPython kernel for Jupyter
Summary(pl.UTF-8):	Jądro IPythona dla Jupytera
Name:		python3-ipykernel
Version:	7.1.0
Release:	1
License:	BSD
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/ipykernel/
Source0:	https://files.pythonhosted.org/packages/source/i/ipykernel/ipykernel-%{version}.tar.gz
# Source0-md5:	6bce3b380b3cafbb89b84068bec1bcd2
URL:		https://pypi.org/project/ipykernel/
BuildRequires:	python3-build
BuildRequires:	python3-hatchling >= 1.22
BuildRequires:	python3-installer
BuildRequires:	python3-jupyter_client >= 6
BuildRequires:	python3-modules >= 1:3.10
%if %{with tests}
BuildRequires:	python3-comm >= 0.1.1
BuildRequires:	python3-debugpy >= 1.6.5
BuildRequires:	python3-flaky
BuildRequires:	python3-ipyparallel
BuildRequires:	python3-ipython >= 7.23.1
BuildRequires:	python3-jedi
BuildRequires:	python3-jupyter_client >= 8.0.0
BuildRequires:	python3-jupyter_core >= 4.12
BuildRequires:	python3-matplotlib_inline >= 0.1.0
BuildRequires:	python3-nest-asyncio >= 1.4
BuildRequires:	python3-packaging >= 22
BuildRequires:	python3-psutil >= 5.7
BuildRequires:	python3-pytest >= 7.0
BuildRequires:	python3-pytest-asyncio >= 0.23.5
BuildRequires:	python3-pytest-cov
BuildRequires:	python3-pytest-timeout
BuildRequires:	python3-traitlets >= 5.4.0
BuildRequires:	python3-tornado >= 6.2
BuildRequires:	python3-zmq >= 25
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-intersphinx_registry
BuildRequires:	python3-myst_parser
BuildRequires:	python3-pydata_sphinx_theme
BuildRequires:	python3-sphinx_autodoc_typehints
BuildRequires:	python3-sphinxcontrib_github_alt
BuildRequires:	python3-sphinxcontrib-spelling
BuildRequires:	python3-trio
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.10
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
%py3_build_pyproject

%if %{with tests}
%{__python3} -m zipfile -e build-3/*.whl build-3-test
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS=flaky.flaky_pytest_plugin,pytest_asyncio.plugin,pytest_timeout \
%{__python3} -m pytest -o pythonpath="$PWD/build-3-test" tests
%endif

%if %{with doc}
PYTHONPATH=$(pwd) \
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

install -d $RPM_BUILD_ROOT%{_examplesdir}/python3-ipykernel-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/python3-ipykernel-%{version}
find $RPM_BUILD_ROOT%{_examplesdir}/python3-ipykernel-%{version} -name '*.py' \
	| xargs sed -i '1s|/usr/bin/env python|%{__python3}|'

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGELOG.md  CONTRIBUTING.md README.md RELEASE.md
%{py3_sitescriptdir}/ipykernel
%{py3_sitescriptdir}/ipykernel_launcher.py
%{py3_sitescriptdir}/__pycache__/ipykernel_launcher.cpython-*.py[co]
%{py3_sitescriptdir}/ipykernel-%{version}.dist-info
%dir %{_datadir}/jupyter
%dir %{_datadir}/jupyter/kernels
%{_datadir}/jupyter/kernels/python3
%{_examplesdir}/python3-ipykernel-%{version}

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,api,*.html,*.js}
%endif
