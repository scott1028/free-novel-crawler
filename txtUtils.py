#!/usr/bin/env python3
# coding: utf

from lib import *


@click.command()
@click.option('--mode', default=2, help='TXTMODE for handle content. DEFAULT=2')
def main(mode):
    """A TXT CLI Tool for handling novel content."""
    txtencode = input('encoding?')
    concat = input('concat?').upper()
    h = HTMLParser()
    t = str(int(time.time()))

    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    files.sort()
    chunks = []
    for f in files:
        matched = re.match('(?P<title>.*?)(?P<ext>(?:.txt$|php$))', f)
        if matched == None:
            continue
        LOG(f)
        avaliable_matched = matched
        if re.match('(?:.txt$|.php$)', avaliable_matched.group('ext').lower()) and f[:5] != 'done-' and f[:12] != 'requirements':
            with open(f, 'rb') as fd:
                buf = fd.read().decode(txtencode, 'ignore')
                LOG('[BUF][Start] %s' % len(buf))
                buf = content_handle(buf, treat_as_pure_text=str(mode))
                LOG('[BUF][End] %s' % len(buf))
                if concat == 'N':
                    with open('done-%s-%s%s' % (avaliable_matched.group('title'), T, avaliable_matched.group('ext')), 'w') as fd2:
                        fd2.write(buf)
                else:
                    chunks.append(buf)
    if len(chunks) > 0:
        with open('done-all-%s-%s%s' % (avaliable_matched.group('title'), T, avaliable_matched.group('ext')), 'w') as fd2:
            fd2.write(''.join(chunks))

if __name__ == "__main__":
    main()
