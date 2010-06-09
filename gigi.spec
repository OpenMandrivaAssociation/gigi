###### Predefinitions #####
%define name		gigi
%define oname		GG
%define revision	812
%define version		0.7.0
%define release		%mkrel 0.1.%{revision}
%define libname		%mklibname %name 0
%define develname	%mklibname %name -d

##### Header #####
Summary:	A GUI library for OpenGL
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source0:	%{name}-%{version}.%{revision}svn.tar.lzma
Patch0:		%{name}-%{version}-symlink-fix.patch
License:	LGPLv2.1
Group:		System/Libraries
URL:		http://gigi.sourceforge.net/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}

BuildRequires:	freetype2-devel 
BuildRequires:	boost-devel >= 1.37
BuildRequires:	ogre-devel >= 1.4.6
BuildRequires:	scons
BuildRequires:	SDL-devel
BuildRequires:	jpeg8-devel
BuildRequires:	ois-devel
#Obsoletes:	%{name} < %{version}-%{release}
#Obsoletes:	%{develname} < %{version}-%{release}

##### Description #####
%description
GiGi (aka GG) is a GUI library for OpenGL. It is platform-independent 
(it runs at least on Linux and Windows, and probably more), 
compiler-independent (it compiles under at GCC 3.2 or higher and MSVC++ 7.1 
or higher, and probably more), and driver-independent. A reference driver 
for SDL is provided, and it is straightforward to write one for yourself 
should you decide to do so.

##### Subpackages #####
%package -n 	%{libname}
Summary:	A GUI library for OpenGL
Group:		System/Libraries
Provides:	%{name} = %{version}-%{release}
Provides:	lib%{name} = %{version}-%{release}
Provides:	lib%{oname} = %{version}-%{release}
Requires:	libjpeg libtiff boost SDL12

%description -n %{libname}
GiGi (aka GG) is a GUI library for OpenGL. It is platform-independent 
(it runs at least on Linux and Windows, and probably more), 
compiler-independent (it compiles under at GCC 3.2 or higher and MSVC++ 7.1 
or higher, and probably more), and driver-independent. A reference driver 
for SDL is provided, and it is straightforward to write one for yourself 
should you decide to do so.

##### Subpackages #####
%package -n 	%{develname}
Summary:	Development headers for GiGi
Group:		System/Libraries
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{develname}
Development headers and includes for GiGi (aka GG),  a GUI library 
for OpenGL. 


##### setup, build, install #####
%prep
%setup -q -n %{oname}
%patch0 -p0

%build
# Unless things evolves otherwise, DeVIL is not necessary...
%configure_scons use_devil=0 build_tutorials=no --install=%{buildroot}
%scons

%install
rm -rf %{buildroot}
%scons_install --install=%{buildroot}

cd %{buildroot}/%{_libdir}
ln -s libGiGi.so.0.6.0 libGiGi.so
ln -s libGiGiOgre.so.0.6.0 libGiGiOgre.so
ln -s libGiGiSDL.so.0.6.0 libGiGiSDL.so
mv libGiGiOgrePlugin_OIS.so libGiGiOgrePlugin_OIS.so.0.6.0
ln -s libGiGiOgrePlugin_OIS.so.0.6.0 libGiGiOgrePlugin_OIS.so
cd -

%ifarch x86_64
mkdir %{buildroot}/usr/lib64/pkgconfig
mv %{buildroot}/usr/lib/pkgconfig/* %{buildroot}/usr/lib64/pkgconfig
%endif

%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig
%endif

##### Files #####
%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libGiGi*

%files -n %{develname}
%defattr(-,root,root)
%{_libdir}/pkgconfig/GiGi*
%dir %{_includedir}/%{oname}
%{_includedir}/%{oname}/*
%attr(644,root,root) %{_includedir}/%{oname}/EveGlue.h
