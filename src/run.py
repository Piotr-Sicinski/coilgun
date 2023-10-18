import multiprocessing
import sys
import time
import argparse

import laser_tracker  # type: ignore
import mindstorms_client  # type: ignore


def run(en_graphics: bool):
    conn1Start, conn1End = multiprocessing.Pipe()
    process_0 = multiprocessing.Process(
        target=laser_tracker.process_run, args=(conn1Start, en_graphics))

    process_1 = multiprocessing.Process(
        target=mindstorms_client.process_run_pid, args=(conn1End,))
    # process_1 = multiprocessing.Process(
    #     target=mindstorms_client.process_run_turret, args=(conn1End,))
    # process_1 = multiprocessing.Process(
    #     target=mindstorms_client.process_run_test_print, args=(conn1End,))

    processes = [process_0, process_1]

    for process in processes:
        process.start()

    while all(process.is_alive() for process in processes):
        time.sleep(1)

    for process in processes:
        if not process.is_alive():
            print(f"Process {processes.index(process)} terminated.")
        else:
            process.terminate()
            process.join()

    print("Exiting... ")
    sys.exit(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run the Laser Tracker')
    parser.add_argument('-g', '--graphics',
                        action='store_true',
                        help='Display camera windows')
    params = parser.parse_args()

    run(params.graphics)
