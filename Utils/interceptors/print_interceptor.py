import sys
import re

class PrintInterceptor:
    def __init__(self, expected_plates_set):
        self.expected_plates = expected_plates_set
        self.confirmed_plates = set()
        self.original_stdout = sys.stdout

        self.pattern1 = re.compile(r"\[Vehicle (\S+)\] Received confirmation to exit the park\.")
        self.pattern2 = re.compile(r"\[INIT\] Agente iniciado: (\S+)")

    def write(self, text):
        if not text.strip():
            return

        match1 = self.pattern1.search(text)
        match2 = self.pattern2.search(text)

        if match1:
            plate = match1.group(1)
            self.confirmed_plates.add(plate)
            self.original_stdout.write(text)
            self.original_stdout.write("\n")
            self.original_stdout.flush()
        elif match2:
            self.original_stdout.write(text)
            self.original_stdout.write("\n")
            self.original_stdout.flush()
        else:
            pass

    def flush(self):
        self.original_stdout.flush()