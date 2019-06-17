## _Function(s) execution timer @decorator with args_

*functions wrapper for a quick Python Built-in 'Timeit' modile reports*
*without interrupting or breaking course of a code run.*

#### installation:
- save QuickTimeit.py file in a same directory as your code file
- or
- in Python modules instalation Path for quick access anytime

#### making it work:
- import to your code:
  - __from QuickTimeit import quick_timeit__

- place quick_timeit() as a @decorator above any function in your code
  - __@quick_timeit()__

- add args to @decorator (_Optional_)
  - __(runs=100000, timing='milli', repeat=3)__ 

- in order for TimeIt to compute, your func must be 'called' with relevant args, if any.

- @decorator can be placed on multiple funcs at once

- __quick_timeit()__ acts as a wrapper and your code/programm will continue run as intended without it
  
  
#### example:

	from QuickTimeit import quick_timeit

	@quick_timeit(runs=100, repeat=3, timing='milli')  # -> QuickTimeIt @decorator with optinal args
	def beaufort_cipher_mathematical(m, key):
		u = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ_'
		key = (key * (int(len(m) / len(key) + 1)))[0: len(m)]
		answr = [u[(u.index(k) - u.index(m)) % len(u)] for m, k in zip(m, key)]
		
		return ''.join(answr)


#### optinal args
- runs = how many runs of a func -> integer
- repeat = how many times to repeat runs -> integer
- timing = 'sec', 'milli', 'nano' -> string
  - respectively seconds, milliseconds, nanosecons

#### defauls
- runs=1000
- repeat=5
- timing='sec'
