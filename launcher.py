import subprocess
import os
import glob
import time
import psutil


def get_game_exe():
    # Ищет первый .exe файл, кроме самого лаунчера
    files = [f for f in glob.glob("*.exe") if f != "launcher.exe"]
    return files[0] if files else None


def launch_and_monitor():
    game_exe = get_game_exe()
    if not game_exe:
        print("Error: No game file found in this folder!")
        input("Press Enter to exit...")
        return

    try:
        user_input = input(f"Game '{game_exe}' detected. Enter number of windows (1-9999999999999999): ")
        count = int(user_input)
        count = max(1, min(count, 9999999999999999))

        print(f"Launching {count} windows...")

        # Список для хранения объектов процессов
        processes = []
        for _ in range(count):
            # Запускаем процесс
            proc = subprocess.Popen([game_exe])
            processes.append(proc)

        print("Done! Monitoring... Close any window to kill all.")

        # Цикл мониторинга
        while True:
            time.sleep(0.5)

            # Проверяем, работают ли еще процессы
            active_processes = [p for p in processes if p.poll() is None]

            # Если количество работающих стало меньше, чем мы запустили
            if len(active_processes) < count:
                print("Closure detected! Killing all other windows...")

                # Убиваем все процессы
                for p in processes:
                    if p.poll() is None:
                        try:
                            # Получаем объект процесса и убиваем его
                            parent = psutil.Process(p.pid)
                            for child in parent.children(recursive=True):
                                child.kill()
                            parent.kill()
                        except:
                            pass
                break

    except ValueError:
        print("Invalid number!")
    except Exception as e:
        print(f"Error: {e}")
        input("Press Enter to close...")


if __name__ == "__main__":
    launch_and_monitor()