from icecream import ic
import multiprocessing
from math import sin


def static_vars(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func
    return decorate


@static_vars(deg=0)
def calc_sin(conn):
    calc_sin.deg += 0.05
    return 200 * sin(calc_sin.deg)


def run():
    conn1Start, conn1End = multiprocessing.Pipe()
    process_1 = multiprocessing.Process(
        target=calc_sin, args=(conn1Start,))

    # process_2 = multiprocessing.Process(
    #     target=mindstorms_client.process_run_degree_table, args=(conn1End,))
    process_2 = multiprocessing.Process(
        target=mindstorms_client.process_run_turret, args=(conn1End,))
    # process_2 = multiprocessing.Process(
    #     target=mindstorms_client.process_run_test_print, args=(conn1End,))

    process_1.start()
    process_2.start()


if __name__ == "__main__":
    run()
