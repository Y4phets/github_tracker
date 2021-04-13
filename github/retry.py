import time
import logging
import functools

__all__ = ('retry', )

logger = logging.getLogger(__name__)


def retry(exceptions=Exception, tries=-1, delay=1, back_off=1):
    def _wrap(func):
        @functools.wraps(func)
        def _inner(*args, **kwargs):
            _tries, _delay = tries, delay
            while _tries:
                try:
                    return func(*args, **kwargs)
                except exceptions as ex:
                    logger.warning(f'Failed to make func call, retry {_tries - 1}/{tries} sleep {_delay}')
                    _tries -= 1
                    if _tries <= 0:
                        raise ex
                    time.sleep(_delay)
                    _delay *= back_off
        return _inner
    return _wrap
