%bcond_without	uclibc
%define	gitdate	20130222

Summary:	Tools to manage multipathed devices with the device-mapper
Name:		multipath-tools
Version:	0.4.9
Release:	2%{?gitdate:.%{gitdate}.1}
License:	GPLv2
Group:		System/Kernel and hardware
Url:		http://christophe.varoqui.free.fr/multipath-tools/
Source0:	multipath-tools-130222.tgz
Source1:	multipathd.init
Source2:	multipath.conf
# Fedora patches
Patch0001:	0001-RH-dont_start_with_no_config.patch
Patch0002:	0002-RH-multipath.rules.patch
Patch0003:	0003-RH-Make-build-system-RH-Fedora-friendly.patch
Patch0004:	0004-RH-multipathd-blacklist-all-by-default.patch
Patch0005:	0005-RH-add-mpathconf.patch
Patch0006:	0006-RH-add-find-multipaths.patch
Patch0007:	0007-RH-add-hp_tur-checker.patch
Patch0008:	0008-RH-revert-partition-changes.patch
Patch0009:	0009-RH-RHEL5-style-partitions.patch
Patch0010:	0010-RH-dont-remove-map-on-enomem.patch
Patch0011:	0011-RH-deprecate-uid-gid-mode.patch
Patch0012:	0012-RH-kpartx-msg.patch
Patch0013:	0013-RHBZ-883981-cleanup-rpmdiff-issues.patch
Patch0014:	0014-RH-handle-other-sector-sizes.patch
Patch0015:	0015-RH-fix-output-buffer.patch
Patch0016:	0016-RH-dont-print-ghost-messages.patch
#Patch0017:	0017-RH-fix-sigusr1.patch
Patch0018:	0018-RH-fix-factorize.patch
Patch0019:	0019-RH-fix-sockets.patch
Patch0020:	0020-RHBZ-907360-static-pthread-init.patch
Patch0021:	0021-RHBZ-919119-respect-kernel-cmdline.patch
Patch0022:	0022-RH-multipathd-check-wwids.patch
Patch0023:	0023-RH-multipath-wipe-wwid.patch
Patch0024:	0024-RH-multipath-wipe-wwids.patch
Patch0025:	0025-UPBZ-916668_add_maj_min.patch
Patch0026:	0026-fix-checker-time.patch
Patch0027:	0027-RH-get-wwid.patch
Patch0028:	0028-RHBZ-929078-refresh-udev-dev.patch
Patch0029:	0029-RH-no-prio-put-msg.patch
Patch0030:	0030-RHBZ-916528-override-queue-no-daemon.patch
Patch0031:	0031-RHBZ-957188-kpartx-use-dm-name.patch
Patch0032:	0032-RHBZ-956464-mpathconf-defaults.patch
Patch0033:	0033-RHBZ-829963-e-series-conf.patch
Patch0034:	0034-RHBZ-851416-mpathconf-display.patch
Patch0035:	0035-RHBZ-891921-list-mpp.patch
Patch0036:	0036-RHBZ-949239-load-multipath-module.patch
Patch0037:	0037-RHBZ-768873-fix-rename.patch
Patch0038:	0038-RHBZ-799860-netapp-config.patch
Patch0039:	0039-RH-detect-prio-fix.patch
Patch0040:	0040-RH-bindings-fix.patch
Patch0041:	0041-RH-check-for-erofs.patch
Patch0042:	0042-UP-fix-signal-handling.patch
Patch0043:	0043-RH-signal-waiter.patch
Patch0044:	0044-RHBZ-976688-fix-wipe-wwids.patch
Patch0045:	0045-RHBZ-977297-man-page-fix.patch
Patch0046:	0046-RHBZ-883981-move-udev-rules.patch
Patch0047:	0047-RHBZ-980777-kpartx-read-only-loop-devs.patch
Patch0048:	0048-RH-print-defaults.patch
Patch0049:	0049-RH-remove-ID_FS_TYPE.patch
#Patch0050:	0050-RH-listing-speedup.patch
Patch0051:	0051-UP-fix-cli-resize.patch
Patch0052:	0052-RH-fix-bad-derefs.patch
Patch0053:	0053-UP-fix-failback.patch
Patch0054:	0054-UP-keep-udev-ref.patch
Patch0055:	0055-UP-handle-quiesced-paths.patch
Patch0056:	0056-UP-alua-prio-fix.patch
Patch0057:	0057-UP-fix-tmo.patch
Patch0058:	0058-UP-fix-failback.patch
Patch0059:	0059-UP-flush-failure-queueing.patch
Patch0060:	0060-UP-uevent-loop-udev.patch
Patch0061:	0061-RH-display-find-mpaths.patch
Patch0062:	0062-RH-dont-free-vecs.patch
Patch0063:	0063-RH-fix-warning.patch
Patch0064:	0064-fix-ID_FS-attrs.patch
Patch0065:	0065-UPBZ-995538-fail-rdac-on-unavailable.patch
Patch0066:	0066-UP-dos-4k-partition-fix.patch
Patch0067:	0067-RHBZ-1022899-fix-udev-partition-handling.patch
Patch0068:	0068-RHBZ-1034578-label-partition-devices.patch
Patch0069:	0069-UPBZ-1033791-improve-rdac-checker.patch
Patch0070:	0070-RHBZ-1036503-blacklist-td-devs.patch
Patch0071:	0071-RHBZ-1031546-strip-dev.patch
Patch0072:	0072-RHBZ-1039199-check-loop-control.patch
Patch0073:	0073-RH-update-build-flags.patch
Patch0074:	0074-RHBZ-1056976-dm-mpath-rules.patch
Patch0075:	0075-RHBZ-1056976-reload-flag.patch
Patch0076:	0076-RHBZ-1056686-add-hw_str_match.patch
#Patch0077:
Patch0078:	0078-RHBZ-1054044-fix-mpathconf-manpage.patch
Patch0079:	0079-RHBZ-1070581-add-wwid-option.patch
Patch0080:	0080-RHBZ-1075796-cmdline-wwid.patch


