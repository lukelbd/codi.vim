# ------------------------------
# UNIX 'script' command emulator
# ------------------------------
# WARNING: Calling this from command line results in infinite hang, but no issue
# when used asynchronously with vim + codi. May be spawning sessions that never
# terminate, or maybe it terminates automatically (???).
# Tried detecting exit pattern in master_read but that is unreliable.
# Adapted from: https://docs.python.org/3.2/library/pty.html
# Timeout stuff from: https://stackoverflow.com/a/494273/4970632
# Also see (did not help) from: https://stackoverflow.com/q/6422016/4970632
import os
import pty
import signal  # noqa: F401
import sys
os.environ['INPUTRC'] = '/dev/null'  # not sure if this works, or is even necessary

stdin = []  # for debugging
master = []  # for debugging
nbytes = 32 * 1024  # allow huge input


class SignalException(Exception):
    pass

def timeout_handler(signum, frame):  # noqa: E302, U100
    raise SignalException

def master_read(fd):  # noqa: E302
    b = os.read(fd, nbytes)
    s = b.decode()
    master.append(s)
    return b

def stdin_read(fd):  # noqa: E302
    b = os.read(fd, nbytes)
    s = b.decode()
    stdin.append(s)
    return b


# Normal output
# pty.spawn(sys.argv[1:], master_read, stdin_read)

# Timed output
signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(5)  # prevent infinite hangs
try:
    pty.spawn(sys.argv[1:], master_read, stdin_read)
except SignalException:
    pass
