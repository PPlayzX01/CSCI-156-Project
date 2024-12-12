import random
import time

class Item:
    def __init__(self, name, units, price):
        self.name = name
        self.units = units
        self.price = price
        self.highest_bid = 0
        self.highest_bidder = None
        self.bidders = []

    def place_bid(self, bid, bidder):
        if bid > self.highest_bid:
            self.highest_bid = bid
            self.highest_bidder = bidder
            self.bidders.append(bidder)

    def update_units(self):
        self.units -= 1

class Server:
    def __init__(self, items):
        self.items = items

    def broadcast_bidding(self):
        for item in self.items:
            # Broadcast item details to clients
            pass

    def start_bidding(self):
        while any(item.units > 0 for item in self.items):
            for item in self.items:
                if item.units > 0:
                    self.broadcast_bidding()
                    self.bidding_round(item)

    def bidding_round(self, item):
        deadline = time.time() + 60  # Set 1-minute deadline
        # Run bidding for 1 minute
        while time.time() < deadline:
            # Let each client bid on the item during this round
            for client in clients:
                client.receive_bidding_info(item)
            time.sleep(1)  # Simulate time passing, so clients don't flood bids too fast

        # After deadline, declare winner and reduce available units
        if item.highest_bidder:
            item.update_units()
            print(f"{item.highest_bidder} wins {item.name} at price {item.highest_bid}")
        else:
            print(f"No bids for {item.name}")

class Client:
    def __init__(self, name, max_bids):
        self.name = name
        self.max_bids = max_bids
        self.won_items = {}

    def receive_bidding_info(self, item):
        if random.random() < 0.3:  # 30% chance not to bid
            return

        # Ensure bid price is above the item price and below client's max bid
        # Check if client's max bid is higher than the item price
        if self.max_bids[item.name] > item.price:
            bid_price = random.randint(item.price + 1, self.max_bids[item.name])
            print(f"{self.name} bids {bid_price} on {item.name}")
            item.place_bid(bid_price, self.name)
        else:
            print(f"{self.name} cannot bid on {item.name} as their maximum bid is lower than the item price.")

    def bid_on_items(self, items):
        for item in items:
            self.receive_bidding_info(item)

    def display_results(self):
        print(f"{self.name} has won:")
        for item, qty in self.won_items.items():
            print(f"  {item}: {qty}")

# Initialize the items and clients
items = [Item("Item1", 40, 121), Item("Item2", 50, 656)]
server = Server(items)

clients = [
    Client("Client1", {"Item1": 150, "Item2": 700}),
    Client("Client2", {"Item1": 130, "Item2": 600}),
    Client("Client3", {"Item1": 180, "Item2": 800}),
    Client("Client4", {"Item1": 120, "Item2": 900}),
    # Add more clients here
]

# Simulate server-client interaction
server.start_bidding()
