import sqlite3
from flask import Flask
from flask import render_template
from flask import g 

from pippi import dsp
import math

# db config
DATABASE = 'data.db'

app = Flask(__name__)

def connect():
    return sqlite3.connect(DATABASE)

def ftpx(frames):
    """ Fixed scale of roughly 20 pixels 
        per second to test positioning shiz.
    """
    factor = 20.0 / 44100
    pixels = math.floor(frames * factor)
    return pixels

def make_tracks(numtracks):
    tracks = range(numtracks)

    g.db.execute('delete from `blocks`;')

    # Testing out display of rendered blocks
    for i, track in enumerate(tracks):
        blocks = range(dsp.randint(1, 5))

        # for each sound:
        for j, snd in enumerate(blocks):
            # render it.
            snd = dsp.tone(dsp.stf(dsp.rand(0.5, 5)))

            # filename is track_id-block_id.wav for now
            filename = "%i-%i-%i" % (i, j, 0)

            # write it to disk
            dsp.write(snd, 'static/sounds/%s' % filename)

            # Calc length in pixels from frames
            length = dsp.flen(snd)
            pxlength = "%ipx" % (length / 441,)
            slength = "%02fs" % dsp.fts(length)
            offset = dsp.stf(dsp.rand(0, 60))


            # save in the db
            block = ( 
                        0,
                        0,
                        i,
                        length,
                        length,
                        offset,
                        filename,
                    )
            g.db.execute('insert into `blocks` (version, generator_id, track_id, length, range, offset, filename) values (?, ?, ?, ?, ?, ?, ?)', 
                    block)

            c = g.db.cursor()
            block_id = c.lastrowid()

            # block is a tuple:
            #   (block index, filename, length in pixels, offset in pixels)
            blocks[j] = (block_id, filename, slength, ftpx(length), ftpx(offset))

        tracks[i] = blocks

    g.db.commit()

    return tracks

def load_tracks():
    pass

@app.before_request
def before_request():
    g.db = connect()

@app.teardown_request
def teardown_request(exception):
    g.db.close()


@app.route('/')
def index():
    tracks = []
    data = g.db.execute('select * from `blocks`')
    data = data.fetchall()
    tracks = [ [] for i in range(10) ]
    for i, row in enumerate(data):
        tracks[row[3]].append((row[0], row[7], dsp.fts(row[4]), ftpx(row[4]), ftpx(row[6])))

    return render_template('index.html', tracks=tracks, data=data)

@app.route('/blocks/regenerate/all')
def generate_all_blocks():
    tracks = make_tracks(10)
    return render_template('timeline.html', tracks=tracks)



if __name__ == '__main__':
    app.run(debug=True)