# our patches
Patch1000:	multipath-tools-0.4.9-20130222-whole-program.patch
# fix path set by redhat path
Patch1001:	multipath-tools-0.4.9-20121222-fix-doc-path-to-config.patch
Patch1002:	multipath-tools-0.4.9-20130222-libudevdir.patch

BuildRequires:	libaio-devel
BuildRequires:	sysfsutils-devel
BuildRequires:	readline-devel
BuildRequires:	pkgconfig(devmapper) 
BuildRequires:	pkgconfig(ncursesw)
%if %{with uclibc}
BuildRequires:	uClibc-devel
%endif
Requires(post,preun,postun):	systemd-units
Requires:	dmsetup
Requires:	kpartx = %{version}
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

%define	major	0
%define	libmultipath %mklibname multipath %{major}

%package -n	%{libmultipath}
Summary:	libmultipath library
Group:		System/Libraries
Conflicts:	multipath-tools < 0.4.9-1.20121222.1

%description -n	%{libmultipath}
This package ships the libmultipath library, part of multipath-tools.

%define	libmpathpersist %mklibname mpathpersist %{major}

%package -n	%{libmpathpersist}
Summary:	libmpathpersist library
Group:		System/Libraries
Conflicts:	multipath-tools < 0.4.9-1.20121222.1

%description -n	%{libmpathpersist}
This package ships the libmpathpersist library, part of multipath-tools.

%package -n	kpartx
Summary:	Partition device manager for device-mapper devices
Group:		System/Kernel and hardware
Conflicts:	multipath-tools < 0.4.8-16

%description -n	kpartx
kpartx manages partition creation and removal for device-mapper devices.

%package -n	uclibc-kpartx
Summary:	Partition device manager for device-mapper devices (uClibc build)
Group:		System/Kernel and hardware
Conflicts:	multipath-tools < 0.4.8-16
Requires:	kpartx = %{EVRD}

%description -n	uclibc-kpartx
kpartx manages partition creation and removal for device-mapper devices.

%prep
%setup -qn multipath-tools-130222
%apply_patches

cp %{SOURCE2} .

%if %{with uclibc}
cp -a kpartx kpartx-uclibc
%endif

%build
%if %{with uclibc}
%make -C kpartx-uclibc OPTFLAGS="%{uclibc_cflags}" CC="%{uclibc_cc}" LIB=%{_lib} WHOLE_PROGRAM=1
%endif
# FIXME:	WHOLE_PROGRAM=1
%make OPTFLAGS="%{optflags}" LIB=%{_lib} #WHOLE_PROGRAM=1 CC=%{__cc}

%install
%makeinstall_std bindir=/sbin syslibdir=/%{_lib} rcdir=%{_initrddir} unitdir=%{_unitdir} libdir=/%{_lib}/multipath libudevdir=%{_udevrulesdir}/.. #WHOLE_PROGRAM=1
%if %{with uclibc}
install -m755 kpartx-uclibc/kpartx -D %{buildroot}%{uclibc_root}/sbin/kpartx
%endif

install -m755 %{SOURCE1} -D %{buildroot}%{_initrddir}/multipathd

# tree fix up
install -d %{buildroot}%{_sysconfdir}/multipath

touch %{buildroot}%{_sysconfdir}/multipath.conf

# without any development headers installed, let's assume that the .so
# symlinks won't actually be of any use, thus remove them

rm %{buildroot}/%{_lib}/{libmultipath,libmpathpersist}.so

%files
%doc AUTHOR README* ChangeLog FAQ
%doc multipath.conf multipath.conf.annotated multipath.conf.defaults multipath.conf.synthetic
%{_initrddir}/multipathd
%dir %{_sysconfdir}/multipath
%ghost %config(noreplace) %{_sysconfdir}/multipath.conf
%{_unitdir}/multipathd.service
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

%if %{with uclibc}
%files -n uclibc-kpartx
%{uclibc_root}/sbin/kpartx
%endif

