"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

# Dataclass is imported only for unittesting
from product import Tea

import unittest
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


class TestMarketplace(unittest.TestCase):
    """
    Unittest for the Marketplace class
    """

    def setUp(self):
        """
        Set up a basic marketplace and a product
        """
        self.marketplace = Marketplace(1)
        self.test_product = Tea(name="Linden", type="Herbal", price=5)

    def test_publish(self):
        """
        Test publish method
        """

        # Register a new producer
        producer_id = self.marketplace.register_producer()

        # check if the new producer can publish a product
        assert self.marketplace.publish(producer_id, self.test_product) is True

        # check if the product is in the marketplace
        assert self.test_product in self.marketplace.producer_queues[producer_id]

        # Make sure producer can't publish another product once it has reached its queue size
        assert self.marketplace.publish(
            producer_id, self.test_product) is False

    def test_new_cart(self):
        """
        Test new_cart method
        """
        # Create a new cart
        cart_id = self.marketplace.new_cart()

        # Check if the cart is in the marketplace
        assert cart_id in self.marketplace.carts.keys()

    def test_add_to_cart(self):
        """
        Test add_to_cart method
        """
        # Register a new producer
        producer_id = self.marketplace.register_producer()

        # Create a new cart
        cart_id = self.marketplace.new_cart()

        # Publish a product to the marketplace
        self.marketplace.publish(producer_id, self.test_product)

        # Check if the product can be added to the cart
        assert self.marketplace.add_to_cart(cart_id, self.test_product) is True

        # Check if the product is in the cart
        assert (self.test_product,
                producer_id) in self.marketplace.carts[cart_id]

        # Make sure the product can't be added to the cart again since it doesn't exist in the marketplace anymore
        assert self.marketplace.add_to_cart(
            cart_id, self.test_product) is False

    def test_remove_from_cart(self):
        """
        Test remove_from_cart method
        """
        # Register a new producer
        producer_id = self.marketplace.register_producer()

        # Create a new cart
        cart_id = self.marketplace.new_cart()

        # Publish a product to the marketplace
        self.marketplace.publish(producer_id, self.test_product)

        # Add the product to the cart
        self.marketplace.add_to_cart(cart_id, self.test_product)

        # Remove the product from the cart
        self.marketplace.remove_from_cart(cart_id, self.test_product)

        # Check and make sure the product is not in the cart
        assert (self.test_product,
                producer_id) not in self.marketplace.carts[cart_id]

        # Check if the product is back in the marketplace
        assert self.test_product in self.marketplace.producer_queues[producer_id]

    def test_place_order(self):
        """
        Test place_order method
        """
        # Register a new producer
        producer_id = self.marketplace.register_producer()

        # Create a new cart
        cart_id = self.marketplace.new_cart()

        # Publish a product to the marketplace
        self.marketplace.publish(producer_id, self.test_product)

        # Add the product to the cart
        self.marketplace.add_to_cart(cart_id, self.test_product)

        # Place the order and make sure there is a list with the product that was added to the cart
        assert self.marketplace.place_order(cart_id) == [self.test_product]

        # Check if the cart is empty
        assert self.marketplace.carts[cart_id] == []

    def test_generate_id(self):
        """
        Test generate_id method
        """
        # generate a new id
        new_id = self.marketplace.generate_id([])

        # check if the id is a string of 8 characters
        assert len(new_id) == 8
