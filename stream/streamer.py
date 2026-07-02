"""
streamer.py

Author: Chad Wangolo

Description
-----------
This module is responsible for connecting to the Finnhub WebSocket API,
subscribing to one or more stock symbols, receiving real-time market data,
and forwarding that data to the rest of the monitoring pipeline.

Architecture
------------
Finnhub WebSocket
        │
        ▼
 FinnhubStreamer
        │
        ▼
  candle_queue (asyncio.Queue)
        │
        ▼
 Feature Worker
        │
        ▼
 ML Worker
        │
        ▼
 Alert Worker

This module acts as the PRODUCER in a Producer-Consumer architecture.

Why a Queue?
------------
Instead of allowing every worker to communicate directly with Finnhub,
the streamer is the only component responsible for network communication.

Each incoming trade is placed into an asyncio.Queue.

Workers consume trades independently without slowing down the WebSocket.

Advantages
----------
✓ Modular
✓ Easy to maintain
✓ Fault tolerant
✓ Scalable
✓ Industry standard
"""

import os
import json
import asyncio
import threading

import websocket
from dotenv import load_dotenv

# -------------------------------------------------------
# Load environment variables from .env
# -------------------------------------------------------

load_dotenv()

FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")

# -------------------------------------------------------
# Shared Queue
#
# Every trade received from Finnhub is placed here.
#
# Feature Worker removes items from this queue.
#
# asyncio.Queue is thread-safe for async applications.
# -------------------------------------------------------

candle_queue = asyncio.Queue()


class FinnhubStreamer:
    """
    Handles communication with the Finnhub WebSocket server.

    Responsibilities
    ----------------
    • Connect to Finnhub

    • Authenticate

    • Subscribe to stock symbols

    • Receive live trade data

    • Push trades into candle_queue

    This class does NOT compute indicators.

    This class does NOT make predictions.

    This class only receives market data.
    """

    def __init__(self):

        self.ws = None

        # asyncio event loop reference
        # Needed because websocket-client runs
        # in another thread.
        self.loop = asyncio.get_event_loop()

    # --------------------------------------------------

    def on_open(self, ws):
        """
        Called automatically once the WebSocket
        successfully connects.

        Subscribe to each stock symbol here.
        """

        print("Connected to Finnhub.")

        symbols = [
            "AAPL",
            "MSFT",
            "GOOGL",
            "NVDA",
            "TSLA"
        ]

        for symbol in symbols:

            message = {
                "type": "subscribe",
                "symbol": symbol
            }

            ws.send(json.dumps(message))

            print(f"Subscribed to {symbol}")

    # --------------------------------------------------

    def on_message(self, ws, message):
        """
        Called every time Finnhub sends market data.

        Example message:

        {
            "data":[
                {
                    "s":"AAPL",
                    "p":213.42,
                    "v":100,
                    "t":17123456789
                }
            ],
            "type":"trade"
        }
        """

        message = json.loads(message)

        # Ignore heartbeat messages
        if message.get("type") != "trade":
            return

        trades = message.get("data", [])

        for trade in trades:

            symbol = trade["s"]

            candle = {

                # Finnhub provides trade price.
                # For now we use it as OHLC.

                "open": trade["p"],
                "high": trade["p"],
                "low": trade["p"],
                "close": trade["p"],

                "volume": trade["v"],

                "timestamp": trade["t"]

            }

            # ------------------------------------------------
            # Since websocket-client runs in another thread,
            # use run_coroutine_threadsafe()
            #
            # This safely inserts data into the asyncio Queue.
            # ------------------------------------------------

            asyncio.run_coroutine_threadsafe(
                candle_queue.put((symbol, candle)),
                self.loop
            )

            print(f"Trade received: {symbol}")

    # --------------------------------------------------

    def on_error(self, ws, error):
        """
        Called automatically whenever the WebSocket
        encounters an error.
        """

        print("WebSocket Error:")
        print(error)

    # --------------------------------------------------

    def on_close(self, ws, close_status_code, close_msg):
        """
        Called whenever the WebSocket disconnects.
        """

        print("Disconnected from Finnhub.")

    # --------------------------------------------------

    def connect(self):
        """
        Creates the WebSocket connection.

        websocket.WebSocketApp handles:

        • reconnect callbacks

        • receiving messages

        • opening

        • closing

        We run it inside a daemon thread so the
        rest of the application can continue running.
        """

        url = f"wss://ws.finnhub.io?token={FINNHUB_API_KEY}"

        self.ws = websocket.WebSocketApp(

            url,

            on_open=self.on_open,

            on_message=self.on_message,

            on_error=self.on_error,

            on_close=self.on_close

        )

        threading.Thread(

            target=self.ws.run_forever,

            daemon=True

        ).start()

    # --------------------------------------------------

    def close(self):
        """
        Gracefully closes the WebSocket connection.
        """

        if self.ws:

            self.ws.close()


# -------------------------------------------------------
# Async wrapper
#
# main.py launches this coroutine along with
# the feature worker, ML worker, and alert worker.
#
# This coroutine simply keeps the streamer alive.
# -------------------------------------------------------

async def finnhub_streamer():

    streamer = FinnhubStreamer()

    streamer.connect()

    while True:

        await asyncio.sleep(1)