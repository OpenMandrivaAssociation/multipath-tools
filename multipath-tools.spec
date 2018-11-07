%define major 0
%define libmultipath %mklibname multipath %{major}
%define libmpathpersist %mklibname mpathpersist %{major}
%define libmpathcmd %mklibname mpathcmd %{major}
%define libdmmp %mklibname dmmp 0
%define devname %mklibname multipath-tools -d
%define devdmmp %mklibname dmmp -d

%define _disable_lto 1
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}devel\\(libmpathcmd

Summary:	Tools to manage multipathed devices with the device-mapper
Name:		multipath-tools
Version:	0.7.8
Release:	2
License:	GPLv2
Group:		System/Kernel and hardware
Url:		http://christophe.varoqui.free.fr/
# The source for this package was pulled from upstream's git repo.  Use the
# following command to generate the tarball
# curl "https://git.opensvc.com/?p=multipath-tools/.git;a=snapshot;h=refs/tags/0.7.8;sf=tgz" -o multipath-tools-0.7.8.tgz
Source0:	%{name}-%{version}.tgz
Source1:	multipath.conf

# (tpg) patches from upstream
Patch0001:	0001-multipath-tweak-logging-style.patch
Patch0002:	0002-multipathd-check-for-NULL-udevice-in-cli_add_path.patch
Patch0003:	0003-libmultipath-remove-max_fds-code-duplication.patch
Patch0004:	0004-multipathd-set-return-code-for-multipathd-commands.patch
Patch0005:	0005-mpathpersist-fix-registration-rollback-issue.patch
Patch0006:	0006-libmultipath-timeout-on-unresponsive-tur-thread.patch
Patch0007:	0007-RH-fixup-udev-rules-for-redhat.patch
Patch0008:	0008-RH-Remove-the-property-blacklist-exception-builtin.patch
Patch0009:	0009-RH-don-t-start-without-a-config-file.patch
Patch0010:	0010-RH-use-rpm-optflags-if-present.patch
Patch0011:	0011-RH-add-mpathconf.patch
Patch0012:	0012-RH-add-wwids-from-kernel-cmdline-mpath.wwids-with-A.patch
Patch0013:	0013-RH-warn-on-invalid-regex-instead-of-failing.patch
Patch0014:	0014-RH-reset-default-find_mutipaths-value-to-off.patch
Patch0100:	multipath-tools-0.7.7-udev-dirs.patch

BuildRequires:	libaio-devel
BuildRequires:	sysfsutils-devel
BuildRequires:	readline-devel
BuildRequires:	pkgconfig(liburcu)
BuildRequires:	pkgconfig(devmapper)
BuildRequires:	pkgconfig(ncursesw)
BuildRequires:	pkgconfig(json-c)
BuildRequires:	pkgconfig(libsystemd)
BuildRequires:	systemd
BuildRequires:	systemd-macros

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

%description -n %{libmultipath}
This package ships the libmultipath library, part of multipath-tools.

%package -n %{libmpathpersist}
Summary:	libmpathpersist library
Group:		System/Libraries
Conflicts:	multipath-tools < 0.4.9-1.20121222.1

%description -n %{libmpathpersist}
This package ships the libmpathpersist library, part of multipath-tools.

%package -n %{libmpathcmd}
Summary:	libmpathcmd library
Group:		System/Libraries

%description -n %{libmpathcmd}
This package ships the libmpathcmd library, part of multipath-tools.

%package -n %{devname}
Summary:	Development libraries and headers for %{name}
Group:		Development/C
Requires:	%{name} = %{EVRD}
Requires:	%{libmultipath} = %{EVRD}
Requires:	%{libmpathpersist} = %{EVRD}
Requires:	%{libmpathcmd} = %{EVRD}
Provides:	device-mapper-multipath-devel = %{EVRD}
Provides:	multipath-devel = %{EVRD}
Provides:	%{name}-devel = %{EVRD}

%description -n %{devname}
This package contains the files need to develop applications that use
device-mapper-multipath's lbmpathpersist and libmpathcmd libraries.

%package -n kpartx
Summary:	Partition device manager for device-mapper devices
Group:		System/Kernel and hardware
Conflicts:	multipath-tools < 0.4.8-16

%description -n kpartx
kpartx manages partition creation and removal for device-mapper devices.

%package -n %{libdmmp}
Summary:	device-mapper-multipath C API library
Group:		System/Libraries
#Requires: json-c
Requires:	%{name} = %{EVRD}

%description -n %{libdmmp}
This package contains the shared library for the device-mapper-multipath
C API library.

%package -n %{devdmmp}
Summary:	device-mapper-multipath C API library headers
Group:		Development/C
Requires:	%{libdmmp} = %{EVRD}
Provides:	libdmmp-devel = %{EVRD}

%description -n %{devdmmp}
This package contains the files needed to develop applications that use
device-mapper-multipath's libdmmp C API library

%prep
%autosetup -p1

cp %{SOURCE1} .

%build
%make_build -j1 BUILD="glibc" OPTFLAGS="%{optflags}" LIB=%{_lib} CC=%{__cc} udevdir="/lib/udev" udevrulesdir="%{_udevrulesdir}" unitdir=%{_unitdir}

%install
%make_install udevdir="/lib/udev" udevrulesdir="%{_udevrulesdir}" unitdir=%{_unitdir} pkgconfdir=%{_libdir}/pkgconfig

install -d %{buildroot}%{_presetdir}
cat > %{buildroot}%{_presetdir}/86-multipathd.preset << EOF
enable multipathd.socket
EOF

# tree fix up
install -d %{buildroot}%{_sysconfdir}/multipath
rm -rf %{buildroot}/%{_initrddir}

%files
%doc README*
%dir %{_sysconfdir}/multipath
%ghost %config(noreplace) %{_sysconfdir}/multipath.conf
%{_udevrulesdir}/*path.rules
%{_udevrulesdir}/*part*.rules
%{_presetdir}/86-multipathd.preset
%{_unitdir}/multipathd.service
%{_unitdir}/multipathd.socket
/sbin/multipath
/sbin/multipathd
/sbin/mpathconf
/sbin/mpathpersist
/sbin/mpathconf
%dir /%{_lib}/multipath/
/%{_lib}/multipath/*
%{_mandir}/man?/*dmmp*
%{_mandir}/man?/multipath*
%{_mandir}/man?/mpath*

%files -n %{libmultipath}
/%{_lib}/libmultipath.so.%{major}*

%files -n %{libmpathpersist}
/%{_lib}/libmpathpersist.so.%{major}*

%files -n %{libmpathcmd}
/%{_lib}/libmpathcmd.so.%{major}*

%files -n %{libdmmp}
/%{_lib}/libdmmp.so.%{major}*

%files -n %{devname}
/%{_lib}/libmpathpersist.so
/%{_lib}/libmpathcmd.so
/%{_lib}/libmultipath.so
%{_includedir}/mpath_cmd.h
%{_includedir}/mpath_persist.h
%{_mandir}/man3/mpath_persistent_reserve_in.3.*
%{_mandir}/man3/mpath_persistent_reserve_out.3.*

%files -n %{devdmmp}
/%{_lib}/libdmmp.so
%dir %{_includedir}/libdmmp
%{_includedir}/libdmmp/*
%{_mandir}/man3/dmmp_*
%{_mandir}/man3/libdmmp.h.3.*
%{_libdir}/pkgconfig//libdmmp.pc

%files -n kpartx
%{_udevrulesdir}/*kpartx.rules
/sbin/kpartx
/lib/udev/kpartx_id
%{_mandir}/man8/kpartx.8*
