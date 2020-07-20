import logging


class XLog():
    level_prefix = {
        logging.DEBUG: "DEBUG",
        logging.INFO: "+",
        logging.WARNING: "!",
        logging.ERROR: "!!",
        logging.CRITICAL: "!!!",
    }

    def __init__(self, name="X-log", level=None):
        self.logger = logging.getLogger(name)

        # level handling
        if level == 'debug':
            level = logging.DEBUG
        elif level == 'info':
            level = logging.INFO
        elif level == 'warn' or level == 'warning':
            level = logging.WARNING
        elif level == 'error':
            level = logging.ERROR
        elif level == 'critical' or level == 'crit':
            level = logging.CRITICAL
        else:
            level = None

        self.level = level if level is not None else logging.INFO
        self.logger.setLevel(self.level)

        # create console handler and set level to debug
        self.ch = logging.StreamHandler()
        self.ch.setLevel(self.level)

        # create formatter
        self.formatter = logging.Formatter(
            '[%(name)s]%(message)s')

        # add formatter to ch
        self.ch.setFormatter(self.formatter)

        # add ch to logger
        self.logger.addHandler(self.ch)


    def _createMsg(self, level, msg):
        prefix = self.level_prefix[level]
        return f"[{prefix}]: {msg}"


    def _hexMsg(self, num):
        return hex(num)


    def debug(self, msg):
        msg = self._createMsg(logging.DEBUG, msg)
        self.logger.debug(msg)


    def info(self, msg):
        msg = self._createMsg(logging.INFO, msg)
        self.logger.info(msg)


    """
        for address leak (libc, heap, canary)
    """
    def libc(self, leak, check=True):
        if check and leak >> 40 != 0x7f and leak & 0xfff != 0:
            self.warning(f"invalid libc address!! ({hex(leak)})")
            return

        msg = f"libc address -> {self._hexMsg(leak)}"
        self.info(msg)


    def heap(self, leak, check=True):
        if check and leak & 0xfff != 0:
            self.warning(f"invalid heap address!! ({hex(leak)})")
            return

        msg = f"heap address -> {self._hexMsg(leak)}"
        self.info(msg)


    def canary(self, leak):
        msg = f"canary -> {self._hexMsg(leak)}"
        self.info(msg)


    def warning(self, msg):
        msg = self._createMsg(logging.WARNING, msg)
        self.logger.warning(msg)


    def error(self, msg, raise_err=False):
        msg = self._createMsg(logging.ERROR, msg)
        self.logger.error(msg)

        if raise_err:
            raise Exception(msg)


    def critical(self, msg):
        msg = self._createMsg(logging.CRITICAL, msg)
        self.logger.critical(msg)

        raise Exception(msg)
