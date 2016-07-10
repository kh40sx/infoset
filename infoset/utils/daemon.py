"""Generic linux daemon base class for python 3.x."""

import sys
import os
import time
import atexit
import signal


class Daemon:
    """A generic daemon class.

    Usage: subclass the daemon class and override the run() method.

    Modified from http://www.jejik.com/files/examples/daemon3x.py

    """

    def __init__(self, pidfile):
        """Method for intializing the class.

        Args:
            pidfile: Name of PID file

        Returns:
            None

        """
        # Initialize key variables
        self.pidfile = pidfile

    def daemonize(self):
        """Deamonize class. UNIX double fork mechanism.

        Args:
            None

        Returns:
            None

        """
        # Create a parent process that will manage the child
        # when the code using this class is done.
        try:
            pid = os.fork()
            if pid > 0:
                # Exit first parent
                sys.exit(0)
        except OSError as err:
            sys.stderr.write('fork #1 failed: {0}\n'.format(err))
            sys.exit(1)

        # Decouple from parent environment
        os.chdir('/')
        os.setsid()
        os.umask(0)

        # Do second fork
        try:
            pid = os.fork()
            if pid > 0:

                # exit from second parent
                sys.exit(0)
        except OSError as err:
            sys.stderr.write('fork #2 failed: {0}\n'.format(err))
            sys.exit(1)

        # Redirect standard file descriptors
        sys.stdout.flush()
        sys.stderr.flush()
        f_handle_si = open(os.devnull, 'r')
        # f_handle_so = open(os.devnull, 'a+')
        f_handle_se = open(os.devnull, 'a+')

        os.dup2(f_handle_si.fileno(), sys.stdin.fileno())
        # os.dup2(f_handle_so.fileno(), sys.stdout.fileno())
        os.dup2(f_handle_se.fileno(), sys.stderr.fileno())

        # write pidfile
        atexit.register(self.delpid)

        pid = str(os.getpid())
        with open(self.pidfile, 'w+') as f_handle:
            f_handle.write(pid + '\n')

    def delpid(self):
        """Delete the PID file.

        Args:
            None

        Returns:
            None

        """
        # Delete file
        os.remove(self.pidfile)

    def start(self):
        """Start the daemon.

        Args:
            None

        Returns:

        """
        # Check for a pidfile to see if the daemon already runs
        try:
            with open(self.pidfile, 'r') as pf_handle:

                pid = int(pf_handle.read().strip())
        except IOError:
            pid = None

        if pid:
            message = "pidfile {0} already exist. " + \
                    "Daemon already running?\n"
            sys.stderr.write(message.format(self.pidfile))
            sys.exit(1)

        # Start the daemon
        self.daemonize()
        self.run()

    def stop(self):
        """Stop the daemon.

        Args:
            None

        Returns:

        """
        # Get the pid from the pidfile
        try:
            with open(self.pidfile, 'r') as pf_handle:
                pid = int(pf_handle.read().strip())
        except IOError:
            pid = None

        if not pid:
            message = "pidfile {0} does not exist. " + \
                    "Daemon not running?\n"
            sys.stderr.write(message.format(self.pidfile))
            # Not an error in a restart
            return

        # Try killing the daemon process
        try:
            while 1:
                os.kill(pid, signal.SIGTERM)
                time.sleep(0.1)
        except OSError as err:
            error = str(err.args)
            if error.find("No such process") > 0:
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
            else:
                print(str(err.args))
                sys.exit(1)

    def restart(self):
        """Restart the daemon.

        Args:
            None

        Returns:

        """
        # Restart
        self.stop()
        self.start()

    def status(self):
        """Get daemon status.

        Args:
            None

        Returns:

        """
        # Get status
        if os.path.exists(self.pidfile) is True:
            print('Daemon is running')
        else:
            print('Daemon is stopped')

    def run(self):
        """You should override this method when you subclass Daemon.

        It will be called after the process has been daemonized by
        start() or restart().
        """
        # Simple comment to pass linter
        pass
