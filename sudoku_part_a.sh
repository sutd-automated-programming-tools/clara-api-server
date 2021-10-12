# part-a cluster and feedback

#clara cluster examples/sudoku/part-a/a*.py --clusterdir clusters/sudoku/part-a --entryfnc string_to_grid \
#--args "[['534678912\n672195348\n198342567\n859761423\n426853791\n713924856\n961537284\n287419635\n345286179']]" \
#--ignoreio 1

clara feedback clusters/sudoku/part-a/c*.py incorrect/sudoku/part-a/a1.py  --entryfnc string_to_grid  \
--args "[['534678912\n672195348\n198342567\n859761423\n426853791\n713924856\n961537284\n287419635\n345286179']]" \
--ignoreio 1 --feedtype python
