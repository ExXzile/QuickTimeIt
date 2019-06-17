
import timeit


def quick_timeit(runs=10000, repeat=5, timing='sec'):
    def arg_wrap(func):
        def wrapper(*args, **kwargs):
            time_dic = {
                'sec': (1, ''),
                'milli': (1000, 'milli'),
                'nano': (10**9, 'nano')
            }

            # small 'failsafe' abort measure..
            # tested func will continue as as normal
            if timing not in time_dic.keys()\
                    or type(runs) != int\
                    or type(repeat) != int:
                print('\n - Invalid QuickTimeit() args!')
                print(' - timing Aborted!')
                print('----------------------------------\n')
                return func(*args, **kwargs)
            # ----------------------------------------------------------

            f_args = [repr(a) for a in args]
            f_kwargs = [f'{k}={v}' for k, v in kwargs.items()]
            argsakwargs = ', '.join(f_args + f_kwargs)

            t = timeit.repeat(
                f'"{func.__name__}({argsakwargs})"',
                setup=f'from __main__ import {func.__name__}',
                repeat=repeat, number=runs
            )

            results_gen = (f'  {run}: - {mes*time_dic[timing][0]:.12f}'
                           for run, mes in enumerate(t, 1))

            print('\n- QuickTimeIt():')
            print('--------------------------------------------')
            print(f'timing func    :  <{func.__name__}> | repeat = {repeat}')
            print(f'*args/**kwargs :  ({argsakwargs})')
            print(f'number of runs :  {runs}')
            print(f'measurement    :  {time_dic[timing][1]}seconds')
            print('completed in   :  ')
            print()

            for result in results_gen:
                print(result)

            print('\naverage: - ', end='')
            print(
                f'{(sum(t) / len(t))*time_dic[timing][0]:.12f} '
                f'{time_dic[timing][1]}seconds'
            )
            print('--------------------------------------------\n')

            return func(*args, **kwargs)
        return wrapper
    return arg_wrap
