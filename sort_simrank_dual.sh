cd simrank_dual_filtered
for entry in *
do
  echo "$entry"
  sort -k3 -n $entry -r | head -n 100 > "../dual_simrank_sorted_head"/$entry
done
