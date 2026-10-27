#!/usr/bin/env python3
"""Upload the files the weekly Bayanath update changes to a web host over FTP with TLS (standard library only).

Only needed when the site is hosted on a plain web host (for example cPanel) instead of being published from this repository.
.github/workflows/update-bayanath.yml runs it after a change, and only when the repository secret CPANEL_FTP_HOST is set.

Settings come from the environment (repository secrets), never from files:
  FTP_HOST      host name of the FTP server
  FTP_USER      FTP account (create one in the host's control panel that can reach only the site folder)
  FTP_PASSWORD  its password (never printed)
  FTP_PORT      port of the FTP server (default 21)
  FTP_DIR       folder of the site on that server, for example /public_html (default: the account's home folder)
  FTP_TLS       'on' (default). 'off' is accepted only for a server on this machine, used by the self-tests.
  FTP_TLS_VERIFY 'on' (default): the server's certificate must be valid for FTP_HOST. Use the host name the certificate is
                issued for (your host shows it in the control panel); set 'off' only if the host has no matching certificate.

Each file is sent under a temporary name and renamed when complete, so a visitor never gets half a file.
Exit code 0 = everything uploaded; 1 = a setting or file is missing, or an upload failed (the message says which).
"""
import ftplib, os, ssl, sys
from pathlib import Path

PUB = Path(os.environ.get('SITE_DIR') or Path(__file__).resolve().parent.parent / 'public')
FILES = ('data/bayanath-videos.json', 'Bayanath.html', 'MuftiMaqsoodImran.html')   # the data first, then the pages that show it
LOOPBACK = ('127.0.0.1', 'localhost', '::1')


def connect(host, port, user, password, tls, verify=True):
    if tls:
        ftp = ftplib.FTP_TLS(context=ssl.create_default_context() if verify else ssl._create_unverified_context())
    else:
        ftp = ftplib.FTP()
    ftp.connect(host, port, timeout=60)
    ftp.login(user, password)
    if tls:
        ftp.prot_p()
    return ftp


def upload(ftp, base, files=FILES):
    if base:
        ftp.cwd(base)
    for rel in files:
        folder, _, name = rel.rpartition('/')
        if folder:
            ftp.cwd(folder)
        with open(PUB / rel, 'rb') as f:
            ftp.storbinary(f'STOR {name}.part', f)
        try:
            ftp.delete(name)
        except ftplib.error_perm:
            pass   # not there yet
        ftp.rename(f'{name}.part', name)
        if folder:
            ftp.cwd('/'.join('..' for _ in folder.split('/')))
        print(f'uploaded {rel}')


def main():
    host, user, password = (os.environ.get(k, '').strip() for k in ('FTP_HOST', 'FTP_USER', 'FTP_PASSWORD'))
    base = os.environ.get('FTP_DIR', '').strip()
    port = int(os.environ.get('FTP_PORT', '21') or 21)
    verify = os.environ.get('FTP_TLS_VERIFY', 'on').strip().lower() != 'off'
    tls = os.environ.get('FTP_TLS', 'on').strip().lower() != 'off'
    if not (host and user and password):
        print('ERROR: FTP_HOST, FTP_USER and FTP_PASSWORD must all be set.', file=sys.stderr)
        return 1
    if not tls and host not in LOOPBACK:
        print('ERROR: FTP without TLS is allowed only for a server on this machine.', file=sys.stderr)
        return 1
    missing = [rel for rel in FILES if not (PUB / rel).is_file()]
    if missing:
        print('ERROR: not found: ' + ', '.join(missing), file=sys.stderr)
        return 1
    try:
        ftp = connect(host, port, user, password, tls, verify)
        try:
            upload(ftp, base)
        finally:
            try:
                ftp.quit()
            except Exception:
                ftp.close()
    except (ftplib.Error, OSError) as e:
        print(f'ERROR: the upload failed ({type(e).__name__}: {e}). The site on the host was left as it was, or partly updated; run the workflow again.', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
