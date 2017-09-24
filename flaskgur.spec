Name:    flaskgur
Version: 1.0
Release: 8%{?dist}
Summary: Image hosting.

License: GPLv2
Source0: flaskgur
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires: systemd
Requires: nginx
Requires: python-flask
Requires: python-pillow
Requires: uwsgi
Requires: uwsgi-plugin-python
Requires: postgresql
Requires: python-psycopg2

%description
Simple image hosting site written with Flask and Python.

%clean
rm -rf %{buildroot}

%prep
%setup -q

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/etc/nginx/conf.d/
install -m 644 conf/nginx/flaskgur.conf %{buildroot}/etc/nginx/conf.d/
mkdir -p %{buildroot}/etc/systemd/system/
install -m 644 conf/systemd/flaskgur.service %{buildroot}/etc/systemd/system/
mkdir -p %{buildroot}/usr/bin/
install -m 755 fgdb %{buildroot}/usr/bin/
mkdir -p %{buildroot}/var/www/flaskgur
install -m 644 *.py %{buildroot}/var/www/flaskgur/
install -m 644 *.ini %{buildroot}/var/www/flaskgur/
mkdir -p %{buildroot}/var/www/flaskgur/pics/
install -m 644 pics/* %{buildroot}/var/www/flaskgur/pics/
mkdir -p %{buildroot}/var/www/flaskgur/static/
install -m 644 static/* %{buildroot}/var/www/flaskgur/static/
mkdir -p %{buildroot}/var/www/flaskgur/templates/
install -m 644 templates/* %{buildroot}/var/www/flaskgur/templates/

%files
%defattr(644,root,root)
%config(noreplace) /etc/nginx/conf.d/flaskgur.conf
/etc/systemd/system/flaskgur.service
%attr(755,root,root) /usr/bin/fgdb
%attr(755,root,root) %dir /var/www/flaskgur/
/var/www/flaskgur/*
%attr(755,root,root) %dir /var/www/flaskgur/pics/
/var/www/flaskgur/pics/blank
%attr(755,root,root) %dir /var/www/flaskgur/static/
/var/www/flaskgur/static/*
%attr(755,root,root) %dir /var/www/flaskgur/templates/
/var/www/flaskgur/templates/*

%changelog
* Fri Sep 22 2017 Jan Dobes <git@owny.cz> 1.0-8
- initial release
- added postgresql support
- store name and extension separately
