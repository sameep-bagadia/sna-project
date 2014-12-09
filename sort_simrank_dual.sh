cd simrank_dual
for entry in *
do
  echo "$entry"
  sort -k3 -n $entry -r | head -n 1000 > "../dual_simrank_sorted_head"/$entry
done
