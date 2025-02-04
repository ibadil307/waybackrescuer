# WaybackRescuer
WaybackRescuer ini adalah sebuah skrip Python yang didesain untuk melakukan scanning terhadap arsip situs web menggunakan Wayback Machine, Dengan alat ini, Anda dapat:

- Mengambil Snapshot Arsip

  Menggunakan API CDX dari Wayback Machine untuk mengumpulkan snapshot dari domain target.
- Memeriksa Status Halaman

  Mengecek apakah URL yang diarsipkan masih aktif secara langsung melalui HTTP HEAD request.
- Mengunduh Halaman Arsip

  Secara otomatis mengunduh versi arsip dari halaman yang tidak responsif (error status) dengan menyimpannya ke direktori lokal.
- Menyediakan Ringkasan Hasil

  Menghasilkan file summary yang merangkum status setiap URL yang diperiksa serta informasi tentang proses pengunduhan. Hasil ini akan tersimpan secara local.

Skrip ini mengimplementasikan mekanisme retry untuk memastikan kestabilan koneksi, sehingga lebih tahan terhadap gangguan jaringan atau error sementara dari server.

#  Cara Menjalankan Script 
- Pastikan python3 sudah terinstall
- Jalankan terminal anda
- Jalankan scriptnya "python WaybackRescuer.py"
- Masukkan domain/URL target contoh "http://example.com" lalu tekan enter
- Hasil nya akan tersimpan otomatis di folder script ini disimpan contoh "E:\WaybackRescuer\downloads\example.com"
