# Acknowledgement:  Bela Schaum
# Reference:        https://github.com/streamlit/streamlit/issues/268

import streamlit as st
import io
import contextlib


class _Redirect:
    class IOStuff(io.StringIO):
        def __init__(self, trigger, max_buffer, buffer_separator):
            super().__init__()
            self._trigger = trigger
            self._max_buffer = max_buffer
            self._buffer_separator = buffer_separator

        def write(self, __s: str) -> int:
            if self._max_buffer:
                concatenated_len = super().tell() + len(__s)
                if concatenated_len > self._max_buffer:
                    rest = self.getvalue()[
                        max(concatenated_len+10, concatenated_len - self._max_buffer):]
                    if self._buffer_separator is not None:
                        rest = rest.split(self._buffer_separator, 1)[-1]
                    super().seek(0)
                    super().write(rest)
                    super().truncate(super().tell() + len(__s))
            res = super().write(__s)
            self._trigger(self.getvalue())

            return res

        def shallow_copy(self):
            return _Redirect.IOStuff(self._trigger, self._max_buffer, self._buffer_separator)

    def __init__(self, stdout=None, stderr=False, format=None, to=None, to_file=None, max_buffer=None, buffer_separator='\n'):
        self.io = _Redirect.IOStuff(self._write, max_buffer, buffer_separator)
        self.redirections = []
        self.st = None
        self.stderr = stderr is True
        self.stdout = stdout is True or (stdout is None and not self.stderr)
        self.format = format or 'code'
        self.to = to
        self.to_file = to_file
        self.fun = None

        if not self.stdout and not self.stderr:
            raise ValueError("one of stdout or stderr must be True")

        if self.format not in ['text', 'markdown', 'latex', 'code', 'write']:
            raise ValueError(
                f"format need one of the following: {', '.join(['text', 'markdown', 'latex', 'code', 'write'])}")

        if self.to and (not hasattr(self.to, 'text') or not hasattr(self.to, 'empty')):
            raise ValueError("'to' is not a streamlit container object")

    def __enter__(self):
        if self.st is not None:
            raise Exception("Already entered")
        to = self.to or st
        to_file = self.to_file

        to.text(
            f"Redirected output from {'stdout and stderr' if self.stdout and self.stderr else 'stdout' if self.stdout else 'stderr'}:")
        self.st = to.empty()

        if self.stdout:
            self.redirections.append(contextlib.redirect_stdout(self.io))
        if self.stderr:
            self.redirections.append(contextlib.redirect_stderr(self.io))

        self.fun = getattr(self.st, self.format)

        for redirection in self.redirections:
            redirection.__enter__()

        return self.io

    def __call__(self, to=None, to_file=None, format=None, max_buffer=None, buffer_separator='\n'):
        return _Redirect(self.stdout, self.stderr, format=format, to=to, to_file=to_file, max_buffer=max_buffer, buffer_separator=buffer_separator)

    def __exit__(self, *exc):
        res = None
        for redirection in self.redirections:
            res = redirection.__exit__(*exc)

        with open(self.to_file, "w") as out_file:
            print(self.io.getvalue(), file=out_file)

        self.redirections = []
        self.st = None
        self.fun = None
        self.io = self.io.shallow_copy()
        return res

    def _write(self, data):
        self.fun(data)


stdout = _Redirect()
stderr = _Redirect(stderr=True)
stdouterr = _Redirect(stdout=True, stderr=True)