#  Hint:  You may not need all of these.  Remove the unused functions.
from hashtables import (HashTable,
                        hash_table_insert,
                        hash_table_remove,
                        hash_table_retrieve,
                        hash_table_resize)


class Ticket:
    def __init__(self, source, destination):
        self.source = source
        self.destination = destination


def reconstruct_trip(tickets, length):
    hashtable = HashTable(length)
    route = [None] * length

    """
    YOUR CODE HERE
    """
    # Insert the tickets into the table
    for ticket in tickets:
        hash_table_insert(hashtable, ticket.source, ticket.destination)
    # Set the first ticket in the route to the ticket with key "NONE"
    route[0] = hash_table_retrieve(hashtable, 'NONE')
    # For each following ticket, retrieve them in order referencing the previous ticket's value
    for idx in range(1, length):
        route[idx] = hash_table_retrieve(hashtable, route[idx - 1])

    return route
