
import os

# Root
root = os.getcwd()

# The dimensionality reduction methods, thus far
methods = ['PCA', 'KERNEL PCA']

# The data set that has been prepared for clustering.
data_urlstrings = ['https://github.com/discourses/hub/raw/develop/data/countries/us/environment/toxins/releases/data.zip']
attributes_urlstring = 'https://raw.githubusercontent.com/discourses/hub/develop/data/countries/us/environment/toxins/releases/attributes.csv'

# Unload Into
directory = os.path.join(root, 'data')

# Hence
data_ = os.path.join(directory, 'data')
attributes_ = os.path.join(directory, 'attributes.csv')

# The data must include a field of unique identifiers
exclude = ['COUNTYGEOID']
identifiers = ['COUNTYGEOID']