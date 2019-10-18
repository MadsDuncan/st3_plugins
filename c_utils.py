import sublime
import sublime_plugin


class CSortIncludesCommand(sublime_plugin.TextCommand):
    """Sorts C includes in alphabetic order.

    Sorts C includes in selected text (region), in alphabetic order within groups. 
    A group is a block of includes with no empty lines or comments in between. 
    """
    def run(self, edit):
        # Get selected region as a list of lines.
        try:
            s = self.view.sel()[0]
        except IndexError:
            return

        lines = [self.view.substr(line) for line in self.view.split_by_newlines(s)]

        include_group = []
        result = []

        include_str = ('#include', '//#include')

        for line in lines:
            if line.startswith(include_str):
                include_group.append(line)
            else:
                if include_group:
                    result.extend(self._sort(include_group))
                    include_group.clear()

                result.append(line + '\n')

        # Catch case where last line of region is an include.
        if include_group:
            result.extend(self._sort(include_group))

        # Append newline if the original region ended with it.
        if not self.view.substr(s).endswith('\n'):
            result.pop()

        self.view.replace(edit, s, ''.join(result))

    def _sort(self, include_group):
        include_group.sort()

        result = []
        for i in include_group:
            result.append(i + '\n')

        return result
        