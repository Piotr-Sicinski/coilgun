import multiprocessing
from laser_tracker import process_run
from mindstorms_ssh import process_run_test_print


def run():
    conn1, conn2 = multiprocessing.Pipe()
    process_1 = multiprocessing.Process(target=process_run, args=(conn1,))
    process_2 = multiprocessing.Process(target=process_run_test_print, args=(conn2,))
    process_1.start()
    process_2.start()


if __name__ == "__main__":
    run()
