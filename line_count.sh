# check if first argument is provided
if [ -z "$1" ]; then
    echo "Error: No directory specified"
    exit 1
fi

# check if first argument is a directory
if [ ! -d "$1" ]; then
    echo "Error: $1 is not a directory"
    exit 1
fi

find "$1" \
    -type d -name .venv -prune -o \
    -type d -name node_modules -prune -o \
    -type d -name playwright-report -prune -o \
    -type d -name test-results -prune -o \
    -type f -exec cat {} + | wc -l