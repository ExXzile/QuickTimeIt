import timeit
import logging


def quick_timeit(runs=10000, repeat=5, timing='sec', file='', overwrite=True):
    def arg_wrap(func):
        def wrapper(*args, **kwargs):

            # set-up and soft 'failsafe' -------------------------------
            # tested func will continue as as normal

            for handler in logging.root.handlers[:]:
                logging.root.removeHandler(handler)
            logging.basicConfig(format='%(message)s', level=logging.DEBUG)

            syntax_error = (
                f'\n- QuickTimeIt() - Invalid quick_timeit() kwargs! '
                f'\nfunc : <{func.__name__}> - timing Aborted!\n'
            )

            kwarg_error = ' --- Invalid operand(s), **kwarg(s): --'
            op_error = []
            if not isinstance(runs, int):
                op_error.append(f'runs={runs!r}')
            if not isinstance(repeat, int):
                op_error.append(f'repeat={repeat!r}')
            if timing not in ['sec', 'milli', 'nano']:
                op_error.append(f'timing={timing!r}')
            if not isinstance(file, str):
                op_error.append(f'file={file!r}')
            if not isinstance(overwrite, bool):
                op_error.append(f'overwrite={overwrite!r}')

            if op_error:
                logging.warning(syntax_error + kwarg_error + ', --'.join(op_error))
                return func(*args, **kwargs)

            if file:
                mode = 'w' if overwrite else 'a'
                for handler in logging.root.handlers[:]:
                    logging.root.removeHandler(handler)
                logging.basicConfig(
                    format='%(message)s',
                    filename=file,
                    filemode=mode,
                    level=logging.DEBUG
                )
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

            logging_msg += f'\n- QuickTimeIt():'\
                           f'\n--------------------------------------------'\
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

            logging_msg += '--------------------------------------------\n\n'

            logging.info(logging_msg)
            return func(*args, **kwargs)
        return wrapper
    return arg_wrap
