from collections import deque
import argparse


class RedisStore:
    def __init__(self):
        self.store = {}
        self.hash_store = {}
        self.list_store = {}

    def set(self, key, value):
        self.store[key] = value

        return "Success"

    def get(self, key):
        if key not in self.store:
            return "(null)"

        return f'"{self.store[key]}"'

    def delete(self, key):
        if key in self.store:
            del self.store[key]
            return "Success"

        return "(null)"

    def lpush(self, key, value):
        if key not in self.list_store:
            self.list_store[key] = deque()
        self.list_store[key].appendleft(value)

        return "Success"

    def lpop(self, key):
        if key not in self.list_store or not self.list_store[key]:
            return "(null)"

        return f'"{self.list_store[key].popleft()}"'

    def lrange(self, key, start, end):
        if key not in self.list_store:
            return "(null)"

        list_len = len(self.list_store[key])
        if start < 0:
            start = max(0, list_len + start)

        if end < 0:
            end = max(0, list_len + end)
        end = min(end + 1, list_len)
        result = list(self.list_store[key])[start:end]

        if not result:
            return "(empty list)"

        return "\n".join(f'"{item}"' for item in result)

    def hset(self, hash_key, field, value):
        if hash_key not in self.hash_store:
            self.hash_store[hash_key] = {}
        self.hash_store[hash_key][field] = value

        return "Success"

    def hget(self, hash_key, field):
        if hash_key not in self.hash_store or field not in self.hash_store[hash_key]:
            return "(null)"

        return f'"{self.hash_store[hash_key][field]}"'


def parse_command(cmd_line):
    if not cmd_line:
        return None, []
    parts = cmd_line.strip().split()
    return parts[0].upper(), parts[1:]


def process_command(redis, user_input):
    command, args = parse_command(user_input)
    commands = {
        "SET": (redis.set, 2),
        "GET": (redis.get, 1),
        "DEL": (redis.delete, 1),
        "LPUSH": (redis.lpush, 2),
        "LPOP": (redis.lpop, 1),
        "LRANGE": (redis.lrange, 3),
        "HSET": (redis.hset, 3),
        "HGET": (redis.hget, 2),
        "HELP": (print_help, 0),
    }
    if not command:
        print("Error: empty command")
        return
    if command not in commands:
        print(f"Error: unknown command '{command}'")
        return
    func, required_args = commands[command]
    if len(args) != required_args:
        print(f"Error: wrong number of arguments for '{command}' command")
        return
    if command == "LRANGE":
        try:
            args[1] = int(args[1])
            args[2] = int(args[2])
        except ValueError:
            print("Error: LRANGE requires numeric start and end indices")
            return
    result = func(*args)
    print(f"> {result}")


def print_help():
    help_text = """
    Available Commands:
    ------------------
    SET key value          - Set key to hold string value
    GET key                - Get the value of key
    DEL key                - Delete a key
    LPUSH key value        - Insert value at the head of the list stored at key
    LPOP key               - Remove and get the first element in a list
    LRANGE key start end   - Get a range of elements from a list
    HSET key field value   - Set the string value of a hash field
    HGET key field         - Get the value of a hash field
    HELP                   - Show this help message
    EXIT                   - Exit the program
    """

    return help_text.strip()


def main():
    parser = argparse.ArgumentParser(description="Redis-like key-value store CLI tool")
    parser.add_argument("command", nargs=argparse.REMAINDER, help="Command to execute")
    args = parser.parse_args()

    redis = RedisStore()

    if args.command:
        # command/s were given as arguments when running program
        user_input = " ".join(args.command)
        process_command(redis, user_input)

    else:
        # no command given, enter interactive mode
        print("Redis-like KV store")
        print("Type 'HELP' for available commands, 'EXIT' to quit")

        while True:
            try:
                print("\nType in your command!")
                user_input = input(">> ").strip()
                if user_input.upper() == "EXIT":
                    print("Bye!")
                    break
                process_command(redis, user_input)

            except KeyboardInterrupt:
                print("\nBye!")
                break

            except Exception as e:
                print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
