#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	doclayout
Summary:	A prettyprinting library for laying out text documents
Summary(pl.UTF-8):	Biblioteka ładnego wypisywania do składania dokumentów tekstowych
Name:		ghc-%{pkgname}
Version:	0.3
Release:	2
License:	BSD
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/doclayout
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	b5ce397205583a70965046864814e9f5
URL:		http://hackage.haskell.org/package/doclayout
BuildRequires:	ghc >= 8.0
BuildRequires:	ghc-base >= 4.9
BuildRequires:	ghc-base < 5
BuildRequires:	ghc-mtl
BuildRequires:	ghc-safe
BuildRequires:	ghc-text
%if %{with prof}
BuildRequires:	ghc-prof >= 8.0
BuildRequires:	ghc-base-prof >= 4.9
BuildRequires:	ghc-mtl-prof
BuildRequires:	ghc-safe-prof
BuildRequires:	ghc-text-prof
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
%requires_eq	ghc
Requires(post,postun):	/usr/bin/ghc-pkg
Requires:	ghc-base >= 4.9
Requires:	ghc-mtl
Requires:	ghc-safe
Requires:	ghc-text
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
doclayout is a prettyprinting library for laying out text documents,
with several features not present in prettyprinting libraries designed
for code. It was designed for use in pandoc.

%description -l pl.UTF-8
doclayout to biblioteka ładnego wypisywania (prettyprint) do składania
dokumentów tekstowych z kilkoma funkcjami nieobecnymi w bibliotekach
ładnego wypisywania zaprojektowanych dla kodu. Powstała z myślą o
użyciu w narzędziu pandoc.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ghc-base-prof >= 4.9
Requires:	ghc-mtl-prof
Requires:	ghc-safe-prof
Requires:	ghc-text-prof

%description prof
Profiling %{pkgname} library for GHC. Should be installed when GHC's
profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.hs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.hs build

runhaskell Setup.hs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.hs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

# packaged as %doc
%{__rm} $RPM_BUILD_ROOT%{_datadir}/%{pkgname}-%{version}/{README.md,changelog.md}

runhaskell Setup.hs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc README.md changelog.md %{name}-%{version}-doc/*
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%attr(755,root,root) %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.so
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.a
%exclude %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*_p.a

%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/*.dyn_hi

%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/*.p_hi
%endif
