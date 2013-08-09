# System resource usage is extremely high so disable extra flags, including debug
%define _enable_debug_packages %{nil}
%define debug_package %{nil}

%define oname GiGi

# 20120910 is from FreeOrion source tree
%define svnrev	20130806

%define major		0
%define libname		%mklibname %{oname} %{major}
%define libggogre	%mklibname %{oname}Ogre %{major}
%define libggois	%mklibname %{oname}OgrePlugin_OIS %{major}
%define libggsdl	%mklibname %{oname}SDL %{major}
%define devname		%mklibname %{oname} -d

Summary:	A GUI library for OpenGL
Name:		gigi
Version:	0.8.0
Release:	8.%{svnrev}.1
License:	LGPLv2+
Group:		System/Libraries
Url:		http://gigi.sourceforge.net/
Source0:	%{name}-%{svnrev}.tar.xz
Patch0:		gigi-20130806-link.patch
Patch1:		gigi-20130806-soversion.patch

BuildRequires:	cmake
BuildRequires:	doxygen
BuildRequires:	boost-devel
BuildRequires:	jpeg-devel
BuildRequires:	libtool-devel
BuildRequires:	tiff-devel
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(libpng)
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

#----------------------------------------------------------------------------

%package -n 	%{libname}
Summary:	A GUI library for OpenGL
Group:		System/Libraries
Provides:	%{name} = %{version}-%{release}
Conflicts:	%{_lib}gigi0 < %{EVRD}
Obsoletes:	%{_lib}gigi0 < %{EVRD}

%description -n %{libname}
This package contains the shared library for GiGi (aka GG), a GUI library
for OpenGL.

%files -n %{libname}
%{_libdir}/lib%{oname}.so.%{major}*

#----------------------------------------------------------------------------

%package -n 	%{libggogre}
Summary:	A GUI library for OpenGL (OGRE)
Group:		System/Libraries
Provides:	%{name} = %{version}-%{release}
Conflicts:	%{_lib}gigi0 < %{EVRD}

%description -n %{libggogre}
This package contains the shared library for GiGi (aka GG), a GUI library
for OpenGL.

%files -n %{libggogre}
%{_libdir}/lib%{oname}Ogre.so.%{major}*

#----------------------------------------------------------------------------

%package -n 	%{libggois}
Summary:	A GUI library for OpenGL (OGRE OIS plugin)
Group:		System/Libraries
Provides:	%{name} = %{version}-%{release}
Conflicts:	%{_lib}gigi0 < %{EVRD}

%description -n %{libggois}
This package contains the shared library for GiGi (aka GG), a GUI library
for OpenGL.

%files -n %{libggois}
%{_libdir}/lib%{oname}OgrePlugin_OIS.so.%{major}*

#----------------------------------------------------------------------------

%package -n 	%{libggsdl}
Summary:	A GUI library for OpenGL (SDL)
Group:		System/Libraries
Provides:	%{name} = %{version}-%{release}
Conflicts:	%{_lib}gigi0 < %{EVRD}

%description -n %{libggsdl}
This package contains the shared library for GiGi (aka GG), a GUI library
for OpenGL.

%files -n %{libggsdl}
%{_libdir}/lib%{oname}SDL.so.%{major}*

#----------------------------------------------------------------------------

%package -n 	%{devname}
Summary:	Development headers for GiGi
Group:		System/Libraries
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}
Conflicts:	%{_lib}gigi-devel < %{EVRD}
Obsoletes:	%{_lib}gigi-devel < %{EVRD}

%description -n %{devname}
Development headers and includes for GiGi (aka GG), a GUI library
for OpenGL.

%files -n %{devname}
%{_libdir}/lib%{oname}*.so
%{_libdir}/pkgconfig/%{oname}*
%{_includedir}/GG

#----------------------------------------------------------------------------

%prep
%setup -qn GG
%patch0 -p1
%patch1 -p1

%build
# System resource usage is extremely high so disable extra flags and parallel build
%global optflags -O2
%cmake -DBUILD_DEBUG:BOON=ON
make VERBOSE=1

%install
%makeinstall_std -C build

