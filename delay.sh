#find . | grep -E "settings.py$" | xargs sed -i '' "s/DOWNLOAD_DEALY = [0-9]+/DOWNLOAD_DELAY=$1/g"
find . | grep -E "settings.py$" | xargs sed -E -i '' "s/DOWNLOAD_DELAY = [0-9]+/DOWNLOAD_DELAY = $1/g"
