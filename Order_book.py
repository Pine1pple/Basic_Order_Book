class Order_Book:

    def __init__(self):
        self.asks = []
        self.bids = []

    def place_order(self, order_type, direction, price, quantity=None):
        if order_type not in ['market', 'limit', 'stop']:
            print("Invalid order type. Use 'market', 'limit', or 'stop'.")
            return
        
        if direction not in ['buy', 'sell']:
            print("Invalid order direction. Use 'buy' or 'sell'.")
            return
        
        order = {'order_type': order_type, 'direction': direction, 'price': price, 'quantity': quantity}

        if order_type == 'market':
            # For market orders, the price parameter is not needed
            if price is not None:
                print("Price parameter is not required for market orders. Ignoring price parameter.")
            # Proceed with placing the order

        elif order_type == 'limit':
            # For limit orders, price parameter is required
            if price is None:
                print("Price parameter is required for limit orders.")
                return
            # Proceed with placing the order

        elif order_type == 'stop':
            # For stop orders, price parameter is required
            if price is None:
                print("Price parameter is required for stop orders.")
                return
            # Proceed with placing the order

        # Place the order
        if direction == 'buy':
            self.bids.append(order)
        elif direction == 'sell':
            self.asks.append(order)

    def cancel_order(self, order_type, direction, price):
        if order_type not in ['market', 'limit', 'stop']:
            print("Invalid order type. Use 'market', 'limit', or 'stop'.")
            return
        
        if direction not in ['buy', 'sell']:
            print("Invalid order direction. Use 'buy' or 'sell'.")
            return

        # Find and remove the specified order
        if direction == 'buy':
            orders = self.bids
        elif direction == 'sell':
            orders = self.asks

        if order_type == 'market':
            # For market orders, ignore the price parameter
            orders[:] = [order for order in orders if order['order_type'] != 'market']

        elif order_type == 'limit':
            # For limit orders, remove orders with the specified price
            orders[:] = [order for order in orders if order['order_type'] != 'limit' or (order['order_type'] == 'limit' and order['price'] != price)]

        elif order_type == 'stop':
            # For stop orders, remove orders with the specified price
            orders[:] = [order for order in orders if order['order_type'] != 'stop' or (order['order_type'] == 'stop' and order['price'] != price)]


    def modify_order(self, order_type, direction, old_price, new_price, new_quantity):
        if order_type not in ['market', 'limit', 'stop']:
            print("Invalid order type. Use 'market', 'limit', or 'stop'.")
            return
        
        if direction not in ['buy', 'sell']:
            print("Invalid order direction. Use 'buy' or 'sell'.")
            return

        # Find and modify the specified order
        if direction == 'buy':
            orders = self.bids
        elif direction == 'sell':
            orders = self.asks

        if order_type == 'market':
            # For market orders, ignore the old and new price parameters
            orders[:] = [order for order in orders if order['order_type'] != 'market']

        elif order_type == 'limit':
            # For limit orders, modify orders with the specified old price
            for order in orders:
                if order['order_type'] == 'limit' and order['price'] == old_price:
                    order['price'] = new_price
                    order['quantity'] = new_quantity

        elif order_type == 'stop':
            # For stop orders, modify orders with the specified old price
            for order in orders:
                if order['order_type'] == 'stop' and order['price'] == old_price:
                    order['price'] = new_price
                    order['quantity'] = new_quantity

    def match_orders(self):
        for bid in self.bids:
            for ask in self.asks:  # Remove sorting and comparison from here
                if bid['order_type'] == 'market' and ask['order_type'] == 'market':
                    # Market order execution
                    matched_quantity = min(ask['quantity'], bid['quantity'])
                    print(f"Matched {matched_quantity} units at price {ask['price']}")

                    # Update the quantities
                    ask['quantity'] -= matched_quantity
                    bid['quantity'] -= matched_quantity

                    # Remove orders with zero quantity
                    if ask['quantity'] == 0:
                        self.asks.remove(ask)
                    if bid['quantity'] == 0:
                        self.bids.remove(bid)

                    # Check if there is more quantity to match
                    if ask['quantity'] > 0:
                        continue
                    else:
                        break

                elif bid['order_type'] == 'limit' and ask['order_type'] == 'limit':
                    # Limit order execution
                    if ask['price'] <= bid['price']:
                        matched_quantity = min(ask['quantity'], bid['quantity'])
                        print(f"Matched {matched_quantity} units at price {ask['price']}")

                        # Update the quantities
                        ask['quantity'] -= matched_quantity
                        bid['quantity'] -= matched_quantity

                        # Remove orders with zero quantity
                        if ask['quantity'] == 0:
                            self.asks.remove(ask)
                        if bid['quantity'] == 0:
                            self.bids.remove(bid)

                        # Check if there is more quantity to match
                        if ask['quantity'] > 0:
                            continue
                        else:
                            break

                elif bid['order_type'] == 'stop' and ask['order_type'] == 'stop':
                    # Stop order execution
                    if ask['price'] >= bid['price']:
                        matched_quantity = min(ask['quantity'], bid['quantity'])
                        print(f"Matched {matched_quantity} units at price {ask['price']}")

                        # Update the quantities
                        ask['quantity'] -= matched_quantity
                        bid['quantity'] -= matched_quantity

                        # Remove orders with zero quantity
                        if ask['quantity'] == 0:
                            self.asks.remove(ask)
                        if bid['quantity'] == 0:
                            self.bids.remove(bid)

                        # Check if there is more quantity to match
                        if ask['quantity'] > 0:
                            continue
                        else:
                            break

    def display_order_book(self):
        print("Bids:")
        for bid in self.bids:
            print (f"Price: {bid['price']}, Quantity: {bid['quantity']}")
        print ("\nAsks:")
        for ask in self.asks:
            print (f"Price: {ask['price']}, Quantity: {ask['quantity']}")
