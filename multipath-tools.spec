Name:         multipath-tools
URL:          http://christophe.varoqui.free.fr/multipath-tools/
License:      GPL
Group:        System/Kernel and hardware
Version:      0.4.8
Release:      %mkrel 10
Summary:      Tools to manage multipathed devices with the device-mapper
Source:       http://christophe.varoqui.free.fr/multipath-tools/%name-%version.tar.bz2
Source1:      multipathd.init.bz2
Patch0:	      multipath-tools-fix-build.patch
# Fedora patches
Patch1:       uevent_fix.patch
# Fix scsi_id usage, actually not the Fedora patch
Patch8:       scsi_id_change.patch
Patch10:      fix_devt.patch
Patch12:      binding_error.patch
# Fix kpartx extended partition handling
Patch13:      fix_kpartx.patch
# Fix insecure permissions on multipathd.sock (CVE-2009-0115)
Patch14:      fix_umask.patch
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Requires:     dmsetup
BuildRequires:	libdevmapper-devel
BuildRequires:  libsysfs-devel
BuildRequires:  readline-devel
BuildRequires:  ncurses-devel
BuildRequires:  libaio-devel
Requires(preun):rpm-helper
Requires(post):	rpm-helper


%description
This package provides the tools to manage multipathed devices by
instructing the device-mapper multipath module what to do. The tools
are:

- multipath: scan the system for multipathed devices, assembles them
  and update the device-mapper's maps

- multipathd: wait for maps events, then execs multipath

- devmap-name: provides a meaningful device name to udev for devmaps

- kpartx: maps linear devmaps upon device partitions, which makes
  multipath maps partionable

%package -n kpartx
Summary: Partition device manager for device-mapper devices
Group: System/Kernel and hardware
Conflicts: multipath-tools < 0.4.8-9

%description -n kpartx
kpartx manages partition creation and removal for device-mapper devices.

%prep
%setup -q
%patch0 -p0

%patch1 -p1 -b .uevent_fix
%patch8 -p1 -b .scsi_id_change
%patch10 -p1 -b .fix_devt
%patch12 -p1 -b .binding_error
%patch13 -p1 -b .ext_part
%patch14 -p1 -b .umask

%build
# parallel build support is broken:
make BUILD="glibc"

%install
rm -fR $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
rm -rf $RPM_BUILD_ROOT/etc/hotplug.d
mkdir -p $RPM_BUILD_ROOT/etc/init.d
bzip2 -dc %{SOURCE1} > $RPM_BUILD_ROOT/etc/init.d/multipathd
chmod 755 $RPM_BUILD_ROOT/etc/init.d/multipathd

%clean
rm -rf $RPM_BUILD_ROOT

%preun
%_preun_service multipathd

%post
%_post_service multipathd


%files
%defattr(-,root,root,755)
%doc AUTHOR COPYING README* ChangeLog FAQ multipath.conf.*
%config(noreplace) /etc/init.d/multipathd
%config(noreplace) /etc/udev/rules.d/multipath.rules
/etc/udev/rules.d/kpartx.rules
/lib/udev/kpartx_id
/sbin/*
%_mandir/man?/*

%files -n kpartx
%defattr(-,root,root,-)
/sbin/kpartx
%{_mandir}/man8/kpartx.8*

