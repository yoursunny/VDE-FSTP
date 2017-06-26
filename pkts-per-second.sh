#!/bin/bash
# count packets transmitted or received per second

DURATION=${1:-60}

for F in /tmp/myfifo-*; do
  tshark -r $F | awk '{ print int($2) }'
done | sort -n | uniq -c |\
awk '
  BEGIN { t=0 }
  t<$2 { print 0; ++t }
  { print $1; ++t }
  END { for (; t<'$DURATION'; ++t) { print 0 } }
'
