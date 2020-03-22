%global gitdate 20200321
%global commit0 3e7c0489b331a644438f3630c78802f24d7c7e86
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global gver .git%{shortcommit0}

%global _with_restricted 1

Name:           deadbeef
Version:        1.8.3
Release:        7%{?gver}%{dist}
Summary:        GTK2 audio player
Group:		Applications/Multimedia
License:        GPLv2
Url:            http://deadbeef.sourceforge.net/
Source0:	https://github.com/Alexey-Yakovenko/deadbeef/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz
Source1: 	%{name}-snapshot.sh
Patch:		desktop.patch
# PATCH-FEATURE-UPSTREAM deadbeef-add-appdata.patch -- Add a translateable AppStream metadata file, https://github.com/Alexey-Yakovenko/deadbeef/pull/1705
Patch2:         %{name}-add-appdata.patch

BuildRequires:  alsa-lib-devel
Buildrequires:  gtk3-devel
BuildRequires:  libcurl-devel
BuildRequires:  libsamplerate-devel
BuildRequires:  libvorbis-devel
BuildRequires:  flac-devel
BuildRequires:  pkgconfig(libcddb)
BuildRequires:  libcdio-devel
BuildRequires:  libsndfile-devel
BuildRequires:  wavpack-devel
BuildRequires:  dbus-devel
BuildRequires:  gcc-c++
BuildRequires:  libnotify-devel
BuildRequires:  pulseaudio
BuildRequires:  pkgconfig
BuildRequires:  imlib2-devel
BuildRequires:  intltool
BuildRequires:  turbojpeg-devel
BuildRequires:  libzip-devel
BuildRequires:  yasm-devel
BuildRequires:	libX11-devel
BuildRequires:	git
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	jansson-devel
BuildRequires:  bison
BuildRequires:	zlib-devel
BuildRequires:	desktop-file-utils

%if 0%{?_with_restricted}
BuildRequires:  faad2-devel >= 2.9.1
BuildRequires:  ffmpeg-devel >= 4.1
BuildRequires:  libmad-devel
%endif

Requires: desktop-file-utils
Recommends: %{name}-restricted-plugins = %{version}-%{release}

%description
DeaDBeeF is an audio player for GNU/Linux and other UNIX-like systems.
It is written in C with some plugins in C++. It has minimal dependencies,
a native GTK2 GUI, cuesheet support, support for MP3, Ogg, FLAC, and APE,
chiptune formats with subtunes, song-length databases, and more.
It is very fast and lightweight, and extensible using plugins
(DSP, GUI, output, input, etc.). The GUI looks similar to Foobar2000.

%if 0%{?_with_restricted}

%package 	restricted-plugins
License:        LGPLv2
Summary:        Restricted plugins Support for %{name}
Group:		Applications/Multimedia
Requires:       %{name} = %{version}-%{release}
Provides:	deadbeef-plugins = %{version}-%{release}

%description restricted-plugins
XMMS2 is an audio framework, but it is not a general multimedia player - it
will not play videos. It has a modular framework and plugin architecture for
audio processing, visualisation and output, but this framework has not been
designed to support video. Also the client-server design of XMMS2 (and the
daemon being independent of any graphics output) practically prevents direct
video output being implemented. It has support for a wide range of audio
formats, which is expandable via plugins. It includes a basic CLI interface
to the XMMS2 framework, but most users will want to install a graphical XMMS2
client (such as gxmms2 or esperanza).
%endif

%package devel
License:        GPLv2
Group:		Development/Libraries
Summary:        Devel files for %name
Requires:       pkgconfig
Requires:       %{name} = %{version}-%{release}

%description devel
This package provides headers to develop deadbeef plugins

%prep
%autosetup -n %{name}-%{commit0} -p1

%build

./autogen.sh
%configure --enable-src=yes \
 --disable-static          \
%if 0%{?_with_restricted}
 --enable-ffmpeg \
 --enable-psf    \
%endif
 --docdir=%{_docdir}/%{name}/

