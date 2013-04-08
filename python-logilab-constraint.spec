# for el5, force use of python2.6
%if 0%{?el5}
%define python python26
%define __python /usr/bin/python2.6
%else
%define python python
%define __python /usr/bin/python
%endif
%{!?_python_sitelib: %define _python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%define project_name logilab-constraint
%define project_version 0.5.0

Summary:        constraints satisfaction solver in Python
Name:           %{python}-%{project_name}
Version:        %{project_version}
Release:        logilab.1%{?dist}
Source0:        http://download.logilab.org/pub/constraint/%{project_name}-%{version}.tar.gz
License:        LGPLv2+
Group:          Development/Languages/Python
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildArch:      noarch
Vendor:         Logilab <contact@logilab.fr>
Url:            http://www.logilab.org/project/%{project_name}

BuildRequires:  %{python}
Requires:       %{python}, %{python}-logilab-common >= 0.55.2


%description
constraints satisfaction solver in Python

%prep
%setup -q -n %{project_name}-%{version}

%build
%{__python} setup.py build
%if 0%{?el5}
# change the python version in shebangs
find . -name '*.py' -type f -print0 |  xargs -0 sed -i '1,3s;^#!.*python.*$;#! /usr/bin/python2.6;'
%endif

%install
rm -rf $RPM_BUILD_ROOT
NO_SETUPTOOLS=1 %{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT%{_python_sitelib}/logilab/__init__.py*

%clean
rm -rf $RPM_BUILD_ROOT

%files 
%defattr(-, root, root)
%doc README ChangeLog COPYING.LESSER
%{_python_sitelib}/logilab*
