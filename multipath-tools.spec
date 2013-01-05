%bcond_without	uclibc

Name:		multipath-tools
URL:		http://christophe.varoqui.free.fr/multipath-tools/
License:	GPLv2
Group:		System/Kernel and hardware
Version:	0.4.9
%define	gitdate	20121222
Release:	1%{?gitdate:.%{gitdate}.1}
Summary:	Tools to manage multipathed devices with the device-mapper
Source0:	http://christophe.varoqui.free.fr/multipath-tools/%{name}-%{version}%{?gitdate:-%{gitdate}}.tar.xz
Source1:	multipathd.init
# kpartx: add -u flag, needed by dracut/systemd
#Patch0:		multipath-tools-implement-update-option-for-kpartx.patch
Patch1:		multipath-tools-0.4.9-20121222-whole-program.patch
Patch1001:	0001-RH-dont_start_with_no_config.patch
Patch1002:	0002-RH-multipath.rules.patch
Patch1003:	0003-RH-Make-build-system-RH-Fedora-friendly.patch
Patch1004:	0004-RH-multipathd-blacklist-all-by-default.patch
Patch1005:	0005-RH-add-mpathconf.patch
Patch1006:	0006-RH-add-find-multipaths.patch
Patch1007:	0007-RH-add-hp_tur-checker.patch
Patch1008:	0008-RH-RHEL5-style-partitions.patch
Patch1009:	0009-RH-dont-remove-map-on-enomem.patch
Patch1010:	0010-RH-deprecate-uid-gid-mode.patch
Patch1011:	0011-RH-use-sync-support.patch
Patch1012:	0012-RH-change-configs.patch
Patch1013:	0013-RH-kpartx-msg.patch
Patch1014:	0014-RH-dm_reassign.patch
Patch1015:	0015-RH-selector_change.patch
Patch1016:	0016-RH-retain_hwhandler.patch
# Patch1017:	0017-RH-netapp_config.patch
Patch1018:	0018-RH-remove-config-dups.patch
Patch1019:	0019-RH-detect-prio.patch
Patch1020:	0020-RH-netapp-config.patch
Patch1021:	0021-RH-fix-oom-adj.patch
Patch1022:	0022-RHBZ-864368-disable-libdm-failback.patch
Patch1023:	0023-RHBZ-866291-update-documentation.patch
Patch1024:	0024-RH-start-multipathd-service-before-lvm.patch
Patch1025:	0025-RH-fix-systemd-start-order.patch
Patch1026:	0026-RH-fix-mpathpersist-fns.patch
Patch1027:	0027-RH-default-partition-delimiters.patch
Patch1028:	0028-RH-storagetek-config.patch
Patch1029:	0029-RH-kpartx-retry.patch
Patch1030:	0030-RH-early-blacklist.patch
Patch1031:	0031-RHBZ-882060-fix-null-strncmp.patch
Patch1032:	0032-RH-make-path-fd-readonly.patch
Patch1033:	0033-RH-dont-disable-libdm-failback-for-sync-case.patch
Patch1034:	0034-RHBZ-887737-check-for-null-key.patch
Patch1035:	0035-RHBZ-883981-cleanup-rpmdiff-issues.patch

Requires:	dmsetup
Requires:	kpartx = %{version}
Conflicts:	kpartx < 0.4.8-16
BuildRequires:	pkgconfig(devmapper) 
BuildRequires:	sysfsutils-devel
BuildRequires:	readline-devel
BuildRequires:	pkgconfig(ncursesw)
BuildRequires:	libaio-devel
%if %{with uclibc}
BuildRequires:	uClibc-devel
%endif
Requires(preun):rpm-helper
Requires(post):	rpm-helper

%description
This package provides the tools to manage multipathed devices by
instructing the device-mapper multipath module what to do. The tools
are:

- multipath: scan the system for multipathed devices, assembles them
  and update the device-mapper's maps

- multipathd: wait for maps events, then execs multipath

- kpartx: maps linear devmaps upon device partitions, which makes
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
%setup -q -n %{name}-%{version}%{?gitdate:-%{gitdate}}
%apply_patches

%if %{with uclibc}
cp -a kpartx kpartx-uclibc
%endif

%build
%if %{with uclibc}
%make -C kpartx-uclibc OPTFLAGS="%{uclibc_cflags}" CC="%{uclibc_cc}" LIB=%{_lib} WHOLE_PROGRAM=1
%endif
# FIXME: WHOLE_PROGRAM=1
%make OPTFLAGS="%{optflags}" LIB=%{_lib} #WHOLE_PROGRAM=1

%install
%makeinstall_std bindir=/sbin syslibdir=/%{_lib} rcdir=%{_initrddir} unitdir=%{_unitdir} libdir=/%{_lib}/multipath #WHOLE_PROGRAM=1
%if %{with uclibc}
install -m755 kpartx-uclibc/kpartx -D %{buildroot}%{uclibc_root}/sbin/kpartx
%endif

install -m755 %{SOURCE1} -D %{buildroot}%{_initrddir}/multipathd

# tree fix up
install -d %{buildroot}%{_sysconfdir}/multipath

# without any development headers installed, let's assume that the .so
# symlinks won't actually be of any use, thus remove them

rm %{buildroot}/%{_lib}/{libmultipath,libmpathpersist}.so

%preun
%_preun_service multipathd

%post
%_post_service multipathd

%files
%doc AUTHOR README* ChangeLog FAQ multipath.conf.*
%config(noreplace) %{_initrddir}/multipathd
%dir %{_sysconfdir}/multipath
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

