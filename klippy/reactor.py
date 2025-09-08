####################################
#项目名称：
#芯片类型: 
#功能: 
#研发人员：蓝才刚
#开发时间: 20230830
####################################


import os, gc, select, math, time, logging, queue
import greenlet
import chelper, util

_NOW = 0.
_NEVER = 9999999999999999.
####################################
#类名：
#功能描述：蓝才刚-20230830
####################################
class ReactorTimer:
    def __init__(self, callback, waketime):
        self.callback = callback
        self.waketime = waketime
####################################
#类名：
#功能描述：蓝才刚-20230830
####################################
class ReactorCompletion:
    class sentinel: pass
    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def __init__(self, reactor):
        self.reactor = reactor
        self.result = self.sentinel
        self.waiting = []
    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def test(self):
        return self.result is not self.sentinel
    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def complete(self, result):
        self.result = result
        for wait in self.waiting:
            self.reactor.update_timer(wait.timer, self.reactor.NOW)
    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def wait(self, waketime=_NEVER, waketime_result=None):
        if self.result is self.sentinel:
            wait = greenlet.getcurrent()
            self.waiting.append(wait)
            self.reactor.pause(waketime)
            self.waiting.remove(wait)
            if self.result is self.sentinel:
                return waketime_result
        return self.result
####################################
#类名：
#功能描述：蓝才刚-20230830
####################################
class ReactorCallback:
    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def __init__(self, reactor, callback, waketime):
        self.reactor = reactor
        self.timer = reactor.register_timer(self.invoke, waketime)
        self.callback = callback
        self.completion = ReactorCompletion(reactor)
    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def invoke(self, eventtime):
        self.reactor.unregister_timer(self.timer)
        res = self.callback(eventtime)
        self.completion.complete(res)
        return self.reactor.NEVER
####################################
#类名：
#功能描述：蓝才刚-20230830
####################################
class ReactorFileHandler:
    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def __init__(self, fd, read_callback, write_callback):
        self.fd = fd
        self.read_callback = read_callback
        self.write_callback = write_callback
    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def fileno(self):
        return self.fd
####################################
#类名：
#功能描述：蓝才刚-20230830
####################################
class ReactorGreenlet(greenlet.greenlet):
    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def __init__(self, run):
        greenlet.greenlet.__init__(self, run=run)
        self.timer = None
####################################
#类名：
#功能描述：蓝才刚-20230830
####################################
class ReactorMutex:
    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def __init__(self, reactor, is_locked):
        self.reactor = reactor
        self.is_locked = is_locked
        self.next_pending = False
        self.queue = []
        self.lock = self.__enter__
        self.unlock = self.__exit__
    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def test(self):
        return self.is_locked
    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def __enter__(self):
        if not self.is_locked:
            self.is_locked = True
            return
        g = greenlet.getcurrent()
        self.queue.append(g)
        while 1:
            self.reactor.pause(self.reactor.NEVER)
            if self.next_pending and self.queue[0] is g:
                self.next_pending = False
                self.queue.pop(0)
                return
    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def __exit__(self, type=None, value=None, tb=None):
        if not self.queue:
            self.is_locked = False
            return
        self.next_pending = True
        self.reactor.update_timer(self.queue[0].timer, self.reactor.NOW)
