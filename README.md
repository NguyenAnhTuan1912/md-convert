# Convert to Markdown Test

Đây là repo thử nghiệm convert từ các file documents, media, ... sang Markdown.

## Benchmark

Hiện tại thì có thể xử lý khoảng 43 files trong 7.8s (máy mạnh thì có thể nhanh hơn).

![benchmark 1](./images/benchmark-1.png)

## Installation

Đầu tiên thì phải tạo môi trường ảo trước.

```bash
python3 -m venv venv
```

Tiếp theo là activate môi trường ảo.

```bash
source ./venv/bin/activate
```

Sau đó tiến hành cài đặt packages.

```bash
pip install .

# Cài thêm để chạy trong Local
pip install .[dev]
```

Tiếp theo là cái ChandraOCR

```bash
pip install chandra-ocr --prefer-binary
```

> Note: bài này được thử nghiệm trên Python 3.12.

### Warnings

Có một số lưu ý trong quá trình chạy script:

#### RuntimeWarning: Couldn't find ffmpeg or avconv - defaulting to ffmpeg, but may not work

Trường hợp này là do máy chưa cài các công cụ thích hợp để đọc ffmpeg hay avconv. Vì thế mà để khắc phục thì mình chỉ cần cài ffmpeg là được:

- Với Windows: cài ffmpeg từ https://ffmpeg.org/download.html, sau đó giải nén và thêm thư mục bin vào biến môi trường **PATH**.
- Với MacOS: cài từ brew.

```bash
brew install ffmpeg
```

- Với Linux (Ubuntu / Debian)

```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

#### Chandra OCR Installation Error

> Note: đa phần các máy sẽ không có, nên bạn cần cài đống này trước tiên để tránh lỗi các phát sinh không mong muốn.

> Note 2: tạm thời thì ChandraOCR vẫn chưa được sử dụng mà sẽ nằm ở trong kế hoạch về sau.

Nếu cài Chandra OCR mà bị lỗi như này có nghĩa là đang thiếu các gói FFmpeg.

```
× Getting requirements to build wheel did not run successfully.
  │ exit code: 1
  ╰─> [11 lines of output]
      Package libavformat was not found in the pkg-config search path.
      Perhaps you should add the directory containing `libavformat.pc'
      to the PKG_CONFIG_PATH environment variable
      Package 'libavformat' not found
      Package 'libavcodec' not found
      Package 'libavdevice' not found
      Package 'libavutil' not found
      Package 'libavfilter' not found
      Package 'libswscale' not found
      Package 'libswresample' not found
      pkg-config could not find libraries ['avformat', 'avcodec', 'avdevice', 'avutil', 'avfilter', 'swscale', 'swresample']
      [end of output]
```

- Với MacOS: cài từ brew.

```bash
brew install pkg-config ffmpeg
```

- Với Linux (Ubuntu / Debian)

```bash
sudo apt update
sudo apt install ffmpeg libavcodec-dev libavformat-dev libavdevice-dev \
                 libavutil-dev libavfilter-dev libswscale-dev libswresample-dev \
                 pkg-config
```

## How to run?

Để chạy thì gõ lệnh

```bash
python test/md_convert.test.py
```

Hoặc các file script khác.