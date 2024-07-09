import os
import subprocess


class Solution:
    origin: str = ''
    filecommands: dict[str, list] = {}
    commands: list[str] = []

    def __init__(self, python_only: bool = True):
        """
        python_only: flag that allow only .py files to read
        """
        self.python_only = python_only

    def __get_input_path(self, repeat: bool = False):
        if not repeat:
            print('Hi! Please enter the absolute path to the root directory:')
        value = str(input())
        if len(value) == 0:
            print('Value should be not empty')
            self.__get_input_path(True)
            return
        value = value.rstrip().lstrip()
        if not os.path.isdir(os.path.abspath(value)):
            print(f'Path "{value}" is not a directory')
            self.__get_input_path(True)
            return
        self.origin = value

    def __find_python_files(self, path: str):
        for entry in os.listdir(os.path.abspath(path)):
            full = os.path.join(path, entry)
            if os.path.isdir(full):
                self.__find_python_files(full)
            else:
                if self.python_only:
                    if full.endswith('.py'):
                        self.__get_variable(full)
                    else:
                        pass
                else:
                    self.__get_variable(full)

    def __get_variable(self, filepath: str):
        with open(os.path.abspath(filepath), 'r') as f:
            code = f.read()
        context = {}
        try:
            compiled = compile(code, '<string>', 'exec')
            exec(compiled, context)
            self.filecommands[filepath] = context.get('CMDS', [])  # in case no CMDS variable
        except Exception as e:
            print(f'Some problems with file "{filepath}": {e}')

    def __collect_commands(self):
        for filecommands in self.filecommands.values():
            self.commands += filecommands

    def __execute(self):
        executed = []
        for command in self.commands:
            if command in executed:
                print(f'The command "{command}" has already been executed')
            else:
                executed.append(command)
                try:
                    subprocess.call(command.split(' '))
                except Exception as e:
                    print(f'Some problems with command "{command}: {e}"')

    def run(self):
        self.__get_input_path()
        self.__find_python_files(self.origin)
        self.filecommands = dict(sorted(self.filecommands.items()))
        self.__collect_commands()
        self.__execute()


if __name__ == '__main__':
    sol = Solution()
    sol.run()
