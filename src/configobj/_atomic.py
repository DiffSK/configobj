"""Atomic replacement of configuration files, without external dependencies."""

import errno
import os
import stat
import uuid


def atomic_write(filename, content):
    """Write bytes beside the destination, sync them, then replace it.

    Resolve symlinks so writing through a link continues to update its target.
    Existing permission bits are preserved; new files respect the process umask.
    Replacement requires write access to the containing directory. Other hard
    links, ownership, ACLs and extended attributes are not carried to the new inode.
    """
    filename = os.path.realpath(filename)
    directory = os.path.dirname(filename)
    try:
        original = os.stat(filename)
    except FileNotFoundError:
        original = None
    if original is not None and not stat.S_ISREG(original.st_mode):
        raise OSError(errno.EINVAL, 'Atomic writes require a regular file', filename)

    # O_EXCL avoids collisions without ever truncating an existing file. Unlike
    # chmod(0666), the creation mode also respects the umask for new configs.
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, 'O_BINARY', 0)
    for attempt in range(100):
        name = '.configobj-' + uuid.uuid4().hex + '.tmp'
        if isinstance(directory, bytes):
            name = name.encode('ascii')
        temporary = os.path.join(directory, name)
        try:
            fd = os.open(temporary, flags, 0o600 if original else 0o666)
        except FileExistsError:
            continue
        break
    else:
        raise FileExistsError(errno.EEXIST, 'Cannot create a temporary config', directory)

    try:
        try:
            stream = os.fdopen(fd, 'wb')
        except BaseException:
            os.close(fd)
            raise
        with stream:
            stream.write(content)
            stream.flush()
            if original is not None:
                os.chmod(temporary, stat.S_IMODE(original.st_mode))
            os.fsync(stream.fileno())
        # Close before replacing: Windows cannot rename an open temporary file.
        os.replace(temporary, filename)
        temporary = None
        if os.name == 'posix':
            # Persist the directory entry as well as the file data. A failure
            # here is reported, but the complete new file is already visible.
            directory_fd = os.open(directory, os.O_RDONLY | getattr(os, 'O_DIRECTORY', 0))
            try:
                os.fsync(directory_fd)
            finally:
                os.close(directory_fd)
    finally:
        if temporary is not None:
            try:
                os.unlink(temporary)
            except PermissionError:
                # The copied mode may make our temporary read-only on Windows.
                os.chmod(temporary, stat.S_IRUSR | stat.S_IWUSR)
                os.unlink(temporary)
