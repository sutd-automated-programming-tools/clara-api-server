if [[ $1 -eq 1 ]]
then
  make > /dev/null 2>&1
fi

# part-a cluster and feedback

. sudoku_part_a.sh

#part b cluster and feedback

. sudoku_part_b.sh

#part c cluster and feedback

. sudoku_part_c.sh

#part d cluster and feedback

. sudoku_part_d.sh

#mkdir -p "clusters/sudoku/part-a" "clusters/sudoku/part-b" "clusters/sudoku/part-c" "clusters/sudoku/part-d" "clusters/sudoku/part-e" "clusters/sudoku/part-f"

#part e cluster and feedback

. sudoku_part_e.sh

#part f cluster and feedback

. sudoku_part_f.sh
