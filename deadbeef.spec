%global gitdate 20200703
%global commit0 d75fcb8545227ea625709d7a723687aaa521221b
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global gver .git%{shortcommit0}

%global _with_restricted 1

%global _lto_cflags %{nil}


Name:           deadbeef
Version:        1.8.8
Release:        8%{dist}
Summary:        GTK2 audio player
Group:		Applications/Multimedia
License:        GPLv2
Url:            https://deadbeef.sourceforge.net/
#Source0:	https://github.com/DeaDBeeF-Player/deadbeef/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz
Source:		https://github.com/DeaDBeeF-Player/%{name}/archive/%{version}/%{name}-%{version}.tar.gz
Source1: 	%{name}-snapshot.sh
Source2:	net.sourceforge.deadbeef.deadbeef.metainfo.xml

# external
Source3:	https://github.com/DeaDBeeF-Player/mp4p/archive/a80941da6e395953b79a1c50cb855f05cc27a5c2.zip

Source4:	https://github.com/DeaDBeeF-Player/apbuild/archive/fc5546517e74ed69ce887dd12050160470c62352.zip

BuildRequires:  dbus-devel
BuildRequires:  gcc-c++
BuildRequires:  pulseaudio
BuildRequires:  pkgconfig
BuildRequires:  intltool
BuildRequires:  turbojpeg-devel
BuildRequires:  yasm-devel
BuildRequires:	git
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:  bison
BuildRequires:	desktop-file-utils 
BuildRequires:	clang 
BuildRequires:	pulseaudio-libs-devel
BuildRequires:	clang
BuildRequires:	unzip
BuildRequires:	libdispatch-devel

BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(atk)
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(flac)
#BuildRequires:  pkgconfig(gtk+-2.0)
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(imlib2)
BuildRequires:  pkgconfig(jansson)
BuildRequires:  pkgconfig(libcddb)
BuildRequires:  pkgconfig(libcdio)
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  pkgconfig(libmpg123)
BuildRequires:  pkgconfig(libnotify)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(libzip)
BuildRequires:  pkgconfig(opusfile)
BuildRequires:  pkgconfig(pango)
BuildRequires:  pkgconfig(sndfile)
BuildRequires:  pkgconfig(vorbis)
BuildRequires:  pkgconfig(wavpack)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(zlib)

%if 0%{?_with_restricted}
BuildRequires:  faad2-devel >= 2.9.1
BuildRequires:  ffmpeg4-devel
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
%autosetup -n %{name}-%{version} -p1 -a3 
rm -rf $PWD/external/mp4p
mv -f mp4p-a80941da6e395953b79a1c50cb855f05cc27a5c2 $PWD/external/mp4p

rm -rf $PWD/external/apbuild
unzip %{S:4} && mv -f apbuild-fc5546517e74ed69ce887dd12050160470c62352 $PWD/external/apbuild

%build


export CC=clang
export CXX=clang++
export CFLAGS="%{optflags} -fno-strict-aliasing -fpie -fPIC"
export CXXFLAGS="$CFLAGS"
export LDFLAGS="$LDFLAGS -pie"

./autogen.sh

%configure \
	--enable-src=yes \
	%ifarch %{ix86}
	--disable-soundtouch \
	%endif
	--disable-static \
	--disable-rpath \
	--disable-gtk2 \
%if 0%{?_with_restricted}
	--enable-ffmpeg \
	--enable-psf    \
%endif
	--enable-gtk3 \
	--docdir=%{_docdir}/%{name}/ \
	--disable-notify 

%make_build

%install
%make_install
rm -f %buildroot/%{_libdir}/deadbeef/*.la
%find_lang %name

find . -name '.cpp' -or -name '.hpp' -or -name '*.h' | xargs chmod 644

install -Dm 644 %{S:2} %{buildroot}%{_datadir}/metainfo/net.sourceforge.deadbeef.deadbeef.metainfo.xml

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
%license COPYING.GPLv2 COPYING.LGPLv2.1
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
%{_datadir}/metainfo/net.sourceforge.deadbeef.deadbeef.metainfo.xml

%if 0%{?_with_restricted}
%files restricted-plugins
%{_libdir}/%{name}/aac.so*
%{_libdir}/%{name}/ffmpeg.so*
%endif

%files devel
%_includedir/%name

%changelog

* Wed Feb 09 2022 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.8.8-8
- Rebuilt for ffmpeg

* Thu Aug 12 2021 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.8.8-7.gitb8832d7
- Updated to 1.8.8

* Mon Feb 15 2021 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.8.7-7.git4e5e467
- Updated to 1.8.7

* Sat Jan 23 2021 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.8.6-7.gitabdd3b1
- Updated to 1.8.6

* Mon Jan 11 2021 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.8.5-7.gitbef1b4a
- Updated to 1.8.5

* Fri Jul 03 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.8.4-7.git69fa2db
- Updated to 1.8.4

* Tue Jun 23 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.8.3-9.git3e7c048
- Rebuilt for ffmpeg

* Fri Apr 10 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.8.3-8.git3e7c048
- Rebuilt for libcdio

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
