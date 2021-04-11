import os

from rgbmatrix import graphics
from cryptofeed.rest.coinbase import Coinbase

from samplebase import SampleBase


FONTS_PATH = r'/home/pi/rpi-rgb-led-matrix/fonts'
# Must be a Coinbase trading pair
ALTCOINS = [
    'ADA-USD',
    'LINK-USD',
    'UNI-USD',
    'FIL-USD',
    'YFI-USD',
    'MANA-USDC',
    'ENJ-USD',
    'AAVE-USD',
    'COMP-USD',
    'CRV-USD',
    '1INCH-USD',
    'LTC-USD',
    'XLM-USD',
    'BAL-USD',
]


class CryptoTickerDisplay(SampleBase):

    def __init__(self, *args, **kwargs):
        super(CryptoTickerDisplay, self).__init__(*args, **kwargs)

    def run(self):
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        font = graphics.Font()
        font.LoadFont(os.path.join(FONTS_PATH, "5x8.bdf"))
        green_color = graphics.Color(0, 128, 0)
        red_color = graphics.Color(255, 0, 0)
        btc_price_old = 0
        eth_price_old = 0
        altcoin_i, altcoin_j = 0, 1
        altcoin_prices_old = {}
        for altcoin in ALTCOINS:
            altcoin_prices_old[altcoin] = 0

        coinbase = Coinbase()

        while True:
            offscreen_canvas.Clear()

            # Handle core coins
            btc_price = coinbase.ticker('BTC-USD')['bid']
            eth_price = coinbase.ticker('ETH-USD')['bid']
            btc_color = green_color if btc_price > btc_price_old else red_color
            eth_color = green_color if eth_price > eth_price_old else red_color
            btc_price_old = btc_price
            eth_price_old = eth_price

            # Handle alt coins
            altcoin_i_price = round(coinbase.ticker(ALTCOINS[altcoin_i])['bid'], 2)
            altcoin_j_price = round(coinbase.ticker(ALTCOINS[altcoin_j])['bid'], 2)
            altcoin_i_color = green_color if altcoin_i_price > altcoin_prices_old[ALTCOINS[altcoin_i]] else red_color
            altcoin_j_color = green_color if altcoin_j_price > altcoin_prices_old[ALTCOINS[altcoin_j]] else red_color
            altcoin_prices_old[ALTCOINS[altcoin_i]] = altcoin_i_price
            altcoin_prices_old[ALTCOINS[altcoin_j]] = altcoin_j_price

            graphics.DrawText(offscreen_canvas, font, 66, 12, btc_color, f"BTC:{btc_price}")
            graphics.DrawText(offscreen_canvas, font, 66, 24, eth_color, f"ETH:{eth_price}")
            graphics.DrawText(offscreen_canvas, font, 2, 12, altcoin_i_color, f"{ALTCOINS[altcoin_i].split('-')[0]}:{altcoin_i_price}")
            graphics.DrawText(offscreen_canvas, font, 2, 24, altcoin_j_color, f"{ALTCOINS[altcoin_j].split('-')[0]}:{altcoin_j_price}")
            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)
            altcoin_i = (altcoin_i + 2) % len(ALTCOINS)
            altcoin_j = (altcoin_j + 2) % len(ALTCOINS)


if __name__ == "__main__":
    crypto_ticker_display = CryptoTickerDisplay()
    crypto_ticker_display.process()
