'''
Execute a command from the OS.
Capture the standard and error output.
Get the exit code.
'''

import subprocess as sp

# successful command 
SUCCESS = 0


# default encoding
DEFAULT_ENCODING = 'utf8'


class Command:
    
    def __init__(self, cmd, shell=True, stdin=None, encoding=DEFAULT_ENCODING):
        '''Initialize the command'''

        # cmd can be a string or a list of strings
        if isinstance(cmd, list):
            _cmd = " ".join(cmd)
        elif isinstance(cmd, str):
            _cmd = cmd
        else:
            raise ValueError
        
        self.cmd = _cmd
        self.shell = shell
        self.stdin = stdin
        self.encoding = encoding
        self.result = None

    def run(self, stdin=None):
        '''Execute the command'''
        
        # we can overwrite the value passed to __init__
        _input = stdin if stdin else self.stdin
        
        self.result = sp.run(
            self.cmd,
            shell=self.shell,
            stdin=_input,
            stdout=sp.PIPE,
            stderr=sp.PIPE,
            encoding=self.encoding
        )
        
    @property
    def success(self):
        '''Result of the command execution'''
        return self.result.returncode==SUCCESS if self.result else False

    @property
    def returncode(self):
        '''Return the exit code'''
        return self.result.returncode if self.result else None

    @property
    def outlines(self):
        '''Standard output of the command'''
        return self.result.stdout.splitlines() if self.result else []   

    @property
    def errlines(self):
        '''Error output of the command'''
        return self.result.stderr.splitlines() if self.result else []   

    @property
    def lines(self):
        '''Standard and error output of the command'''
        return self.outlines + self.errlines


if __name__ == '__main__':
    
    import argparse
    import pathlib

    def parse_args():

        parser = argparse.ArgumentParser(
            description='''Execute a command from the OS, capturing the generated output and the exit code.'''            
        )

        parser.add_argument(
            '-e', '--encoding',
            default=DEFAULT_ENCODING,
            help=f'Character encoding. Default: {DEFAULT_ENCODING}'
        )

        parser.add_argument(
            'command',
            help='Command to execute and its parameters, between quotation marks .'
        )

        parser.epilog = f'Sample: {pathlib.Path(__file__).name} "ls -l ~/"'

        return parser.parse_args()


    args = parse_args()
    
    # command to execute
    cmd = Command(args.command, encoding=args.encoding)
    
    # execute the command
    cmd.run()
    
    # executed command
    print(f'Command: {cmd.cmd}')
    exit_msg = f'Exit code: {cmd.returncode}'

    # result of the command execution
    if cmd.success:
        exit_msg = f'Success (exit code={cmd.returncode})'
        output_lines = cmd.outlines
    else:
        exit_msg = f'Fail (exit code={cmd.returncode})'
        output_lines = cmd.errlines

    print(f'{exit_msg}')
    print('Output:') 
    # pretty printing the output
    for index, line in enumerate(output_lines):
        print(f'{index:03d}: {line}')  
