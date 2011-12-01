Name:         multipath-tools
URL:          http://christophe.varoqui.free.fr/multipath-tools/
License:      GPL
Group:        System/Kernel and hardware
Version:      0.4.8
Release:      %mkrel 20
Summary:      Tools to manage multipathed devices with the device-mapper
Source:       http://christophe.varoqui.free.fr/multipath-tools/%name-%version.tar.bz2
Source1:      multipathd.init.bz2
Patch0:	      multipath-tools-fix-build.patch
Patch20:      multipath-tools-0.4.8-fix_make_install.patch
# (bor) send udev event for block devices only (upstream)
Patch21:      multipath-tools-0.4.8-send-udev-event-for-block-only.patch

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
# fix kpartx udev rule for dmraid
Patch15:      fix-kpartx-udev-rules-for-dmraid.patch
# kpartx: use current name of the device node
Patch16:      multipath-tools-Use-current-name-of-the-device-node.patch
# kpartx: deal with more than 256 minor numbers
Patch17:      kpartx-make-kpartx-deal-with-more-than-256-minor-numbers.patch

BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Requires:     dmsetup
Requires:     kpartx = %{version}
Conflicts:    kpartx < 0.4.8-16
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
Conflicts: multipath-tools < 0.4.8-16

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
%patch15 -p1 -b .kpartx_udev
%patch16 -p1 -b .node_name
%patch17 -p1 -b .minor_numbers
%patch20 -p1 -b .install
%patch21 -p1 -b .udev_subsys_block

%build
# parallel build support is broken:
make BUILD="glibc"

%install
rm -fR %{buildroot}
make DESTDIR=%{buildroot} install
rm -rf %{buildroot}/etc/hotplug.d
mkdir -p %{buildroot}/etc/init.d
bzip2 -dc %{SOURCE1} > %{buildroot}/etc/init.d/multipathd
chmod 755 %{buildroot}/etc/init.d/multipathd

%clean
rm -rf %{buildroot}

%preun
%_preun_service multipathd

%post
%_post_service multipathd


%files
%defattr(-,root,root,755)
%doc AUTHOR COPYING README* ChangeLog FAQ multipath.conf.*
%config(noreplace) /etc/init.d/multipathd
%config(noreplace) /etc/udev/rules.d/multipath.rules
/sbin/devmap_name
/sbin/mpath_prio_*
/sbin/multipath
/sbin/multipathd
%_mandir/man?/devmap_name*
%_mandir/man?/mpath_prio_*
%_mandir/man?/multipath*

%files -n kpartx
%defattr(-,root,root,-)
/sbin/kpartx
/etc/udev/rules.d/kpartx.rules
/lib/udev/kpartx_id
%{_mandir}/man8/kpartx.8*

