import multiprocessing
import laser_tracker  # type: ignore
import mindstorms_client  # type: ignore


def run():
    conn1Start, conn1End = multiprocessing.Pipe()
    process_1 = multiprocessing.Process(
        target=laser_tracker.process_run, args=(conn1Start,))

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
