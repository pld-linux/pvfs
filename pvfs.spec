Summary:	PVFS
Summary(pl):	PVFS
Name:		pvfs
Version:	1.5.2
Release:	1
Copyright:	GPL
Group:		Libraries
Source0:	ftp://ftp.parl.clemson.edu/pub/%{name}/%{name}-%{version}.tgz
#BuildRequires:	
#Requires:	
Buildroot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define	_prefix	/usr

%description

%description -l pl

%prep
%setup -q

#%patch

%build
./configure --prefix=%{_prefix} \
	--enable-lfs
%{__make} RPM_OPT_FLAGS="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
%{__make} prefix=$RPM_BUILD_ROOT%{_prefix} \
	MANDIR=$RPM_BUILD_ROOT%{_mandir} \
	install

%post
%postun

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc
%attr(755, root, root) %{_bindir}/*
%attr(644, root, root) %{_libdir}/*
%attr(644, root, root) %{_includedir}/*.h
%attr(750, root, root) %{_sbindir}/*
%attr(644, root, root) %{_mandir}/man*/*
