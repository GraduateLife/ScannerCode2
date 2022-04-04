from PIL import Image
import random
import pandas as pd
import matplotlib.pyplot as plt
import math
import random
import numpy as np
import scipy.misc
import imageio


image_array = pd.read_csv('FFTOutput.csv')



imageio.imwrite('outfile.jpg', image_array)



