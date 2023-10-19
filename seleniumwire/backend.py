import logging
import threading

from seleniumwire.server import MitmProxy

log = logging.getLogger(__name__)


def create(addr='127.0.0.1', port=0, options=None):
    """Create a new proxy backend.

    Args:
        addr: The address the proxy server will listen on. Default 127.0.0.1.
        port: The port the proxy server will listen on. Default 0 - which means
            use the first available port.
        options: Additional options to configure the proxy.

    Returns:
        An instance of the proxy backend.
    """
    # 选项
    if options is None:
        options = {}

    # 后端
    backend = MitmProxy(addr, port, options)

    # 启动一个后端线程
    t = threading.Thread(name='Selenium Wire Proxy Server', target=backend.serve_forever)
    t.daemon = not options.get('standalone')
    t.start()

    # 启动日志
    addr, port, *_ = backend.address()
    log.info('Created proxy listening on %s:%s', addr, port)

    # 创建后端成功
    return backend
