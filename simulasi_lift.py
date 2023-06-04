import time
from tkinter import Tk, Canvas
from PersonClass import Person

def simulation(alg, jumlah_orang, jumlah_lantai, kapasitas, animate = True, animation_speed=0.1):
    if jumlah_lantai < 2 or jumlah_orang < 2:
        return 0
    
    tinggi_lantai = round(600 / jumlah_lantai)
    total_pop = []
    lift_pop = []
    boarding_times = []
    floor_pop = [0] * (jumlah_lantai + 1)
    lantai = 0
    lantai_target = 0
    if animate:
        tiba_pop = [0] * (jumlah_lantai + 1)
        lift_animation = [0] * kapasitas
        tk = Tk()
        tk.attributes("-fullscreen", True)
        canvas = Canvas(tk, width=2000, height=1000)
        tk.title('Simulasi Lift')
        canvas.pack()

        def gerak(animation, x, y):
            for j in range(0, 50):
                canvas.move(animation, x/50, y/50)
                tk.update()
                time.sleep(animation_speed/50)

        canvas.create_oval(600, 70, 610, 80, fill='black')
        canvas.create_oval(600, 100, 610, 110, fill='white')
        label_menunggu = canvas.create_text(615, 75, text='Menunggu', anchor='w', font=('Arial', 20))
        label_dalam = canvas.create_text(615, 105, text='Di dalam lift', anchor='w', font=('Arial', 20))

        for k in range(jumlah_lantai):
            canvas.create_line(515, 200 + (jumlah_lantai - k) * tinggi_lantai, 1065, 200 + (jumlah_lantai - k) * tinggi_lantai)
            canvas.create_text(470, 200 + (jumlah_lantai - k) * tinggi_lantai, text='Lantai' + str(k), anchor='w')
        canvas.create_rectangle(665, 200, 865, 200 + tinggi_lantai*jumlah_lantai)
        lift = canvas.create_rectangle(668, 200 + tinggi_lantai*(jumlah_lantai-1), 862, 200 + tinggi_lantai*jumlah_lantai, fill='black')
        tk.update()

        labels_arrival = []
        for k in range(jumlah_lantai):
            label_arrival = canvas.create_text(1070, 200 + (jumlah_lantai - k) * tinggi_lantai, anchor='w', font=('Arial', 16))
            labels_arrival.append(label_arrival)
        tk.update()

    for p in range(jumlah_orang):
        orang = Person(jumlah_lantai, tinggi_lantai)
        l_a = orang.lantai_awal
        if animate:
            offset = floor_pop[l_a] * 13
            orang.animasi = canvas.create_oval(650 - offset, 190 + (jumlah_lantai - l_a)*tinggi_lantai, 660 - offset, 200 + (jumlah_lantai - l_a)*tinggi_lantai, fill='black')
            tk.update
        floor_pop[l_a] += 1
        total_pop.append(orang)
        boarding_times.append(orang.wait_time)
    arah_lift = 1

    wait_times = []

    while sum(floor_pop) + len(lift_pop) > 0:
        for orang in total_pop:
            orang.wait_time += 1 if not orang.selesai else 0

            if orang.dalam_lift and orang.tiba(lantai):
                orang.dalam_lift = False
                orang.selesai = True
                lift_pop.remove(orang)
                if animate:
                    lift_animation[orang.lift_spot] = False
                    canvas.itemconfig(orang.animasi, fill='blue')
                    tiba_pop[lantai] += 1
                    canvas.itemconfig(labels_arrival[lantai], text='Orang yang tiba: ' + str(tiba_pop[lantai]))

                    gerak(orang.animasi, 885 + tiba_pop[lantai]*12 - canvas.coords(orang.animasi)[0], 15*(orang.lift_spot%2))
                    canvas.itemconfig(label_dalam, text='Di dalam lift - ' + str(len(lift_pop)))
                    canvas.itemconfig(label_menunggu, text='Menunggu - ' + str(sum(floor_pop)))
        for orang in total_pop:
            if orang.menunggu() and orang.lantai_awal == lantai and len(
                lift_pop) < kapasitas and (
                (
                        arah_lift == orang.arah or lantai == 0 or lantai == jumlah_lantai -1 or lantai == lantai_target)):
                lift_pop.append(orang)
                orang.dalam_lift = True
                floor_pop[lantai] -= 1
                boarding_times.append(orang.wait_time)
                if animate:
                    for spot in range(len(lift_animation)):
                        if not lift_animation[spot]:
                            lift_animation[spot] = True
                            orang.lift_spot = spot
                            gerak(orang.animasi, (740 + (spot%3)*15) - canvas.coords(orang.animasi)[0], -15*(spot%2))
                            break
                    canvas.itemconfig(orang.animasi, fill='white')
                    canvas.itemconfig(label_dalam, text='Di dalam lift - ' + str(len(lift_pop)))
                    canvas.itemconfig(label_menunggu, text='Menunggu - ' + str(sum(floor_pop)))
        if sum(floor_pop) + len(lift_pop) == 0:
            break

        if alg == 1:
            tombol_lift = [False] * jumlah_lantai
            for orang in lift_pop:
                tombol_lift[orang.lantai_target] = True
            # x = lantai yang ingin dituju orang
            x = [i for i in range(len(tombol_lift)) if tombol_lift[i]]
            if len(lift_pop) < kapasitas:
                x.extend([lt for lt in range(jumlah_lantai) if bool(floor_pop[lt])])
            lt_tertinggi = max(x)
            lt_terendah = min(x)
            if arah_lift == -1:
                lantai_target = lt_terendah
            elif arah_lift == 1:
                lantai_target = lt_tertinggi
            arah_lift = -1 if lantai_target < lantai else 1
            if lantai == lantai_target:
                arah_lift *= -1
        
        if animate:
            print('Lantai tujuan:', lantai_target, 'dan arah', arah_lift, 'Lantai saat ini:', lantai)
            for i in range (tinggi_lantai):
                tk.update()
                time.sleep(animation_speed/tinggi_lantai)
                canvas.move(lift, 0, -arah_lift)
                for orang in lift_pop:
                    canvas.move(orang.animasi, 0, -arah_lift)
            time.sleep(animation_speed)
        lantai += arah_lift
    for orang in total_pop:
        if orang.selesai: wait_times.append(orang.wait_time)

    wait_time_terlama = max(wait_times)
    wait_time_avg = sum(wait_times)/jumlah_orang
    avg_boarding_time = sum(boarding_times) / jumlah_orang  # Calculate average boarding time


    print('Waktu tunggu terlama:', wait_time_terlama)
    print('Waktu tunggu tercepat:', min(wait_times))
    print('Simulasi', jumlah_orang, 'orang menggunakan lift SGLC dengan', jumlah_lantai, 'lantai tujuan.')
    print('Rata-rata waktu tunggu adalah', wait_time_avg)
    print("Rata-rata waktu naik: ", avg_boarding_time)  # Print average boarding time
    
    tmp = 0
    while tmp < jumlah_orang:
        boarding_times.pop(0)
        tmp = tmp+1

    for i in range(len(boarding_times)):
        boarding_times[i] = boarding_times[i] * wait_time_avg
    
    maxboard = max(boarding_times)
    minboard = min(boarding_times)
    boarding_times = sum(boarding_times)/jumlah_orang
    print(boarding_times)
    print(maxboard)
    print(minboard)

    tk.mainloop()
        
    return wait_time_avg