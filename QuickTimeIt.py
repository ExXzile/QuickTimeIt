import timeit
import logging
import datetime


def quick_timeit(runs=1000, repeat=5, timing='sec', logfile=False):
    def arg_wrap(func):
        def wrapper(*args, **kwargs):

            if logfile:
                handler = logging.FileHandler(f'{func.__name__}.QTimeIt.log', mode='a')
            else:
                handler = logging.StreamHandler()

            formatter = logging.Formatter('%(message)s')
            handler.setFormatter(formatter)
            logger = logging.getLogger(f'{func.__name__}_QTimeIt')
            logger.setLevel(level=logging.DEBUG)
            logger.addHandler(handler)

            syntax_error = (
                f'\n- QuickTimeIt() - Invalid quick_timeit() kwarg(s)! '
                f'\nfunc : <{func.__name__}> - timing Aborted!'
                f'\n--- Invalid kwarg(s): --'
            )

            op_error = []
            if not isinstance(runs, int):
                op_error.append(f'runs={runs!r}')
            if not isinstance(repeat, int):
                op_error.append(f'repeat={repeat!r}')
            if timing not in ['sec', 'milli', 'nano']:
                op_error.append(f'timing={timing!r}')
            if not isinstance(logfile, bool):
                op_error.append(f'file={logfile!r}')

            if op_error:  # if syntax error, return func, discontinue
                logger.info(syntax_error + ', --'.join(op_error))
                logger.removeHandler(handler)
                return func(*args, **kwargs)

            # ----------------------------------------------------------

            timing_dic = {
                'sec': (1, 'second'),
                'milli': (1000, 'millisecond'),
                'nano': (10**9, 'nanosecond')
            }
            logging_msg = ''
            f_args = [repr(a) for a in args]
            f_kwargs = [f'{k}={repr(v)}' for k, v in kwargs.items()]
            all_args = ', '.join(f_args + f_kwargs)

            time_rep = timeit.repeat(
                f'"{func.__name__}({all_args})"',
                setup=f'from __main__ import {func.__name__}',
                repeat=repeat, number=runs
            )

            results_gen = (f'\n{run:>9}: - {mes*timing_dic[timing][0]:.12f}'
                           for run, mes in enumerate(time_rep, 1))

            logging_msg += f'\n- QuickTimeIt():  '
            if logfile:
                logging_msg += f'call logged at {datetime.datetime.now()}'
            logging_msg += f'\n--------------------------------------------'\
                           f'\ntiming func    :  <{func.__name__}> | repeat = {repeat}'

            if len(all_args) > 120:
                all_args = str(all_args)[:120] + ' .... <truncated> ..'
            logging_msg += f'\n*args/**kwargs :  ({all_args})'\
                           f'\nnumber of runs :  {runs}'\
                           f'\nmeasurement    :  {timing_dic[timing][1]}'\
                           f'\ncompleted in   :  \n'

            for result in results_gen:
                logging_msg += result

            logging_msg += f'\n\n average: - ' \
                           f'{(sum(time_rep) / len(time_rep))*timing_dic[timing][0]:.12f} ' \
                           f'{timing_dic[timing][1]}\n'

            logging_msg += '--------------------------------------------'

            logger.info(logging_msg)
            logger.removeHandler(handler)
            return func(*args, **kwargs)
        return wrapper
    return arg_wrap
