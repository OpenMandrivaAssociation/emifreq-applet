%define name emifreq-applet
%define version 0.18

Summary : EmiFreq applet is just a little applet to show and control the CPU
Name: %name
Version: %{version}
Release: %mkrel 2
Source:  %{name}-%{version}.tar.bz2
Source1: emifreq-applet-initscript.bz2
License: GPL
Group: Monitoring
Url: http://zzrough.free.fr


BuildRequires: perl-XML-Parser
BuildRequires: pkgconfig
BuildRequires: intltool
BuildRequires: gnome-panel-devel
BuildRequires: libgnomeui2-devel
BuildRequires: libGConf2-devel

#Requires: libpanel-applet
#Requires: libGConf2
Requires: gnome-panel

Requires(post,preun): rpm-helper, chkconfig

%description
EmiFreq applet is a little GNOME applet that shows/control
the CPU frequency and temperature thanks to the cpufreq sysfs 
kernel interface. The emifreqd daemon is also included to enable 
the applet to change the cpu speed through the CPUFreq extension 
of the sysfs.

%prep
%setup -q

%build
%configure2_5x
%make

%install
rm -rf %buildroot
GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
%makeinstall_std

%find_lang %name --with-gnome

mkdir -p %{buildroot}%{_initrddir}
bzcat %{SOURCE1} > %{buildroot}%{_initrddir}/emifreqd
chmod 0755 %{buildroot}%{_initrddir}/emifreqd

perl -pi -e "s|/etc/rc.d/init.d|%{_initrddir}|" $RPM_BUILD_ROOT%{_initrddir}/*

%clean
rm -rf %buildroot

%post
%_post_service emifreqd

# handle init sequence change
if [ -f /etc/rc5.d/S85emifreqd ]; then
        /sbin/chkconfig --add emifreqd
fi

%preun
%_preun_service emifreqd

%files -f %name.lang
%defattr(-,root,root)
%doc AUTHORS COPYING NEWS README TODO
%config(noreplace) %{_sysconfdir}/gconf/schemas/%{name}.schemas
%{_sbindir}/emifreqd
%{_libdir}/emifreq-applet
%{_libdir}/bonobo/servers/*
%{_datadir}/pixmaps/*
%dir %{_datadir}/emifreq-applet/
%{_datadir}/emifreq-applet/*
%{_datadir}/gnome-2.0/ui/GNOME_EmiFreqApplet.xml
%config(noreplace) %{_initrddir}/emifreqd

