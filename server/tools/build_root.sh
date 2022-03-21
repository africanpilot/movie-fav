#/bin/bash
set -e

ln -s /usr/local/bin/python /usr/bin/python

chown -R moviefav:moviefav /home/moviefav

# for d in / ~moviefav ~root /etc; do
#     cp /home/moviefav/server/tools/NOTICE $d
#     chmod -w $d/NOTICE
# done
