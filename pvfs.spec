Summary:	Parallel Virtual File System
Summary(pl):	PVFS - Równoleg³y Wirtualny System Plików
Name:		pvfs
Version:	1.5.2
Release:	1
License:	GPL
Group:		Libraries
Source0:	ftp://ftp.parl.clemson.edu/pub/%{name}/%{name}-%{version}.tgz
URL:		http://www.parl.clemson.edu/pvfs/
BuildRequires:	autoconf
Buildroot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Parallel Virtual File System.

%description -l pl
PVFS - Równoleg³y Wirtualny System Plików.

%package devel
Summary:	Header files for PVFS
Summary(pl):	Pliki naglowkowe dla PVFSa
Group:		Development/Libraries
Requires:	%{name}=%{version}

%description devel
Header files for PVFS.

%description devel -l pl
Pliki naglowkowe dla PVFSa.

%prep
%setup -q

%build
%{__autoconf}
%configure --enable-lftp

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	install_root=$RPM_BUILD_ROOT \
	MANDIR=$RPM_BUILD_ROOT%{_mandir}


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc BUGS NOTES README
%attr(755,root,root) %{_bindir}/*
%attr(750,root,root) %{_sbindir}/*
%attr(644,root,root) %{_mandir}/man*/*

%files devel
%defattr(644,root,root,755)
%attr(644,root,root) %{_includedir}/*.h
%attr(755,root,root) %{_libdir}/*
