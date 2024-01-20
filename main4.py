import argparse
import asyncio
import multiprocessing
import os
import threading
import time
import requests


def download_file(url, folder, name_proc):
    image_name = os.path.join(folder, os.path.basename(url))

    start_time_sin = time.time()

    download_image = requests.get(url)

    with open(image_name, "wb") as im_file:
        im_file.write(download_image.content)

    end_time_sin = time.time()

    #print(f"Время скачивания файла {name_proc}: {end_time_sin - start_time_sin}")


def download_images_multithread(urls, folder):
    threads = []
    for url in urls:
        thread = threading.Thread(target=download_file, args=(url, folder, "многопоточно"))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


def download_images_multiprocess(urls, folder):
    processes = []
    for url in urls:
        process = multiprocessing.Process(target=download_file, args=(url, folder, "многопроцессорно"))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()


async def download_images_async(urls, folder):
    loop = asyncio.get_event_loop()
    tasks = []

    for url in urls:
        task = loop.run_in_executor(None, lambda: download_file(url, folder, "асинхронно"))
        tasks.append(task)

    await asyncio.gather(*tasks)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", choices=["manual", "array"], default="array")
    parser.add_argument("--folder")
    args = parser.parse_args()

    if args.source == "array":
        urls = ["https://w.forfun.com/fetch/4a/4af0bcc2b0c34fd573eca9f1be9ab245.jpeg",
                "https://gas-kvas.com/uploads/posts/2023-02/1675495569_gas-kvas-com-p-luchshie-kartinki-dlya-fonovogo-risunka-ra-31.jpg",
                "https://avatanplus.com/files/resources/original/579091ceb27a91560cb98f8b.jpg",
                "https://mobimg.b-cdn.net/v3/fetch/f4/f4e488ef69ea10573c0ce9cfbaf08643.jpeg",
                "https://gas-kvas.com/uploads/posts/2023-02/1675489758_gas-kvas-com-p-izobrazheniya-i-kartinki-na-fonovii-risuno-41.jpg"
                ]
    else:
        urls = input("Введите URL адреса через пробел для скачивания: ").split()

    folder = args.folder if args.folder else os.getcwd()

    start_time_sin = time.time()

    # Синхронный подход
    for url in urls:
        download_file(url, folder, "синхронно")
    end_time_sin = time.time()
    print(f"Суммарное время выполелния синхронного: {end_time_sin - start_time_sin}")
    start_time_theard = time.time()
    # Многопоточный подход
    download_images_multithread(urls, folder)
    end_time_theard= time.time()
    print(f"Суммарное время выполелния многопоточного: {end_time_theard - start_time_theard}")

    start_time_proc = time.time()
    # Многопроцессорный подход
    download_images_multiprocess(urls, folder)
    end_time_proc = time.time()
    print(f"Суммарное время выполелния многопроцессорного: {end_time_proc - start_time_proc}")

    start_time_asin = time.time()
    # Асинхронный подход
    loop = asyncio.get_event_loop()
    loop.run_until_complete(download_images_async(urls, folder))

    end_time_asin = time.time()

    print(f"Суммарное время выполелния асинхронного: {end_time_asin - start_time_asin}")


if __name__ == "__main__":
    main()
