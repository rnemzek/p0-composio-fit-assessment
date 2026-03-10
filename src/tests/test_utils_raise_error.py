import os
import sys
from src.utils.util import Util

print("🚀 Starting test on util class!")
print("⛯ Usage: raiseError(v_name, v_value, env_variable")
v_name = sys.argv[1]       # if len(sys.argv) > 1 else "MISSING"
v_value = sys.argv[2]      # if len(sys.argv)  > 2 else "MISSING"
env_variable = sys.argv[3] # if len(sys.argv) > 3 else "MISSING"

# Create test object
raise_error_test = Util()

# Run test
print("📋 Preparing to run test:" +
     f" v_name = {v_name}" +
     f" | v_value = {v_value}" +
     f" | env_variable = {env_variable}")
print("Running test")
try:
    raise_error_test.raiseError(v_name, v_value, env_variable)
    print("✅ Test passed!")
except ValueError as e:
    print("❌ Test failed!")
    print(e)


