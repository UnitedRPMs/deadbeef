# deadbeef-0.7.1-20160427-499da45.tar.xz
%global gitdate 20160427
%global gitversion 499da45
%global snapshot %{gitdate}-%{gitversion}
%global gver .%{gitdate}git%{gitversion}

%global _with_restricted 1

Name:           deadbeef
Version:        0.7.1
Release:        2%{?gver}%{dist}
Summary:        GTK2 audio player
Group:          Productivity/Multimedia/Sound/Players
License:        GPL-2.0+
Url:            http://deadbeef.sourceforge.net/
Source0:	%{name}-%{version}-%{snapshot}.tar.xz
Source1: 	%{name}-snapshot.sh

BuildRequires:  alsa-lib-devel
Buildrequires:  gtk3-devel
BuildRequires:  libcurl-devel
BuildRequires:  libsamplerate-devel
BuildRequires:  libvorbis-devel
BuildRequires:  flac-devel
BuildRequires:  libcddb-devel
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

%if 0%{?_with_restricted}
BuildRequires:  faad2-devel
BuildRequires:  ffmpeg-devel
BuildRequires:  libmad-devel
%endif

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
License:        GPL+ or Artistic
Summary:        Restricted plugins Support for %{name}
Group:          Productivity/Multimedia/Sound/Players
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
Group:          Development/Libraries/C and C++
Summary:        Devel files for %name
Requires:       pkgconfig
Requires:       %{name} = %{version}-%{release}

%description devel
This package provides headers to develop deadbeef plugins

%prep
%setup -n deadbeef


%build
export CFLAGS="%optflags"
export CXXFLAGS="%optflags"

./autogen.sh
%configure --enable-src=yes \
%if 0%{?_with_restricted}
 --enable-ffmpeg \
%endif

make

%install
%makeinstall
rm -f %buildroot/%_libdir/deadbeef/*.la
%find_lang %name


%files 

%{_bindir}/deadbeef
%{_libdir}/deadbeef/
%if 0%{?_with_restricted}
%exclude %{_libdir}/deadbeef/aac.so*
%exclude %{_libdir}/deadbeef/ffmpeg.so*
%endif
%{_datadir}/applications/deadbeef.desktop
%{_datadir}/deadbeef/
%{_docdir}/deadbeef/
%{_datadir}/icons/hicolor/*/apps/deadbeef.png
%{_datadir}/icons/hicolor/scalable/apps/deadbeef.svg
%{_datadir}/locale/*/LC_MESSAGES/deadbeef.mo

%if 0%{?_with_restricted}
%files restricted-plugins
%_libdir/deadbeef/aac.so*
%_libdir/deadbeef/ffmpeg.so*
%endif

%files devel
%_includedir/%name

%changelog

* Wed Apr 27 2016 David Vásquez <davidjeremias82 AT gmail DOT com> - 0.7.1-20160427-499da45-2
- Updated to 0.7.1-20160427-499da45

* Tue Mar 29 2016 David Vásquez <davidjeremias82 AT gmail DOT com> - 0.7.1-20160329-1cfcd8b-1
- Updated to 0.7.1-20160329-1cfcd8b

* Mon Aug 10 2015 David Vásquez <davidjeremias82 AT gmail DOT com> - 0.3.1-20150810-acb0ee4-1
- Initial build
