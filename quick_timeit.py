
import timeit


def quick_timeit(runs=10000, repeat=5, timing='sec'):
    def arg_wrap(func):
        def wrapper(*args, **kwargs):
            time_dic = {
                'sec': (1, ''),
                'milli': (1000, 'milli'),
                'nano': (10**9, 'nano')
            }
            f_args = ', '.join(str(a) for a in args)
            f_kwargs = ', '.join(f'{k}={v}' for k, v in kwargs.items())
            t = timeit.repeat(
                stmt=f'{func(*args, **kwargs)}',
                number=runs, repeat=repeat
            )
            results_gen = (f'  {run}: - {mes*time_dic[timing][0]:.12f}'
                           for run, mes in enumerate(t, 1))

            print('\n- QuickTimeIt():')
            print('--------------------------------------------')
            print(f'timing func    :  <{func.__name__}> | repeat = {repeat}')
            print(f'passed args    :  ({f_args}, {f_kwargs})')
            print(f'number of runs :  {runs}')
            print(f'measurement    :  {time_dic[timing][1]}seconds')
            print('completed in   :  ')
            print()

            for result in results_gen:
                print(result)

            print('\naverage: - ', end='')
            print(f'{(sum(t) / len(t))*time_dic[timing][0]:.12f} {time_dic[timing][1]}seconds')

            print('--------------------------------------------\n')
            return func(*args)
        return wrapper
    return arg_wrap
    
