import timeit
import logging
import datetime


def quick_timeit(runs=1000, repeat=5, timing='sec', logfile=False):
    def arg_wrap(func):
        def wrapper(*args, **kwargs):

            # set-up and soft 'failsafe' abort -------------------------
            logger = logging.getLogger(__name__)
            logger.setLevel(level=logging.DEBUG)
            if logfile:
                handler = logging.FileHandler(
                    f'{func.__name__}.QTimeIt.log', mode='a'
                )
            else:
                handler = logging.StreamHandler()
            logger.addHandler(handler)

            op_error = []
            if not isinstance(runs, int):
                op_error.append(f'runs={runs!r}')
            if not isinstance(repeat, int):
                op_error.append(f'repeat={repeat!r}')
            if timing not in ['sec', 'milli', 'nano']:
                op_error.append(f'timing={timing!r}')
            if not isinstance(logfile, bool):
                op_error.append(f'file={logfile!r}')

            if op_error:  # if syntax error, return func and discontinue
                logger.info(
                    f'\n- QuickTimeIt() - Invalid quick_timeit() kwarg(s)! '
                    f'\nfunc : <{func.__name__}> - timing Aborted!'
                    f'\n--- kwarg(s) Syntax Error: --'
                    + ', --'.join(op_error)
                )
                logger.removeHandler(handler)
                return func(*args, **kwargs)
            # ----------------------------------------------------------

            timing_dic = {
                'sec': (1, 'seconds'),
                'milli': (1000, 'milliseconds'),
                'nano': (10**9, 'nanoseconds')
            }
            time_rep = timeit.repeat(
                lambda: func(*args, **kwargs),
                repeat=repeat, number=runs
            )
            logging_out = f'\n- QuickTimeIt():  '
            if logfile:
                logging_out += f'call logged at {datetime.datetime.now()}'
            logging_out += '\n--------------------------------------------'\
                           f'\ntiming func    :  <{func.__name__}> | repeat = {repeat}'

            all_args = ', '.join(
                [repr(a) for a in args]
                + [f'{k}={repr(v)}' for k, v in kwargs.items()]
            )

            if len(all_args) > 120:
                all_args = all_args[:120] + ' .... <truncated> ..'

            logging_out += f'\n*args/**kwargs :  ({all_args})'\
                           f'\nnumber of runs :  {runs}'\
                           f'\nmeasure in     :  {timing_dic[timing][1]}'\
                           '\ncompleted in   :  \n'

            logging_out += ''.join(f'\n{run:>9}: - {measure*timing_dic[timing][0]:.9f} '
                                   for run, measure in enumerate(time_rep, 1))

            if repeat > 1:
                logging_out += f'\n\n  fastest: - ' \
                               f'{min(time_rep):.9f} {timing_dic[timing][1]}\n' \
                               f'  average: - ' \
                               f'{(sum(time_rep) / len(time_rep))*timing_dic[timing][0]:.9f} ' \
                               f'{timing_dic[timing][1]}'
            else:
                logging_out += timing_dic[timing][1]
            logging_out += '\n--------------------------------------------'

            logger.info(logging_out)
            logger.removeHandler(handler)
            return func(*args, **kwargs)
        return wrapper
    return arg_wrap
