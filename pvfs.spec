%define		no_install_post_compress_modules	1

Summary:	Parallel Virtual File System
Summary(pl):	PVFS - Równoleg³y Wirtualny System Plików
Name:		pvfs
Version:	1.5.6
%define		_rel 1
Release:	%{_rel}
License:	GPL
Group:		Libraries
Source0:	ftp://ftp.parl.clemson.edu/pub/%{name}/%{name}-%{version}.tgz
Source1:	ftp://ftp.parl.clemson.edu/pub/%{name}/%{name}-kernel-%{version}-linux-2.4.tgz
Source10:	ftp://ftp.parl.clemson.edu/pub/%{name}/user-guide.pdf
Source11:	ftp://ftp.parl.clemson.edu/pub/%{name}/quickstart.pdf
Patch1:		pvfs-kernel-Makefile.in.patch
URL:		http://www.parl.clemson.edu/pvfs/
BuildRequires:	autoconf
Buildroot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_progdocdir	%{_datadir}/doc/%{name}-%{version}

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

%package -n kernel-%{name}
Summary:	Kernel driver for PVFS
Summary(pl):	Sterownik kernela dla PVFSa
Group:		Development/Libraries
Release:	%{_rel}@%{_kernel_ver_str}
#Requires:	%{name}=%{version}

%description -n kernel-%{name}
%description -l pl -n kernel-%{name} 

%package -n kernel-smp-%{name}
Summary:	Kernel SMP driver for PVFS
Summary(pl):	Sterownik kernela SMP dla PVFSa
Group:		Development/Libraries
Release:	%{_rel}@%{_kernel_ver_str}
#Requires:	%{name}=%{version}
%description -n kernel-smp-%{name}
%description -l pl -n kernel-smp-%{name}

%prep
%setup -q -a1 

%patch1 -p1

%build
%{__autoconf}
%configure \
	--without-single \
	--enable-scyld \
	--enable-nodelay \
	--enable-lfs \
	--enable-madvise

%{__make}

echo Installing documentations ...
install %SOURCE10 .
install %SOURCE11 .

echo Building kernel pvfs.o module...
cd %name-kernel-%{version}-linux-2.4
%configure \
	--with-newstyle \
	--with-pvfs=".." \
	--with-libpvfs-dir="../lib"
# make UP
%{__make} SMPFLAGS=""
mv pvfs.o pvfs.up
%{__make} clean

echo Building SMP kernel pvfs.o module...
# make SMP
%{__make} SMPFLAGS="-D__SMP__ -D__KERNEL_SMP=1"


%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	install_root=$RPM_BUILD_ROOT \
	MANDIR=$RPM_BUILD_ROOT%{_mandir}

install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver_str}{,smp}/fs/
install -d $RPM_BUILD_ROOT%{_progdocdir}

cd %name-kernel-%{version}-linux-2.4
install pvfs.up $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver_str}/fs/pvfs.o

install pvfs.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver_str}smp/fs

install mount.pvfs $RPM_BUILD_ROOT%{_bindir}
install %SOURCE10 $RPM_BUILD_ROOT%{_progdocdir}
install %SOURCE11 $RPM_BUILD_ROOT%{_progdocdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README BUGS NOTES *.pdf
%attr(755,root,root) %{_bindir}/*
%attr(750,root,root) %{_sbindir}/*
%attr(644,root,root) %{_mandir}/man*/*

%files devel
%defattr(644,root,root,755)
%attr(644,root,root) %{_includedir}/*.h
%attr(755,root,root) %{_libdir}/*

%files -n kernel-%{name}
%attr(600,root,root) /lib/modules/%{_kernel_ver_str}/fs/pvfs.o

%files -n kernel-smp-%{name}
%attr(600,root,root) /lib/modules/%{_kernel_ver_str}smp/fs/pvfs.o
