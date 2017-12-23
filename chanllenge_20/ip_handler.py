import re
import os
from wechatpy.messages import TextMessage
from wechatpy import create_reply
from wechatpy.replies import TextReply
from qqwry import QQwry

class CommandHandler:
    command = ""

    def check_match(self, message):
        if not isinstance(message, TextMessage):
            return False
        if not message.content.strip().lower().startswith(self.command):
            return False
        return True

class IPLocationHandler(CommandHandler):
    command = "ip"
    def __init__(self):
        pass
    def handle(self, message):
        if not self.check_match(message):
            return 
        lookup_data = message.content.strip().split()
        if len(lookup_data) == 1 or len(lookup_data) > 2:
            return create_reply("invalid IP", message)
        ip = lookup_data[1]
        if not re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$',ip):
            return create_reply("IP invalid", message)
        q = QQwry()
        q.load_file('qqwry.dat')
        
        reply = q.lookup(ip)
        if reply is None:
            return None
        return create_reply(reply[0], message)
        