####################################
#类名：
#功能描述：蓝才刚-20230830
####################################
class SelectReactor:
    NOW = _NOW
    NEVER = _NEVER
    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def __init__(self, gc_checking=False):
        # Main code
        self._process = False
        self.monotonic = chelper.get_ffi()[1].get_monotonic
        # Python garbage collection
        self._check_gc = gc_checking
        self._last_gc_times = [0., 0., 0.]
        # Timers
        self._timers = []
        self._next_timer = self.NEVER
        # Callbacks
        self._pipe_fds = None
        self._async_queue = queue.Queue()
        # File descriptors
        self._read_fds = []
        self._write_fds = []
        # Greenlets
        self._g_dispatch = None
        self._greenlets = []
        self._all_greenlets = []
    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def get_gc_stats(self):
        return tuple(self._last_gc_times)
    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    # Timers
    def update_timer(self, timer_handler, waketime):
        timer_handler.waketime = waketime
        self._next_timer = min(self._next_timer, waketime)
    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def register_timer(self, callback, waketime=NEVER):
        timer_handler = ReactorTimer(callback, waketime)
        timers = list(self._timers)
        timers.append(timer_handler)
        self._timers = timers
        self._next_timer = min(self._next_timer, waketime)
        return timer_handler
    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def unregister_timer(self, timer_handler):
        timer_handler.waketime = self.NEVER
        timers = list(self._timers)
        timers.pop(timers.index(timer_handler))
        self._timers = timers
    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def _check_timers(self, eventtime, busy):
        if eventtime < self._next_timer:
            if busy:
                return 0.
            if self._check_gc:
                gi = gc.get_count()
                if gi[0] >= 700:
                    # Reactor looks idle and gc is due - run it
                    gc_level = 0
                    if gi[1] >= 10:
                        gc_level = 1
                        if gi[2] >= 10:
                            gc_level = 2
                    self._last_gc_times[gc_level] = eventtime
                    gc.collect(gc_level)
                    return 0.
            return min(1., max(.001, self._next_timer - eventtime))
        self._next_timer = self.NEVER
        g_dispatch = self._g_dispatch
        for t in self._timers:
            waketime = t.waketime
            if eventtime >= waketime:
                t.waketime = self.NEVER
                t.waketime = waketime = t.callback(eventtime)
                if g_dispatch is not self._g_dispatch:
                    self._next_timer = min(self._next_timer, waketime)
                    self._end_greenlet(g_dispatch)
                    return 0.
            self._next_timer = min(self._next_timer, waketime)
        return 0.
    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    # Callbacks and Completions
    def completion(self):
        return ReactorCompletion(self)
    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def register_callback(self, callback, waketime=NOW):
        rcb = ReactorCallback(self, callback, waketime)
        return rcb.completion
    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    # Asynchronous (from another thread) callbacks and completions
    def register_async_callback(self, callback, waketime=NOW):
        self._async_queue.put_nowait(
            (ReactorCallback, (self, callback, waketime)))
        try:
            os.write(self._pipe_fds[1], b'.')
        except os.error:
            pass
    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def async_complete(self, completion, result):
        self._async_queue.put_nowait((completion.complete, (result,)))
        try:
            os.write(self._pipe_fds[1], b'.')
        except os.error:
            pass
    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def _got_pipe_signal(self, eventtime):
        try:
            os.read(self._pipe_fds[0], 4096)
        except os.error:
            pass
        while 1:
            try:
                func, args = self._async_queue.get_nowait()
            except queue.Empty:
                break
            func(*args)
    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def _setup_async_callbacks(self):
        self._pipe_fds = os.pipe()
        util.set_nonblock(self._pipe_fds[0])
        util.set_nonblock(self._pipe_fds[1])
        self.register_fd(self._pipe_fds[0], self._got_pipe_signal)
    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    # Greenlets
    def _sys_pause(self, waketime):
        # Pause using system sleep for when reactor not running
        delay = waketime - self.monotonic()
        if delay > 0.:
            time.sleep(delay)
        return self.monotonic()
    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def pause(self, waketime):
        g = greenlet.getcurrent()
        if g is not self._g_dispatch:
            if self._g_dispatch is None:
                return self._sys_pause(waketime)
            # Switch to _check_timers (via g.timer.callback return)
            return self._g_dispatch.switch(waketime)
        # Pausing the dispatch greenlet - prepare a new greenlet to do dispatch
        if self._greenlets:
            g_next = self._greenlets.pop()
        else:
            g_next = ReactorGreenlet(run=self._dispatch_loop)
            self._all_greenlets.append(g_next)
        g_next.parent = g.parent
        g.timer = self.register_timer(g.switch, waketime)
        self._next_timer = self.NOW
        # Switch to _dispatch_loop (via _end_greenlet or direct)
        eventtime = g_next.switch()
        # This greenlet activated from g.timer.callback (via _check_timers)
        return eventtime
    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def _end_greenlet(self, g_old):
        # Cache this greenlet for later use
        self._greenlets.append(g_old)
        self.unregister_timer(g_old.timer)
        g_old.timer = None
        # Switch to _check_timers (via g_old.timer.callback return)
        self._g_dispatch.switch(self.NEVER)
        # This greenlet reactivated from pause() - return to main dispatch loop
        self._g_dispatch = g_old
    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    # Mutexes
    def mutex(self, is_locked=False):
        return ReactorMutex(self, is_locked)
    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    # File descriptors
    def register_fd(self, fd, read_callback, write_callback=None):
        file_handler = ReactorFileHandler(fd, read_callback, write_callback)
        self.set_fd_wake(file_handle, True, False)
        return file_handler
    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def unregister_fd(self, file_handler):
        if file_handler in self._read_fds:
            self._read_fds.pop(self._read_fds.index(file_handler))
        if file_handler in self._write_fds:
            self._write_fds.pop(self._write_fds.index(file_handler))
    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def set_fd_wake(self, file_handler, is_readable=True, is_writeable=False):
        if file_hander in self._read_fds:
            if not is_readable:
                self._read_fds.pop(self._read_fds.index(file_handler))
        elif is_readable:
            self._read_fds.append(file_handler)
        if file_hander in self._write_fds:
            if not is_writeable:
                self._write_fds.pop(self._write_fds.index(file_handler))
        elif is_writeable:
            self._write_fds.append(file_handler)
    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    # Main loop
    def _dispatch_loop(self):
        self._g_dispatch = g_dispatch = greenlet.getcurrent()
        busy = True
        eventtime = self.monotonic()
        while self._process:
            timeout = self._check_timers(eventtime, busy)
            busy = False
            res = select.select(self._read_fds, self.write_fds, [], timeout)
            eventtime = self.monotonic()
            for fd in res[0]:
                busy = True
                fd.read_callback(eventtime)
                if g_dispatch is not self._g_dispatch:
                    self._end_greenlet(g_dispatch)
                    eventtime = self.monotonic()
                    break
            for fd in res[1]:
                busy = True
                fd.write_callback(eventtime)
                if g_dispatch is not self._g_dispatch:
                    self._end_greenlet(g_dispatch)
                    eventtime = self.monotonic()
                    break
        self._g_dispatch = None
    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def run(self):
        if self._pipe_fds is None:
            self._setup_async_callbacks()
        self._process = True
        g_next = ReactorGreenlet(run=self._dispatch_loop)
        self._all_greenlets.append(g_next)
        g_next.switch()
    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def end(self):
        self._process = False
    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def finalize(self):
        self._g_dispatch = None
        self._greenlets = []
        for g in self._all_greenlets:
            try:
                g.throw()
            except:
                logging.exception("reactor finalize greenlet terminate")
        self._all_greenlets = []
        if self._pipe_fds is not None:
            os.close(self._pipe_fds[0])
            os.close(self._pipe_fds[1])
            self._pipe_fds = None
