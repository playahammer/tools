#coding:utf-8

import struct, time

header_structure = 'BBBBIBB'
ids = (0x1f, 0x8b)
compress_methods = {8: 'defalte'}
FLAGS = {1: 'FTEXT', 2: 'FHCRC', 4: 'FEXTRA', 8: 'FNAME', 16: 'FCOMMENT'}
XFLS = {2: 'compressor used maximum compression, slowest algorithm',
        4: 'compressor used fastest algorithm'}
OSs = ['FAT filesystem (MS-DOS, OS/2, NT/Win32)', 'Amiga', 'VMS (or OpenVMS)',
       'Unix', 'VM/CMS', 'Atari TOS', 'HPFS filesystem (OS/2, NT)', 'Macintosh',
       'Z-System', 'CP/M', 'TOPS-20', 'NTFS filesystem (NT)', 'QDOS',
       'Acorn RISCOS']
FTEXT = 1
FHCRC = 2
FEXTRA = 4
FNAME = 8
FCOMMENT = 16


def print_hex(value):
    hex_alpha = '0123456789ABCDEF'
    v = ''
    if not value:
        return '0x00'
    while value:
        value, p = divmod(value, 16)
        v += hex_alpha[p]

    return '0x' + v[::-1] if len(v) % 2 == 0 else '0x0' + v[::-1]

class GzipTest:

    def __init__(self, file_path):
        self._file_path = file_path
        self._id1 = None
        self._id2 = None
        self._cm = 0
        self._flag = 0
        self._mtime = 0
        self._xfl = 0
        self._os = None
        self._read_handler = None

    def _read(self):
        with open(self._file_path, 'rb') as f:
            n = 10
            while True:
                b = f.read(n)
                if not b:
                    break
                n = yield b

    def _check_header(self, value):
        try:
            self._id1, \
            self._id2, \
            self._cm, \
            self._flag, \
            self._mtime, \
            self._xfl, \
            self._os = struct.unpack(header_structure, value)
        except:
            print('Invalid gzip header')
            exit(-1)

        if (self._id1, self._id2) \
            != ids:
            print('Invalid gzip header')
            exit(-1)

        print('IDentification 1: %s' % print_hex(self._id1))
        print('IDentification 2: %s' % print_hex(self._id2))

        try:
            print('Compress Method: %s' % compress_methods[self._cm])
        except:
            print('Invalid gzip header')
            exit(-1)

        flags = []

        for k, v in FLAGS.items():
            if k & self._flag:
                flags.append(v)

        print('Flags: %s' % ','.join(flags))

        print('Modification TIME: %s' %
              time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self._mtime)))
        print('Extra flag: %d' % self._xfl)

        try:
            print('OS: %s' % OSs[self._os])
        except:
            print('OS: unknown')

        print()

        if self._flag & FEXTRA:
            self._read_fextra()

        if self._flag & FNAME:
            self._read_fname()

        if self._flag & FCOMMENT:
            self._read_fcomment()

        print('Computing crc32...')
        print(hex(self._compute_crc32()))

        if self._flag & FHCRC:
            self._read_fhcrc()

    def _read_fextra(self):
        xlen = struct.unpack('H', self._read_handler.send(2))

        extra_field = self._read_handler.send(xlen)
        s1, s2, _len = struct.unpack('BBH', extra_field[:4])
        subfield_data = extra_field[4 : 4 + _len]

    def _read_fname(self):
        name = b''
        b = self._read_handler.send(1)
        while b != b'\x00':
            name += b
            b = self._read_handler.send(1)

        print('File Name: %s' % name.decode('latin1'))

    def _read_fcomment(self):
        fc = b''
        b = self._read_handler.send(1)
        while b != b'\x00':
            fc += b
            b = self._read_handler.send(1)

        print('File Comment %s' % fc.decode('latin1'))

    def _read_fhcrc(self):
        pass

    def _compute_crc32(self):
        crc_table = []

        def make_crc_table():
            for n in range(256):
                for k  in range(8):
                    if n & 1:
                        n = 0xedb88340 ^ (n >> 1)
                    else:
                        n = n >> 1
                crc_table.append(n)

        make_crc_table()
        c = 0 ^ 0xffffffff

        while True:
            try:
                b = self._read_handler.send(1)
                c = crc_table[(c ^ struct.unpack('B', b)[0]) & 0xff] ^ (c >> 8)
            except:
                break

        return c ^ 0xffffffff

    def execute(self):
        self._read_handler = self._read()
        self._check_header(self._read_handler.send(None))

if __name__ == '__main__':
    GzipTest('/Users/Dream/downloads/ssl-1.16.tar.gz').execute()


