Summary:	Parallel Virtual File System
Summary(pl):	PVFS - RÛwnoleg≥y Wirtualny System PlikÛw
Name:		pvfs
Version:	1.5.2
Release:	1
License:	GPL
Group:		Libraries
Group(de):	Libraries
Group(es):	Bibliotecas
Group(fr):	Librairies
Group(pl):	Biblioteki
Group(pt_BR):	Bibliotecas
Group(ru):	‚…¬Ã…œ‘≈À…
Group(uk):	‚¶¬Ã¶œ‘≈À…
Source0:	ftp://ftp.parl.clemson.edu/pub/%{name}/%{name}-%{version}.tgz
URL:		http://www.parl.clemson.edu/pvfs/
BuildRequires:	autoconf
Buildroot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Parallel Virtual File System.

%description -l pl
PVFS - RÛwnoleg≥y Wirtualny System PlikÛw.

%prep
%setup -q

%build
autoconf
%configure --enable-lftp

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	install_root=$RPM_BUILD_ROOT \
	MANDIR=$RPM_BUILD_ROOT%{_mandir}

gzip -9nf BUGS NOTES README

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.gz
%attr(755,root,root) %{_bindir}/*
%{_libdir}/*
%{_includedir}/*.h
%attr(750,root,root) %{_sbindir}/*
%{_mandir}/man*/*
