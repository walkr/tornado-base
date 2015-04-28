# This module contains WebSocket handlers

import json
import logging

import tornado.web
import tornado.websocket

from app.lib.torhelp.handler import *
from app.lib.torhelp.session import *

from app.src.pipelines import *
from app.src import models


class ChatHandler(tornado.websocket.WebSocketHandler):
    """ WebSocket handler """

    channels = {}
    events = {
        'server-sent': ('pong', 'new_msg'),
        'client-sent': ('ping', 'new_msg')
    }

    # ===================== OPEN / CLOSE / MESSAGE  ======================

    def open(self, channel_name):
        logging.debug('* new user joined channel: {}'.format(channel_name))
        self.channel_name = channel_name.strip()
        channel = self.channels.get(
            self.channel_name, models.Channel(name=channel_name)
        )
        channel.subscribers.add(self)
        ChatHandler.channels[self.channel_name] = channel

    def on_close(self):
        logging.debug('* closing connection')
        try:
            self.channels[self.channel_name].subscribers.remove(self)
        except KeyError:
            pass

    def on_message(self, payload):
        logging.debug('* new payload received: {}'.format(payload))
        payload = json.loads(payload)
        event, msg = payload['event'], payload['msg']
        assert event in self.events['client-sent']
        self.trigger(event, self.channel_name, msg)

    # ===================== EVENT FUNCTIONS ===========================

    @classmethod
    def trigger(cls, event, channel_name, msg):
        getattr(cls, 'on_' + event)(channel_name, msg)

    @classmethod
    def on_ping(cls, channel_name, msg):
        """ On ping check for updates on the streamlet channel """
        cls.send_to_all(channel_name, 'pong', msg)

    @classmethod
    def on_new_msg(cls, channel_name, msg):
        """ Broadcast the message to all in the room """
        cls.send_to_all(channel_name, 'new_msg', msg)

    # ==================================================================

    @classmethod
    def send_to_all(cls, channel_name, event, msg):
        """ Broadcast a payload to all subscribers """

        payload = {'event': event, 'msg': msg}

        for subscriber in cls.channels[channel_name].subscribers:
            try:
                logging.error('* write payload {}'.format(payload))
                subscriber.write_message(json.dumps(payload))
            except:
                logging.error("Error writing payload", exc_info=True)
