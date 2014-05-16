%define		php_name	php%{?php_suffix}
%define		modname	hidef
%define		status		stable
Summary:	%{modname} - Constants for real
Summary(pl.UTF-8):	%{modname} - mechanizm definiowana stałych
Name:		%{php_name}-pecl-%{modname}
Version:	0.1.13
Release:	4
License:	PHP 3.01
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
# Source0-md5:	41cec59636c38abfd0cf15011a1184f4
URL:		http://pecl.php.net/package/hidef/
BuildRequires:	%{php_name}-devel >= 3:5.0.0
BuildRequires:	rpmbuild(macros) >= 1.650
%{?requires_php_extension}
Provides:	php(%{modname}) = %{version}
Obsoletes:	php-pecl-hidef < 0.1.13-3
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
