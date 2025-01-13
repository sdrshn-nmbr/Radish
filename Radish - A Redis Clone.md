# Radish - Redis-like In-Memory Store CLI Tool

A Python CLI tool that implements a Redis-like in-memory key-value store. It supports basic operations and additional commands for lists and hashes.

## Features

### Core Commands

- `SET key value`: Store a key-value pair
- `GET key`: Retrieve a value by key
- `DEL key`: Delete a key-value pair

### List Commands

- `LPUSH key value`: Push an element to the head of a list
- `LPOP key`: Remove and return the first element of a list
- `LRANGE key start end`: Return a range of elements from a list

### Hash Commands

- `HSET hash field value`: Set the value of a field in a hash
- `HGET hash field`: Get the value of a field in a hash

## Implementation Assumptions

1. **Data Persistence**

   - All data is stored in memory only, as specified in the original instructions
   - The program can be cleanly terminated using `EXIT` / `exit` / `Ctrl+C`.

2. **Data Types**

   - All values are stored and returned as strings
   - List indices for `LRANGE` follow Python's convention but the end index is inclusive
   - Negative indices are supported for `LRANGE` since I implemented it using `deque`, aka double-ended queue, which acts like a list but allows for appends and pops from both ends

3. **Error Handling**

   - Invalid commands return appropriate error messages
   - Wrong number of arguments are caught and reported
   - Non-existent keys or fields return `(null)`
   - Empty lists return `(empty list)`

4. **Command Format**

   - Commands are case-insensitive so user can type in `set`, `SET`, `SeT` etc.
   - Arguments are space-separated
   - Values containing spaces must be handled as separate arguments

## Design Decisions

1. **Efficient List Operations**

   - Used `deque` from the `collections` module for list operations to achieve O(1) complexity for left-side operations

2. **User-Friendly Output**

   - Followed Redis-like output formatting with quoted strings for clarity in return value data types

## Running the Program

1. **Prerequisites**

   - Ensure Python 3.6 or higher is installed on your system.

2. **Execution**

   - Run the script from your terminal or command prompt:

     ```bash
     python radish.py
     ```

3. **Using the CLI**

   - After running the script, you'll see:

     ```bash
     Redis-like key-value store
     Type 'EXIT' to quit

     What is your command?
     ```

   - Type your commands at the `>>` prompt.

4. **Exiting the Program**

   - Type `EXIT` or press `Ctrl+C` to exit the program gracefully.

## Example Usage

```bash
Redis-like key-value store
Type 'EXIT' to quit

What is your command?
>> SET mykey Hello
> Success

What is your command?
>> GET mykey
> "Hello"

What is your command?
>> LPUSH mylist world
> Success

What is your command?
>> LPUSH mylist hello
> Success

What is your command?
>> LRANGE mylist 0 -1
> "hello"
> "world"

What is your command?
>> HSET myhash field1 value1
> Success

What is your command?
>> HGET myhash field1
> "value1"

What is your command?
>> DEL mykey
> Success

What is your command?
>> GET mykey
> (null)

What is your command?
>> EXIT
Bye!
```

## Additional Notes

- **List Indexing with `LRANGE`**

  - Start and end indices can be negative
  - The end index is inclusive, meaning `LRANGE mylist 0 1` returns the first two elements
  - If the start index is greater than the end index, an empty list is returned

- **Error Messages**

  - Unknown commands result in: `Error: Unknown command 'COMMAND'`
  - Wrong number of arguments result in: `Error: Wrong number of arguments for 'COMMAND' command`
  - Non-integer indices for `LRANGE` result in: `Error: LRANGE requires numeric start and end indices`
