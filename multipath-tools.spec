Name:         multipath-tools
URL:          http://christophe.varoqui.free.fr/multipath-tools/
License:      GPL
Group:        System/Kernel and hardware
Version:      0.4.7
Release:      %mkrel 5
Summary:      Tools to manage multipathed devices with the device-mapper
Source:       http://christophe.varoqui.free.fr/multipath-tools/%name-%version.tar.bz2
Source1:      multipathd.init.bz2
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Requires:     dmsetup
BuildRequires:	libdevmapper-devel
BuildRequires:  libsysfs-devel
BuildRequires:  readline-devel
BuildRequires:  ncurses-devel
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

%prep
%setup -q

%build
# parallel build support is broken:
make BUILD="glibc"

%install
rm -fR $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
rm -rf $RPM_BUILD_ROOT/etc/hotplug.d
mkdir -p $RPM_BUILD_ROOT/etc/init.d
bzip2 -dc %{SOURCE1} > $RPM_BUILD_ROOT/etc/init.d/multipathd

%clean
rm -rf $RPM_BUILD_ROOT

%preun
%_preun_service multipathd

%post
%_post_service multipathd


%files
%defattr(-,root,root,755)
%doc AUTHOR COPYING README ChangeLog 
%config(noreplace) /etc/init.d/multipathd
%config(noreplace) /etc/udev/rules.d/multipath.rules
/sbin/*
%_mandir/man8/*
/sbin/multipathd


