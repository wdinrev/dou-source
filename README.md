# ⛩️ Dou Extensions (動)

<div align="center">

[![CI](https://github.com/wdinrev/dou-source/actions/workflows/build_push.yml/badge.svg)](https://github.com/wdinrev/dou-source/actions/workflows/build_push.yml)

**Repository Ekstensi Anime Khusus Sumber Indonesia untuk Aniyomi, Anikku, Dantotsu, & Mihon variants.**

</div>

---

## 📥 Cara Menambahkan Repo

Di aplikasi Anda (Aniyomi / Anikku / Dantotsu), masuk ke:
**Settings > Browse > Extension repositories > Add Repository**
```text
https://raw.githubusercontent.com/wdinrev/dou-repo/main/index.min.json
```

---

## 🧩 Sumber yang Tersedia (Indonesian Sources)

- **AnimeIndo**
- **Kuramanime**
- **Kuronime**
- **MiniOppai** (NSFW)
- **Nekopoi** (NSFW)
- **Neonime**
- **NimeGami**
- **Oploverz**
- **OtakuDesu**
- **Samehadaku**

---

## 🛠️ Pengembangan & Kontribusi

1. Pastikan terinstall JDK 17 dan Android SDK.
2. Buat ekstensi baru di folder `src/id/<nama-sumber>`.
3. Jalankan build lokal:
   ```bash
   ./gradlew :src:id:<nama-sumber>:assembleDebug
   ```

---

## 📜 Lisensi
Kode ekstensi dilisensikan di bawah lisensi [Apache 2.0](LICENSE).
Semua konten video dan media disediakan langsung oleh situs pihak ketiga dan tidak berafiliasi dengan repositori ini.
