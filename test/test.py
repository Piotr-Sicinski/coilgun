import time

start_time_real = time.time()
start_time_monotonic = time.monotonic()

# Simulate a delay or computation
time.sleep(2)

end_time_real = time.time()
end_time_monotonic = time.monotonic()

print("Real time elapsed:", end_time_real - start_time_real, "seconds")
print("Monotonic time elapsed:", end_time_monotonic -
      start_time_monotonic, "seconds")
