# build number
%define h_build_num  %(test -n "$build_number" && echo "$build_number" || echo 1)

# mero git revision
#   assume that Mero package release has format 'buildnum_gitid_kernelver'
%define h_mero_gitrev %(rpm -q --queryformat '%{RELEASE}' mero | cut -f2 -d_)

# mero version
%define h_mero_version %(rpm -q --queryformat '%{VERSION}-%{RELEASE}' mero)

# parallel build jobs
%define h_build_jobs_opt  %(test -n "$build_jobs" && echo "-j$build_jobs" || echo '')

Summary: HARE (HAlon REplacement)
Name: hare
Version: %{h_version}
Release: %{h_build_num}_%{h_gitrev}_m0%{h_mero_gitrev}%{?dist}
License: All rights reserved
Group: System Environment/Daemons
Source: %{name}-%{h_version}.tar.gz

BuildRequires: binutils-devel
BuildRequires: git
BuildRequires: mero
BuildRequires: mero-devel
BuildRequires: python36
BuildRequires: python36-devel
BuildRequires: python36-pip
BuildRequires: python36-setuptools

Requires: mero = %{h_mero_version}
Requires: python36

%description
Cluster monitoring and recovery for high-availability.

%prep
%setup -qn %{name}

%build
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_exec_prefix}/lib/systemd/system/*
%{_sharedstatedir}/hare/
%{_localstatedir}/mero/hax/
/opt/seagate/hare/*

%post
systemctl daemon-reload

%postun
systemctl daemon-reload

# FIXME: don't fail if /usr/lib/rpm/brp-python-bytecompile reports synatx erros,
# the script doesn't work with python3, there should a better way to disable it
# completely
# https://github.com/scylladb/scylla/issues/2235 suggests that a proper fix is
# to rename all *.py files as *.py3
%define _python_bytecompile_errors_terminate_build 0