# tsd
The tsd is a tiny software written in Rust, getting links of ts media files in your given m3u8 url, and then donwloading and converting them into a single MP4 file.
## Usage
```shell
tsd [m3u8-url] [output] [-p|--proxy]

```
Example: 
* with proxy mode: tsd http://xxx.m3u8 yyy.mp4 -p http://localhost:8001. 
* without proxy mode: tsd http://xxx.m3u8 yyy.mp4

**Note** that the argument ```p``` is used to send all request throngh proxy tool like ```v2ray``` or ```shadowsocks``` which has built-in http proxy mode that should be opened when you run the tsd program. It's an optional item.

## Installation
Previously in installation, make sure that you have already installed ```rust``` and its toolchain. Then type and run below command in your terminal for installing.
```shell
git clone git@github.com:playahammer/tools.git
cd tools/tsd
cargo install --path ./
```
Due to successfully convert serveral ```ts``` files into an integrated MP4, you firstly should install ```ffmpeg``` whose version at least is ```4.4```. The configure of ffmpeg in my computer **macOS Big Sur 11.5.2** shows as follow:
```
ffmpeg version 4.4 Copyright (c) 2000-2021 the FFmpeg developers
  built with Apple clang version 12.0.0 (clang-1200.0.32.29)
  configuration: --prefix=/usr/local/Cellar/ffmpeg/4.4_1 --enable-shared --enable-pthreads --enable-version3 --enable-avresample --cc=clang --host-cflags= --host-ldflags= --enable-ffplay --enable-gnutls --enable-gpl --enable-libaom --enable-libbluray --enable-libdav1d --enable-libmp3lame --enable-libopus --enable-librav1e --enable-librubberband --enable-libsnappy --enable-libsrt --enable-libtesseract --enable-libtheora --enable-libvidstab --enable-libvorbis --enable-libvpx --enable-libwebp --enable-libx264 --enable-libx265 --enable-libxml2 --enable-libxvid --enable-lzma --enable-libfontconfig --enable-libfreetype --enable-frei0r --enable-libass --enable-libopencore-amrnb --enable-libopencore-amrwb --enable-libopenjpeg --enable-libspeex --enable-libsoxr --enable-libzmq --enable-libzimg --disable-libjack --disable-indev=jack --enable-videotoolbox
  libavutil      56. 70.100 / 56. 70.100
  libavcodec     58.134.100 / 58.134.100
  libavformat    58. 76.100 / 58. 76.100
  libavdevice    58. 13.100 / 58. 13.100
  libavfilter     7.110.100 /  7.110.100
  libavresample   4.  0.  0 /  4.  0.  0
  libswscale      5.  9.100 /  5.  9.100
  libswresample   3.  9.100 /  3.  9.100
  libpostproc    55.  9.100 / 55.  9.100
Hyper fast Audio and Video encoder
usage: ffmpeg [options] [[infile options] -i infile]... {[outfile options] outfile}...
```
## TODO

