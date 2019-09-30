#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

Summary:	IPython kernel for Jupyter
Summary(pl.UTF-8):	Jądro IPythona dla Jupytera
Name:		python-ipykernel
Version:	4.10.1
Release:	2
License:	BSD
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/ipykernel/
Source0:	https://files.pythonhosted.org/packages/source/i/ipykernel/ipykernel-%{version}.tar.gz
# Source0-md5:	23871bb7da2907749cb65a9446c9e637
Patch0:		%{name}-use_setuptools.patch
URL:		https://pypi.org/project/ipykernel/
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-ipython >= 4.0.0
BuildRequires:	python-jupyter_client
BuildRequires:	python-mock
BuildRequires:	python-nose
BuildRequires:	python-pytest
BuildRequires:	python-pytest-cov
BuildRequires:	python-traitlets >= 4.1.0
BuildRequires:	python-tornado >= 4.0
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.4
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-ipython >= 4.0.0
BuildRequires:	python3-jupyter_client
BuildRequires:	python3-nose
BuildRequires:	python3-pytest
BuildRequires:	python3-pytest-cov
BuildRequires:	python3-traitlets >= 4.1.0
BuildRequires:	python3-tornado >= 4.0
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	sed >= 4.0
%if %{with doc}
BuildRequires:	python3-sphinxcontrib_github_alt
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python-modules >= 1:2.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package provides the IPython kernel for Jupyter.

%description -l pl.UTF-8
Ten pakiet dostarcza jądro IPythona dla Jupytera.

%package -n python3-ipykernel
Summary:	IPython kernel for Jupyter
Summary(pl.UTF-8):	Jądro IPythona dla Jupytera
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.4

%description -n python3-ipykernel
This package provides the IPython kernel for Jupyter.

%description -n python3-ipykernel -l pl.UTF-8
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
%patch0 -p1

%build
%if %{with python2}
%py_build

%if %{with tests}
# test_oinfo_detail test requires ipython source code
PYTHONPATH=$(pwd) \
%{__python} -m pytest -k 'not test_oinfo_detail' ipykernel
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
PYTHONPATH=$(pwd) \
%{__python3} -m pytest ipykernel
%endif
%endif

%if %{with doc}
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

install -d $RPM_BUILD_ROOT%{_examplesdir}/python-ipykernel-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/python-ipykernel-%{version}
find $RPM_BUILD_ROOT%{_examplesdir}/python-ipykernel-%{version} -name '*.py' \
	| xargs sed -i '1s|/usr/bin/env python|%{__python}|'

%py_postclean
%{__rm} -r $RPM_BUILD_ROOT%{py_sitescriptdir}/ipykernel/tests \
	$RPM_BUILD_ROOT%{py_sitescriptdir}/ipykernel/inprocess/tests
%endif

%if %{with python3}
%py3_install

install -d $RPM_BUILD_ROOT%{_examplesdir}/python3-ipykernel-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/python3-ipykernel-%{version}
find $RPM_BUILD_ROOT%{_examplesdir}/python3-ipykernel-%{version} -name '*.py' \
	| xargs sed -i '1s|/usr/bin/env python|%{__python3}|'

%{__rm} -r $RPM_BUILD_ROOT%{py3_sitescriptdir}/ipykernel/tests \
	$RPM_BUILD_ROOT%{py3_sitescriptdir}/ipykernel/inprocess/tests
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc COPYING.md README.md
%{py_sitescriptdir}/ipykernel
%{py_sitescriptdir}/ipykernel_launcher.py[co]
%{py_sitescriptdir}/ipykernel-%{version}-py*.egg-info
%dir %{_datadir}/jupyter
%dir %{_datadir}/jupyter/kernels
%{_datadir}/jupyter/kernels/python2
%{_examplesdir}/python-ipykernel-%{version}
%endif

%if %{with python3}
%files -n python3-ipykernel
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
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,*.html,*.js}
%endif
