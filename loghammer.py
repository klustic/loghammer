import argparse
import socket
import struct
import time


class UtmpRecord(object):
    RECORD_STRUCT = b'hI32s4s32s256shhiii4s4s4s4s20s'
    RECORD_STRUCT_SIZE = struct.calcsize(RECORD_STRUCT)

    UTMP_TYPES = [
        (0, 'EMPTY'),
        (1, 'RUN_LVL'),
        (2, 'BOOT_TIME'),
        (3, 'NEW_TIME'),
        (4, 'OLD_TIME'),
        (5, 'INIT_PROCESS'),
        (6, 'LOGIN_PROCESS'),
        (7, 'USER_PROCESS'),
        (8, 'DEAD_PROCESS'),
        (9, 'ACCOUNTING')
    ]

    def __init__(self):
        self.ut_type = 0
        self.ut_pid = 0
        self.ut_line = b''
        self.ut_id = b''
        self.ut_user = b''
        self.ut_host = b''
        self.ut_exit_e_termination = 0
        self.ut_exit_e_exit = 0
        self.ut_session = 0
        self.ut_tv_tv_sec = 0
        self.ut_tv_tv_usec = 0
        self.ut_addr_v61 = b''
        self.ut_addr_v62 = b''
        self.ut_addr_v63 = b''
        self.ut_addr_v64 = b''
        self.__unused = b''

    @property
    def type_ntoa(self):
        return {x:y for (x,y) in self.UTMP_TYPES}

    @property
    def type_aton(self):
        return {y:x for (x,y) in self.UTMP_TYPES}

    def __str__(self):
        return '{type:>13} | {pid:>6} | {line:>6} | {id:>8} | {user:>12} | {host:>20} | {time:>24} | {ip}'.format(
            type=self.type_ntoa.get(self.ut_type, '<unknown type>'),
            pid=self.ut_pid,
            line=self.ut_line.strip(b'\x00'),
            id=self.ut_id.strip(b'\x00'),
            user=self.ut_user.strip(b'\x00'),
            host=self.ut_host.strip(b'\x00'),
            time=time.ctime(self.ut_tv_tv_sec),
            ip=socket.inet_ntoa(self.ut_addr_v61)
        )

    def unpack(self, data):
        (self.ut_type,
         self.ut_pid,
         self.ut_line,
         self.ut_id,
         self.ut_user,
         self.ut_host,
         self.ut_exit_e_termination,
         self.ut_exit_e_exit,
         self.ut_session,
         self.ut_tv_tv_sec,
         self.ut_tv_tv_usec,
         self.ut_addr_v61,
         self.ut_addr_v62,
         self.ut_addr_v63,
         self.ut_addr_v64,
         self.__unused) = struct.unpack(self.RECORD_STRUCT, data[:self.RECORD_STRUCT_SIZE])
        return data[self.RECORD_STRUCT_SIZE:]


class UtmpParser(object):
    def __init__(self, fname='/var/run/utmp'):
        self.utmp = UtmpRecord()
        self.fname = fname

    def dump(self):
        entries = []
        with open(self.fname, 'rb') as f:
            data = f.read()
        while data:
            u = UtmpRecord()
            try:
                data = u.unpack(data)
            except struct.error:
                break
            entries.append(u)
            print(u)
        print('Unpacked {} entries'.format(len(entries)))
        return entries

    def delete(self, pid, dry_run=False):
        index = 0
        deleted = 0
        out_data = b''
        with open(self.fname, 'rb') as f:
            data = f.read()
        while data[index:]:
            u = UtmpRecord()
            try:
                u.unpack(data[index:])
            except struct.error:
                break
            if u.ut_pid == pid:
                print('Deleting entry: {}'.format(u))
                deleted += 1
            else:
                out_data += data[index:index + u.RECORD_STRUCT_SIZE]
            index += u.RECORD_STRUCT_SIZE
        if not dry_run:
            with open(self.fname, 'wb') as f:
                f.write(out_data)
        print('[+] Deleted {} entries'.format(deleted))
        return


class WtmpParser(UtmpParser):
    def __init__(self, fname='/var/log/wtmp'):
        super(WtmpParser, self).__init__(fname)


class BtmpParser(UtmpParser):
    def __init__(self, fname='/var/log/btmp'):
        super(BtmpParser, self).__init__(fname)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true', help='SIMULATE deleting entries but do not delete them')
    parser.add_argument('--dump-wtmp', action='store_true', help='Dump the contents of the WTMP file')
    parser.add_argument('--dump-utmp', action='store_true', help='Dump the contents of the UTMP file')
    parser.add_argument('--dump-btmp', action='store_true', help='Dump the contents of the BTMP file')
    parser.add_argument('--delete-pids', nargs='*', default=[], help='PIDs to delete from WTMP/UTMP')
    args = parser.parse_args()

    if args.dry_run:
        print('[-] WARNING: Dry-Run mode is enabled')

    if args.delete_pids:
        up = UtmpParser()
        wp = WtmpParser()
        bp = BtmpParser()
        for pid in args.delete_pids:
            up.delete(int(pid), dry_run=args.dry_run)
            wp.delete(int(pid), dry_run=args.dry_run)
            bp.delete(int(pid), dry_run=args.dry_run)

    if args.dump_utmp:
        up = UtmpParser()
        up.dump()

    if args.dump_wtmp:
        wp = WtmpParser()
        wp.dump()

    if args.dump_btmp:
        bp = BtmpParser()
        bp.dump()

if __name__ == '__main__':
    main()
