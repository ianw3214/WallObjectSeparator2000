import sys

if len(sys.argv) > 1:
    index = sys.argv.index("--") + 1
    argv = sys.argv[index:]
    print(argv)
else:
    print("NOO")
