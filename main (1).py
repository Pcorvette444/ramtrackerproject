import psutil
import platform
import time
import threading
import datetime
import json
import matplotlib.pyplot as plt


x = [0,0]
y = [0,0]

def format_size(bytes, suffix="B"):
  """
    Returns a formatted string from an integer 
    number of bytes using JEDEC conventions:
    - https://en.wikipedia.org/wiki/Binary_prefix

    (uses binary multiples [2^10 = kilo, 2^20 = mega, etc], 
    NOT decimal [10^3 = kilo, 10^6 = mega, etc.])

    example:
        10293 -> 10.1KB
        2098234 -> 11.5MB
    """

  factor = 1024

  for prefix in ["", "K", "M", "G", "T"]:
    if bytes < factor:
      return f"{bytes:.1f}{prefix}{suffix}"
    bytes /= factor


def get_mem_info():
  """
    Returns a dictionary containing memory info.

    Keys ending WITH "_f" correspond with formatted 
    string values for bytes (B, KB, MB, etc.).
    Keys ending WITHOUT "_f" correspond with integers
    (amount in bytes).
    """

  svmem = psutil.virtual_memory()

  return {
      "total_mem": svmem.total,
      "total_mem_f": format_size(svmem.total),
      "available_mem": svmem.available,
      "available_mem_f": format_size(svmem.available),
      "used_mem": svmem.used,
      "used_mem_f": format_size(svmem.used),
      "free_mem": svmem.free,
      "free_mem_f": format_size(svmem.free),
      "percent_mem": svmem.percent,
  }


def update_loop(interval=1.0):
  """
    Updates the "memory_info" dictionary every interval 
    (time in seconds) using threading.

    Time drift is adjusted for by calculating the remaining 
    amount of the interval after the other components of the 
    loop have been executed.

    This function runs as a daemon thread, meaning the 
    program will terminate itself if this is the only thread 
    remaining (if main.py stops being interpreted, it
    """

  starting_time = time.time()
  iteration = 0


  while True:
    memory_info = get_mem_info()

    iteration += 1

    #print(datetime.datetime.now())
    mem = json.dumps(memory_info)
    mem2 = json.loads(mem)
    #print(mem2["percent_mem"])

    # x axis values
    x.append(iteration)
    y.append(mem2["percent_mem"])
    # corresponding y axis values
    

    # plotting the points 
    plt.plot(x, y)
   
    # naming the x axis
    plt.xlabel('Time (Seconds)')
    # naming the y axis
    plt.ylabel('% of RAM in use')
    plt.xscale("linear")
    # giving a title to my graph
    plt.title('RAM Monitor')
    plt.pause(1)
    
    # function to show the plot
    #plt.show()

    # corresponding y axis values

    # plotting the points 
  
    #print(iteration)
    #next_call = starting_time + (interval * iteration)
    #time.sleep(next_call - time.time())


"""
uname is a namedtuple() (tuple subclass) that contains six attributes:
system, node, release, version, machine, and processor.

Each can be accessed as a string via: uname.<attribute>

If something cannot be determined, an empty string is returned

example:
    uname.system = Windows
"""
uname = platform.uname()

loop_thread = threading.Thread(target=update_loop)
loop_thread.daemon = True
loop_thread.start()

# Main while loop; program ends when it ends
input_string = ""
while input_string != "terminate":
  input_string = input()
