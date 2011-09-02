#!/usr/bin/env python
#################################################################
# pyusb access for ud7 display device
# By Kyle Machulis <kyle@nonpolynomial.com>
# http://www.nonpolynomial.com
#
# Licensed under the BSD License, as follows
#
# Copyright (c) 2011, Kyle Machulis/Nonpolynomial Labs
# All rights reserved.
#
# Redistribution and use in source and binary forms, 
# with or without modification, are permitted provided 
# that the following conditions are met:
#
#    * Redistributions of source code must retain the 
#      above copyright notice, this list of conditions 
#      and the following disclaimer.
#    * Redistributions in binary form must reproduce the 
#      above copyright notice, this list of conditions and 
#      the following disclaimer in the documentation and/or 
#      other materials provided with the distribution.
#    * Neither the name of the Nonpolynomial Labs nor the names 
#      of its contributors may be used to endorse or promote 
#      products derived from this software without specific 
#      prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND 
# CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, 
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF 
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR 
# CONTRIBUbTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, 
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT 
# NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; 
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR 
# OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, 
# EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#################################################################

import usb
import sys
import time
class ud7:
    ep = { 'in'  : 0x81, \
           'out' : 0x02
           }

    cmd_prefix = [0x50, 0x42, 0x54, 0x20]

    cmds = {
        "turn_on": [0x01, 0x01],
        "black" : [0x01, 0x02],
        "white" : [0x01, 0x03],
        "turn_off" : [0x01, 0x04],
        "set_backlight": [0x01, 0x06], #requires extra byte
        "status": [0x07],
        # orientation with base on top (upside down)
        # command: 0x02, ???, draw rect top, draw rect bottom, draw rect left, draw rect right, ???, ???
        "ready_image_update": [0x02, 0x00, 0x00, 0x7f, 0x00, 0x7f, 0x00, 0x02],
    }

    def __init__(self):
        self.ud7 = usb.core.find(idVendor = 0x04f3,
                                 idProduct = 0x1002)

        self.ud7.set_configuration()

    def button_read(self):
        ret = self.ud7.read(self.ep['in'], 64, 0, 1000)
        print ret

    def black_out(self):
        self.send_command("black")

    def turn_on(self):
        self.send_command("turn_on")

    def turn_off(self):
        self.send_command("turn_off")

    def check_button_state(self):
        self.send_command("status")
        ret = self.ud7.read(self.ep['in'], 64, 0, 1000)
        if ret[0xf] == 0x0:
            return True
        return False

    def send_frame(self, color):
        self.ready_image_update()
        self.ud7.write(self.ep['out'], [color for x in range(0, 32768)], 0, 1000)

    def send_command(self, command, arguments = []):
        cmd = self.cmd_prefix + self.cmds[command] + arguments 
        # pad to 64 bytes
        cmd = cmd + [0 for x in range(0, 64 - len(cmd))]
        self.ud7.write(self.ep['out'], cmd, 0, 1000)

    def set_backlight(self, brightness):
        self.send_command("set_backlight", [brightness])

    def ready_image_update(self):
        self.send_command("ready_image_update")

    def close(self):
        return
        #self.ud7.close()

def main():
    dev = ud7()
    # for i in range(0, 5):
    #     dev.send_status()
    #     time.sleep(0.010)
    dev.turn_on()
    dev.set_backlight(0xff)
    # for i in range(0, 20):
    #     dev.send_frame(0xf8)
    #     dev.send_frame(0x80)
    #     dev.send_status()
    # time.sleep(1.0)
    print dev.check_button_state()
    
    # dev.black_out()
    # for i in range(0, 255):
    #     dev.set_backlight(i)

    # dev.send_command(dev.form_command("unknown_3"))
    # dev.send_frame(0xf0)
    # dev.send_status()
    # time.sleep(.5)
    # dev.black_out()
    # dev.send_frame(0x0f)
    # dev.send_status()
    # time.sleep(.5)
    # for j in range(255, 0, -1):
    #     dev.set_backlight(j)

    # dev.turn_off()
    dev.close()    

    return 0

if __name__ == '__main__':

    sys.exit(main())