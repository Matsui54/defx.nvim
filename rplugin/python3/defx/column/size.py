# ============================================================================
# FILE: size.py
# AUTHOR: Shougo Matsushita <Shougo.Matsu at gmail.com>
# License: MIT license
# ============================================================================

from defx.base.column import Base, Highlights
from defx.context import Context
from defx.util import Nvim, readable, Candidate

import typing


class Column(Base):

    def __init__(self, vim: Nvim) -> None:
        super().__init__(vim)

        self.name = 'size'
        self.has_get_with_highlights = True

    def get_with_highlights(self, context: Context,
                            candidate: Candidate) -> typing.Tuple[
                                str, Highlights]:
        path = candidate['action__path']
        if not readable(path) or path.is_dir():
            return (' ' * 9, [])
        size = self._get_size(path.stat().st_size)
        text = '{:>6s}{:>3s}'.format(size[0], size[1])
        return (text, [('Constant', self.start, len(text))])

    def _get_size(self, size: float) -> typing.Tuple[str, str]:
        multiple = 1024
        suffixes = ['KB', 'MB', 'GB', 'TB']
        if size < multiple:
            return (str(size), 'B')
        for suffix in suffixes:
            size /= multiple
            if size < multiple:
                return ('{:.1f}'.format(size), suffix)
        return ('INF', '')

    def length(self, context: Context) -> int:
        return 9

    def highlight_commands(self) -> typing.List[str]:
        commands: typing.List[str] = []
        commands.append(
            f'highlight default link {self.syntax_name} Constant')
        return commands
