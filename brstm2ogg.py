#!/usr/bin/python3

# MIT License
#
# Copyright (c) 2023 Vitaly Novichkov
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from subprocess import Popen, PIPE
import re
import sys
import os
import tempfile

reg_start = "loop start: (\d+) samples"
reg_end = "loop end: (\d+) samples"

if __name__ == '__main__':

    in_file = ""
    out_file = ""

    if len(sys.argv) < 2:
        print("Syntax:\n\n%s <input file> [<output file>]\n\n" % sys.argv[0])
        exit(1)

    in_file = sys.argv[1]
    if len(sys.argv) < 3:
        out_file = sys.argv[1]
        if out_file.endswith(".brstm"):
            out_file = out_file.removesuffix(".brstm") + ".ogg"
        elif out_file.endswith(".ras"):
            out_file = out_file.removesuffix(".ras") + ".ogg"
        elif out_file.endswith(".bwav"):
            out_file = out_file.removesuffix(".bwav") + ".ogg"
        else:
            out_file = out_file + ".ogg"

    output = Popen(["vgmstream-cli", "-m", in_file], stdout=PIPE)
    response = output.communicate()[0].decode('utf-8')
    loop_start_r = re.search(reg_start, response)
    loop_start = ""
    if loop_start_r:
        loop_start = loop_start_r.group(1)

    loop_end_r = re.search(reg_end, response)
    loop_end = ""
    if loop_end_r:
        loop_end = loop_end_r.group(1)

    print("LOOPSTART=%s, LOOPEND=%s" % (loop_start, loop_end))

    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, 'convert.wav')
        print("Temp file %s" % path)

        output = Popen(["vgmstream-cli", "-l", "1", "-f", "0", in_file, "-o", path], stdout=PIPE)
        response = output.communicate()[0].decode('utf-8')
        print(response)

        if loop_start != "" and loop_end != "":
            output = Popen(["oggenc", "-q", "5",
                            "-c", "LOOPSTART=%s" % loop_start,
                            "-c", "LOOPEND=%s" % loop_end,
                            "-o", out_file,
                            path], stdout=PIPE)
        else:
            output = Popen(["oggenc", "-q", "5", "-o", out_file, path], stdout=PIPE)

        response = output.communicate()[0].decode('utf-8')
        print(response)
