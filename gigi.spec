%define svnrev	1074
%define major	0
%define libname	%mklibname %{name} %{major}
%define devname	%mklibname %{name} -d

Summary:	A GUI library for OpenGL
Name:		gigi
Version:	0.8.0
Release:	8.%{svnrev}.1
License:	LGPLv2+
Group:		System/Libraries
URL:		http://gigi.sourceforge.net/
Source0:	%{name}-%{svnrev}.tar.xz
Patch0:		gigi-938-link.patch
#from https://build.opensuse.org/package/files?package=gigi&project=home%3Adbuck
Patch1:		gigi-vector.patch
Patch2:		gigi-adobe-cmath.patch
Patch3:		gigi-cmake-tests.patch

BuildRequires:	cmake
BuildRequires:	doxygen
BuildRequires:	boost-devel
BuildRequires:	jpeg-devel
BuildRequires:	libtool-devel
BuildRequires:	tiff-devel
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(OGRE)
BuildRequires:	pkgconfig(OIS)
BuildRequires:	pkgconfig(sdl)

%description
GiGi (aka GG) is a GUI library for OpenGL. It is platform-independent 
(it runs at least on Linux and Windows, and probably more), 
compiler-independent (it compiles under at GCC 3.2 or higher and MSVC++ 7.1 
or higher, and probably more), and driver-independent. A reference driver 
for SDL is provided, and it is straightforward to write one for yourself 
should you decide to do so.

%package -n 	%{libname}
Summary:	A GUI library for OpenGL
Group:		System/Libraries
Provides:	%{name} = %{version}-%{release}

%description -n %{libname}
This package contains the shared libraries for GiGi (aka GG), a GUI library
for OpenGL.

%package -n 	%{devname}
Summary:	Development headers for GiGi
Group:		System/Libraries
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}

%description -n %{devname}
Development headers and includes for GiGi (aka GG),  a GUI library 
for OpenGL. 

%prep
%setup -qn GG
%apply_patches

%build
%cmake

%make

%install
%makeinstall_std -C build

pushd %{buildroot}%{_libdir}
for lib in *.so; do
    mv $lib $lib.%{version};
    ln -s $lib.%{version} $lib;
done
popd

install -d -m 755 %{buildroot}%{_datadir}/cmake/Modules/GG
install -m 644 cmake/*.cmake %{buildroot}%{_datadir}/cmake/Modules/GG

# move documentation to the correct place
install -d -m 755 %{buildroot}%{_docdir}/%{name}
mv %{buildroot}%{_prefix}/doc/GG %{buildroot}%{_docdir}/%{name}

%files -n %{libname}
%doc README COPYING INSTALLING PACKAGING
%{_libdir}/libGiGi*.so.%{major}*

%files -n %{devname}
%doc %{_docdir}/%{name}/GG
%{_libdir}/libGiGi*.so
%{_libdir}/pkgconfig/GiGi*
%{_datadir}/cmake/Modules/GG
%{_includedir}/GG

