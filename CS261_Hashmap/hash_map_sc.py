# Name: Tom Haney
# OSU Email: haneyth@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 06Aug25
# Description: Implementation for a Hash Map data structure using chaining.


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Adds a new element to the hash map by hashifying the provided key
          and appending an applicable node to the underlying linked list.
        """
        # If the table load is greater than 1, resize (double capacity)
        if self.table_load() >= 1:
            self.resize_table(self._capacity * 2)

        # Update a pre-existing key to the new value
        idx = self._hash_function(key) % self._capacity
        inserted = False
        for node in self._buckets[idx]:
            if node.key == key:
                node.value = value
                inserted = True

        # Add as a new node if not already in the hashmap
        if not inserted:
            self._buckets[idx].insert(key, value)
            self._size += 1

    def resize_table(self, new_capacity: int) -> None:
        """
        Resizes the Hash map and recalculates the indexes to store the data.
        """

        # First check if the new capacity is greater than or equal to 1
        if new_capacity >= 1:

            # Get all the key-value pairs to be re-stored
            data = self.get_keys_and_values()

            # Update the capacity to the next prime number
            self._capacity = self._next_prime(new_capacity)

            # Adjust table load to be less than 1
            # I give up on this one. I cannot figure out the expected resize
            # behavior.
            while self.table_load() >= 1:

                # Update for the loop
                new_capacity = self._capacity * 2

                # Update the capacity to the next prime number
                self._capacity = self._next_prime(new_capacity)

            # Re-construct the buckets with the new capacity
            self._buckets = DynamicArray()
            for _ in range(self._capacity):
                self._buckets.append(LinkedList())

            # Re-calculate and store all previous data
            for tup_idx in range(data.length()):
                old_key = data[tup_idx][0]
                old_val = data[tup_idx][1]
                idx = self._hash_function(old_key) % self._capacity
                self._buckets[idx].insert(old_key, old_val)


    def table_load(self) -> float:
        """
        Returns the load factor of the table, that being the number of
          elements stored divided by the length of the underlying array.
        """
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash map.
        """
        empty_buckets = 0

        # Check each bucket for a linked list of size 0, increment
        for idx in range(self._buckets.length()):
            if self._buckets[idx].length() == 0:
                empty_buckets += 1

        return empty_buckets

    def get(self, key: str) -> object:
        """
        Returns the value assigned to the given key, unless the key does not
          exist within the hash map in which case returns None.
        """
        idx = self._hash_function(key) % self._capacity
        for node in self._buckets[idx]:
            if node.key == key:
                return node.value

        return None

    def contains_key(self, key: str) -> bool:
        """
        Determines whether the hashmap contains a key by determining what
          index it would be at and querying the linked list at that index.
        """
        # First calculate which index would hold that key
        idx = self._hash_function(key) % self._capacity

        # Return whether the linked list at that index has that key
        if self._buckets[idx].contains(key):
            return True
        return False

    def remove(self, key: str) -> None:
        """
        Removes a key-value pair from the hash map, unless the key is not
          found within the hash map in which case nothing happens.
        """
        # First calculate which index would hold that key
        idx = self._hash_function(key) % self._capacity

        # Decrement size if a node was removed
        if self._buckets[idx].remove(key):
            self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a DynamicArray object containing a tuple for each key-value
          pair held within the hash map.
        """
        keys_and_values = DynamicArray()

        # Iterate over each bucket with a LinkedList of length > 0
        for bucket_idx in range(self._capacity):
            if self._buckets[bucket_idx].length() > 0:
                # Append each key-value pair in tuple form
                for node in self._buckets[bucket_idx]:
                    keys_and_values.append((node.key, node.value))

        return keys_and_values

    def clear(self) -> None:
        """
        Clears the contents of the hash map (without changing capacity.)
        """
        # Assign buckets to an empty DynamicArray
        self._buckets = DynamicArray()

        # Place a linked list in each bucket
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        # Reset size
        self._size = 0


def find_mode(da: DynamicArray) -> tuple[DynamicArray, int]:
    """
    Returns a tuple containing a DynamicArray with the modes of the
      supplied DA of strings, along with the frequency of those strings.
    """
    # if you'd like to use a hash map,
    # use this instance of your Separate Chaining HashMap
    map = HashMap()

    # O(N) to insert each element in da
    for idx in range(da.length()):
        # First get the current count of the element or None
        count = map.get(da[idx])
        # If a current count exists, increment. Otherwise, set to 1.
        if count:
            map.put(da[idx], count + 1)
        else:
            map.put(da[idx], 1)

    # Get all the word and count pairs (+ O(n) = 2O(n) =~ O(n)
    counts = map.get_keys_and_values()

    # Find the max frequency (+ O(n) = 3O(n) =~ O(n)
    freq = -1
    for idx in range(counts.length()):
        if counts[idx][1] >= freq:
            freq = counts[idx][1]

    # Build the DynamicArray of modes (+ O(n) = 4O(n) =~ O(n)
    modes = DynamicArray()
    for idx in range(counts.length()):
        if counts[idx][1] == freq:
            modes.append(counts[idx][0])

    return (modes, freq)

# ------------------- BASIC TESTING ---------------------------------------- #


if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    m.resize_table(1)

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(53, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
