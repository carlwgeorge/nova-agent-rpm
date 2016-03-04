Name:           nova-agent
Version:        1.39.1
Release:        2%{?dist}
Summary:        Unix Guest Agent for Openstack
%if 0%{?rhel} && 0%{?rhel} < 7
Group:          System Environment/Base
%endif
Vendor:         OpenStack
License:        ASL 2.0
URL:            https://github.com/rackerlabs/openstack-guest-agents-unix
Source0:        nova-agent-Linux-x86_64-%{version}.tar.gz
ExclusiveArch:  x86_64

# these are important
# https://fedoraproject.org/wiki/Packaging:FrequentlyMadeMistakes?rd=Packaging/FrequentlyMadeMistakes
%global _enable_debug_package 0
%global debug_package %{nil}
%global __os_install_post /usr/lib/rpm/brp-compress %{nil}


%description
This guest agent provides functionality such as configuring the networking for a guest.


%prep
tar -xzvf nova-agent-Linux-x86_64-1.39.1.tar.gz -C $RPM_BUILD_DIR


%install
mkdir -p $RPM_BUILD_ROOT/usr/share/nova-agent-install
rm -f $RPM_BUILD_DIR/usr/share/nova-agent/1.39.1/etc/gentoo/nova-agent
mv $RPM_BUILD_DIR/* $RPM_BUILD_ROOT/usr/share/nova-agent-install


%files
/usr/share/nova-agent-install/*


%post -p /bin/bash
cd /usr/share/nova-agent-install
./installer.sh


%preun
if [ $1 -eq 0 ] ; then
    /sbin/service nova-agent stop >/dev/null 2>&1
    /sbin/chkconfig --del nova-agent
    rm -rf /usr/share/nova-agent
    rm -rf /usr/share/nova-agent-install
    rm -f /etc/init.d/nova-agent
fi


%changelog
* Fri Mar 04 2016 Carl George <carl.george@rackspace.com> - 1.39.1-2
- Add ExclusiveArch to match the pre-compiled binary tarball
- License is ASL 2.0, not GPL

* Wed Oct 15 2014 Greg Ball <greg.ball@rackspace.com> - 1.39.1-1
- 1.39.1 release
