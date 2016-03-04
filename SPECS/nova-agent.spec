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
%setup -q -c


%install
pushd ./%{_datadir}/nova-agent/%{version}
# bundled libraries and python bytecode
mkdir -p %{buildroot}%{_datadir}/nova-agent/%{version}
cp -r --preserve=timestamps lib %{buildroot}%{_datadir}/nova-agent/%{version}
cp -r --preserve=timestamps commands %{buildroot}%{_datadir}/nova-agent/%{version}
cp -r --preserve=timestamps plugins %{buildroot}%{_datadir}/nova-agent/%{version}
# main binary
install -Dpm755 sbin/nova-agent %{buildroot}%{_sbindir}/nova-agent
# agent config
install -Dpm644 nova-agent.py %{buildroot}%{_datadir}/nova-agent/%{version}/nova-agent.py
popd


%preun
if [ $1 -eq 0 ] ; then
    /sbin/service nova-agent stop >/dev/null 2>&1
    /sbin/chkconfig --del nova-agent
    rm -f /etc/init.d/nova-agent
fi


%files
%{_datadir}/nova-agent
%{_sbindir}/nova-agent


%changelog
* Fri Mar 04 2016 Carl George <carl.george@rackspace.com> - 1.39.1-2
- Add ExclusiveArch to match the pre-compiled binary tarball
- License is ASL 2.0, not GPL
- Install files directly
- Don't run installer.sh in %%post
- Don't put files in /usr/share/nova-agent-install
- Own files in /usr/share/nova-agent

* Wed Oct 15 2014 Greg Ball <greg.ball@rackspace.com> - 1.39.1-1
- 1.39.1 release
