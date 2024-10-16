#Module-Specific definitions
%define apache_version 2.2.8
%define mod_name mod_xslt_filter
%define mod_conf B37_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	Performs XSL transformation on the fly
Name:		apache-%{mod_name}
Version:	1.5.2
Release:	8
Group:		System/Servers
License:	Apache License
URL:		https://sourceforge.net/projects/xslt-filter/
Source0:	xslt_filter-%{version}.tar.gz
Source1:	%{mod_conf}
Patch0:		xslt_filter-correct_naming_fix.diff
Patch1:		xslt_filter-1.5.2-format_not_a_string_literal_and_no_format_arguments.diff
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):  apache-conf >= %{apache_version}
Requires(pre):  apache >= %{apache_version}
Requires:	apache-conf >= %{apache_version}
Requires:	apache >= %{apache_version}
BuildRequires:	apache-devel >= %{apache_version}
BuildRequires:	automake
BuildRequires:	dos2unix
BuildRequires:	libtool
BuildRequires:	libxml2-devel >= 2.6.30
BuildRequires:	libxslt-devel >= 1.1.20

%description
XSLT Filter is an Apache2 loadable module which performs XSL transformation on
the fly. It uses LibXML2+LibXSLT as parsing and transformation engines. The
module acts as an Apache output fitler and is compatible with mod_perl, CGI and
PHP applications.

%prep

%setup -q -n xslt_filter-%{version}
%patch0 -p1
%patch1 -p0

mv xslt_filter.c %{mod_name}.c

cp %{SOURCE1} %{mod_conf}

find -type f -exec dos2unix {} \;

%build
rm -f configure
libtoolize --copy --force; aclocal; autoconf; automake --add-missing --copy --foreign; autoconf
export APXS2="%{_bindir}/apxs"

%configure2_5x --localstatedir=/var/lib

%make

%install

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

%files
%doc README
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}


%changelog
* Sat Feb 11 2012 Oden Eriksson <oeriksson@mandriva.com> 1.5.2-7mdv2012.0
+ Revision: 773243
- rebuild

* Tue May 24 2011 Oden Eriksson <oeriksson@mandriva.com> 1.5.2-6
+ Revision: 678449
- mass rebuild

* Mon Jan 03 2011 Oden Eriksson <oeriksson@mandriva.com> 1.5.2-5mdv2011.0
+ Revision: 627741
- don't force the usage of automake1.7

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1.5.2-4mdv2011.0
+ Revision: 588110
- rebuild

* Mon Mar 08 2010 Oden Eriksson <oeriksson@mandriva.com> 1.5.2-3mdv2010.1
+ Revision: 516284
- rebuilt for apache-2.2.15

* Sat Aug 01 2009 Oden Eriksson <oeriksson@mandriva.com> 1.5.2-2mdv2010.0
+ Revision: 406691
- rebuild

* Wed Jan 07 2009 Oden Eriksson <oeriksson@mandriva.com> 1.5.2-1mdv2009.1
+ Revision: 326518
- 1.5.2
- fix build with -Wformat-security

* Sun Aug 10 2008 Oden Eriksson <oeriksson@mandriva.com> 1.5.1-1mdv2009.0
+ Revision: 270293
- 1.5.1
- rediffed P0

* Mon Jul 14 2008 Oden Eriksson <oeriksson@mandriva.com> 1.5-3mdv2009.0
+ Revision: 235138
- rebuild

* Thu Jun 05 2008 Oden Eriksson <oeriksson@mandriva.com> 1.5-2mdv2009.0
+ Revision: 215681
- fix rebuild
- hard code %%{_localstatedir}/lib to ease backports

* Sun May 18 2008 Oden Eriksson <oeriksson@mandriva.com> 1.5-1mdv2009.0
+ Revision: 208640
- import apache-mod_xslt_filter


* Sun May 18 2008 Oden Eriksson <oeriksson@mandriva.com> 1.5-1mdv2009.0
- initial Mandriva package
