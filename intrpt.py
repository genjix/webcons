import code
import sys

class FileCacher:
    
    def __init__(self):
        self.reset()

    def reset(self):
        self.out = []

    def write(self, line):
        self.out.append(line)

    def flush(self):
        raw_buffer = self.out
        self.reset()
        output = []
        line = ""
        for out in raw_buffer:
            if "\n" in out:
                # Replace first occurance of \n
                line += out.replace("\n", "", 1)
                output.append(line)
                line = ""
            else:
                line += out
        if line:
            output.append(line)
        return output

class Shell(code.InteractiveConsole):

    def __init__(self):
        self.stdout = sys.stdout
        self.stderr = sys.stderr
        self.cache = FileCacher()
        code.InteractiveConsole.__init__(self)

    def push(self, line):
        sys.stdout.flush()
        sys.stderr.flush()
        sys.stdout = self.cache
        sys.stderr = self.cache
        retval = code.InteractiveConsole.push(self, line)
        sys.stdout = self.stdout
        sys.stderr = self.stderr
        return retval

    def flush_output(self):
        return self.cache.flush()

if __name__ == "__main__":
    sh = Shell()
    while True:
        line = raw_input(">>> ")
        while sh.push(line):
            line = raw_input("... ")
        output = sh.flush_output()
        print line
        print "outski", output

