Name:    flaskgur
Version: 1.0
Release: 1%{?dist}
Summary: Say hello, Texas style

License: GPLv2
Source0: flaskgur

Requires: systemd
Requires: nginx
Requires: python-flask
Requires: python-pillow
Requires: uwsgi
Requires: uwsgi-plugin-python
Requires: postgresql

%description
Simple image hosting site written with Flask and Python.

%clean
rm -rf %{buildroot}

%prep
%setup -q

%install
rm -rf %{buildroot}
install -m 644 conf/nginx/flaskgur.conf %{buildroot}/etc/nginx/conf.d/
install -m 644 conf/systemd/flaskgur.service %{buildroot}/etc/systemd/system/
mkdir -p %{buildroot}/var/www/flaskgur
install -m 644 *.py %{buildroot}/var/www/flaskgur/
install -m 644 *.ini %{buildroot}/var/www/flaskgur/
install -m 644 pics %{buildroot}/var/www/flaskgur/
install -m 644 static %{buildroot}/var/www/flaskgur/
install -m 644 templates %{buildroot}/var/www/flaskgur/

%files
%config(noreplace) /etc/nginx/conf.d/flaskgur.conf
config /etc/systemd/system/flaskgur.service
%dir /var/www/flaskgur/
/var/www/flaskgur/*
%dir /var/www/flaskgur/pics/
/var/www/flaskgur/pics/blank
%dir /var/www/flaskgur/static/
/var/www/flaskgur/static/*
%dir /var/www/flaskgur/templates/
/var/www/flaskgur/templates/*

%changelog
* Fri Sep 22 2017 Jan Dobes <git@owny.cz> 1.0-1
- initial release

