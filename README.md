# terbilang-id

Library Python kecil dan CLI tanpa dependensi untuk mengubah bilangan bulat menjadi kata Bahasa Indonesia. Berguna untuk kuitansi, invoice, dokumen pembayaran, formulir, atau sebagai pemeriksa deterministik saat membuat teks dengan AI.

## Contoh CLI

```sh
terbilang-id 1250000 --rupiah
# satu juta dua ratus lima puluh ribu rupiah

terbilang-id 1.250.000
# satu juta dua ratus lima puluh ribu
```

Input menerima angka polos atau pemisah ribuan berupa titik/spasi yang konsisten. Koma dan nilai pecahan ditolak supaya tidak ambigu. Rentang yang didukung: `-999.999.999.999.999.999` sampai `999.999.999.999.999.999`.

## Sebagai library

```python
from terbilang_id import terbilang, terbilang_rupiah

terbilang(1250000)         # "satu juta dua ratus lima puluh ribu"
terbilang_rupiah(1250000)  # "satu juta dua ratus lima puluh ribu rupiah"
```

Instalasi (Python 3.9+):

```sh
python -m pip install .
```

Atau tanpa instalasi perintah:

```sh
python -m terbilang_id 1250000 --rupiah
```

## Batasan

Versi ini hanya menerima bilangan bulat; tidak mengolah pecahan/sen, nominal dengan mata uang lain, atau angka berbentuk kata. `terbilang-id` adalah konversi deterministik, bukan saran akuntansi atau hukum.

## Tes

```sh
python -m unittest discover -s tests -v
```

## Lisensi

MIT. Lihat [LICENSE](LICENSE).