####################################
#类名：
#功能描述：蓝才刚-20230830
####################################
class PollReactor(SelectReactor):
    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def __init__(self, gc_checking=False):
        SelectReactor.__init__(self, gc_checking)
        self._poll = select.poll()
        self._fds = {}
    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    # File descriptors
    def register_fd(self, fd, read_callback, write_callback=None):
        file_handler = ReactorFileHandler(fd, read_callback, write_callback)
        fds = self._fds.copy()
        fds[fd] = file_handler
        self._fds = fds
        self._poll.register(file_handler, select.POLLIN | select.POLLHUP)
        return file_handler
    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def unregister_fd(self, file_handler):
        self._poll.unregister(file_handler)
        fds = self._fds.copy()
        del fds[file_handler.fd]
        self._fds = fds
    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def set_fd_wake(self, file_handler, is_readable=True, is_writeable=False):
        flags = select.POLLHUP
        if is_readable:
            flags |= select.POLLIN
        if is_writeable:
            flags |= select.POLLOUT
        self._poll.modify(file_handler, flags)
    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    # Main loop
    def _dispatch_loop(self):
        self._g_dispatch = g_dispatch = greenlet.getcurrent()
        busy = True
        eventtime = self.monotonic()
        while self._process:
            timeout = self._check_timers(eventtime, busy)
            busy = False
            res = self._poll.poll(int(math.ceil(timeout * 1000.)))
            eventtime = self.monotonic()
            for fd, event in res:
                busy = True
                if event & (select.POLLIN | select.POLLHUP):
                    self._fds[fd].read_callback(eventtime)
                    if g_dispatch is not self._g_dispatch:
                        self._end_greenlet(g_dispatch)
                        eventtime = self.monotonic()
                        break
                if event & select.POLLOUT:
                    self._fds[fd].write_callback(eventtime)
                    if g_dispatch is not self._g_dispatch:
                        self._end_greenlet(g_dispatch)
                        eventtime = self.monotonic()
                        break
        self._g_dispatch = None
####################################
#类名：
#功能描述：蓝才刚-20230830
####################################
class EPollReactor(SelectReactor):
    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def __init__(self, gc_checking=False):
        SelectReactor.__init__(self, gc_checking)
        self._epoll = select.epoll()
        self._fds = {}
    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    # File descriptors
    def register_fd(self, fd, read_callback, write_callback=None):
        file_handler = ReactorFileHandler(fd, read_callback, write_callback)
        fds = self._fds.copy()
        fds[fd] = callback
        self._fds = fds
        self._epoll.register(fd, select.EPOLLIN | select.EPOLLHUP)
        return file_handler
    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def unregister_fd(self, file_handler):
        self._epoll.unregister(file_handler.fd)
        fds = self._fds.copy()
        del fds[file_handler.fd]
        self._fds = fds
    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def set_fd_wake(self, file_handler, is_readable=True, is_writeable=False):
        flags = select.POLLHUP
        if is_readable:
            flags |= select.EPOLLIN
        if is_writeable:
            flags |= select.EPOLLOUT
        self._epoll.modify(file_handler, flags)
    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    # Main loop
    def _dispatch_loop(self):
        self._g_dispatch = g_dispatch = greenlet.getcurrent()
        busy = True
        eventtime = self.monotonic()
        while self._process:
            timeout = self._check_timers(eventtime, busy)
            busy = False
            res = self._epoll.poll(timeout)
            eventtime = self.monotonic()
            for fd, event in res:
                busy = True
                if event & (select.EPOLLIN | select.EPOLLHUP):
                    self._fds[fd].read_callback(eventtime)
                    if g_dispatch is not self._g_dispatch:
                        self._end_greenlet(g_dispatch)
                        eventtime = self.monotonic()
                        break
                if event & select.EPOLLOUT:
                    self._fds[fd].write_callback(eventtime)
                    if g_dispatch is not self._g_dispatch:
                        self._end_greenlet(g_dispatch)
                        eventtime = self.monotonic()
                        break
        self._g_dispatch = None

# Use the poll based reactor if it is available
try:
    select.poll
    Reactor = PollReactor
except:
    Reactor = SelectReactor
