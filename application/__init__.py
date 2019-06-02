import sys
import json
import os
import getopt


class Application:
    def __init__(self):
        self.proj = {}
        self.usage = 'Usage: bi.py [-h] [project file]'

        try:
            opts, args = getopt.getopt(sys.argv[1:], 'h', ['help'])
        except getopt.GetoptError:
            sys.stderr.write(self.usage + '\n')
            sys.exit(1)

        for opt, arg in opts:
            if opt in ('-h', '--help'):
                print(self.usage)
                sys.exit(0)

        if len(args) == 0:
            print("Warning: Not refer to a project file, use 'default.json' in working directory instead")
            self.proj['file_name'] = 'default.json'
        elif len(args) > 1:
            sys.stderr.printf(self.usage)
            sys.exit(1)
        else:
            self.proj['file_name'] = args[0]

        self.parser_proj()

    def parser_proj(self):
        try:
            with open(self.proj['file_name'], 'r') as file:
                dict = json.load(file)
                self.proj['source_file'] = os.path.join(dict['data_dir'], dict['source_file'])
                self.proj['output_file'] = os.path.join(dict['data_dir'], dict['output_file'])
        except KeyError as e:
            s = "Invalid key found in project file: '" + e.args[0] + "'\n"
            sys.stderr.write(s)
            sys.exit(2)
        except Exception as e:
            sys.stderr.write(str(e) + '\n')
            sys.exit(2)


app = Application()