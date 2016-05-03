# deadbeef-0.7.2-20160427-3762995.tar.xz
%global gitdate 20160427
%global gitversion 3762995
%global snapshot %{gitdate}-%{gitversion}
%global gver .%{gitdate}git%{gitversion}

%global _with_restricted 1

Name:           deadbeef
Version:        0.7.2
Release:        2%{?gver}%{dist}
Summary:        GTK2 audio player
Group:		Applications/Multimedia
License:        GPLv2
Url:            http://deadbeef.sourceforge.net/
Source0:	%{name}-%{version}-%{snapshot}.tar.xz
Source1: 	%{name}-snapshot.sh
Patch:		desktop.patch

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
BuildRequires:	desktop-file-utils

%if 0%{?_with_restricted}
BuildRequires:  faad2-devel
BuildRequires:  ffmpeg-devel
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
%setup -n deadbeef
%patch -p0


%build

./autogen.sh
%configure --enable-src=yes \
%if 0%{?_with_restricted}
 --enable-ffmpeg \
%endif

make

%install
%make_install
rm -f %buildroot/%_libdir/deadbeef/*.la
%find_lang %name


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


%if 0%{?_with_restricted}
%files restricted-plugins
%_libdir/deadbeef/aac.so*
%_libdir/deadbeef/ffmpeg.so*
%endif

%files devel
%_includedir/%name

%changelog
* Mon May 2  2016 Pavlo Rudyi <paulcarroty at riseup.net> - 0.7.2-20160427-3762995-2
- Added scriptlets 

* Wed Apr 27 2016 David Vásquez <davidjeremias82 AT gmail DOT com> - 0.7.2-20160427-3762995-1
- Updated to 0.7.2-20160427-3762995

* Tue Mar 29 2016 David Vásquez <davidjeremias82 AT gmail DOT com> - 0.7.1-20160329-1cfcd8b-1
- Updated to 0.7.1-20160329-1cfcd8b

* Mon Aug 10 2015 David Vásquez <davidjeremias82 AT gmail DOT com> - 0.3.1-20150810-acb0ee4-1
- Initial build
