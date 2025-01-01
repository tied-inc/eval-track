"""Check required dependencies for testing."""

try:
    from importlib.util import find_spec

    if find_spec("boto3"):
        print("boto3 available")
    else:
        print("boto3 not available")
except ImportError:
    print("boto3 not available")
