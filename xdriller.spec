%define debug_package %{nil}

#
# spec file for package xdriller
#
# Copyright (c) 2014 SUSE LINUX Products GmbH, Nuernberg, Germany.
# Copyright (c) 2014 B1 Systems GmbH, Vohburg, Germany.
# Copyright Vincent Petry <PVince81@yahoo.fr>
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#


Name:           xdriller
BuildRequires:  pkgconfig(sdl)
BuildRequires:  SDL_mixer-devel
BuildRequires:  gcc-c++
BuildRequires:  gettext
BuildRequires:  pkgconfig(OIS)
BuildRequires:  pkgconfig(OGRE)
BuildRequires:  pkgconfig(OGRE-Overlay)
BuildRequires:  pkgconfig(ogg)
BuildRequires:  libtinyxml-devel
BuildRequires:	boost-devel
Summary:        Drill through Tetris-like screens of blocks
License:        GPL-3.0
Group:          Games/Arcade
Version:        0.8.0
Release:        2
# Downloaded from SourceForge
Source:         %{name}-%{version}.tar.bz2
# Wrapper that copies the default config files to the user's
# $HOME/.config/xdriller/
Source1:        %{name}-wrapper.sh
Patch0:         %{name}-tinyxml.patch
Patch1:         ogre-1.8_fix.patch
# PATCH-FIX-OPENSUSE ogre-1.9_fix.patch -- fix build with ogre-1.9 -- seife+obs@b1-systems.com
Patch2:         ogre-1.9_fix.patch
Url:            http://xdriller.sourceforge.net/
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
Xdriller is a portable Puzzle/Arcade video game. Xdriller is based 
on the gameplay of the Mr. Driller series, where you have to drill 
through Tetris-like screens of blocks and collect power-ups while 
avoiding being squashed by falling blocks.

Features:
---------

* A lot of fun

* Two characters to choose from

* Levels are png images where each pixel represents a block. 
  Can be made with Gimp, etc...

* Infinite random levels

* Internationalization with gettext. Translations: English, 
  Spanish, Catalan, Euskara and German

* Joystick/Gamepad control

* Force Feedback "Rumble" on devices that support it (linux only).
  I've only tested it with Logitech RumblePad2 gamepad but should 
  work with the Xbox controller too.

* And the list goes on...

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

sed -i 's|OIS/OIS|ois/OIS|' include/*.h

# Clean up backup files
find -name \*~ -delete

# Remove invalid version number in desktop file
sed -i -e /^Version/d %{name}.desktop

# Fix data path
sed -i -e "s|/usr/lib/OGRE|%{_libdir}/OGRE|" -e "s|/usr/share/games/xdriller/\?|%{_datadir}/%{name}/|g" src/GameManager.cpp default_config/*.cfg

# Remove tinyxml sources, as we're using the shared tinyxml one
rm src/tiny{str,xml*}.cpp include/tiny{str,xml}.h

# For some reason the italian translation is installed but not compiled
sed -i -e "s/\(^LOCALES\s*=.*$\)/\1 it/" Makefile

%build
%make

%install
%makeinstall_std
mv %{buildroot}%{_bindir}/%{name} %{buildroot}%{_bindir}/%{name}-bin
install -m 755 %{S:1} %{buildroot}%{_bindir}/%{name}

%find_lang %{name}

%files
%doc COPYING README
%{_bindir}/%{name}
%{_bindir}/%{name}-bin
%dir %{_datadir}/%{name}/
%dir %{_datadir}/%{name}/default_config
%dir %{_datadir}/%{name}/sounds
%dir %{_datadir}/%{name}/locale
%{_datadir}/%{name}/media.zip
%{_datadir}/%{name}/default_config/*
%{_datadir}/%{name}/sounds/*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/%{name}/locale/*
