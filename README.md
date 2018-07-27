# loghammer
Loghammer is an unimaginatively named tool for parsing utmp/wtmp/btmp log files on Linux (maybe *nix?) systems.

## Requirements

- Python 2.7
- Root permissions (for entry removal only)

## Usage

```
user@user-virtual-machine /opt/loghammer $ last
user     pts/1        127.0.0.1        Fri Jul 27 16:57   still logged in
user     pts/1        127.0.0.1        Tue Jul 24 16:33 - 16:34  (00:00)
user     pts/5        127.0.0.1        Tue Jul 24 16:30 - 16:31  (00:00)
user     pts/2        127.0.0.1        Tue Jul 24 16:21 - 16:21  (00:00)
user     pts/2        127.0.0.1        Tue Jul 24 16:21 - 16:21  (00:00)
user     tty7         :0               Wed May 24 17:22    gone - no logout
reboot   system boot  4.4.0-21-generic Wed May 24 17:22   still running

wtmp begins Wed May 24 17:22:36 2017


/opt/loghammer $ python loghammer.py --dump-wtmp
      RUN_LVL |      0 |      ~ |       ~~ |     shutdown |     4.4.0-21-generic | Wed May 24 17:22:36 2017 | 0.0.0.0
    BOOT_TIME |      0 |      ~ |       ~~ |       reboot |     4.4.0-21-generic | Wed May 24 17:22:43 2017 | 0.0.0.0
      RUN_LVL |     53 |      ~ |       ~~ |     runlevel |     4.4.0-21-generic | Wed May 24 17:22:48 2017 | 0.0.0.0
 INIT_PROCESS |   1263 |   tty1 |     tty1 |              |                      | Wed May 24 17:22:48 2017 | 0.0.0.0
LOGIN_PROCESS |   1263 |   tty1 |     tty1 |        LOGIN |                      | Wed May 24 17:22:48 2017 | 0.0.0.0
 USER_PROCESS |   1832 |   tty7 |       :0 |         user |                   :0 | Wed May 24 17:22:56 2017 | 0.0.0.0
 USER_PROCESS |  80954 |  pts/2 |     ts/2 |         user |            127.0.0.1 | Tue Jul 24 16:21:05 2018 | 127.0.0.1
 DEAD_PROCESS |  80954 |  pts/2 |          |              |                      | Tue Jul 24 16:21:06 2018 | 0.0.0.0
 USER_PROCESS |  81007 |  pts/2 |     ts/2 |         user |            127.0.0.1 | Tue Jul 24 16:21:32 2018 | 127.0.0.1
 DEAD_PROCESS |  81007 |  pts/2 |          |              |                      | Tue Jul 24 16:21:52 2018 | 0.0.0.0
 USER_PROCESS |  81448 |  pts/5 |     ts/5 |         user |            127.0.0.1 | Tue Jul 24 16:30:54 2018 | 127.0.0.1
 DEAD_PROCESS |  81448 |  pts/5 |          |              |                      | Tue Jul 24 16:31:26 2018 | 0.0.0.0
 USER_PROCESS |  81583 |  pts/1 |     ts/1 |         user |            127.0.0.1 | Tue Jul 24 16:33:39 2018 | 127.0.0.1
 DEAD_PROCESS |  81583 |  pts/1 |          |              |                      | Tue Jul 24 16:34:15 2018 | 0.0.0.0
 USER_PROCESS |  86324 |  pts/1 |     ts/1 |         user |            127.0.0.1 | Fri Jul 27 16:57:38 2018 | 127.0.0.1
Unpacked 15 entries


/opt/loghammer $ sudo python loghammer.py --delete-pids 86324
[sudo] password for user:
Deleting entry:  USER_PROCESS |  86324 |  pts/1 |     ts/1 |         user |            127.0.0.1 | Fri Jul 27 16:57:38 2018 | 127.0.0.1
[+] Deleted 1 entries
Deleting entry:  USER_PROCESS |  86324 |  pts/1 |     ts/1 |         user |            127.0.0.1 | Fri Jul 27 16:57:38 2018 | 127.0.0.1
[+] Deleted 1 entries
[+] Deleted 0 entries
user@user-virtual-machine /opt/loghammer $ last
user     pts/1        127.0.0.1        Tue Jul 24 16:33 - 16:34  (00:00)
user     pts/5        127.0.0.1        Tue Jul 24 16:30 - 16:31  (00:00)
user     pts/2        127.0.0.1        Tue Jul 24 16:21 - 16:21  (00:00)
user     pts/2        127.0.0.1        Tue Jul 24 16:21 - 16:21  (00:00)
user     tty7         :0               Wed May 24 17:22    gone - no logout
reboot   system boot  4.4.0-21-generic Wed May 24 17:22   still running

wtmp begins Wed May 24 17:22:36 2017
```

## What are utmp-based files?

- utmp: `w` and `who` commands use this file to display currently logged in users
- wtmp: `last` uses this file to display historical logons
- btmp: This file is used to track unsuccessful login attempts (e.g. at SSH connection)

## What is the effect of removing entries from those files?

- utmp: You are not logged in (e.g. remove you from output of `who`)
- wtmp: You never logged in, in the first place
- btmp: Your bad password guesses before you got in never happened

## This is the most powerful tool ever created

Thanks! But you should know that:

- This tool doesn't remove log entries from text log files under `/var/log` (e.g. `/var/log/auth.log`)
- This tool doesn't hide the fact that you're logged in from the process list or netstat
- This tool doesn't touch the timestamp back after making edits to the files
- This tool is not special

