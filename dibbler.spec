Summary:	Dibbler - a portable DHCPv6
Summary(pl):	Dibbler - przenośny DHCPv6
Name:		dibbler
Version:	0.3.1
Release:	0.2
License:	GPL v2
Group:		Networking/Daemons
Source0:	http://klub.com.pl/dhcpv6/%{name}-%{version}-src.tar.gz
# Source0-md5:	6bc2b0932f1000ad50624789873115d8
Patch0:		%{name}-Makefile.patch
URL:		http://klub.com.pl/dhcpv6/
#BuildRequires:	bison++ >= 1.21.9
BuildRequires:	flex
BuildRequires:	libstdc++-devel
BuildRequires:	libxml2-devel
BuildRequires:	pkgconfig
Requires(post,preun):	/sbin/chkconfig
#Provides:	dhcpd?
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
Dibbler to przenośna implementacja DHCPv6. Obsługuje stanową (tzn. z
nadawaniem adresów IPv6), jak i bezstanową (tzn. z nadawaniem opcji)
autokonfigurację IPv6. Aktualnie dostępne są porty dla Linuksa 2.4/2.6
i Windows XP oraz Windows 2003. Zalety to łatwa instalacja (klikalny
instalator pod Windows i pakiety RPM/DEB pod Linuksa) i wyczerpująca
dokumentacja (zarówno dla użytkowników, jak i programistów).

#%package doc
#Summary:	Documentation for Dibbler - a portable DHCPv6
#Summary(pl):	Dokumentacja dla Dibblera - przenośnego DHCPv6
#Group:		Documentation

#%description doc
#Documentation for Dibbler - a portable DHCPv6

#%description doc -l pl
#Dokumentacja dla Dibblera - przenośnego DHCPv6

%package client
Summary:	Dibbler DHCPv6 client
Summary(pl):	Dibbler - klient DHCPv6
Group:		Networking/Daemons

%description client
DHCPv6 protocol client.

%description client -l pl
Klient protokołu DHCPv6.

%prep
%setup -q -n %{name}
%patch0 -p0

%build
%{__make} server client \
	ARCH=LINUX \
	CFLAGS="%{rpmcflags}" \
	CPP="%{__cpp}" \
	CXX="%{__cxx}" \
	CC="%{__cc}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man8} \
	$RPM_BUILD_ROOT{%{_sharedstatedir}/%{name},%{_sysconfdir}/%{name}}

install dibbler-{client,server} $RPM_BUILD_ROOT%{_sbindir}
install *.conf $RPM_BUILD_ROOT%{_sharedstatedir}/%{name}
install doc/man/* $RPM_BUILD_ROOT%{_mandir}/man8

%clean
rm -rf $RPM_BUILD_ROOT

%post
ln -s %{_sharedstatedir}/%{name}/server.conf %{_sysconfdir}/%{name}/server.conf
/sbin/chkconfig -add dibbler

%preun
if [ "$1" = "0" ];then
        if [ -f /var/lock/subsys/dhcpd ]; then
                /etc/rc.d/init.d/dhcpd stop >&2
        fi
        /sbin/chkconfig --del dhcpd
fi

%post client
if [ -d %{_sharedstatedir}/%{name} ]; then
install -d %{_sharedstatedir}/%{name}
ln -s %{_sharedstatedir}/%{name}/client.conf %{_sysconfdir}/%{name}/client.conf
fi

%files
%defattr(644,root,root,755)
%doc CHANGELOG FUN LICENSE GUIDELINES RELNOTES TODO VERSION WILD-IDEAS 
%doc server.conf server-stateless.conf doc/man/dibbler-server.8
%attr(755,root,root) %{_sbindir}/dibbler-server
%dir %{_sharedstatedir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sharedstatedir}/%{name}/server.conf
%{_mandir}/man8/*.8*

%files client
%defattr(644,root,root,755)
%doc CHANGELOG FUN LICENSE GUIDELINES RELNOTES TODO VERSION WILD-IDEAS
%doc client.conf client-stateless.conf doc/man/dibbler-client.8
%attr(755,root,root) %{_sbindir}/dibbler-client
%dir %{_sharedstatedir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sharedstatedir}/%{name}/client.conf
%{_mandir}/man8/*.8*

#%files doc
#%defattr(644,root,root,755)
#%doc doc/*.blah
