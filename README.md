# Version 1.0 : Script tool for doing with manga

## Setting up the environment

1. Install Python 3.10 or higher link [here](https://www.python.org/downloads/)
2. Create a virtual environment

```
python -m venv venv
```

3. Activate the virtual environment

```
.\venv\Scripts\activate
```

4. Install the required packages

```
pip install -r requirements.txt
```

## Run the script

1. Download the manga

```
python -m tasks.DownloadManga
```

| Option | Argument | Description                                                                |
| ------ | -------- | -------------------------------------------------------------------------- |
| -l     | L        | Link to the manga page                                                     |
| -n     | N        | Number of chapters to download (-1: all chapters, !-1: number of chapters) |
| -s     | S        | Server to download from (1: nettruyen, 2: mangasee)                        |
| -s_i   | S_I      | Start index (-1: top down -- default, !-1: start from index)               |

Example 1: Download from mangasee

```
python -m tasks.DownloadManga -l https://mangasee123.com/read-online/Kanojo-Okarishimasu-chapter-357-page-1.html -n -1 -s 2 -s_i 0
```

Example 2: Download from nettruyen

```
python -m tasks.DownloadManga -l https://nettruyen.com/truyen/one-piece -n -1 -s 1 -s_i 0
```

2. Create metadata manga

```
python -m tasks.CreateMetadata
```

| Option | Argument | Description      |
| ------ | -------- | ---------------- |
| -b     | B        | Bookmark file    |
| -c     | C        | Comic info file  |
| -o     | O        | Target folder    |
| -m     | -        | Multiple folders |

Example multiple folders:

```
python -m tasks.CreateMetadata -c ./resource/comicInfo.json -o 'Rent a Girlfriend' -m
```

Example single folder:

```
python -m tasks.CreateMetadata -b ./resource/bookmarks.json -c ./resource/comicInfo.json -o 'Rent a Girlfriend'
```

3. Archive the manga

```
python -m tasks.ArchiveFolders
```

| Option | Argument | Description                           |
| ------ | -------- | ------------------------------------- |
| -o     | O        | Target folder                         |
| -m     | -        | Multiple folders                      |
| -d     | -        | Delete folders after archiving        |

Example:

```
python -m tasks.ArchiveFolders -o 'Rent a Girlfriend' -m -d
```

3. Download the covers

```
python -m tasks.DownloadCovers
```
| Option | Argument | Description      |
| ------ | -------- | ---------------- |
| -l     | L        | Link to mangadex |

Example:

```
python -m tasks.DownloadCovers -l https://mangadex.org/title/32fdfe9b-6e11-4a13-9e36-dcd8ea77b4e4/rent-a-girlfriend?tab=art
```

4. Resize the images

```
python -m tasks.ResizeImages
```
