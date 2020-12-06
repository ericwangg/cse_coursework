#!/usr/bin/bash

patterns=('a*e' 'm*c' 'd*txt' 'X*1' 
    'a*' 'app*' 'd*' 
    '*conf' '*fs.conf' 
    'dat*.txt' 'data*08.txt' 'data*a08.txt' 
    '*' '*LongLongFilename' 'abcd*' 'abcd*abcdef'
    )
INPUTFN='filenames.txt'
TMPFN='tmp-myglob.out'

set -e
make
trap "echo 'Error: output from last run does not look correct'; cat $TMPFN" ERR

echo "Test globbing from stdin ..."
for p in "${patterns[@]}"; do
	echo "./myglob - - '$p' < $INPUTFN > $TMPFN"
	./myglob - - "$p" < "$INPUTFN" > "$TMPFN" 
	# if [[ "$p" = "*fs.conf" ]]; then  echo "something" >> "$TMPFN"; fi  
	diff "$TMPFN" <(bash ./glob.sh "$p")
done

echo "Your program seems to work fine with all the patterns in this test."

echo "Test redirecting stdin ..."
p='a*'
echo "./myglob $INPUTFN - '$p' > $TMPFN" 
./myglob "$INPUTFN" - "$p" > "$TMPFN" 
# cat "$TMPFN"
diff "$TMPFN" <(bash ./glob.sh "$p")

echo "Test redirecting stdin and stdout ..."
echo "./myglob $INPUTFN $TMPFN '$p'" 
./myglob "$INPUTFN" "$TMPFN" "$p"
# cat "$TMPFN"
diff "$TMPFN" <(bash ./glob.sh "$p")

echo "Your program seems to have redirected stdin and stdout correctly."
rm -rf "$TMPFN"
