#Module-Specific definitions
%define apache_version 2.2.8
%define mod_name mod_xslt_filter
%define mod_conf B37_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	Performs XSL transformation on the fly
Name:		apache-%{mod_name}
Version:	1.5.1
Release:	%mkrel 1
Group:		System/Servers
License:	Apache License
URL:		http://sourceforge.net/projects/xslt-filter/
Source0:	xslt_filter-%{version}.tar.gz
Source1:	%{mod_conf}
Patch0:		xslt_filter-correct_naming_fix.diff
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):  apache-conf >= %{apache_version}
Requires(pre):  apache >= %{apache_version}
Requires:	apache-conf >= %{apache_version}
Requires:	apache >= %{apache_version}
BuildRequires:	apache-devel >= %{apache_version}
BuildRequires:	automake1.7
BuildRequires:	dos2unix
BuildRequires:	libtool
BuildRequires:	libxml2-devel >= 2.6.30
BuildRequires:	libxslt-devel >= 1.1.20
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
XSLT Filter is an Apache2 loadable module which performs XSL transformation on
the fly. It uses LibXML2+LibXSLT as parsing and transformation engines. The
module acts as an Apache output fitler and is compatible with mod_perl, CGI and
PHP applications.

%prep

%setup -q -n xslt_filter-%{version}
%patch0 -p1

mv xslt_filter.c %{mod_name}.c

cp %{SOURCE1} %{mod_conf}

find -type f -exec dos2unix -U {} \;

%build
rm -f configure
libtoolize --copy --force; aclocal-1.7; autoconf; automake-1.7 --add-missing --copy --foreign; autoconf
export APXS="%{_sbindir}/apxs"

%configure2_5x --localstatedir=/var/lib

%make

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/apache-extramodules
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d

install -m0755 .libs/%{mod_so} %{buildroot}%{_libdir}/apache-extramodules/
install -m0644 %{mod_conf} %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

%post
if [ -f %{_var}/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f %{_var}/lock/subsys/httpd ]; then
        %{_initrddir}/httpd restart 1>&2
    fi
fi

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}
