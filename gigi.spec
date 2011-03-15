%define name		gigi
%define revision	938
%define version		0.8.0
%define release		%mkrel 6
%define libname		%mklibname %name 0
%define develname	%mklibname %name -d

Summary:	A GUI library for OpenGL
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	LGPLv2+
Group:		System/Libraries
URL:		http://gigi.sourceforge.net/
Source0:	%{name}-%{revision}.tar.gz
Patch0:		gigi-938-link.patch
BuildRequires:	freetype2-devel 
BuildRequires:	boost-devel >= 1.37
BuildRequires:	ogre-devel >= 1.4.6
BuildRequires:	SDL-devel
BuildRequires:	jpeg8-devel
BuildRequires:	ois-devel
BuildRequires:	libtool-devel
BuildRequires:	cmake
BuildRequires:	doxygen
BuildRoot:	%{_tmppath}/%{name}-%{version}

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
GiGi (aka GG) is a GUI library for OpenGL. It is platform-independent 
(it runs at least on Linux and Windows, and probably more), 
compiler-independent (it compiles under at GCC 3.2 or higher and MSVC++ 7.1 
or higher, and probably more), and driver-independent. A reference driver 
for SDL is provided, and it is straightforward to write one for yourself 
should you decide to do so.

%package -n 	%{develname}
Summary:	Development headers for GiGi
Group:		System/Libraries
Provides:	%{name}-devel = %{version}-%{release}
Requires:       %{libname} = %{version}-%{release}
Conflicts:	%{libname} < %{version}-%{release}

%description -n %{develname}
Development headers and includes for GiGi (aka GG),  a GUI library 
for OpenGL. 

%prep
%setup -q -n GG
%patch0 -p0

%build
# for a strange reason, the -g flag triggers a segfault in cpp
# https://qa.mandriva.com/show_bug.cgi?id=62558
export CFLAGS="$(echo %{optflags} | sed -e s/-g//)"
export CXXFLAGS="$(echo %{optflags} | sed -e s/-g//)"
%cmake
%make

%install
rm -rf %{buildroot}
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

%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig
%endif

##### Files #####
%files -n %{libname}
%doc README COPYING INSTALLING PACKAGING
%defattr(-,root,root)
%{_libdir}/libGiGi*.so.*

%files -n %{develname}
%defattr(-,root,root)
%doc %{_docdir}/%{name}/GG
%{_libdir}/libGiGi*.so
%{_libdir}/pkgconfig/GiGi*
%{_datadir}/cmake/Modules/GG
%{_includedir}/GG
