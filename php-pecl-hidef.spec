%define		modname	hidef
%define		status		stable
Summary:	%{modname} - Constants for real
Summary(pl.UTF-8):	%{modname} - mechanizm definiowana stałych
Name:		php-pecl-%{modname}
Version:	0.1.11
Release:	1
License:	PHP 3.01
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
# Source0-md5:	e2bef447832d8c7f6237a27e36242f7c
URL:		http://pecl.php.net/package/hidef/
BuildRequires:	php-devel >= 3:5.0.0
BuildRequires:	rpmbuild(macros) >= 1.344
%{?requires_php_extension}
Requires:	php-common >= 4:5.0.4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Allow definition of user defined constants in simple ini files, which
are then processed like internal constants, without any of the usual
performance penalties.

In PECL status of this extension is: %{status}.

%description -l pl.UTF-8
Rozszerzenie to pozwala na zdefiniowanie stałych w prostym pliku ini.
Stałe te są później przetwarzane tak jak wewnętrzne stałe PHP, bez
typowych spowolnień wydajności.

To rozszerzenie ma w PECL status: %{status}.

%prep
%setup -qc
mv %{modname}-%{version}/* .

%build
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d

%{__make} install \
	EXTENSION_DIR=%{php_extensiondir} \
	INSTALL_ROOT=$RPM_BUILD_ROOT
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{modname}.ini
; Enable %{modname} extension module
extension=%{modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%doc INSTALL CREDITS
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{modname}.so
