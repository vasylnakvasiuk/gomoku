class RedisCommandsMixin(object):

    def append(self, key, value, callback=None):
        """
        Append a value to a key

            :param key:
            :param value:

        Complexity
        ----------
        O(1). The amortized time complexity is O(1) assuming the appended
        value is small and the already present value is of any size, since the
        dynamic string library used by Redis will double the free space
        available on every reallocation.
        """
        args = ["APPEND"]
        args.append(key)
        args.append(value)
        self.send_message(args, callback)

    def auth(self, password, callback=None):
        """
        Authenticate to the server

            :param password:
        """
        args = ["AUTH"]
        args.append(password)
        self.send_message(args, callback)

    def bgrewriteaof(self, callback=None):
        """
        Asynchronously rewrite the append-only file
        """
        self.send_message(["BGREWRITEAOF"], callback)

    def bgsave(self, callback=None):
        """
        Asynchronously save the dataset to disk
        """
        self.send_message(["BGSAVE"], callback)

    def bitcount(self, key, start=None, end=None, callback=None):
        """
        Count set bits in a string

            :param key:
            :param start:
            :param end:

        Complexity
        ----------
        O(N)
        """
        args = ["BITCOUNT"]
        args.append(key)
        args.append(start)
        args.append(end)
        self.send_message(args, callback)

    def bitop(self, operation, destkey, keys, callback=None):
        """
        Perform bitwise operations between strings

            :param operation:
            :param destkey:
            :param keys:
                string or list of strings

        Complexity
        ----------
        O(N)
        """
        args = ["BITOP"]
        args.append(operation)
        args.append(destkey)
        if isinstance(keys, str):
            args.append(keys)
        else:
            args.extend(keys)
        self.send_message(args, callback)

    def blpop(self, keys, timeout, callback=None):
        """
        Remove and get the first element in a list, or block until one is
        available

            :param keys:
                string or list of strings
            :param timeout:

        Complexity
        ----------
        O(1)
        """
        args = ["BLPOP"]
        if isinstance(keys, str):
            args.append(keys)
        else:
            args.extend(keys)
        args.append(timeout)
        self.send_message(args, callback)

    def brpop(self, keys, timeout, callback=None):
        """
        Remove and get the last element in a list, or block until one is
        available

            :param keys:
                string or list of strings
            :param timeout:

        Complexity
        ----------
        O(1)
        """
        args = ["BRPOP"]
        if isinstance(keys, str):
            args.append(keys)
        else:
            args.extend(keys)
        args.append(timeout)
        self.send_message(args, callback)

    def brpoplpush(self, source, destination, timeout, callback=None):
        """
        Pop a value from a list, push it to another list and return it; or
        block until one is available

            :param source:
            :param destination:
            :param timeout:

        Complexity
        ----------
        O(1)
        """
        args = ["BRPOPLPUSH"]
        args.append(source)
        args.append(destination)
        args.append(timeout)
        self.send_message(args, callback)

    def client_kill(self, ip_port, callback=None):
        """
        Kill the connection of a client

            :param ip_port:

        Complexity
        ----------
        O(N) where N is the number of client connections
        """
        args = ["CLIENT KILL"]
        args.append(ip_port)
        self.send_message(args, callback)

    def client_list(self, callback=None):
        """
        Get the list of client connections

        Complexity
        ----------
        O(N) where N is the number of client connections
        """
        self.send_message(["CLIENT LIST"], callback)

    def config_get(self, parameter, callback=None):
        """
        Get the value of a configuration parameter

            :param parameter:
        """
        args = ["CONFIG GET"]
        args.append(parameter)
        self.send_message(args, callback)

    def config_resetstat(self, callback=None):
        """
        Reset the stats returned by INFO

        Complexity
        ----------
        O(1)
        """
        self.send_message(["CONFIG RESETSTAT"], callback)

    def config_set(self, parameter, value, callback=None):
        """
        Set a configuration parameter to the given value

            :param parameter:
            :param value:
        """
        args = ["CONFIG SET"]
        args.append(parameter)
        args.append(value)
        self.send_message(args, callback)

    def dbsize(self, callback=None):
        """
        Return the number of keys in the selected database
        """
        self.send_message(["DBSIZE"], callback)

    def debug_object(self, key, callback=None):
        """
        Get debugging information about a key

            :param key:
        """
        args = ["DEBUG OBJECT"]
        args.append(key)
        self.send_message(args, callback)

    def debug_segfault(self, callback=None):
        """
        Make the server crash
        """
        self.send_message(["DEBUG SEGFAULT"], callback)

    def decr(self, key, callback=None):
        """
        Decrement the integer value of a key by one

            :param key:

        Complexity
        ----------
        O(1)
        """
        args = ["DECR"]
        args.append(key)
        self.send_message(args, callback)

    def decrby(self, key, decrement, callback=None):
        """
        Decrement the integer value of a key by the given number

            :param key:
            :param decrement:

        Complexity
        ----------
        O(1)
        """
        args = ["DECRBY"]
        args.append(key)
        args.append(decrement)
        self.send_message(args, callback)

    def delete(self, keys, callback=None):
        """
        Delete a key

            :param keys:
                string or list of strings

        Complexity
        ----------
        O(N) where N is the number of keys that will be removed. When a key to
        remove holds a value other than a string, the individual complexity
        for this key is O(M) where M is the number of elements in the list,
        set, sorted set or hash. Removing a single key that holds a string
        value is O(1).
        """
        args = ["DEL"]
        if isinstance(keys, str):
            args.append(keys)
        else:
            args.extend(keys)
        self.send_message(args, callback)

    def discard(self, callback=None):
        """
        Discard all commands issued after MULTI
        """
        self.send_message(["DISCARD"], callback)

    def dump(self, key, callback=None):
        """
        Return a serialized version of the value stored at the specified key.

            :param key:

        Complexity
        ----------
        O(1) to access the key and additional O(N*M) to serialized it, where N
        is the number of Redis objects composing the value and M their average
        size. For small string values the time complexity is thus O(1)+O(1*M)
        where M is small, so simply O(1).
        """
        args = ["DUMP"]
        args.append(key)
        self.send_message(args, callback)

    def echo(self, message, callback=None):
        """
        Echo the given string

            :param message:
        """
        args = ["ECHO"]
        args.append(message)
        self.send_message(args, callback)

    def eval(self, script, keys, args, callback=None):
        """
        Execute a Lua script server side

            :param script:
            :param keys:
                string or list of strings
            :param args:
                string or list of strings

        Complexity
        ----------
        Depends on the script that is executed.
        """
        args = ["EVAL"]
        args.append(script)
        args.append(len(keys))
        if isinstance(keys, str):
            args.append(keys)
        else:
            args.extend(keys)
        if isinstance(args, str):
            args.append(args)
        else:
            args.extend(args)
        self.send_message(args, callback)

    def evalsha(self, sha1, keys, args, callback=None):
        """
        Execute a Lua script server side

            :param sha1:
            :param keys:
                string or list of strings
            :param args:
                string or list of strings

        Complexity
        ----------
        Depends on the script that is executed.
        """
        args = ["EVALSHA"]
        args.append(sha1)
        args.append(len(keys))
        if isinstance(keys, str):
            args.append(keys)
        else:
            args.extend(keys)
        if isinstance(args, str):
            args.append(args)
        else:
            args.extend(args)
        self.send_message(args, callback)

    def execute(self, callback=None):
        """
        Execute all commands issued after MULTI
        """
        self.send_message(["EXEC"], callback)

    def exists(self, key, callback=None):
        """
        Determine if a key exists

            :param key:

        Complexity
        ----------
        O(1)
        """
        args = ["EXISTS"]
        args.append(key)
        self.send_message(args, callback)

    def expire(self, key, seconds, callback=None):
        """
        Set a key's time to live in seconds

            :param key:
            :param seconds:

        Complexity
        ----------
        O(1)
        """
        args = ["EXPIRE"]
        args.append(key)
        args.append(seconds)
        self.send_message(args, callback)

    def expireat(self, key, timestamp, callback=None):
        """
        Set the expiration for a key as a UNIX timestamp

            :param key:
            :param timestamp:

        Complexity
        ----------
        O(1)
        """
        args = ["EXPIREAT"]
        args.append(key)
        args.append(timestamp)
        self.send_message(args, callback)

    def flushall(self, callback=None):
        """
        Remove all keys from all databases
        """
        self.send_message(["FLUSHALL"], callback)

    def flushdb(self, callback=None):
        """
        Remove all keys from the current database
        """
        self.send_message(["FLUSHDB"], callback)

    def get(self, key, callback=None):
        """
        Get the value of a key

            :param key:

        Complexity
        ----------
        O(1)
        """
        args = ["GET"]
        args.append(key)
        self.send_message(args, callback)

    def getbit(self, key, offset, callback=None):
        """
        Returns the bit value at offset in the string value stored at key

            :param key:
            :param offset:

        Complexity
        ----------
        O(1)
        """
        args = ["GETBIT"]
        args.append(key)
        args.append(offset)
        self.send_message(args, callback)

    def getrange(self, key, start, end, callback=None):
        """
        Get a substring of the string stored at a key

            :param key:
            :param start:
            :param end:

        Complexity
        ----------
        O(N) where N is the length of the returned string. The complexity is
        ultimately determined by the returned length, but because creating a
        substring from an existing string is very cheap, it can be considered
        O(1) for small strings.
        """
        args = ["GETRANGE"]
        args.append(key)
        args.append(start)
        args.append(end)
        self.send_message(args, callback)

    def getset(self, key, value, callback=None):
        """
        Set the string value of a key and return its old value

            :param key:
            :param value:

        Complexity
        ----------
        O(1)
        """
        args = ["GETSET"]
        args.append(key)
        args.append(value)
        self.send_message(args, callback)

    def hdel(self, key, fields, callback=None):
        """
        Delete one or more hash fields

            :param key:
            :param fields:
                string or list of strings

        Complexity
        ----------
        O(N) where N is the number of fields to be removed.
        """
        args = ["HDEL"]
        args.append(key)
        if isinstance(fields, str):
            args.append(fields)
        else:
            args.extend(fields)
        self.send_message(args, callback)

    def hexists(self, key, field, callback=None):
        """
        Determine if a hash field exists

            :param key:
            :param field:

        Complexity
        ----------
        O(1)
        """
        args = ["HEXISTS"]
        args.append(key)
        args.append(field)
        self.send_message(args, callback)

    def hget(self, key, field, callback=None):
        """
        Get the value of a hash field

            :param key:
            :param field:

        Complexity
        ----------
        O(1)
        """
        args = ["HGET"]
        args.append(key)
        args.append(field)
        self.send_message(args, callback)

    def hgetall(self, key, callback=None):
        """
        Get all the fields and values in a hash

            :param key:

        Complexity
        ----------
        O(N) where N is the size of the hash.
        """
        args = ["HGETALL"]
        args.append(key)
        self.send_message(args, callback)

    def hincrby(self, key, field, increment, callback=None):
        """
        Increment the integer value of a hash field by the given number

            :param key:
            :param field:
            :param increment:

        Complexity
        ----------
        O(1)
        """
        args = ["HINCRBY"]
        args.append(key)
        args.append(field)
        args.append(increment)
        self.send_message(args, callback)

    def hincrbyfloat(self, key, field, increment, callback=None):
        """
        Increment the float value of a hash field by the given amount

            :param key:
            :param field:
            :param increment:

        Complexity
        ----------
        O(1)
        """
        args = ["HINCRBYFLOAT"]
        args.append(key)
        args.append(field)
        args.append(increment)
        self.send_message(args, callback)

    def hkeys(self, key, callback=None):
        """
        Get all the fields in a hash

            :param key:

        Complexity
        ----------
        O(N) where N is the size of the hash.
        """
        args = ["HKEYS"]
        args.append(key)
        self.send_message(args, callback)

    def hlen(self, key, callback=None):
        """
        Get the number of fields in a hash

            :param key:

        Complexity
        ----------
        O(1)
        """
        args = ["HLEN"]
        args.append(key)
        self.send_message(args, callback)

    def hmget(self, key, fields, callback=None):
        """
        Get the values of all the given hash fields

            :param key:
            :param fields:
                string or list of strings

        Complexity
        ----------
        O(N) where N is the number of fields being requested.
        """
        args = ["HMGET"]
        args.append(key)
        if isinstance(fields, str):
            args.append(fields)
        else:
            args.extend(fields)
        self.send_message(args, callback)

    def hmset(self, key, field_dict, callback=None):
        """
        Set multiple hash fields to multiple values

            :param key:
            :param member_score_dict:
                key value dictionary

        Complexity
        ----------
        O(N) where N is the number of fields being set.
        """
        args = ["HMSET"]
        args.append(key)
        for field, value in field_dict.items():
            args.append(field)
            args.append(value)
        self.send_message(args, callback)

    def hset(self, key, field, value, callback=None):
        """
        Set the string value of a hash field

            :param key:
            :param field:
            :param value:

        Complexity
        ----------
        O(1)
        """
        args = ["HSET"]
        args.append(key)
        args.append(field)
        args.append(value)
        self.send_message(args, callback)

    def hsetnx(self, key, field, value, callback=None):
        """
        Set the value of a hash field, only if the field does not exist

            :param key:
            :param field:
            :param value:

        Complexity
        ----------
        O(1)
        """
        args = ["HSETNX"]
        args.append(key)
        args.append(field)
        args.append(value)
        self.send_message(args, callback)

    def hvals(self, key, callback=None):
        """
        Get all the values in a hash

            :param key:

        Complexity
        ----------
        O(N) where N is the size of the hash.
        """
        args = ["HVALS"]
        args.append(key)
        self.send_message(args, callback)

    def incr(self, key, callback=None):
        """
        Increment the integer value of a key by one

            :param key:

        Complexity
        ----------
        O(1)
        """
        args = ["INCR"]
        args.append(key)
        self.send_message(args, callback)

    def incrby(self, key, increment, callback=None):
        """
        Increment the integer value of a key by the given amount

            :param key:
            :param increment:

        Complexity
        ----------
        O(1)
        """
        args = ["INCRBY"]
        args.append(key)
        args.append(increment)
        self.send_message(args, callback)

    def incrbyfloat(self, key, increment, callback=None):
        """
        Increment the float value of a key by the given amount

            :param key:
            :param increment:

        Complexity
        ----------
        O(1)
        """
        args = ["INCRBYFLOAT"]
        args.append(key)
        args.append(increment)
        self.send_message(args, callback)

    def info(self, callback=None):
        """
        Get information and statistics about the server
        """
        self.send_message(["INFO"], callback)

    def keys(self, pattern, callback=None):
        """
        Find all keys matching the given pattern

            :param pattern:

        Complexity
        ----------
        O(N) with N being the number of keys in the database, under the
        assumption that the key names in the database and the given pattern
        have limited length.
        """
        args = ["KEYS"]
        args.append(pattern)
        self.send_message(args, callback)

    def lastsave(self, callback=None):
        """
        Get the UNIX time stamp of the last successful save to disk
        """
        self.send_message(["LASTSAVE"], callback)

    def lindex(self, key, index, callback=None):
        """
        Get an element from a list by its index

            :param key:
            :param index:

        Complexity
        ----------
        O(N) where N is the number of elements to traverse to get to the
        element at index. This makes asking for the first or the last element
        of the list O(1).
        """
        args = ["LINDEX"]
        args.append(key)
        args.append(index)
        self.send_message(args, callback)

    def linsert(self, key, where, pivot, value, callback=None):
        """
        Insert an element before or after another element in a list

            :param key:
            :param where:
            :param pivot:
            :param value:

        Complexity
        ----------
        O(N) where N is the number of elements to traverse before seeing the
        value pivot. This means that inserting somewhere on the left end on
        the list (head) can be considered O(1) and inserting somewhere on the
        right end (tail) is O(N).
        """
        args = ["LINSERT"]
        args.append(key)
        args.append(where)
        args.append(pivot)
        args.append(value)
        self.send_message(args, callback)

    def llen(self, key, callback=None):
        """
        Get the length of a list

            :param key:

        Complexity
        ----------
        O(1)
        """
        args = ["LLEN"]
        args.append(key)
        self.send_message(args, callback)

    def lpop(self, key, callback=None):
        """
        Remove and get the first element in a list

            :param key:

        Complexity
        ----------
        O(1)
        """
        args = ["LPOP"]
        args.append(key)
        self.send_message(args, callback)

    def lpush(self, key, values, callback=None):
        """
        Prepend one or multiple values to a list

            :param key:
            :param values:
                string or list of strings

        Complexity
        ----------
        O(1)
        """
        args = ["LPUSH"]
        args.append(key)
        if isinstance(values, str):
            args.append(values)
        else:
            args.extend(values)
        self.send_message(args, callback)

    def lpushx(self, key, value, callback=None):
        """
        Prepend a value to a list, only if the list exists

            :param key:
            :param value:

        Complexity
        ----------
        O(1)
        """
        args = ["LPUSHX"]
        args.append(key)
        args.append(value)
        self.send_message(args, callback)

    def lrange(self, key, start, stop, callback=None):
        """
        Get a range of elements from a list

            :param key:
            :param start:
            :param stop:

        Complexity
        ----------
        O(S+N) where S is the start offset and N is the number of elements in
        the specified range.
        """
        args = ["LRANGE"]
        args.append(key)
        args.append(start)
        args.append(stop)
        self.send_message(args, callback)

    def lrem(self, key, count, value, callback=None):
        """
        Remove elements from a list

            :param key:
            :param count:
            :param value:

        Complexity
        ----------
        O(N) where N is the length of the list.
        """
        args = ["LREM"]
        args.append(key)
        args.append(count)
        args.append(value)
        self.send_message(args, callback)

    def lset(self, key, index, value, callback=None):
        """
        Set the value of an element in a list by its index

            :param key:
            :param index:
            :param value:

        Complexity
        ----------
        O(N) where N is the length of the list. Setting either the first or
        the last element of the list is O(1).
        """
        args = ["LSET"]
        args.append(key)
        args.append(index)
        args.append(value)
        self.send_message(args, callback)

    def ltrim(self, key, start, stop, callback=None):
        """
        Trim a list to the specified range

            :param key:
            :param start:
            :param stop:

        Complexity
        ----------
        O(N) where N is the number of elements to be removed by the operation.
        """
        args = ["LTRIM"]
        args.append(key)
        args.append(start)
        args.append(stop)
        self.send_message(args, callback)

    def mget(self, keys, callback=None):
        """
        Get the values of all the given keys

            :param keys:
                string or list of strings

        Complexity
        ----------
        O(N) where N is the number of keys to retrieve.
        """
        args = ["MGET"]
        if isinstance(keys, str):
            args.append(keys)
        else:
            args.extend(keys)
        self.send_message(args, callback)

    def migrate(self, host, port, key, destination_db, timeout, callback=None):
        """
        Atomically transfer a key from a Redis instance to another one.

            :param host:
            :param port:
            :param key:
            :param destination_db:
            :param timeout:

        Complexity
        ----------
        This command actually executes a DUMP+DEL in the source instance, and
        a RESTORE in the target instance. See the pages of these commands for
        time complexity. Also an O(N) data transfer between the two instances
        is performed.
        """
        args = ["MIGRATE"]
        args.append(host)
        args.append(port)
        args.append(key)
        args.append(destination_db)
        args.append(timeout)
        self.send_message(args, callback)

    def monitor(self, callback=None):
        """
        Listen for all requests received by the server in real time
        """
        self.send_message(["MONITOR"], callback)

    def move(self, key, db, callback=None):
        """
        Move a key to another database

            :param key:
            :param db:

        Complexity
        ----------
        O(1)
        """
        args = ["MOVE"]
        args.append(key)
        args.append(db)
        self.send_message(args, callback)

    def mset(self, key_dict, callback=None):
        """
        Set multiple keys to multiple values

            :param member_score_dict:
                key value dictionary

        Complexity
        ----------
        O(N) where N is the number of keys to set.
        """
        args = ["MSET"]
        for key, value in key_dict.items():
            args.append(key)
            args.append(value)
        self.send_message(args, callback)

    def msetnx(self, key_dict, callback=None):
        """
        Set multiple keys to multiple values, only if none of the keys exist

            :param member_score_dict:
                key value dictionary

        Complexity
        ----------
        O(N) where N is the number of keys to set.
        """
        args = ["MSETNX"]
        for key, value in key_dict.items():
            args.append(key)
            args.append(value)
        self.send_message(args, callback)

    def multi(self, callback=None):
        """
        Mark the start of a transaction block
        """
        self.send_message(["MULTI"], callback)

    def object(self, subcommand, argumentss=[], callback=None):
        """
        Inspect the internals of Redis objects

            :param subcommand:
            :param argumentss:
                string or list of strings

        Complexity
        ----------
        O(1) for all the currently implemented subcommands.
        """
        args = ["OBJECT"]
        args.append(subcommand)
        if isinstance(argumentss, str):
            args.append(argumentss)
        else:
            args.extend(argumentss)
        self.send_message(args, callback)

    def persist(self, key, callback=None):
        """
        Remove the expiration from a key

            :param key:

        Complexity
        ----------
        O(1)
        """
        args = ["PERSIST"]
        args.append(key)
        self.send_message(args, callback)

    def pexpire(self, key, milliseconds, callback=None):
        """
        Set a key's time to live in milliseconds

            :param key:
            :param milliseconds:

        Complexity
        ----------
        O(1)
        """
        args = ["PEXPIRE"]
        args.append(key)
        args.append(milliseconds)
        self.send_message(args, callback)

    def pexpireat(self, key, milliseconds_timestamp, callback=None):
        """
        Set the expiration for a key as a UNIX timestamp specified in
        milliseconds

            :param key:
            :param milliseconds_timestamp:

        Complexity
        ----------
        O(1)
        """
        args = ["PEXPIREAT"]
        args.append(key)
        args.append(milliseconds_timestamp)
        self.send_message(args, callback)

    def ping(self, callback=None):
        """
        Ping the server
        """
        self.send_message(["PING"], callback)

    def psetex(self, key, milliseconds, value, callback=None):
        """
        Set the value and expiration in milliseconds of a key

            :param key:
            :param milliseconds:
            :param value:

        Complexity
        ----------
        O(1)
        """
        args = ["PSETEX"]
        args.append(key)
        args.append(milliseconds)
        args.append(value)
        self.send_message(args, callback)

    def psubscribe(self, patterns, callback=None):
        """
        Listen for messages published to channels matching the given patterns

            :param member_score_dict:
                string or list of strings

        Complexity
        ----------
        O(N) where N is the number of patterns the client is already
        subscribed to.
        """
        args = ["PSUBSCRIBE"]
        if isinstance(patterns, str):
            args.append(patterns)
        else:
            args.extend(patterns)
        self.send_message(args, callback)

    def pttl(self, key, callback=None):
        """
        Get the time to live for a key in milliseconds

            :param key:

        Complexity
        ----------
        O(1)
        """
        args = ["PTTL"]
        args.append(key)
        self.send_message(args, callback)

    def publish(self, channel, message, callback=None):
        """
        Post a message to a channel

            :param channel:
            :param message:

        Complexity
        ----------
        O(N+M) where N is the number of clients subscribed to the receiving
        channel and M is the total number of subscribed patterns (by any
        client).
        """
        args = ["PUBLISH"]
        args.append(channel)
        args.append(message)
        self.send_message(args, callback)

    def punsubscribe(self, patterns=[], callback=None):
        """
        Stop listening for messages posted to channels matching the given
        patterns

            :param patterns:
                string or list of strings

        Complexity
        ----------
        O(N+M) where N is the number of patterns the client is already
        subscribed and M is the number of total patterns subscribed in the
        system (by any client).
        """
        args = ["PUNSUBSCRIBE"]
        if isinstance(patterns, str):
            args.append(patterns)
        else:
            args.extend(patterns)
        self.send_message(args, callback)

    def quit(self, callback=None):
        """
        Close the connection
        """
        self.send_message(["QUIT"], callback)

    def randomkey(self, callback=None):
        """
        Return a random key from the keyspace

        Complexity
        ----------
        O(1)
        """
        self.send_message(["RANDOMKEY"], callback)

    def rename(self, key, newkey, callback=None):
        """
        Rename a key

            :param key:
            :param newkey:

        Complexity
        ----------
        O(1)
        """
        args = ["RENAME"]
        args.append(key)
        args.append(newkey)
        self.send_message(args, callback)

    def renamenx(self, key, newkey, callback=None):
        """
        Rename a key, only if the new key does not exist

            :param key:
            :param newkey:

        Complexity
        ----------
        O(1)
        """
        args = ["RENAMENX"]
        args.append(key)
        args.append(newkey)
        self.send_message(args, callback)

    def restore(self, key, ttl, serialized_value, callback=None):
        """
        Create a key using the provided serialized value, previously obtained
        using DUMP.

            :param key:
            :param ttl:
            :param serialized_value:

        Complexity
        ----------
        O(1) to create the new key and additional O(N*M) to recostruct the
        serialized value, where N is the number of Redis objects composing the
        value and M their average size. For small string values the time
        complexity is thus O(1)+O(1*M) where M is small, so simply O(1).
        However for sorted set values the complexity is O(N*M*log(N)) because
        inserting values into sorted sets is O(log(N)).
        """
        args = ["RESTORE"]
        args.append(key)
        args.append(ttl)
        args.append(serialized_value)
        self.send_message(args, callback)

    def rpop(self, key, callback=None):
        """
        Remove and get the last element in a list

            :param key:

        Complexity
        ----------
        O(1)
        """
        args = ["RPOP"]
        args.append(key)
        self.send_message(args, callback)

    def rpoplpush(self, source, destination, callback=None):
        """
        Remove the last element in a list, append it to another list and
        return it

            :param source:
            :param destination:

        Complexity
        ----------
        O(1)
        """
        args = ["RPOPLPUSH"]
        args.append(source)
        args.append(destination)
        self.send_message(args, callback)

    def rpush(self, key, values, callback=None):
        """
        Append one or multiple values to a list

            :param key:
            :param values:
                string or list of strings

        Complexity
        ----------
        O(1)
        """
        args = ["RPUSH"]
        args.append(key)
        if isinstance(values, str):
            args.append(values)
        else:
            args.extend(values)
        self.send_message(args, callback)

    def rpushx(self, key, value, callback=None):
        """
        Append a value to a list, only if the list exists

            :param key:
            :param value:

        Complexity
        ----------
        O(1)
        """
        args = ["RPUSHX"]
        args.append(key)
        args.append(value)
        self.send_message(args, callback)

    def sadd(self, key, members, callback=None):
        """
        Add one or more members to a set

            :param key:
            :param members:
                string or list of strings

        Complexity
        ----------
        O(N) where N is the number of members to be added.
        """
        args = ["SADD"]
        args.append(key)
        if isinstance(members, str):
            args.append(members)
        else:
            args.extend(members)
        self.send_message(args, callback)

    def save(self, callback=None):
        """
        Synchronously save the dataset to disk
        """
        self.send_message(["SAVE"], callback)

    def scard(self, key, callback=None):
        """
        Get the number of members in a set

            :param key:

        Complexity
        ----------
        O(1)
        """
        args = ["SCARD"]
        args.append(key)
        self.send_message(args, callback)

    def script_exists(self, scripts, callback=None):
        """
        Check existence of scripts in the script cache.

            :param scripts:
                string or list of strings

        Complexity
        ----------
        O(N) with N being the number of scripts to check (so checking a single
        script is an O(1) operation).
        """
        args = ["SCRIPT EXISTS"]
        if isinstance(scripts, str):
            args.append(scripts)
        else:
            args.extend(scripts)
        self.send_message(args, callback)

    def script_flush(self, callback=None):
        """
        Remove all the scripts from the script cache.

        Complexity
        ----------
        O(N) with N being the number of scripts in cache
        """
        self.send_message(["SCRIPT FLUSH"], callback)

    def script_kill(self, callback=None):
        """
        Kill the script currently in execution.

        Complexity
        ----------
        O(1)
        """
        self.send_message(["SCRIPT KILL"], callback)

    def script_load(self, script, callback=None):
        """
        Load the specified Lua script into the script cache.

            :param script:

        Complexity
        ----------
        O(N) with N being the length in bytes of the script body.
        """
        args = ["SCRIPT LOAD"]
        args.append(script)
        self.send_message(args, callback)

    def sdiff(self, keys, callback=None):
        """
        Subtract multiple sets

            :param keys:
                string or list of strings

        Complexity
        ----------
        O(N) where N is the total number of elements in all given sets.
        """
        args = ["SDIFF"]
        if isinstance(keys, str):
            args.append(keys)
        else:
            args.extend(keys)
        self.send_message(args, callback)

    def sdiffstore(self, destination, keys, callback=None):
        """
        Subtract multiple sets and store the resulting set in a key

            :param destination:
            :param keys:
                string or list of strings

        Complexity
        ----------
        O(N) where N is the total number of elements in all given sets.
        """
        args = ["SDIFFSTORE"]
        args.append(destination)
        if isinstance(keys, str):
            args.append(keys)
        else:
            args.extend(keys)
        self.send_message(args, callback)

    def select(self, index, callback=None):
        """
        Change the selected database for the current connection

            :param index:
        """
        args = ["SELECT"]
        args.append(index)
        self.send_message(args, callback)

    def set(self, key, value, callback=None):
        """
        Set the string value of a key

            :param key:
            :param value:

        Complexity
        ----------
        O(1)
        """
        args = ["SET"]
        args.append(key)
        args.append(value)
        self.send_message(args, callback)

    def setbit(self, key, offset, value, callback=None):
        """
        Sets or clears the bit at offset in the string value stored at key

            :param key:
            :param offset:
            :param value:

        Complexity
        ----------
        O(1)
        """
        args = ["SETBIT"]
        args.append(key)
        args.append(offset)
        args.append(value)
        self.send_message(args, callback)

    def setex(self, key, seconds, value, callback=None):
        """
        Set the value and expiration of a key

            :param key:
            :param seconds:
            :param value:

        Complexity
        ----------
        O(1)
        """
        args = ["SETEX"]
        args.append(key)
        args.append(seconds)
        args.append(value)
        self.send_message(args, callback)

    def setnx(self, key, value, callback=None):
        """
        Set the value of a key, only if the key does not exist

            :param key:
            :param value:

        Complexity
        ----------
        O(1)
        """
        args = ["SETNX"]
        args.append(key)
        args.append(value)
        self.send_message(args, callback)

    def setrange(self, key, offset, value, callback=None):
        """
        Overwrite part of a string at key starting at the specified offset

            :param key:
            :param offset:
            :param value:

        Complexity
        ----------
        O(1), not counting the time taken to copy the new string in place.
        Usually, this string is very small so the amortized complexity is
        O(1). Otherwise, complexity is O(M) with M being the length of the
        value argument.
        """
        args = ["SETRANGE"]
        args.append(key)
        args.append(offset)
        args.append(value)
        self.send_message(args, callback)

    def shutdown(self, nosave=False, save=False, callback=None):
        """
        Synchronously save the dataset to disk and then shut down the server

            :param nosave:
            :param save:
        """
        args = ["SHUTDOWN"]
        if nosave:
            args.append("NOSAVE")
        if save:
            args.append("SAVE")
        self.send_message(args, callback)

    def sinter(self, keys, callback=None):
        """
        Intersect multiple sets

            :param keys:
                string or list of strings

        Complexity
        ----------
        O(N*M) worst case where N is the cardinality of the smallest set and M
        is the number of sets.
        """
        args = ["SINTER"]
        if isinstance(keys, str):
            args.append(keys)
        else:
            args.extend(keys)
        self.send_message(args, callback)

    def sinterstore(self, destination, keys, callback=None):
        """
        Intersect multiple sets and store the resulting set in a key

            :param destination:
            :param keys:
                string or list of strings

        Complexity
        ----------
        O(N*M) worst case where N is the cardinality of the smallest set and M
        is the number of sets.
        """
        args = ["SINTERSTORE"]
        args.append(destination)
        if isinstance(keys, str):
            args.append(keys)
        else:
            args.extend(keys)
        self.send_message(args, callback)

    def sismember(self, key, member, callback=None):
        """
        Determine if a given value is a member of a set

            :param key:
            :param member:

        Complexity
        ----------
        O(1)
        """
        args = ["SISMEMBER"]
        args.append(key)
        args.append(member)
        self.send_message(args, callback)

    def slaveof(self, host, port, callback=None):
        """
        Make the server a slave of another instance, or promote it as master

            :param host:
            :param port:
        """
        args = ["SLAVEOF"]
        args.append(host)
        args.append(port)
        self.send_message(args, callback)

    def slowlog(self, subcommand, argument=None, callback=None):
        """
        Manages the Redis slow queries log

            :param subcommand:
            :param argument:
        """
        args = ["SLOWLOG"]
        args.append(subcommand)
        args.append(argument)
        self.send_message(args, callback)

    def smembers(self, key, callback=None):
        """
        Get all the members in a set

            :param key:

        Complexity
        ----------
        O(N) where N is the set cardinality.
        """
        args = ["SMEMBERS"]
        args.append(key)
        self.send_message(args, callback)

    def smove(self, source, destination, member, callback=None):
        """
        Move a member from one set to another

            :param source:
            :param destination:
            :param member:

        Complexity
        ----------
        O(1)
        """
        args = ["SMOVE"]
        args.append(source)
        args.append(destination)
        args.append(member)
        self.send_message(args, callback)

    def sort(self, key, by=None, limit=None, get=tuple(), order=None, sorting=False, store=None, callback=None):
        """
        Sort the elements in a list, set or sorted set

            :param key:
            :param by:
            :param limit:
            :param get:
            :param order:
            :param sorting:
            :param store:

        Complexity
        ----------
        O(N+M*log(M)) where N is the number of elements in the list or set to
        sort, and M the number of returned elements. When the elements are not
        sorted, complexity is currently O(N) as there is a copy step that will
        be avoided in next releases.
        """
        args = ["SORT"]
        args.append(key)
        if by:
            args.append("BY")
            args.append(by)
        if limit:
            args.append("LIMIT")
            offset, count = limit
            args.append(offset)
            args.append(count)
        for pattern in get:
            args.append("GET")
            args.append(pattern)
        args.append(order)
        if sorting:
            args.append("ALPHA")
        if store:
            args.append("STORE")
            args.append(store)
        self.send_message(args, callback)

    def spop(self, key, callback=None):
        """
        Remove and return a random member from a set

            :param key:

        Complexity
        ----------
        O(1)
        """
        args = ["SPOP"]
        args.append(key)
        self.send_message(args, callback)

    def srandmember(self, key, count=None, callback=None):
        """
        Get one or multiple random members from a set

            :param key:
            :param count:

        Complexity
        ----------
        Without the count argument O(1), otherwise O(N) where N is the
        absolute value of the passed count.
        """
        args = ["SRANDMEMBER"]
        args.append(key)
        args.append(count)
        self.send_message(args, callback)

    def srem(self, key, members, callback=None):
        """
        Remove one or more members from a set

            :param key:
            :param members:
                string or list of strings

        Complexity
        ----------
        O(N) where N is the number of members to be removed.
        """
        args = ["SREM"]
        args.append(key)
        if isinstance(members, str):
            args.append(members)
        else:
            args.extend(members)
        self.send_message(args, callback)

    def strlen(self, key, callback=None):
        """
        Get the length of the value stored in a key

            :param key:

        Complexity
        ----------
        O(1)
        """
        args = ["STRLEN"]
        args.append(key)
        self.send_message(args, callback)

    def subscribe(self, channels, callback=None):
        """
        Listen for messages published to the given channels

            :param member_score_dict:
                string or list of strings

        Complexity
        ----------
        O(N) where N is the number of channels to subscribe to.
        """
        args = ["SUBSCRIBE"]
        if isinstance(channels, str):
            args.append(channels)
        else:
            args.extend(channels)
        self.send_message(args, callback)

    def sunion(self, keys, callback=None):
        """
        Add multiple sets

            :param keys:
                string or list of strings

        Complexity
        ----------
        O(N) where N is the total number of elements in all given sets.
        """
        args = ["SUNION"]
        if isinstance(keys, str):
            args.append(keys)
        else:
            args.extend(keys)
        self.send_message(args, callback)

    def sunionstore(self, destination, keys, callback=None):
        """
        Add multiple sets and store the resulting set in a key

            :param destination:
            :param keys:
                string or list of strings

        Complexity
        ----------
        O(N) where N is the total number of elements in all given sets.
        """
        args = ["SUNIONSTORE"]
        args.append(destination)
        if isinstance(keys, str):
            args.append(keys)
        else:
            args.extend(keys)
        self.send_message(args, callback)

    def sync(self, callback=None):
        """
        Internal command used for replication
        """
        self.send_message(["SYNC"], callback)

    def time(self, callback=None):
        """
        Return the current server time

        Complexity
        ----------
        O(1)
        """
        self.send_message(["TIME"], callback)

    def ttl(self, key, callback=None):
        """
        Get the time to live for a key

            :param key:

        Complexity
        ----------
        O(1)
        """
        args = ["TTL"]
        args.append(key)
        self.send_message(args, callback)

    def type(self, key, callback=None):
        """
        Determine the type stored at key

            :param key:

        Complexity
        ----------
        O(1)
        """
        args = ["TYPE"]
        args.append(key)
        self.send_message(args, callback)

    def unsubscribe(self, channels=[], callback=None):
        """
        Stop listening for messages posted to the given channels

            :param channels:
                string or list of strings

        Complexity
        ----------
        O(N) where N is the number of clients already subscribed to a channel.
        """
        args = ["UNSUBSCRIBE"]
        if isinstance(channels, str):
            args.append(channels)
        else:
            args.extend(channels)
        self.send_message(args, callback)

    def unwatch(self, callback=None):
        """
        Forget about all watched keys

        Complexity
        ----------
        O(1)
        """
        self.send_message(["UNWATCH"], callback)

    def watch(self, keys, callback=None):
        """
        Watch the given keys to determine execution of the MULTI/EXEC block

            :param keys:
                string or list of strings

        Complexity
        ----------
        O(1) for every key.
        """
        args = ["WATCH"]
        if isinstance(keys, str):
            args.append(keys)
        else:
            args.extend(keys)
        self.send_message(args, callback)

    def zadd(self, key, member_score_dict, callback=None):
        """
        Add one or more members to a sorted set, or update its score if it
        already exists

            :param key:
            :param member_score_dict:
                member score dictionary

        Complexity
        ----------
        O(log(N)) where N is the number of elements in the sorted set.
        """
        args = ["ZADD"]
        args.append(key)
        for member, score in member_score_dict.items():
            args.append(score)
            args.append(member)
        self.send_message(args, callback)

    def zcard(self, key, callback=None):
        """
        Get the number of members in a sorted set

            :param key:

        Complexity
        ----------
        O(1)
        """
        args = ["ZCARD"]
        args.append(key)
        self.send_message(args, callback)

    def zcount(self, key, min, max, callback=None):
        """
        Count the members in a sorted set with scores within the given values

            :param key:
            :param min:
            :param max:

        Complexity
        ----------
        O(log(N)+M) with N being the number of elements in the sorted set and
        M being the number of elements between min and max.
        """
        args = ["ZCOUNT"]
        args.append(key)
        args.append(min)
        args.append(max)
        self.send_message(args, callback)

    def zincrby(self, key, increment, member, callback=None):
        """
        Increment the score of a member in a sorted set

            :param key:
            :param increment:
            :param member:

        Complexity
        ----------
        O(log(N)) where N is the number of elements in the sorted set.
        """
        args = ["ZINCRBY"]
        args.append(key)
        args.append(increment)
        args.append(member)
        self.send_message(args, callback)

    def zinterstore(self, destination, keys, weights=tuple(), aggregate=None, callback=None):
        """
        Intersect multiple sorted sets and store the resulting sorted set in a
        new key

            :param destination:
            :param keys:
                string or list of strings
            :param weights:
            :param aggregate:

        Complexity
        ----------
        O(N*K)+O(M*log(M)) worst case with N being the smallest input sorted
        set, K being the number of input sorted sets and M being the number of
        elements in the resulting sorted set.
        """
        args = ["ZINTERSTORE"]
        args.append(destination)
        args.append(len(keys))
        if isinstance(keys, str):
            args.append(keys)
        else:
            args.extend(keys)
        if len(weights):
            args.append("WEIGHTS")
            args.extend(weights)
        if aggregate:
            args.append("AGGREGATE")
            args.append(aggregate)
        self.send_message(args, callback)

    def zrange(self, key, start, stop, withscores=False, callback=None):
        """
        Return a range of members in a sorted set, by index

            :param key:
            :param start:
            :param stop:
            :param withscores:

        Complexity
        ----------
        O(log(N)+M) with N being the number of elements in the sorted set and
        M the number of elements returned.
        """
        args = ["ZRANGE"]
        args.append(key)
        args.append(start)
        args.append(stop)
        if withscores:
            args.append("WITHSCORES")
        self.send_message(args, callback)

    def zrangebyscore(self, key, min, max, withscores=False, limit=None, callback=None):
        """
        Return a range of members in a sorted set, by score

            :param key:
            :param min:
            :param max:
            :param withscores:
            :param limit:

        Complexity
        ----------
        O(log(N)+M) with N being the number of elements in the sorted set and
        M the number of elements being returned. If M is constant (e.g. always
        asking for the first 10 elements with LIMIT), you can consider it
        O(log(N)).
        """
        args = ["ZRANGEBYSCORE"]
        args.append(key)
        args.append(min)
        args.append(max)
        if withscores:
            args.append("WITHSCORES")
        if limit:
            args.append("LIMIT")
            offset, count = limit
            args.append(offset)
            args.append(count)
        self.send_message(args, callback)

    def zrank(self, key, member, callback=None):
        """
        Determine the index of a member in a sorted set

            :param key:
            :param member:

        Complexity
        ----------
        O(log(N))
        """
        args = ["ZRANK"]
        args.append(key)
        args.append(member)
        self.send_message(args, callback)

    def zrem(self, key, members, callback=None):
        """
        Remove one or more members from a sorted set

            :param key:
            :param members:
                string or list of strings

        Complexity
        ----------
        O(M*log(N)) with N being the number of elements in the sorted set and
        M the number of elements to be removed.
        """
        args = ["ZREM"]
        args.append(key)
        if isinstance(members, str):
            args.append(members)
        else:
            args.extend(members)
        self.send_message(args, callback)

    def zremrangebyrank(self, key, start, stop, callback=None):
        """
        Remove all members in a sorted set within the given indexes

            :param key:
            :param start:
            :param stop:

        Complexity
        ----------
        O(log(N)+M) with N being the number of elements in the sorted set and
        M the number of elements removed by the operation.
        """
        args = ["ZREMRANGEBYRANK"]
        args.append(key)
        args.append(start)
        args.append(stop)
        self.send_message(args, callback)

    def zremrangebyscore(self, key, min, max, callback=None):
        """
        Remove all members in a sorted set within the given scores

            :param key:
            :param min:
            :param max:

        Complexity
        ----------
        O(log(N)+M) with N being the number of elements in the sorted set and
        M the number of elements removed by the operation.
        """
        args = ["ZREMRANGEBYSCORE"]
        args.append(key)
        args.append(min)
        args.append(max)
        self.send_message(args, callback)

    def zrevrange(self, key, start, stop, withscores=False, callback=None):
        """
        Return a range of members in a sorted set, by index, with scores
        ordered from high to low

            :param key:
            :param start:
            :param stop:
            :param withscores:

        Complexity
        ----------
        O(log(N)+M) with N being the number of elements in the sorted set and
        M the number of elements returned.
        """
        args = ["ZREVRANGE"]
        args.append(key)
        args.append(start)
        args.append(stop)
        if withscores:
            args.append("WITHSCORES")
        self.send_message(args, callback)

    def zrevrangebyscore(self, key, max, min, withscores=False, limit=None, callback=None):
        """
        Return a range of members in a sorted set, by score, with scores
        ordered from high to low

            :param key:
            :param max:
            :param min:
            :param withscores:
            :param limit:

        Complexity
        ----------
        O(log(N)+M) with N being the number of elements in the sorted set and
        M the number of elements being returned. If M is constant (e.g. always
        asking for the first 10 elements with LIMIT), you can consider it
        O(log(N)).
        """
        args = ["ZREVRANGEBYSCORE"]
        args.append(key)
        args.append(max)
        args.append(min)
        if withscores:
            args.append("WITHSCORES")
        if limit:
            args.append("LIMIT")
            offset, count = limit
            args.append(offset)
            args.append(count)
        self.send_message(args, callback)

    def zrevrank(self, key, member, callback=None):
        """
        Determine the index of a member in a sorted set, with scores ordered
        from high to low

            :param key:
            :param member:

        Complexity
        ----------
        O(log(N))
        """
        args = ["ZREVRANK"]
        args.append(key)
        args.append(member)
        self.send_message(args, callback)

    def zscore(self, key, member, callback=None):
        """
        Get the score associated with the given member in a sorted set

            :param key:
            :param member:

        Complexity
        ----------
        O(1)
        """
        args = ["ZSCORE"]
        args.append(key)
        args.append(member)
        self.send_message(args, callback)

    def zunionstore(self, destination, keys, weights=tuple(), aggregate=None, callback=None):
        """
        Add multiple sorted sets and store the resulting sorted set in a new
        key

            :param destination:
            :param keys:
                string or list of strings
            :param weights:
            :param aggregate:

        Complexity
        ----------
        O(N)+O(M log(M)) with N being the sum of the sizes of the input sorted
        sets, and M being the number of elements in the resulting sorted set.
        """
        args = ["ZUNIONSTORE"]
        args.append(destination)
        args.append(len(keys))
        if isinstance(keys, str):
            args.append(keys)
        else:
            args.extend(keys)
        if len(weights):
            args.append("WEIGHTS")
            args.extend(weights)
        if aggregate:
            args.append("AGGREGATE")
            args.append(aggregate)
        self.send_message(args, callback)
