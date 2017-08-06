%global jsondir jsoncpp

Name:       jsoncpp
Version:    0.10.6
Release:    8%{?dist}
Summary:    JSON library implemented in C++

License:    Public Domain or MIT
URL:        https://github.com/open-source-parsers/jsoncpp
Source0:    https://github.com/open-source-parsers/%{name}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz

Patch1:     json-c-conflict.patch

BuildRequires:  cmake
BuildRequires:  doxygen
BuildRequires:  graphviz
BuildRequires:  python

%description
%{name} is an implementation of a JSON (http://json.org) reader and writer in
C++. JSON (JavaScript Object Notation) is a lightweight data-interchange format.
It is easy for humans to read and write. It is easy for machines to parse and
generate.


%package devel
Summary:    Development headers and library for %{name}
Requires:   %{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains the development headers and library for %{name}.


%package doc
Summary:    Documentation for %{name}
BuildArch:  noarch

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n %{name}-%{version}
%patch1 -p1


%build
%if 0%{?rhel} && 0%{?rhel} <= 6
export LD_LIBRARY_PATH="$(pwd)/src/lib_json:${LD_LIBRARY_PATH}"
%endif # 0%%{?rhel} && 0%%{?rhel} <= 6
%cmake -DBUILD_STATIC_LIBS=OFF                \
       -DJSONCPP_WITH_WARNING_AS_ERROR=OFF    \
       -DJSONCPP_WITH_PKGCONFIG_SUPPORT=ON    \
       -DJSONCPP_WITH_CMAKE_PACKAGE=ON        \
%if 0%{?rhel} && 0%{?rhel} <= 6
       -DJSONCPP_WITH_POST_BUILD_UNITTEST=OFF \
%endif # 0%%{?rhel} && 0%%{?rhel} <= 6
       .
make %{?_smp_mflags}
# Build the doc
python doxybuild.py --with-dot --doxygen %{_bindir}/doxygen


%install
make install DESTDIR=%{buildroot}

mkdir -p $RPM_BUILD_ROOT%{_docdir}/%{name}/html
for f in NEWS.txt README.md ; do
    install -p -m 0644 $f $RPM_BUILD_ROOT%{_docdir}/%{name}
done
install -p -m 0644 dist/doxygen/*/*.{html,png} $RPM_BUILD_ROOT%{_docdir}/%{name}/html


%check
# Tests are run automatically in the build section
# ctest -V %{?_smp_mflags}


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%license AUTHORS LICENSE
%doc %dir %{_docdir}/%{name}
%doc %{_docdir}/%{name}/README.md
%exclude %{_docdir}/%{name}/html
%{_libdir}/lib%{name}.so.*


%files devel
%doc %dir %{_docdir}/%{name}
%doc %{_docdir}/%{name}/NEWS.txt
%{_libdir}/lib%{name}.so
%{_includedir}/%{jsondir}/
%{_libdir}/cmake
%{_libdir}/pkgconfig/jsoncpp.pc


%files doc
%{?_licensedir:%license %{_datadir}/licenses/%{name}*}
%doc %{_docdir}/%{name}/


%changelog
* Sun Aug 06 2017 Jajauma's Packages <jajauma@yandex.ru> - 0.10.6-8
- Update to latest upstream release
- Drop nowerror.patch
- Bump Release to force update

* Sat Apr 23 2016 Sébastien Willmann <sebastien.willmann@gmail.com> - 0.10.5-2
- Fix file conflict with json-c

* Fri Mar 25 2016 Björn Esser <fedora@besser82.io> - 0.10.5-1
- Update to version 0.10.5
- Use %%license and %%doc properly
- Add generated CMake-target
- Move %%check after %%install
- Remove Group-tag, needed for el <= 5, only
- Drop Patch0, not needed anymore
- Disabled Werror
- Add disttag
- Use cmake instead of scons

* Fri Mar 15 2013 Sébastien Willmann <sebastien.willmann@gmail.com> - 0.6.0-0.9.rc2
- Changed Summary
- Added %%doc files to the doc package
- Added python as an explicit BuildRequires

* Fri Feb 15 2013 Sebastien Willmann <sebastien.willmann@gmail.com> - 0.6.0-0.8.rc2
- Added documentation sub-package

* Sun Jan 20 2013 Sebastien Willmann <sebastien.willmann@gmail.com> - 0.6.0-0.7.rc2
- Added graphviz as a BuildRequire

* Sat Jan 19 2013 Sebastien Willmann <sebastien.willmann@gmail.com> - 0.6.0-0.6.rc2
- Install the corrected library

* Sat Dec 22 2012 Sebastien Willmann <sebastien.willmann@gmail.com> - 0.6.0-0.5.rc2
- Added libjsoncpp.so.0
- Moved the shared lib build to the correct section

* Fri Dec 21 2012 Sebastien Willmann <sebastien.willmann@gmail.com> - 0.6.0-0.4.rc2
- Removed doc subpackage
- Added .pc file
- Fixed shared lib

* Wed Dec 12 2012 Sebastien Willmann <sebastien.willmann@gmail.com> - 0.6.0-0.3.rc2
- Removed static package
- Preserving timestamp on installed files
- Added guard grep to the sed expression
- Removed duplicated doc files
- Removed dependency on pkgconfig
- Changed base package group

* Sun Dec 02 2012 Sébastien Willmann <sebastien.willmann@gmail.com> - 0.6.0-0.2.rc2
- Changed license field to Public Domain or MIT

* Tue Nov 27 2012 Sébastien Willmann <sebastien.willmann@gmail.com> 0.6.0-0.1.rc2
- Creation of the spec file

