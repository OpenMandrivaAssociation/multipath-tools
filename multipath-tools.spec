%bcond_without	uclibc
%define	gitdate	20121222

Summary:	Tools to manage multipathed devices with the device-mapper
Name:		multipath-tools
Version:	0.4.9
Release:	2%{?gitdate:.%{gitdate}.1}
License:	GPLv2
Group:		System/Kernel and hardware
Url:		http://christophe.varoqui.free.fr/multipath-tools/
Source0:	http://christophe.varoqui.free.fr/multipath-tools/%{name}-%{version}%{?gitdate:-%{gitdate}}.tar.xz
Source1:	multipathd.init
Source2:	multipath.conf
# Fedora patches
Patch1:		0001-RH-dont_start_with_no_config.patch
Patch2:		0002-RH-multipath.rules.patch
Patch3:		0003-RH-Make-build-system-RH-Fedora-friendly.patch
Patch4:		0004-RH-multipathd-blacklist-all-by-default.patch
Patch5:		0005-RH-add-mpathconf.patch
Patch6:		0006-RH-add-find-multipaths.patch
Patch7:		0007-RH-add-hp_tur-checker.patch
Patch8:		0008-RH-RHEL5-style-partitions.patch
Patch9:		0009-RH-dont-remove-map-on-enomem.patch
Patch10:	0010-RH-deprecate-uid-gid-mode.patch
Patch11:	0011-RH-use-sync-support.patch
Patch12:	0012-RH-change-configs.patch
Patch13:	0013-RH-kpartx-msg.patch
Patch14:	0014-RH-dm_reassign.patch
Patch15:	0015-RH-selector_change.patch
Patch16:	0016-RH-retain_hwhandler.patch
# Patch17:	0017-RH-netapp_config.patch
Patch18:	0018-RH-remove-config-dups.patch
Patch19:	0019-RH-detect-prio.patch
Patch20:	0020-RH-netapp-config.patch
Patch21:	0021-RH-fix-oom-adj.patch
Patch22:	0022-RHBZ-864368-disable-libdm-failback.patch
Patch23:	0023-RHBZ-866291-update-documentation.patch
Patch24:	0024-RH-start-multipathd-service-before-lvm.patch
Patch25:	0025-RH-fix-systemd-start-order.patch
Patch26:	0026-RH-fix-mpathpersist-fns.patch
Patch27:	0027-RH-default-partition-delimiters.patch
Patch28:	0028-RH-storagetek-config.patch
Patch29:	0029-RH-kpartx-retry.patch
Patch30:	0030-RH-early-blacklist.patch
Patch31:	0031-RHBZ-882060-fix-null-strncmp.patch
Patch32:	0032-RH-make-path-fd-readonly.patch
Patch33:	0033-RH-dont-disable-libdm-failback-for-sync-case.patch
Patch34:	0034-RHBZ-887737-check-for-null-key.patch
Patch35:	0035-RHBZ-883981-cleanup-rpmdiff-issues.patch
# our patches
Patch1000:	multipath-tools-0.4.9-20121222-whole-program.patch
# fix path set by redhat path
Patch1001:	multipath-tools-0.4.9-20121222-fix-doc-path-to-config.patch

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
%setup -qn %{name}-%{version}%{?gitdate:-%{gitdate}}
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
%make OPTFLAGS="%{optflags}" LIB=%{_lib} #WHOLE_PROGRAM=1

%install
%makeinstall_std bindir=/sbin syslibdir=/%{_lib} rcdir=%{_initrddir} unitdir=%{_unitdir} libdir=/%{_lib}/multipath #WHOLE_PROGRAM=1
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

%post
%systemd_post multipathd.service

%preun
%systemd_preun multipathd.service

%postun
%systemd_postun_with_restart multipathd.service

%files
%doc AUTHOR README* ChangeLog FAQ
%doc multipath.conf multipath.conf.annotated multipath.conf.defaults multipath.conf.synthetic
%{_initrddir}/multipathd
%dir %{_sysconfdir}/multipath
%ghost %config(noreplace) %{_sysconfdir}/multipath.conf
%{_unitdir}/multipathd.service
%config /lib/udev/rules.d/62-multipath.rules
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

