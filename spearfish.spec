%define _mapserverdir %{_var}/www/html/mapserver

Name:		spearfish
Version:	1.0
Release:	1mdk
License:	GPL
Url:		http://grass.itc.it/data.html
Source:		http://grass.itc.it/sampledata/%{name}_grass50data.tar.bz2
Source1:	grass5-spearfish
Source2:	http://grass.itc.it/spearfish/grass5_mapserver.tar.bz2
Patch:		grass5_mapserver-mandrake-paths.patch
Summary:	The Spearfish sample GIS data set
Group:		Sciences/Geosciences
Buildroot:	%{_tmppath}/%{name}-%{version}
Buildarch:	noarch

%description
SPEARFISH data set (9.7MB size) - contains raster, vector and 
point data of South Dakota [fixed some roads vector types and 
soils topology 2/2003].

(UTM projection, Clarke66 ellipsoid, NAD27 conus)

%package grass
Summary:	Grass support for the Spearfish sample GIS data set
Requires:	grass %{name}
License:	GPL
Group:		Sciences/Geosciences

%description grass
This package allows the user to easily access the Spearfish data set
from the Grass GIS. Running grass5-spearfish will create a grassdata/spearfish
directory in the users home directory, create a link the data set, and start
Grass with the data set. This arrangement allows the user to make use of the
data set without copying the entire data set.

%package mapserver
Summary:	Mapserver support for the Spearfish sample GIS data set
Requires:	mapserver %{name}
License:	GPL
Group:		Sciences/Geosciences
Url:		http://grass.itc.it/start.html

%description mapserver
This package contains the files to support the use of the Spearfish data set
from Mapserver. The mapserver should be accessible on the local machine with
the url:
http://localhost/mapserver/spearfish

%prep

%setup -q -n %{name} -a 2
%patch

%build

%install
rm -Rf %{buildroot}
mkdir -p %{buildroot}/%{_datadir}/grass/%{name}
cp -a * %{buildroot}/%{_datadir}/grass/%{name}

mkdir -p %{buildroot}/%{_bindir}
install -m755 %{SOURCE1} %{buildroot}/%{_bindir}

mkdir -p %{buildroot}/%{_menudir}
cat << EOF > $RPM_BUILD_ROOT/%{_menudir}/%{name}-grass
?package(%{name}-grass):command="%{_bindir}/grass5-spearfish -tcltk" \
icon="grass.png" \
needs="text" \
section="Applications/Sciences/Geosciences" \
title="Grass (Spearfish)" \
longtitle="Grass using the Spearfish sample data set"
EOF

#mapserver:
mkdir -p %{buildroot}/%{_mapserverdir}/spearfish
pushd grass5_mapserver
cp -a map-script spearfish/* spearfish.html %{buildroot}/%{_mapserverdir}/spearfish
install start.html %{buildroot}/%{_mapserverdir}/spearfish/index.html
#ln -s %{_datadir}/grass/spearfish %{buildroot}/%{_mapserverdir}/spearfish/spearfish
install spearfish/.grassrc5 %{buildroot}/%{_var}/www/html
popd

%clean
rm -Rf %{buildroot}

%post grass
%update_menus

%postun grass
%clean_menus

%files
%defattr(-,root,root)
%{_datadir}/grass/%{name}

%files grass
%defattr(-,root,root)
%{_bindir}/grass5-spearfish
%{_menudir}/%{name}-grass

%files mapserver
%defattr(-,root,root)
%{_mapserverdir}/*
%{_var}/www/html/.grassrc5
%doc grass5_mapserver/README