%changelog
* Sat Jan  5 2013 Per Øyvind Karlsen <peroyvind@mandriva.org> 0.4.9-1.20121222.1
- libify package
- update to latest code from git upstream
- sync with fedora patches

* Thu Dec 27 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 0.4.9-1
- compile kpartx & multipathd with -fwhole-program (P1)
- do uclibc build of kpartx
- enable parallel build
- compile with %%optflags
- drop 'COPYING', it's shipped with common-licenses
- cleanups
- new version

* Wed May 04 2011 Oden Eriksson <oeriksson@mandriva.com> 0.4.8-20mdv2011.0
+ Revision: 666499
- mass rebuild

* Fri Mar 04 2011 Andrey Borzenkov <arvidjaar@mandriva.org> 0.4.8-19
+ Revision: 641622
- P21: send multipath event for block device only (upstream)

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 0.4.8-18mdv2011.0
+ Revision: 606670
- rebuild

* Sat Feb 20 2010 Thomas Backlund <tmb@mandriva.org> 0.4.8-17mdv2010.1
+ Revision: 508762
- kpartx: deal with more than 256 minor numbers
- kpartx.rules: use current name of the device node

* Fri Feb 19 2010 Thomas Backlund <tmb@mandriva.org> 0.4.8-16mdv2010.1
+ Revision: 508452
- fix kpartx udev rule for dmraid
- move kpartx.rules and kpartx_id from multipath-tools to kpartx rpm

* Thu Aug 20 2009 Anssi Hannula <anssi@mandriva.org> 0.4.8-15mdv2010.0
+ Revision: 418368
- fix duplicated files between multipath-tools and kpartx
- require kpartx in multipath-tools

* Mon Aug 17 2009 Pascal Terjan <pterjan@mandriva.org> 0.4.8-14mdv2010.0
+ Revision: 417272
- Fix kpartx extended partition handling fix

* Tue Jul 28 2009 Pascal Terjan <pterjan@mandriva.org> 0.4.8-12mdv2010.0
+ Revision: 401386
- Avoid failure when pp_hp_sw gets installed before other executables
- Bump release due to misterious build failure
- Add missing conflict and drop useless provide

* Mon Jul 27 2009 Pascal Terjan <pterjan@mandriva.org> 0.4.8-9mdv2010.0
+ Revision: 400518
- Fix group of kpartx
- Split kpartx in a separate package, so that mkinitrd can require only it

* Mon Jul 20 2009 Eugeni Dodonov <eugeni@mandriva.com> 0.4.8-8mdv2010.0
+ Revision: 398031
- Updated init script to be LSB-compliant.

* Sun Jul 19 2009 Pascal Terjan <pterjan@mandriva.org> 0.4.8-7mdv2010.0
+ Revision: 397455
- Fix correctly scsi_id usage
- Add a few fedora patches (#52270, CVE-2009-0115)

* Tue Mar 17 2009 Guillaume Rousse <guillomovitch@mandriva.org> 0.4.8-5mdv2009.1
+ Revision: 356300
- rebuild for latest readline

* Mon Sep 29 2008 Thierry Vignaud <tv@mandriva.org> 0.4.8-4mdv2009.0
+ Revision: 289765
- include more doc (per #43925 request)
- make service executable (#43925)
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Mon Oct 22 2007 Thierry Vignaud <tv@mandriva.org> 0.4.8-1mdv2008.1
+ Revision: 101331
- adjust file list
- patch 0: fix build
- BuildRequires:  libaio-devel
- new release


* Sat Nov 25 2006 Thierry Vignaud <tvignaud@mandriva.com> 0.4.7-5mdv2007.0
+ Revision: 87151
- Import multipath-tools

* Sat Nov 25 2006 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.4.7-5mdv2007.1
- rebuild for libdevmapper

* Mon Jul 03 2006 Emmanuel Andry <eandry@mandriva.org> 0.4.7-4mdv2007.0
- rebuild for libdevmapper

* Wed May 03 2006 Thierry Vignaud <tvignaud@mandriva.com> 0.4.7-3mdk
- fix buildrequires (thus fixing x86_64 build with iurt)

* Wed Apr 19 2006 Thierry Vignaud <tvignaud@mandriva.com> 0.4.7-2mdk
- fix buildrequires

* Fri Mar 31 2006 Thierry Vignaud <tvignaud@mandriva.com> 0.4.7-1mdk
- new release

* Wed Dec 07 2005 Nicolas Lécureuil <neoclust@mandriva.org> 0.4.6-2mdk
- Fix BuildRequires

* Wed Nov 16 2005 Thierry Vignaud <tvignaud@mandriva.com> 0.4.6-1mdk
- new release
- drop patch 0 (now useless)

* Wed Jun 29 2005 Pascal Terjan <pterjan@mandriva.org> 0.4.2.7-3mdk
- BuildRequires libdevmapper-devel
- PreReq -> Requires(post)

* Sat Mar 05 2005 Luca Berra <bluca@vodka.it> 0.4.2.7-2mdk 
- rebuild for new libdevmapper
- use a mandrakelinux initscript
- specfile cleanup

* Thu Jan 20 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.4.2.7-1mdk
- new release
- automatically updatable
- patch 0: fix build

* Thu Dec 23 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.4.2.0-1mdk
- new release

* Thu Nov 25 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.3.8-1mdk
- new release

* Fri Nov 05 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.3.6-1mdk
- initial releaee

