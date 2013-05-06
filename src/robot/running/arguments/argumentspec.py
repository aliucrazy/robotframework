#  Copyright 2008-2012 Nokia Siemens Networks Oyj
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import sys

from robot import utils


class ArgumentSpec(object):

    def __init__(self, name, type='Keyword', positional=None, defaults=None,
                 varargs=None, kwargs=None):
        self.name = name
        self.type = type
        self.positional = positional or []
        self.defaults = defaults or []
        self.varargs = varargs
        self.kwargs = kwargs

    @property
    def minargs(self):
        return len(self.positional) - len(self.defaults)

    @property
    def maxargs(self):
        return len(self.positional) \
            if not (self.varargs or self.kwargs) else sys.maxint

    # FIXME: Move logging elsewhere
    def trace_log_args(self, logger, positional, named):
        message = lambda: self._get_trace_log_arg_message(positional, named)
        logger.trace(message)

    def _get_trace_log_arg_message(self, positional, named):
        args = [utils.safe_repr(arg) for arg in positional]
        if named:
            args += ['%s=%s' % (utils.unic(name), utils.safe_repr(value))
                     for name, value in named.items()]
        return 'Arguments: [ %s ]' % ' | '.join(args)

    def trace_log_uk_args(self, logger, variables):
        message = lambda: self._get_trace_log_uk_arg_message(variables)
        logger.trace(message)

    def _get_trace_log_uk_arg_message(self, variables):
        names = self._get_positional_with_decoration() \
                + self._get_varargs_with_decoration()
        args = ['%s=%s' % (name, utils.safe_repr(variables[name]))
                for name in names]
        return 'Arguments: [ %s ]' % ' | '.join(args)

    def _get_positional_with_decoration(self):
        return ['${%s}' % arg for arg in self.positional]

    def _get_varargs_with_decoration(self):
        return ['@{%s}' % self.varargs] if self.varargs else []