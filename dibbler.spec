Summary:	Dibbler - a portable DHCPv6
Summary(pl):	Dibbler - przeno¶ny DHCPv6
Name:		dibbler
Version:	0.3.1
Release:	0.1
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
Dibbler to przeno¶na implementacja DHCPv6. Obs³uguje stanow± (tzn. z
nadawaniem adresów IPv6), jak i bezstanow± (tzn. z nadawaniem opcji)
autokonfiguracjê IPv6. Aktualnie dostêpne s± porty dla Linuksa 2.4/2.6
i Windows XP oraz Windows 2003. Zalety to ³atwa instalacja (klikalny
instalator pod Windows i pakiety RPM/DEB pod Linuksa) i wyczerpuj±ca
dokumentacja (zarówno dla u¿ytkowników, jak i programistów).

#%package doc
#Summary:	Documentation for Dibbler - a portable DHCPv6
#Summary(pl):	Dokumentacja dla Dibblera - przeno¶nego DHCPv6
#Group:		Documentation

#%description doc
#Documentation for Dibbler - a portable DHCPv6

#%description doc -l pl
#Dokumentacja dla Dibblera - przeno¶nego DHCPv6

%prep
%setup -q -n %{name}
%patch0 -p0

%build
%{__make} \
	ARCH=LINUX \
	CFLAGS="%{rpmcflags}" \
	CPP="%{__cpp}" \
	CXX="%{__cxx}" \
	CC="%{__cc}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man8,%{_sharedstatedir}/dibbler}

install dibbler-{client,server} $RPM_BUILD_ROOT%{_sbindir}
install *.conf $RPM_BUILD_ROOT%{_sharedstatedir}/dibbler
install doc/man/* $RPM_BUILD_ROOT%{_mandir}/man8

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGELOG GUIDELINES RELNOTES TODO WILD-IDEAS
%attr(755,root,root) %{_sbindir}/*
%dir %{_sharedstatedir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sharedstatedir}/%{name}/*.conf
%{_mandir}/man8/*.8*

#%files doc
#%defattr(644,root,root,755)
#%doc doc/*.blah
