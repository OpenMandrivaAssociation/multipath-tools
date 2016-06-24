%define major 0
%define libmultipath %mklibname multipath %{major}
%define libmpathpersist %mklibname mpathpersist %{major}
%define _disable_lto 1

Summary:	Tools to manage multipathed devices with the device-mapper
Name:		multipath-tools
Version:	0.5.0
Release:	1
License:	GPLv2
Group:		System/Kernel and hardware
Url:		http://christophe.varoqui.free.fr/multipath-tools/
Source0:	http://christophe.varoqui.free.fr/multipath-tools/%{name}-%{version}.tar.bz2
Source1:	multipath.conf
Patch0:		multipath-tools-0.5.0-udevrulesdir.patch
Patch1:		multipath-tools-0.5.0-format-security.patch
BuildRequires:	libaio-devel
BuildRequires:	sysfsutils-devel
BuildRequires:	readline-devel
BuildRequires:	pkgconfig(devmapper)
BuildRequires:	pkgconfig(ncursesw)
BuildRequires:	pkgconfig(libsystemd)
Requires:	dmsetup
Requires:	kpartx = %{EVRD}
Conflicts:	kpartx < 0.4.8-16

%description
This package provides the tools to manage multipathed devices by
instructing the device-mapper multipath module what to do. The tools
are:

- multipath:	scan the system for multipathed devices, assembles them
  and update the device-mapper's maps
- multipathd:	wait for maps events, then execs multipath
- kpartx:	maps linear devmaps upon device partitions, which makes
  multipath maps partionable


%package -n %{libmultipath}
Summary:	libmultipath library
Group:		System/Libraries
Conflicts:	multipath-tools < 0.4.9-1.20121222.1

%description -n	%{libmultipath}
This package ships the libmultipath library, part of multipath-tools.

%package -n %{libmpathpersist}
Summary:	libmpathpersist library
Group:		System/Libraries
Conflicts:	multipath-tools < 0.4.9-1.20121222.1

%description -n	%{libmpathpersist}
This package ships the libmpathpersist library, part of multipath-tools.

%package -n kpartx
Summary:	Partition device manager for device-mapper devices
Group:		System/Kernel and hardware
Conflicts:	multipath-tools < 0.4.8-16

%description -n	kpartx
kpartx manages partition creation and removal for device-mapper devices.

%prep
%setup -q
%apply_patches
sed -i -e s/lsystemd-daemon/lsystemd/g multipathd/Makefile ./libmultipath/Makefile

cp %{SOURCE1} .

%build
%make -j1 BUILD="glibc" OPTFLAGS="%{optflags}" LIB=%{_lib} CC=%{__cc}

%install
%makeinstall_std bindir=/sbin syslibdir=/%{_lib} unitdir=%{_unitdir} libdir=/%{_lib}/multipath libudevdir=%{_udevrulesdir}/..

install -d %{buildroot}%{_presetdir}
cat > %{buildroot}%{_presetdir}/multipathd.preset << EOF
enable multipathd.socket
EOF

# tree fix up
install -d %{buildroot}%{_sysconfdir}/multipath
touch %{buildroot}%{_sysconfdir}/multipath.conf

#(tpg) not needed
rm -rf %{buildroot}/%{_lib}/libmpathpersist.so

%files
%doc AUTHOR README* ChangeLog FAQ
%doc multipath.conf multipath.conf.annotated multipath.conf.defaults multipath.conf.synthetic
%dir %{_sysconfdir}/multipath
%ghost %config(noreplace) %{_sysconfdir}/multipath.conf
%{_presetdir}/multipathd.preset
%{_unitdir}/multipathd.service
%{_unitdir}/multipathd.socket
%config %{_udevrulesdir}/11-dm-mpath.rules
%config %{_udevrulesdir}/62-multipath.rules
/sbin/multipath
/sbin/multipathd
/sbin/mpathconf
/sbin/mpathpersist
%{_mandir}/man?/multipath*
%{_mandir}/man?/mpath*
%dir /%{_lib}/multipath/
/%{_lib}/multipath/*

%files -n %{libmultipath}
/%{_lib}/libmultipath.so.%{major}*

%files -n %{libmpathpersist}
/%{_lib}/libmpathpersist.so.%{major}*

%files -n kpartx
/sbin/kpartx
%{_mandir}/man8/kpartx.8*
