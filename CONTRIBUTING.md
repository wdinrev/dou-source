# ⛩️ Panduan Kontribusi - Dou Extensions (動)

Terima kasih atas minat Anda untuk berkontribusi pada Dou. Repositori ini khusus merawat dan mengembangkan ekstensi anime berbahasa Indonesia untuk Anikku, Aniyomi, dan Dantotsu.

---

## Daftar Isi
1. [Prasyarat](#prasyarat)
2. [Struktur Repositori](#struktur-repositori)
3. [Menulis Ekstensi Baru](#menulis-ekstensi-baru)
   - [Struktur Folder](#1-struktur-folder)
   - [Konfigurasi build.gradle](#2-konfigurasi-buildgradle)
   - [Kelas Utama (AnimeHttpSource)](#3-kelas-utama-animehttpsource)
   - [Ekstraksi Video & Multi-Source](#4-ekstraksi-video--multi-source)
4. [Penanganan Konten NSFW](#penanganan-konten-nsfw)
5. [Testing & Build Lokal](#testing--build-lokal)
6. [Aturan Versi](#aturan-versi)
7. [Membuat Pull Request](#membuat-pull-request)

---

## Prasyarat
Sebelum mulai mengembangkan ekstensi, pastikan Anda telah menginstal:
* Java Development Kit (JDK) 17 (Temurin / OpenJDK 17).
* Android SDK (API Level 34+).
* Android Studio atau VS Code dengan ekstensi Kotlin & Gradle.
* Git.

---

## Struktur Repositori

```text
dou-source/
├── lib/               # Library ekstraktor video (dood, streamwish, vidhide, dll.)
├── lib-multisrc/      # Tema scraper bersama (animestream, dooplay, dll.)
├── src/
│   └── id/            # Murni seluruh ekstensi Anime Indonesia
│       ├── animeindo/
│       ├── nekopoi/
│       ├── otakudesu/
│       └── <nama-ekstensi-baru>/
└── .github/workflows/ # Pipeline CI/CD untuk otomatis build APK
```

---

## Menulis Ekstensi Baru

### 1. Struktur Folder
Setiap ekstensi berada di dalam direktori `src/id/<nama-sumber>/`:

```text
src/id/contoh/
├── build.gradle
├── res/
│   ├── mipmap-hdpi/ic_launcher.png
│   ├── mipmap-mdpi/ic_launcher.png
│   ├── mipmap-xhdpi/ic_launcher.png
│   ├── mipmap-xxhdpi/ic_launcher.png
│   └── mipmap-xxxhdpi/ic_launcher.png
└── src/eu/kanade/tachiyomi/animeextension/id/contoh/
    ├── Contoh.kt
    ├── Dto.kt       (opsional)
    └── Filters.kt   (opsional)
```

### 2. Konfigurasi build.gradle
Contoh `build.gradle` standar:

```groovy
ext {
    extName = 'ContohAnime'
    extClass = '.ContohAnime'
    extVersionCode = 1
    isNsfw = false // set true jika sumber khusus konten dewasa
}

apply plugin: "kei.plugins.extension.legacy"

dependencies {
    implementation(project(":lib:streamwishextractor"))
    implementation(project(":lib:doodextractor"))
}
```

### 3. Kelas Utama (AnimeHttpSource / ParsedAnimeHttpSource)
Setiap ekstensi harus mengimplementasikan alur scraping dasar:

```kotlin
package eu.kanade.tachiyomi.animeextension.id.contoh

import eu.kanade.tachiyomi.animesource.model.AnimeFilterList
import eu.kanade.tachiyomi.animesource.model.AnimesPage
import eu.kanade.tachiyomi.animesource.model.SAnime
import eu.kanade.tachiyomi.animesource.model.SEpisode
import eu.kanade.tachiyomi.animesource.model.Video
import eu.kanade.tachiyomi.animesource.online.ParsedAnimeHttpSource
import okhttp3.Request
import okhttp3.Response
import org.jsoup.nodes.Document
import org.jsoup.nodes.Element

class ContohAnime : ParsedAnimeHttpSource() {
    override val name = "ContohAnime"
    override val baseUrl = "https://contohanime.com"
    override val lang = "id"
    override val supportsLatest = true

    // 1. Popular Anime
    override fun popularAnimeRequest(page: Int): Request = GET("$baseUrl/popular/page/$page")
    override fun popularAnimeFromElement(element: Element): SAnime = ...
    override fun popularAnimeNextPageSelector(): String? = "a.next"

    // 2. Latest Updates
    override fun latestUpdatesRequest(page: Int): Request = GET("$baseUrl/latest/page/$page")
    override fun latestUpdatesFromElement(element: Element): SAnime = ...
    override fun latestUpdatesNextPageSelector(): String? = "a.next"

    // 3. Search Anime
    override fun searchAnimeRequest(page: Int, query: String, filters: AnimeFilterList): Request = ...
    override fun searchAnimeFromElement(element: Element): SAnime = ...
    override fun searchAnimeNextPageSelector(): String? = "a.next"

    // 4. Anime Details
    override fun animeDetailsParse(document: Document): SAnime = ...

    // 5. Episode List
    override fun episodeListSelector(): String = "ul.episodes li"
    override fun episodeFromElement(element: Element): SEpisode = ...

    // 6. Video Extractor
    override fun videoListParse(response: Response): List<Video> = ...
}
```

### 4. Ekstraksi Video & Multi-Source
* Selalu manfaatkan ekstraktor yang sudah tersedia di `lib/` (misal: `StreamWishExtractor`, `DoodExtractor`, `VidHideExtractor`, `FilemoonExtractor`, dll.).
* Jika website target menggunakan template CMS umum (seperti Animestream), daftarkan di `lib-multisrc/animestream`.

---

## Penanganan Konten NSFW
Ekstensi yang menyediakan konten dewasa (18+ / Hentai / Ecchi eksplisit) wajib mencantumkan:
```groovy
ext {
    ...
    isNsfw = true
}
```

---

## Testing & Build Lokal

Untuk menguji apakah ekstensi Anda bisa di-compile tanpa error:

```bash
# Build APK versi Debug
./gradlew :src:id:<nama-ekstensi>:assembleDebug

# Jalankan format & linter
./gradlew spotlessApply
```
File APK hasil build lokal akan berada di:
`src/id/<nama-ekstensi>/build/outputs/apk/debug/<nama-ekstensi>-debug.apk`

Anda dapat menginstal file APK tersebut langsung ke HP atau Emulator Android untuk pengujian di aplikasi Anikku, Aniyomi, atau Dantotsu.

---

## Aturan Versi

Ketika Anda melakukan perbaikan atau pembaruan domain:
1. Wajib menaikkan `extVersionCode` sebanyak +1 pada `build.gradle` ekstensi terkait.
2. Jika ada perubahan lib bersama, GitHub Actions akan otomatis mendeteksi dan meng-compile modul terdampak.

---

## Membuat Pull Request

1. Buat branch baru dari `main`:
   ```bash
   git checkout -b feat/tambah-sumber-xyz
   ```
2. Lakukan commit dengan pesan yang jelas (mengikuti Conventional Commits):
   * `feat(id/xyz): add new XYZ anime source`
   * `fix(id/xyz): update video extractor and fix baseUrl`
3. Pastikan `./gradlew spotlessApply` sudah dijalankan sebelum commit.
4. Buka Pull Request ke repository `wdinrev/dou-source` branch `main`.
5. CI akan otomatis memverifikasi build ekstensi Anda.
