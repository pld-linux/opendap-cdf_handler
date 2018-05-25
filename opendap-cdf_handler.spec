Summary:	CDF 3 data handler for the OPeNDAP data server
Summary(pl.UTF-8):	Moduł obsługujący dane CDF 3 dla serwera danych OPeNDAP
Name:		opendap-cdf_handler
Version:	1.0.3
Release:	5
License:	LGPL v2.1+
Group:		Daemons
Source0:	http://www.opendap.org/pub/source/cdf_handler-%{version}.tar.gz
# Source0-md5:	79060adceda4e72265e1899f80926639
Patch0:		%{name}-libdap.patch
Patch1:		%{name}-includes.patch
Patch2:		%{name}-bes.patch
URL:		http://opendap.org/
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake
BuildRequires:	bes-devel >= 3.6.0
BuildRequires:	cdflib-devel >= 3.1
BuildRequires:	libdap-devel >= 3.8.0
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:1.5
BuildRequires:	pkgconfig
Requires:	bes >= 3.6.0
Requires:	cdflib >= 3.1
Requires:	libdap >= 3.8.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is the CDF data handler for OPeNDAP data server. It reads
cdf31-dist files and returns DAP responses that are compatible with
DAP2 and the dap-server software.

%description -l pl.UTF-8
Ten pakiet zawiera moduł obsługi danych CDF dla serwera danych
OPeNDAP. Odczytuje pliki cdf31-dist i zwraca odpowiedzi DAP zgodne z
DAP2 oraz oprogramowaniem dap-server.

%prep
%setup -q -n cdf_handler-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
# rebuild autotools for -as-needed to work
%{__libtoolize}
%{__aclocal} -I conf
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-static \
	--with-cdf-include=%{_includedir}/cdf \
	--with-cdf-libdir=%{_libdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/bes/*.la
# API not exported
%{__rm} $RPM_BUILD_ROOT%{_libdir}/lib*.{la,so}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYRIGHT ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/bes-cdf-data.sh
%attr(755,root,root) %{_bindir}/dap_cdf_handler
%attr(755,root,root) %{_libdir}/libcdf_handler.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcdf_handler.so.1
%attr(755,root,root) %{_libdir}/bes/libcdf_module.so
%dir %{_datadir}/hyrax/data/cdf
%{_datadir}/hyrax/data/cdf/*.cdf
