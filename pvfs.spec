#
# Conditional build:
%bcond_without	dist_kernel	# without kernel from distribution
#
%define		_rel 1
Summary:	Parallel Virtual File System
Summary(pl):	PVFS - Równoleg³y Wirtualny System Plików
Name:		pvfs
Version:	1.6.3
Release:	%{_rel}
License:	GPL
Group:		Libraries
Source0:	ftp://ftp.parl.clemson.edu/pub/pvfs/%{name}-%{version}.tgz
# Source0-md5:	06990cd60cc41be113861f54e2ad94ec
Source1:	ftp://ftp.parl.clemson.edu/pub/pvfs/%{name}-kernel-%{version}-linux-2.4.tgz
# Source1-md5:	4a13ce814e7d17564d399f29d78687da
Source10:	ftp://ftp.parl.clemson.edu/pub/pvfs/user-guide.pdf
# Source10-md5:	3b21d77e3e04b607ad1d792c20ebdd3e
Source11:	ftp://ftp.parl.clemson.edu/pub/pvfs/quickstart.pdf
# Source11-md5:	934bcedeb47cb802257925d990281c4d
#Patch1:	%{name}-kernel-Makefile.in.patch
URL:		http://www.parl.clemson.edu/pvfs/
BuildRequires:	autoconf
%{?with_dist_kernel:BuildRequires:	kernel24-headers}
BuildRequires:	rpmbuild(macros) >= 1.118
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_progdocdir	%{_datadir}/doc/%{name}-%{version}
%define		_kernelsrcdir	/usr/src/linux-2.4

%description
Parallel Virtual File System.

%description -l pl
PVFS - Równoleg³y Wirtualny System Plików.

%package devel
Summary:	Header files for PVFS
Summary(pl):	Pliki nag³ówkowe dla PVFS-a
Group:		Development/Libraries
Requires:	%{name}=%{version}

%description devel
Header files for PVFS.

%description devel -l pl
Pliki nag³ówkowe dla PVFS-a.

%package -n kernel24-%{name}
Summary:	Linux kernel driver for PVFS
Summary(pl):	Sterownik j±dra Linuksa dla PVFS-a
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_up}
Requires(post,postun):	/sbin/depmod
#Requires:	%{name}=%{version}

%description -n kernel24-%{name}
Linux kernel driver for PVFS.

%description -n kernel24-%{name} -l pl
Sterownik j±dra Linuksa dla PVFS-a.

%package -n kernel24-smp-%{name}
Summary:	Linux SMP kernel driver for PVFS
Summary(pl):	Sterownik j±dra Linuksa SMP dla PVFS-a
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_smp}
Requires(post,postun):	/sbin/depmod
#Requires:	%{name}=%{version}

%description -n kernel24-smp-%{name}
Linux SMP kernel driver for PVFS.

%description -n kernel24-smp-%{name} -l pl
Sterownik j±dra Linuksa SMP dla PVFS-a.

%prep
%setup -q -a1
#%patch1 -p1

%build
%configure2_13 \
	--without-single \
	--enable-scyld \
	--enable-nodelay \
	--enable-lfs \
	--enable-madvise

%{__make}

echo Installing documentations ...
install %{SOURCE10} .
install %{SOURCE11} .

echo Building kernel pvfs.o module...
cd %{name}-kernel-%{version}-linux-2.4
%configure \
	--with-newstyle \
	--with-pvfs=".." \
	--with-kernel-headers="%{_kernelsrcdir}/include" \
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

install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver_str}{,smp}/fs
install -d $RPM_BUILD_ROOT%{_progdocdir}

cd %{name}-kernel-%{version}-linux-2.4
install pvfs.up $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver_str}/fs/pvfs.o

install pvfs.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver_str}smp/fs

install mount.pvfs $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel24-%{name}
%depmod %{_kernel_ver}

%postun -n kernel24-%{name}
%depmod %{_kernel_ver}

%post	-n kernel24-smp-%{name}
%depmod %{_kernel_ver}smp

%postun -n kernel24-smp-%{name}
%depmod %{_kernel_ver}smp

%files
%defattr(644,root,root,755)
%doc README BUGS NOTES *.pdf
%attr(755,root,root) %{_bindir}/*
%attr(750,root,root) %{_sbindir}/*
%{_mandir}/man*/*

%files devel
%defattr(644,root,root,755)
%{_includedir}/*.h
%attr(755,root,root) %{_libdir}/*

%files -n kernel24-%{name}
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver_str}/fs/pvfs.o*

%files -n kernel24-smp-%{name}
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver_str}smp/fs/pvfs.o*
