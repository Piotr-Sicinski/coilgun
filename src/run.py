import multiprocessing
import laser_tracker
import mindstorms_client


def run():
    conn1, conn2 = multiprocessing.Pipe()
    process_1 = multiprocessing.Process(
        target=laser_tracker.process_run, args=(conn1,))
    # process_2 = multiprocessing.Process(
    #     target=process_run_test_print, args=(conn2,))
    process_2 = multiprocessing.Process(
        target=mindstorms_client.process_run_turret, args=(conn2,))
    process_1.start()
    process_2.start()


if __name__ == "__main__":
    run()
