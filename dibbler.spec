Summary:	Dibbler - a portable DHCPv6
Summary(pl.UTF-8):	Dibbler - przenośny DHCPv6
Name:		dibbler
Version:	0.4.1
Release:	1
License:	GPL v2
Group:		Networking/Daemons
Source0:	http://dl.sourceforge.net/dibbler/%{name}-%{version}-src.tar.gz
# Source0-md5:	e9c25cc84b881309bbb650d2d36c5fb0
Source1:	http://dl.sourceforge.net/dibbler/%{name}-%{version}-doc.tar.gz
# Source1-md5:	d7ee175bb1994b597e07583f4cc0113f
Source2:	%{name}.init
URL:		http://sourceforge.net/projects/dibbler/
BuildRequires:	libstdc++-devel
BuildRequires:	pkgconfig
Requires(post,preun):	/sbin/chkconfig
Provides:	dhcpv6-server
Obsoletes:	dhcpv6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Dibbler is a portable DHCPv6 implementation. It supports stateful
(i.e. IPv6 address granting) as well as stateless (i.e. option
granting) autoconfiguration for IPv6. Currently Linux 2.4/2.6 and
Windows XP and Windows 2003 ports are available. It features easy to
use install packages (Clickable Windows installer and RPM and DEB
packages for Linux) and extensive documentation (both for users as
well as developers).

%description -l pl.UTF-8
Dibbler to przenośna implementacja DHCPv6. Obsługuje stanową (tzn. z
nadawaniem adresów IPv6), jak i bezstanową (tzn. z nadawaniem opcji)
autokonfigurację IPv6. Aktualnie dostępne są porty dla Linuksa 2.4/2.6
i Windows XP oraz Windows 2003. Zalety to łatwa instalacja (klikalny
instalator pod Windows i pakiety RPM/DEB pod Linuksa) i wyczerpująca
dokumentacja (zarówno dla użytkowników, jak i programistów).

%package doc
Summary:	Documentation for Dibbler - a portable DHCPv6
Summary(pl.UTF-8):	Dokumentacja dla Dibblera - przenośnego DHCPv6
Group:		Documentation

%description doc
Documentation for Dibbler - a portable DHCPv6 (pdf files).

%description doc -l pl.UTF-8
Dokumentacja dla Dibblera - przenośnego DHCPv6 (pliki pdf).

%package client
Summary:	Dibbler DHCPv6 client
Summary(pl.UTF-8):	Dibbler - klient DHCPv6
Group:		Applications/Networking
Provides:	dhcpv6-client

%description client
DHCPv6 protocol client.

%description client -l pl.UTF-8
Klient protokołu DHCPv6.

%prep
%setup -q

%build
%{__make} server client relay\
	ARCH=LINUX \
	CFLAGS="%{rpmcflags}" \
	CPP="%{__cpp}" \
	CXX="%{__cxx}" \
	CC="%{__cc}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man8} \
	$RPM_BUILD_ROOT{%{_sharedstatedir}/%{name},/etc/{rc.d/init.d,dibbler}}

install dibbler-{client,server,relay} $RPM_BUILD_ROOT%{_sbindir}
install *.conf $RPM_BUILD_ROOT%{_sharedstatedir}/%{name}
install doc/man/* $RPM_BUILD_ROOT%{_mandir}/man8
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/dibbler
tar zxf %{SOURCE1} doc/dibbler-user.pdf
tar zxf %{SOURCE1} doc/dibbler-devel.pdf
ln -sf %{_sharedstatedir}/%{name}/client.conf $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/client.conf
ln -sf %{_sharedstatedir}/%{name}/client-stateless.conf $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/client-stateless.conf
ln -sf %{_sharedstatedir}/%{name}/relay.conf $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/relay.conf
ln -sf %{_sharedstatedir}/%{name}/server.conf $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/server.conf
ln -sf %{_sharedstatedir}/%{name}/server-relay.conf $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/server-relay.conf
ln -sf %{_sharedstatedir}/%{name}/server-stateless.conf $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/server-stateless.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
if [ "$1" = "1" ]; then
	/sbin/chkconfig --add dibbler
	if [ -f /var/lock/subsys/dibbler ]; then
        	/etc/rc.d/init.d/dibbler restart 1>&2
	else
        	echo "Run \"/etc/rc.d/init.d/dibbler start\" to start dibbler DHCP daemon."
	fi
fi


%preun
/sbin/ldconfig
if [ "$1" = "0" ];then
	if [ -f /var/lock/subsys/dibbler ]; then
		/etc/rc.d/init.d/dibbler stop >&2
	fi
	/sbin/chkconfig --del dibbler
fi

%files
%defattr(644,root,root,755)
%doc CHANGELOG RELNOTES VERSION
%doc server.conf server-stateless.conf server-relay.conf doc/man/dibbler-server.8
%attr(755,root,root) %{_sbindir}/dibbler-server
%attr(755,root,root) %{_sbindir}/dibbler-relay
%attr(754,root,root) /etc/rc.d/init.d/dibbler
%dir %{_sharedstatedir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sharedstatedir}/%{name}/relay.conf
%config(noreplace) %verify(not md5 mtime size) %{_sharedstatedir}/%{name}/2relays-client.conf
%config(noreplace) %verify(not md5 mtime size) %{_sharedstatedir}/%{name}/2relays-relay1.conf
%config(noreplace) %verify(not md5 mtime size) %{_sharedstatedir}/%{name}/2relays-relay2.conf
%config(noreplace) %verify(not md5 mtime size) %{_sharedstatedir}/%{name}/2relays-server.conf
%config(noreplace) %verify(not md5 mtime size) %{_sharedstatedir}/%{name}/relay-1interface.conf
%config(noreplace) %verify(not md5 mtime size) %{_sharedstatedir}/%{name}/server.conf
%config(noreplace) %verify(not md5 mtime size) %{_sharedstatedir}/%{name}/server-relay.conf
%config(noreplace) %verify(not md5 mtime size) %{_sharedstatedir}/%{name}/server-3classes.conf
%config(noreplace) %verify(not md5 mtime size) %{_sharedstatedir}/%{name}/server-stateless.conf
%dir %{_sysconfdir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/relay.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/server.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/server-relay.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/server-stateless.conf
%{_mandir}/man8/*-server.*
%{_mandir}/man8/*-relay.*

%files client
%defattr(644,root,root,755)
%doc CHANGELOG RELNOTES VERSION
%doc client.conf client-stateless.conf doc/man/dibbler-client.8
%attr(755,root,root) %{_sbindir}/dibbler-client
%dir %{_sharedstatedir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sharedstatedir}/%{name}/client.conf
%config(noreplace) %verify(not md5 mtime size) %{_sharedstatedir}/%{name}/client-stateless.conf
%dir %{_sysconfdir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/client.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/client-stateless.conf
%{_mandir}/man8/*-client.*

%files doc
%defattr(644,root,root,755)
%doc doc/dibbler-user.pdf doc/dibbler-devel.pdf
