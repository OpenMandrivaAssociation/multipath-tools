Name:		multipath-tools
URL:		http://christophe.varoqui.free.fr/multipath-tools/
License:	GPLv2
Group:		System/Kernel and hardware
Version:	0.4.9
Release:	1
Summary:	Tools to manage multipathed devices with the device-mapper
Source0:	http://christophe.varoqui.free.fr/multipath-tools/%{name}-%{version}.tar.bz2
Source1:	multipathd.init
# kpartx: add -u flag, needed by dracut/systemd
Patch0:		multipath-tools-implement-update-option-for-kpartx.patch

Requires:	dmsetup
Requires:	kpartx = %{version}
Conflicts:	kpartx < 0.4.8-16
BuildRequires:	pkgconfig(devmapper) 
BuildRequires:	sysfsutils-devel
BuildRequires:	readline-devel
BuildRequires:	pkgconfig(ncursesw)
BuildRequires:	libaio-devel
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

%package -n	kpartx
Summary:	Partition device manager for device-mapper devices
Group:		System/Kernel and hardware
Conflicts:	multipath-tools < 0.4.8-16

%description -n	kpartx
kpartx manages partition creation and removal for device-mapper devices.

%prep
%setup -q
%patch0 -p1 -b .kpartx-update~

%build
%make BUILD="glibc" OPTFLAGS="%{optflags}"

%install
%makeinstall_std

install -m755 %{SOURCE1} -D %{buildroot}%{_initrddir}/multipathd

%preun
%_preun_service multipathd

%post
%_post_service multipathd

%files
%doc AUTHOR README* ChangeLog FAQ multipath.conf.*
%config(noreplace) %{_initrddir}/multipathd
%config(noreplace) %{_sysconfdir}/udev/rules.d/multipath.rules
/sbin/multipath
/sbin/multipathd
%{_mandir}/man?/multipath*
%dir /%{_lib}/multipath/
/%{_lib}/multipath/*
/%{_lib}/libmultipath*

%files -n kpartx
/sbin/kpartx
%{_sysconfdir}/udev/rules.d/kpartx.rules
/lib/udev/kpartx_id
%{_mandir}/man8/kpartx.8*

%changelog
* Thu Dec 27 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 0.4.9-1
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

