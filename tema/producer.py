"""
This module represents the Producer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Thread
from time import sleep


class Producer(Thread):
    """
    Class that represents a producer.
    """

    def __init__(self, products, marketplace, republish_wait_time, **kwargs):
        """
        Constructor.

        @type products: List()
        @param products: a list of products that the producer will produce

        @type marketplace: Marketplace
        @param marketplace: a reference to the marketplace

        @type republish_wait_time: Time
        @param republish_wait_time: the number of seconds that a producer must
        wait until the marketplace becomes available

        @type kwargs:
        @param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self, **kwargs)

        self.products = products
        self.marketplace = marketplace
        self.republish_wait_time = republish_wait_time

        self.id = self.marketplace.register_producer()

    def run(self):
        while True:
            # Iterate through the products
            for product in self.products:
                p = product[0]
                quantity = product[1]
                wait_time = product[2]
                # Publish each product for quantity times
                for i in range(quantity):
                    accepted = False

                    # If the product can be published, wait republish_wait_time seconds and try again
                    while not accepted:
                        accepted = self.marketplace.publish(self.id, p)
                        if not accepted:
                            sleep(self.republish_wait_time)

                    # After publishing, wait wait_time seconds
                    sleep(wait_time)
