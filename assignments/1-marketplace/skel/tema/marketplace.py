"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
"""
import random
import string
from threading import Lock

ALPHABET = string.ascii_lowercase + string.digits


class Marketplace:
    """
    Class that represents the Marketplace. It's the central part of the implementation.
    The producers and consumers use its methods concurrently.
    """

    def __init__(self, queue_size_per_producer):
        """
        Constructor

        :type queue_size_per_producer: Int
        :param queue_size_per_producer: the maximum size of a queue associated with each producer
        """
        self.queue_size_per_producer = queue_size_per_producer

        self.producer_queues = {}
        self.carts = {}

        self.products = []
        self.products_lock = Lock()

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        id = self.generate_id(self.producer_queues.keys())
        self.producer_queues[id] = []
        return id

    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.
        """

        count = len(self.producer_queues[producer_id])
        if count >= self.queue_size_per_producer:
            return False

        self.producer_queues[producer_id].append(product)
        return True

    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """
        cart_ids = [f[0] for f in self.carts.items()]
        id = int(self.generate_id(cart_ids, only_ints=True))
        self.carts[id] = []
        return id

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """

        for id in self.producer_queues.keys():
            if product in self.producer_queues[id]:
                self.carts[cart_id].append((product, id))
                self.producer_queues[id].remove(product)
                return True
        return False

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """
        for (prod, id) in self.carts[cart_id]:
            if prod == product:
                self.carts[cart_id].remove((product, id))
                self.producer_queues[id].append(product)
                return

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        final_cart = [f[0] for f in self.carts[cart_id]]
        self.carts[cart_id] = []
        return final_cart

    def generate_id(self, existing_ids, only_ints=False):
        """
        Generate 8 character string representing a unique id.
        Used to generate ids for producers and consumers.

        :type existing_ids: List
        :param existing_ids: List of existing ids
        """
        characters = ALPHABET if only_ints is False else string.digits
        new_id = ''.join(random.choices(characters, k=8))
        if new_id in existing_ids:
            return self.generate_id(existing_ids)
        else:
            return new_id
