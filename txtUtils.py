#!/usr/bin/env python3
# coding: utf-8

import html
import time
import re
import os

import click

from lib.textProcessor import content_handle
from lib.logger import LOG
from lib import T


@click.command()
@click.option("--mode", default=2, help="TXTMODE for handle content. DEFAULT=2")
@click.option(
    "--chapter_type", default="text", help="chapterType looked on line. DEFAULT=text"
)
@click.option("--ocr_mode", default="0", help="remove all line wrap. DEFAULT=0")
def main(mode, chapter_type, ocr_mode):
    """A TXT CLI Tool for handling novel content."""
    txtencode = input("encoding?")
    concat = input("concat?").upper()
    h = html
    t = str(int(time.time()))

    files = [f for f in os.listdir(".") if os.path.isfile(f)]
    files.sort()
    chunks = []
    for f in files:
        matched = re.match("(?P<title>.*?)(?P<ext>(?:.txt$|php$))", f)
        if matched == None:
            continue
        LOG(f)
        avaliable_matched = matched
        if (
            re.match("(?:.txt$|.php$)", avaliable_matched.group("ext").lower())
            and f[:5] != "done-"
            and f[:12] != "requirements"
        ):
            with open(f, "rb") as fd:
                buf = fd.read().decode(txtencode, "ignore")
                LOG("[BUF][Start] %s" % len(buf))
                buf = content_handle(
                    buf,
                    treat_as_pure_text=str(mode),
                    chapterType=chapter_type,
                    ocrMode=ocr_mode,
                )
                LOG("[BUF][End] %s" % len(buf))
                if concat == "N":
                    with open(
                        "done-%s-%s%s"
                        % (
                            avaliable_matched.group("title"),
                            T,
                            avaliable_matched.group("ext"),
                        ),
                        "w",
                    ) as fd2:
                        fd2.write(buf)
                else:
                    chunks.append(buf)
    if len(chunks) > 0:
        with open(
            "done-all-%s-%s%s"
            % (avaliable_matched.group("title"), T, avaliable_matched.group("ext")),
            "w",
        ) as fd2:
            fd2.write("".join(chunks))


if __name__ == "__main__":
    main()
