"""tools/upload_to_host.py against a small FTP server on this machine (no network, no extra packages)."""
import os, socket, socketserver, subprocess, sys, tempfile, threading, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_update_bayanath import child_env  # noqa: E402


class FtpHandler(socketserver.StreamRequestHandler):
    """Just enough FTP for the upload: USER PASS TYPE PASV CWD CDUP STOR DELE RNFR RNTO QUIT, on a folder tree held in memory."""

    def reply(self, text):
        self.wfile.write(text.encode() + b'\r\n')
        self.wfile.flush()

    def handle(self):
        srv, cwd, rnfr, data_sock = self.server, '/', None, None
        self.reply('220 ready')
        for raw in self.rfile:
            cmd, _, arg = raw.decode().rstrip('\r\n').partition(' ')
            cmd = cmd.upper()
            if cmd == 'USER':
                self.reply('331 password please')
            elif cmd == 'PASS':
                ok = arg == srv.password
                self.reply('230 in' if ok else '530 no')
                if not ok:
                    return
            elif cmd == 'TYPE':
                self.reply('200 ok')
            elif cmd == 'CWD':
                new = os.path.normpath(os.path.join(cwd, arg)).replace('\\', '/')
                if any(p.startswith(new.rstrip('/') + '/') or new == '/' for p in srv.files) or new in srv.dirs:
                    cwd = new
                    self.reply('250 ok')
                else:
                    self.reply('550 no such folder')
            elif cmd == 'CDUP':
                cwd = os.path.dirname(cwd) or '/'
                self.reply('250 ok')
            elif cmd == 'PASV':
                data_sock = socket.socket(); data_sock.bind(('127.0.0.1', 0)); data_sock.listen(1)
                port = data_sock.getsockname()[1]
                self.reply(f'227 Entering Passive Mode (127,0,0,1,{port >> 8},{port & 255})')
            elif cmd == 'STOR':
                self.reply('150 go')
                conn, _ = data_sock.accept()
                body = b''.join(iter(lambda: conn.recv(65536), b''))
                conn.close(); data_sock.close()
                srv.files[os.path.join(cwd, arg).replace('\\', '/')] = body
                self.reply('226 done')
            elif cmd == 'DELE':
                path = os.path.join(cwd, arg).replace('\\', '/')
                if path in srv.files:
                    del srv.files[path]; self.reply('250 deleted')
                else:
                    self.reply('550 not found')
            elif cmd == 'RNFR':
                rnfr = os.path.join(cwd, arg).replace('\\', '/')
                self.reply('350 ok' if rnfr in srv.files else '550 not found')
            elif cmd == 'RNTO':
                srv.files[os.path.join(cwd, arg).replace('\\', '/')] = srv.files.pop(rnfr)
                self.reply('250 renamed')
            elif cmd == 'QUIT':
                self.reply('221 bye'); return
            else:
                self.reply('502 not implemented')


class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


class Upload(unittest.TestCase):
    def setUp(self):
        self.srv = Server(('127.0.0.1', 0), FtpHandler)
        self.srv.password = 'secret-pass'
        self.srv.files = {'/site/Bayanath.html': b'old page', '/site/data/keep.txt': b'k'}
        self.srv.dirs = {'/', '/site', '/site/data'}
        threading.Thread(target=self.srv.serve_forever, daemon=True).start()
        self.tmp = tempfile.TemporaryDirectory()
        site = Path(self.tmp.name)
        (site / 'data').mkdir()
        (site / 'data' / 'bayanath-videos.json').write_text('{"videos": []}', encoding='utf-8')
        (site / 'Bayanath.html').write_text('new page', encoding='utf-8')
        (site / 'MuftiMaqsoodImran.html').write_text('new profile', encoding='utf-8')
        self.site = site

    def tearDown(self):
        self.srv.shutdown(); self.srv.server_close(); self.tmp.cleanup()

    def run_script(self, **env):
        e = child_env()
        e.update({'SITE_DIR': str(self.site), 'FTP_HOST': '127.0.0.1', 'FTP_USER': 'u', 'FTP_PASSWORD': self.srv.password,
                  'FTP_DIR': '/site', 'FTP_TLS': 'off', 'FTP_PORT': str(self.srv.server_address[1])})
        e.update(env)
        return subprocess.run([sys.executable, '-I', str(ROOT / 'tools' / 'upload_to_host.py')], capture_output=True, text=True, timeout=60, env=e)

    def test_uploads_the_three_files_replacing_old_ones_and_leaving_others(self):
        p = self.run_script()
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        self.assertEqual(self.srv.files['/site/Bayanath.html'], b'new page')
        self.assertEqual(self.srv.files['/site/MuftiMaqsoodImran.html'], b'new profile')
        self.assertEqual(self.srv.files['/site/data/bayanath-videos.json'], b'{"videos": []}')
        self.assertEqual(self.srv.files['/site/data/keep.txt'], b'k')
        self.assertFalse([k for k in self.srv.files if k.endswith('.part')], 'a temporary file was left behind')

    def test_a_wrong_password_changes_nothing_and_is_not_printed(self):
        p = self.run_script(FTP_PASSWORD='wrong-password')
        self.assertEqual(p.returncode, 1)
        self.assertNotIn('wrong-password', p.stdout + p.stderr)
        self.assertEqual(self.srv.files['/site/Bayanath.html'], b'old page')

    def test_refuses_to_run_without_settings_or_with_plain_ftp_to_a_remote_host(self):
        self.assertEqual(self.run_script(FTP_HOST='').returncode, 1)
        p = self.run_script(FTP_HOST='ftp.example.org', FTP_TLS='off')
        self.assertEqual(p.returncode, 1)
        self.assertIn('without TLS', p.stderr)

    def test_a_missing_local_file_stops_before_connecting(self):
        (self.site / 'Bayanath.html').unlink()
        p = self.run_script()
        self.assertEqual(p.returncode, 1)
        self.assertIn('Bayanath.html', p.stderr)


if __name__ == '__main__':
    unittest.main()
