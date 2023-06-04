import time
from datetime import datetime
from simulasi_lift import simulation

if __name__ == "__main__":
    print("Simulasi dimulai pada {}".format(datetime.now().strftime("%H:%M:%S")))
    for i in range(10):
        simulation(1, 20, 11, 15, animate = True, animation_speed=0.5)
    start_time = time.perf_counter()