make %{?_smp_mflags} V=0

%install
%make_install
rm -f %buildroot/%{_libdir}/deadbeef/*.la
%find_lang %name

find . -name '.cpp' -or -name '.hpp' -or -name '*.h' | xargs chmod 644

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

%post
/usr/bin/update-desktop-database &> /dev/null || :
/bin/touch --no-create %{_datadir}/icons/hicolor &> /dev/null || :

%postun
/usr/bin/update-desktop-database &> /dev/null || :
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &> /dev/null || :
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :

%files -f %{name}.lang
%doc %{_docdir}/%{name}/
%{_bindir}/%{name}
%{_libdir}/%{name}/
%if 0%{?_with_restricted}
%exclude %{_libdir}/%{name}/aac.so*
%exclude %{_libdir}/%{name}/ffmpeg.so*
%endif
%{_datadir}/applications/deadbeef.desktop
%{_datadir}/%{name}/
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg
%{_datadir}/appdata/%{name}.appdata.xml

%if 0%{?_with_restricted}
%files restricted-plugins
%{_libdir}/%{name}/aac.so*
%{_libdir}/%{name}/ffmpeg.so*
%endif

%files devel
%_includedir/%name

%changelog

* Sat Mar 21 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.8.3-7.git3e7c048
- Updated to 1.8.3

* Sat Nov 09 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.8.2-7.git7aafde0
- Rebuilt for faad2

* Wed Aug 07 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.8.2-2.git7aafde0
- Updated to 1.8.2

* Tue Jun 25 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.8.1-2.gitfd16773
- Updated to current commit

* Tue Apr 23 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.8.0-2.git479a641
- Updated to current commit

* Wed Feb 27 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.8.0-1.git373f556
- Updated to 1.8.0

* Fri Jan 04 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> 0.7.2-12.git06de3d0 
- Updated to current commit

* Thu Dec 06 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 0.7.2-11.gite0f03a6  
- Rebuilt for ffmpeg

* Thu Apr 26 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 0.7.2-10.gite0f03a6  
- Automatic Mass Rebuild

* Sat Apr 07 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 0.7.2-9.gite0f03a6
- Updated to current commit

* Thu Sep 28 2017 Unitedrpms Project <unitedrpms AT protonmail DOT com> 0.7.2-8.20170318git87d3fd5  
- Automatic Mass Rebuild

* Mon Jul 31 2017 Unitedrpms Project <unitedrpms AT protonmail DOT com> 0.7.2-7.20170318git87d3fd5  
- Automatic Mass Rebuild

* Sat Mar 18 2017 David Vásquez <davidjeremias82 AT gmail DOT com> - 0.7.2-6-20170318git87d3fd5
- Updated to 0.7.2-6-20170318git87d3fd5

* Thu Jan 26 2017 David Vásquez <davidjeremias82 AT gmail DOT com> - 0.7.2-5-20170126git4c5af84
- Updated to 0.7.2-20170126git4c5af84

* Thu Jun 30 2016 David Vásquez <davidjeremias82 AT gmail DOT com> - 0.7.2-4-20160427git3762995
- Massive rebuild F25

* Tue May 3  2016 Pavlo Rudyi <paulcarroty at riseup.net> - 0.7.2-3-20160427-3762995
- dropped redundant flags

* Mon May 2  2016 Pavlo Rudyi <paulcarroty at riseup.net> - 0.7.2-2-20160427-3762995
- Added scriptlets 

* Wed Apr 27 2016 David Vásquez <davidjeremias82 AT gmail DOT com> - 0.7.2-1-20160427-3762995
- Updated to 0.7.2-20160427-3762995

* Tue Mar 29 2016 David Vásquez <davidjeremias82 AT gmail DOT com> - 0.7.1-1-20160329-1cfcd8b
- Updated to 0.7.1-20160329-1cfcd8b

* Mon Aug 10 2015 David Vásquez <davidjeremias82 AT gmail DOT com> - 0.3.1-1-20150810-acb0ee4
- Initial build
