
import requests
import json
import os
from urllib.parse import urlparse
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

def create_session_with_retries(total_retries=5, backoff_factor=1, status_forcelist=None, timeout=60):
    if status_forcelist is None:
        status_forcelist = [429, 500, 502, 503, 504]

    session = requests.Session()
    retries = Retry(
        total=total_retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist
    )
    adapter = HTTPAdapter(max_retries=retries)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    return session, timeout

def get_wayback_snapshots(domain):
    cdx_url = (
        f"https://web.archive.org/cdx/search/cdx?"
        f"url={domain}/*&output=json&fl=original,timestamp&collapse=urlkey"
    )

    session, timeout = create_session_with_retries()
    snapshots = []

    try:
        resp = session.get(cdx_url, timeout=timeout)
        resp.raise_for_status()
        data = resp.json()

        # Baris pertama biasanya header ["original", "timestamp"]
        for row in data[1:]:
            original_url, timestamp = row
            snapshots.append((original_url, timestamp))

    except Exception as e:
        print(f"Error mengambil data dari Wayback Machine: {e}")

    return snapshots

def check_url_status(url):
    session, timeout = create_session_with_retries()
    try:
        resp = session.head(url, timeout=timeout)
        return resp.status_code
    except Exception as e:
        print(f"Error cek status {url}: {e}")
        return 999 

def download_from_wayback(url, timestamp, domain):
    archived_url = f"https://web.archive.org/web/{timestamp}if_/{url}"
    parsed = urlparse(url)
    filename = os.path.basename(parsed.path) or "index.html"
    domain_folder = domain.replace("://", "_").replace("/", "_")
    output_dir = os.path.join("downloads", domain_folder)
    os.makedirs(output_dir, exist_ok=True)

    save_path = os.path.join(output_dir, f"{timestamp}_{filename}")

    session, timeout = create_session_with_retries()

    try:
        resp = session.get(archived_url, timeout=timeout)
        if resp.status_code == 200:
            with open(save_path, "wb") as f:
                f.write(resp.content)
            print(f"Berhasil mengunduh: {archived_url} -> {save_path}")
            return save_path
        else:
            print(f"Gagal mengunduh: {archived_url} (status: {resp.status_code})")
    except Exception as e:
        print(f"Error mengunduh {archived_url}: {e}")

    return None

def save_summary(domain, all_results):
    domain_folder = domain.replace("://", "_").replace("/", "_")
    output_dir = os.path.join("downloads", domain_folder)
    os.makedirs(output_dir, exist_ok=True)

    summary_path = os.path.join(output_dir, "summary.txt")

    try:
        with open(summary_path, "w", encoding="utf-8") as f:
            f.write("creator by : ibadil\n")
            f.write(f"Hasil Scan untuk Domain: {domain}\n")
            f.write(f"Total URL yang dicek: {len(all_results)}\n\n")
            for item in all_results:
                info = (
                    f"URL: {item['url']}\n"
                    f"Status Live: {item['status']}\n"
                )
                if item["downloaded"]:
                    info += f"Download: Berhasil dari arsip -> {item['download_path']}\n"
                else:
                    info += "Download: Tidak diunduh (URL masih valid / atau gagal)\n"

                info += "-"*50 + "\n"
                f.write(info)

        print(f"Summary disimpan di: {summary_path}")
    except Exception as e:
        print(f"Gagal menyimpan summary untuk {domain}: {e}")

def main():
    print("creator by : ibadil")
    target_domain = input("Masukkan domain/URL target (misal: http://example.com): ")

    snapshots = get_wayback_snapshots(target_domain)
    print(f"Total snapshot ditemukan: {len(snapshots)} untuk {target_domain}")

    all_results = []

    try:
        for original_url, timestamp in snapshots:
            status = check_url_status(original_url)
            downloaded_path = None
            downloaded_flag = False

            if status >= 400:
                print(f"URL {original_url} tidak tersedia (status {status}). Mencoba unduh dari arsip.")
                downloaded_path = download_from_wayback(original_url, timestamp, target_domain)
                if downloaded_path:
                    downloaded_flag = True
            else:
                print(f"URL {original_url} masih valid (status {status}).")

            all_results.append({
                "url": original_url,
                "status": status,
                "downloaded": downloaded_flag,
                "download_path": downloaded_path
            })

    except KeyboardInterrupt:
        print("\nProses dihentikan oleh pengguna (Ctrl + C).")
    finally:
        print("Menyimpan hasil (summary)...")
        save_summary(target_domain, all_results)

if __name__ == "__main__":
    main() 
