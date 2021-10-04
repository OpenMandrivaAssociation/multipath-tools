%define major 0
%define libmultipath %mklibname multipath %{major}
%define libmpathpersist %mklibname mpathpersist %{major}
%define libmpathcmd %mklibname mpathcmd %{major}
%define libmpathvalid %mklibname mpathvalid %{major}
%define libdmmp %mklibname dmmp 0
%define devname %mklibname multipath-tools -d
%define devdmmp %mklibname dmmp -d

%define _disable_ld_no_undefined 1
%define _disable_lto 1
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}devel\\(libmpathcmd
%define systemd_ver %(pkg-config --modversion systemd 2> /dev/null)

Summary:	Tools to manage multipathed devices with the device-mapper
Name:		multipath-tools
Version:	0.8.6
Release:	2
License:	GPLv2
Group:		System/Kernel and hardware
Url:		http://christophe.varoqui.free.fr/
Source0:	https://github.com/opensvc/multipath-tools/archive/%{version}.tar.gz
Source1:	multipath.conf
Patch0001:	0001-libmultipath-fix-memory-leak-in-checker_cleanup_thre.patch
Patch0002:	0002-multipathd-fix-compilation-issue-with-liburcu-0.8.patch
Patch0003:	0003-multipathd-don-t-fail-to-remove-path-once-the-map-is.patch
Patch0004:	0004-multipathd-remove-duplicate-orphan_paths-in-flush_ma.patch
Patch0005:	0005-multipathd-fix-ev_remove_path-return-code-handling.patch
Patch0006:	0006-multipath-free-vectors-in-configure.patch
Patch0007:	0007-kpartx-Don-t-leak-memory-when-getblock-returns-NULL.patch
Patch0008:	0008-multipathd-don-t-rescan_path-on-wwid-change-in-uev_u.patch
Patch0009:	0009-multipathd-cli_handlers-cleanup-setting-reply-length.patch
Patch0010:	0010-multipathd-cli_getprkey-fix-return-value.patch
Patch0011:	0011-multipath-tools-enable-Wformat-overflow-2.patch
Patch0012:	0012-libdmmp-use-KBUILD_BUILD_TIMESTAMP-when-building-man.patch
Patch0013:	0013-multipath-tools-add-info-about-HPE-Alletra-6000-and-.patch
Patch0014:	0014-multipathd-don-t-start-in-containers.patch
Patch0015:	0015-libmultipath-fix-build-without-LIBDM_API_DEFERRED.patch
Patch0016:	0016-libmultipath-use-uint64_t-for-sg_id.lun.patch
Patch0017:	0017-multipath-tools-Remove-trailing-leading-whitespaces.patch
Patch0018:	0018-multipath-tools-make-HUAWEI-XSG1-config-work-with-al.patch
Patch0019:	0019-multipath.conf-fix-typo-in-ghost_delay-description.patch
Patch0020:	0020-mpathpersist-fail-commands-when-no-usable-paths-exis.patch
Patch0021:	0021-multipath-print-warning-if-multipathd-is-not-running.patch
Patch0022:	0022-libmultipath-remove-unneeded-code-in-coalesce_paths.patch
Patch0023:	0023-libmultipath-deal-with-dynamic-PTHREAD_STACK_MIN.patch
Patch0024:	0024-RH-fixup-udev-rules-for-redhat.patch
Patch0025:	0025-RH-Remove-the-property-blacklist-exception-builtin.patch
Patch0026:	0026-RH-don-t-start-without-a-config-file.patch
Patch0027:	0027-RH-Fix-nvme-function-missing-argument.patch
Patch0028:	0028-RH-use-rpm-optflags-if-present.patch
Patch0029:	0029-RH-add-mpathconf.patch
Patch0030:	0030-RH-add-wwids-from-kernel-cmdline-mpath.wwids-with-A.patch
Patch0031:	0031-RH-reset-default-find_mutipaths-value-to-off.patch
Patch0032:	0032-RH-attempt-to-get-ANA-info-via-sysfs-first.patch
Patch0033:	0033-RH-make-parse_vpd_pg83-match-scsi_id-output.patch
BuildRequires:	libaio-devel
BuildRequires:	sysfsutils-devel
BuildRequires:	pkgconfig(readline)
BuildRequires:	pkgconfig(liburcu)
BuildRequires:	pkgconfig(devmapper)
BuildRequires:	pkgconfig(ncursesw)
BuildRequires:	pkgconfig(json-c)
BuildRequires:	pkgconfig(libsystemd)
BuildRequires:	systemd

Requires:	dmsetup
Requires:	kpartx = %{EVRD}
Conflicts:	kpartx < 0.4.8-16
%systemd_requires

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

%package -n %{libmpathvalid}
Summary:	libmpathvalid library
Group:		System/Libraries

%description -n %{libmpathvalid}
This package ships the libmpathvalid library, part of multipath-tools.

%package -n %{devname}
Summary:	Development libraries and headers for %{name}
Group:		Development/C
Requires:	%{name} = %{EVRD}
Requires:	%{libmultipath} = %{EVRD}
Requires:	%{libmpathpersist} = %{EVRD}
Requires:	%{libmpathcmd} = %{EVRD}
Requires:	%{libmpathvalid} = %{EVRD}
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
%set_build_flags
%make_build BUILD="glibc" RPM_OPT_FLAGS="%{optflags} -Wno-strict-aliasing" LIB=%{_libdir} CC=%{__cc} udevdir="$(dirname %{_udevrulesdir})" udevrulesdir="%{_udevrulesdir}" unitdir=%{_unitdir} SYSTEMD=%{systemd_ver} -j1

%install
%make_install \
	syslibdir=%{_libdir} \
	usrlibdir=%{_libdir} \
	libdir=%{_libdir}/multipath \
	libudevdir="/lib/udev" \
	udevrulesdir="%{_udevrulesdir}" \
	unitdir=%{_unitdir} \
	includedir=%{_includedir} \
	pkgconfdir=%{_libdir}/pkgconfig

rm -rf %{buildroot}%{_sysconfig}/hotplug.d

install -d %{buildroot}%{_presetdir}
cat > %{buildroot}%{_presetdir}/86-multipathd.preset << EOF
enable multipathd.socket
EOF

# tree fix up
install -d %{buildroot}%{_sysconfdir}/multipath
rm -rf %{buildroot}/%{_initrddir}

%post
%systemd_post multipathd.socket

%preun
%systemd_preun multipathd.service

%postun
%systemd_postun_with_restart multipathd.service

%files
%doc README*
%dir %{_sysconfdir}/multipath
%ghost %config(noreplace) %{_sysconfdir}/multipath.conf
%config %{_udevrulesdir}//62-multipath.rules
%config %{_udevrulesdir}//11-dm-mpath.rules
%{_presetdir}/86-multipathd.preset
%{_unitdir}/multipathd.service
%{_unitdir}/multipathd.socket
%{_sbindir}/multipath
%{_sbindir}/mpathconf
%{_sbindir}/multipathd
%{_sbindir}/mpathpersist
%dir %{_libdir}/multipath/
%{_libdir}/multipath/*
%doc %{_mandir}/man?/*dmmp*
%doc %{_mandir}/man?/multipath*
%doc %{_mandir}/man?/mpath*

%files -n %{libmultipath}
%{_libdir}/libmultipath.so.%{major}{,.*}

%files -n %{libmpathpersist}
%{_libdir}/libmpathpersist.so.%{major}*

%files -n %{libmpathcmd}
%{_libdir}/libmpathcmd.so.%{major}*

%files -n %{libmpathvalid}
%{_libdir}/libmpathvalid.so.%{major}*

%files -n %{libdmmp}
%{_libdir}/libdmmp.so.%{major}*

%files -n %{devname}
%{_libdir}/libmpathpersist.so
%{_libdir}/libmpathcmd.so
%{_libdir}/libmultipath.so
%{_libdir}/libmpathvalid.so
%{_includedir}/mpath_cmd.h
%{_includedir}/mpath_persist.h
%{_includedir}/mpath_valid.h
%doc %{_mandir}/man3/mpath_persistent_reserve_in.3.*
%doc %{_mandir}/man3/mpath_persistent_reserve_out.3.*

%files -n %{devdmmp}
%{_libdir}/libdmmp.so
%dir %{_includedir}/libdmmp
%{_includedir}/libdmmp/*
%doc %{_mandir}/man3/dmmp_*
%doc %{_mandir}/man3/libdmmp.h.3.*
%{_libdir}/pkgconfig/libdmmp.pc

%files -n kpartx
%config %{_udevrulesdir}/11-dm-parts.rules
%config %{_udevrulesdir}/66-kpartx.rules
%config %{_udevrulesdir}/68-del-part-nodes.rules
%{_sbindir}/kpartx
/lib/udev/kpartx_id
%doc %{_mandir}/man8/kpartx.8*
