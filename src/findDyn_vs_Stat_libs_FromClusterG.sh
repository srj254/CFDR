#!/bin/bash

use_tmp=true

# Make some temporary files
if $use_tmp; then
    libdirs_file=$(mktemp)
    libs_file=$(mktemp)
else
    libdirs_file=libdirs.txt
    libs_file=libs.txt
    rm -f $libdirs_file
    rm -f $libs_file
fi
rm -f libs.out


for dir in "$@"; do
    echo $dir
    find "$dir" -maxdepth 4 -mtime -1825 -type d -a \( -name 'lib' -o -name lib64 \)  > $libdirs_file #2>/dev/null

    for dir in $(cat "$libdirs_file"); do
        find $dir -maxdepth 2 -type f -name "lib*" >> $libs_file #2>/dev/null
    done

    # filter out only unique .so and .a names w/o versions.
    cat "$libs_file" | \
        perl -pe 's/^(.*lib[^\/]*\.(so|a))(.\d+)*/\1/' | \
        perl -pe 's/.*(lib[^\/]*)\.(so|a)/\1.\2/' | \
        perl -pe 's/[\d\._\-]*\.(so|a)$/.\1/' |\
        grep -v vtk |\
        sort | uniq | \
        grep '\.so$\|\.a$' \
        >> libs.out 2>/dev/null

done

# count static vs dynamic libs
cat libs.out | \
perl -pe 's/.*.a$/.a/; s/.*.so$/.so/' | sort | uniq -c

#rm "$libdirs_file"
#rm "$libs_file"

