%if 0%{?fedora} >= 19 || 0%{?rhel} >= 7
%bcond_without systemd
%else
%bcond_with systemd
%endif

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
Source1:        nova-agent.service
Source2:        nova-agent.init
ExclusiveArch:  x86_64

%if %{with systemd}
BuildRequires:  systemd
%endif

%if %{with systemd}
Requires(post):    systemd
Requires(preun):   systemd
Requires(postun):  systemd
%else
Requires(post):    chkconfig
Requires(preun):   chkconfig
Requires(preun):   initscripts
Requires(postun):  initscripts
%endif

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
# service
%if %{with systemd}
install -Dpm644 %{SOURCE1} %{buildroot}%{_unitdir}/nova-agent.service
%else
install -Dpm755 %{SOURCE2} %{buildroot}%{_initrddir}/nova-agent
%endif


%post
%if %{with systemd}
%systemd_post nova-agent.service
%else
chkconfig --add nova-agent
%endif


%preun
%if %{with systemd}
%systemd_preun nova-agent.service
%else
if [ $1 -eq 0 ] ; then
    service nova-agent stop &> /dev/null
    chkconfig --del nova-agent &> /dev/null
fi
%endif


%postun
%if %{with systemd}
%systemd_postun_with_restart nova-agent.service
%else
if [ $1 -ge 1 ] ; then
    service nova-agent condrestart &> /dev/null || :
fi
%endif


%files
%{_datadir}/nova-agent
%{_sbindir}/nova-agent
%if %{with systemd}
%{_unitdir}/nova-agent.service
%else
%{_initrddir}/nova-agent
%endif


%changelog
* Fri Mar 04 2016 Carl George <carl.george@rackspace.com> - 1.39.1-2
- Add ExclusiveArch to match the pre-compiled binary tarball
- License is ASL 2.0, not GPL
- Install files directly
- Don't run installer.sh in %%post
- Don't put files in /usr/share/nova-agent-install
- Own files in /usr/share/nova-agent
- Add dual systemd/sysvinit compatibility
- Add standard scriptlets
- Overhaul sysvinit script
- Clean up systemd service file

* Wed Oct 15 2014 Greg Ball <greg.ball@rackspace.com> - 1.39.1-1
- 1.39.1 release
