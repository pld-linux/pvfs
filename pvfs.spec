Summary:	Parallel Virtual File System
Summary(pl):	PVFS - RСwnolegЁy Wirtualny System PlikСw
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
Group(ru):	Библиотеки
Group(uk):	Б╕бл╕отеки
Source0:	ftp://ftp.parl.clemson.edu/pub/%{name}/%{name}-%{version}.tgz
URL:		http://www.parl.clemson.edu/pvfs/
BuildRequires:	autoconf
Buildroot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Parallel Virtual File System.

%description -l pl
PVFS - RСwnolegЁy Wirtualny System PlikСw.

%package devel
Summary:	Header files for PVFS.
Summary(pl):	Pliki naglowkowe dla PVFSa.
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(es):	Desarrollo/Bibliotecas
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Group(pt_BR):	Desenvolvimento/Bibliotecas
Group(ru):	Разработка/Библиотеки
Group(uk):	Розробка/Б╕бл╕отеки
Requires:	%{name}=%{version}

%description devel 
%description -l pl devel

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
%attr(750,root,root) %{_sbindir}/*
%attr(644,root,root) %{_mandir}/man*/*

%files devel
%attr(644,root,root) %{_includedir}/*.h
%attr(755,root,root) %{_libdir}/*
