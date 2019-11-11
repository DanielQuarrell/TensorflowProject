import sys

import tensorflow.keras
import pandas
import tensorflow

print(f"Tensor Flow Version: {tensorflow.__version__}")
print(f"Keras Version: {tensorflow.keras.__version__}")
print()
print(f"Python {sys.version}")
print(f"Pandas Version: {pandas.__version__}")
print("GPU Availibility: ", "Available" if tensorflow.test.is_gpu_available() else "Not Available")