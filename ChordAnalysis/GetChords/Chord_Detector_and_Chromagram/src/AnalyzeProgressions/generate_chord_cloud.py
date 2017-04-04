#!/usr/bin/env python
"""
Image-colored wordcloud
========================
You can color a word-cloud by using an image-based coloring strategy
implemented in ImageColorGenerator. It uses the average color of the region
occupied by the word in a source image. You can combine this with masking -
pure-white will be interpreted as 'don't occupy' by the WordCloud object when
passed as mask.
If you want white as a legal color, you can just pass a different image to
"mask", but make sure the image shapes line up.
"""

from os import path
from PIL import Image
from count_chords import count_chords
import numpy as np
import matplotlib.pyplot as plt

from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

d = '.'

# Read the whole text.
#text = open(path.join(d, 'clef.txt')).read()
chord_counts = count_chords()
text = ''
for chord in chord_counts:
    chord_space = chord + ' '
    text += chord_space * chord_counts[chord]

clef_mask = np.array(Image.open(path.join(d, "g_clef_mask.png")))

stopwords = set(STOPWORDS)
stopwords.add("said")

wc = WordCloud(background_color="white", max_words=2000, mask=clef_mask,
               stopwords=stopwords)
# generate word cloud
wc.generate(text)

# store to file
wc.to_file(path.join(d, "clef.png"))

# show
plt.imshow(wc, interpolation='bilinear')
plt.axis("off")
plt.figure()
plt.imshow(clef_mask, cmap=plt.cm.gray, interpolation='bilinear')
plt.axis("off")
plt.show()
