Summary:	Dibbler - a portable DHCPv6
Summary(pl):	Dibbler - przeno¶ny DHCPv6
Name:		dibbler
Version:	0.4.0
Release:	0.3
License:	GPL v2
Group:		Networking/Daemons
Source0:	http://klub.com.pl/dhcpv6/dibbler/%{name}-%{version}-src.tar.gz
# Source0-md5:	2056e15305c9e5432bf7ad853e3f864c
Source1:	http://klub.com.pl/dhcpv6/dibbler/%{name}-%{version}-doc.tar.gz
# Source1-md5:	576168d8cf3eb5ffe82dde05338cb902
Source2:	%{name}.init
URL:		http://klub.com.pl/dhcpv6/
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

%description -l pl
Dibbler to przeno¶na implementacja DHCPv6. Obs³uguje stanow± (tzn. z
nadawaniem adresów IPv6), jak i bezstanow± (tzn. z nadawaniem opcji)
autokonfiguracjê IPv6. Aktualnie dostêpne s± porty dla Linuksa 2.4/2.6
i Windows XP oraz Windows 2003. Zalety to ³atwa instalacja (klikalny
instalator pod Windows i pakiety RPM/DEB pod Linuksa) i wyczerpuj±ca
dokumentacja (zarówno dla u¿ytkowników, jak i programistów).

%package doc
Summary:	Documentation for Dibbler - a portable DHCPv6
Summary(pl):	Dokumentacja dla Dibblera - przeno¶nego DHCPv6
Group:		Documentation

%description doc
Documentation for Dibbler - a portable DHCPv6 (pdf files).

%description doc -l pl
Dokumentacja dla Dibblera - przeno¶nego DHCPv6 (pliki pdf).

%package client
Summary:	Dibbler DHCPv6 client
Summary(pl):	Dibbler - klient DHCPv6
Group:		Applications/Networking
Provides:	dhcpv6-client

%description client
DHCPv6 protocol client.

%description client -l pl
Klient protoko³u DHCPv6.

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
ln -sf %{_sharedstatedir}/%{name}/relay.conf $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/relay.conf
ln -sf %{_sharedstatedir}/%{name}/server.conf $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/server.conf
ln -sf %{_sharedstatedir}/%{name}/server-relay.conf $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/server-relay.conf

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
%config(noreplace) %verify(not md5 mtime size) %{_sharedstatedir}/%{name}/server.conf
%config(noreplace) %verify(not md5 mtime size) %{_sharedstatedir}/%{name}/server-relay.conf
%dir %{_sysconfdir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/relay.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/server.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/server-relay.conf
%{_mandir}/man8/*.8*

%files client
%defattr(644,root,root,755)
%doc CHANGELOG LICENSE RELNOTES VERSION
%doc client.conf client-stateless.conf doc/man/dibbler-client.8
%attr(755,root,root) %{_sbindir}/dibbler-client
%dir %{_sharedstatedir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sharedstatedir}/%{name}/client.conf
%dir %{_sysconfdir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/client.conf
%{_mandir}/man8/*.8*

%files doc
%defattr(644,root,root,755)
%doc doc/dibbler-user.pdf doc/dibbler-devel.pdf
