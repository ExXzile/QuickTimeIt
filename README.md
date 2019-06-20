## _Function(s) execution timer @decorator with args_

*functions wrapper for a quick Python Built-in 'Timeit' module reports*
*without interrupting or breaking course of a code run.*

#### installation:
- save QuickTimeIt.py file in a same directory as your code file
- or
- in Python modules installation Path for quick access anytime

#### making it work:
- import to your code:
  - __from QuickTimeIt import quick_timeit__

- place quick_timeit() as a @decorator above function in your code
    - __@quick_timeit()__
   
    - as of this release, only main code funcs can be tested i.e. QuickTimeIt @decorator
    will fail to execute when attempting to test funcs within classes or funcs nested within other funcs

- add args to @decorator (_Optional_)
  - __(runs=100000, timing='milli', repeat=3, logfile=True)__

- in order for TimeIt to compute, your func **must** be 'called' with relevant args/kwargs, if applicable.

- __@quick_timeit()__ can be placed on multiple funcs at once

- __@quick_timeit()__ acts as a wrapper and your code/program/script will continue run as intended without it

- __@quick_timeit()__ will execute every time @decorated function is called:
	- _for presentability, avoid adding to frequently called or recurring functions, unless logged to file_
	- _given it's nature, will execute for every next() or otherwise call from 'generator' type functions_
	- _as it is using logger mode in a separate thread (if log file not specified),
	console STDOUT's may overlap with func console outputs, if any_

#### warning:
- _to avoid unpredictable behaviour, avoid using with 'side-effect' functions_
	- _i.e functions with **global** declarations_.
  
#### example:

	from QuickTimeIt import quick_timeit

	@quick_timeit(runs=100, repeat=3, timing='milli')  # -> QuickTimeIt @decorator with optional args
	def beaufort_cipher_mathematical(m, key):
		u = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ_'
		key = (key * (int(len(m) / len(key) + 1)))[0: len(m)]
		answer = [u[(u.index(k) - u.index(m)) % len(u)] for m, k in zip(m, key)]
		
		return ''.join(answer)


#### optional kwargs:
- runs= how many runs of a func -> integer
- repeat= how many times to repeat runs -> integer
- timing= 'sec', 'milli', 'nano' -> string
  - respectively seconds, milliseconds, nanoseconds
- logfile= if specified, log will be timestamped and appended to file -> string
  - separate log file will be created for each tested function

 
#### defaults:
- runs=1000
- repeat=5
- timing='sec'
- logfile=None

