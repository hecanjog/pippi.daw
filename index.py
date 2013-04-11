from flask import Flask
from flask import render_template
from pippi import dsp

app = Flask(__name__)

@app.route('/')
def index():
    tracks = range(10)

    # Testing out display of rendered blocks
    for i, track in enumerate(tracks):
        blocks = range(dsp.randint(1, 5))

        # for each sound:
        for j, snd in enumerate(blocks):
            # render it.
            snd = dsp.tone(dsp.randint(100, 10000))

            # filename is track_id-block_id.wav for now
            filename = "%i-%i" % (i, j)

            # write it to disk
            dsp.write(snd, 'static/sounds/%s' % filename)

            # Calc length in pixels from frames
            length = dsp.flen(snd)
            pxlength = "%ipx" % (length / 41,)
            slength = "%02fs" % dsp.fts(length)

            # block is a tuple:
            #   (block index, filename, length in pixels)
            blocks[j] = (j, filename, slength, pxlength)

        tracks[i] = blocks

    return render_template('index.html', tracks=tracks)

if __name__ == '__main__':
    app.run(debug=True)
