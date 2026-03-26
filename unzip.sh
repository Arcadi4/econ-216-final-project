#!/bin/bash
pushd data || exit
find . -name '*.zip' | while read -r zipfile; do
	dirname="${zipfile%.zip}"
	unzip "$zipfile" -d "$dirname" && rm "$zipfile"
	cd "$dirname"
	topdirs=($(find . -mindepth 1 -maxdepth 1 -type d))
	if [ ${#topdirs[@]} -eq 1 ]; then
		mv "${topdirs[0]}"/* . && rmdir "${topdirs[0]}"
	fi
	cd - >/dev/null
done
popd || exit
