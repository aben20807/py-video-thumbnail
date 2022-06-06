# py-video-thumbnail

Create thumbnail from a video (default 4x4).

## Environment
```bash
$ virtualenv -p python3 venv
$ source venv/bin/activate
$ pip install opencv-python
```

## Usage

```bash
$ git clone https://github.com/aben20807/py-video-thumbnail.git
$ cd py-video-thumbnail/
$ python pvt.py BigBuckBunny.mp4
# Or
$ python pvt.py *.mp4
```

## Optional

```bash
$ sudo mount -t drvfs '\\ben-nas\private' /mnt/share
$ sudo umount /mnt/share
```

## Result

![](img/BigBuckBunny.jpg)
