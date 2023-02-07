import multiprocessing


def run():
    conn1, conn2 = multiprocessing.Pipe()
    process_1 = multiprocessing.Process(target=process1_send_function, args=(conn1))
    process_2 = multiprocessing.Process(target=process2_recv_function, args=(conn2))
    process_1.start()
    process_2.start()


if __name__ == "__main__":
    run()
