clara cluster examples/sudoku/part-f/*.py --clusterdir clusters/sudoku/part-f --entryfnc check_sudoku \
--args "[['534678912\n672195348\n198342567\n859761423\n426853791\n713924856\n961537284\n287419635\n345286179\n'],['534678912\n672195348\n198342567\n859761423\n426853791\n713924856\n961537284\n287419635\n'],['534678912\n67219534\n198342567\n859761423\n426853791\n713924856\n961537284\n287419635\n345286179\n'],['504678912\n672195348\n198342567\n859761423\n426853791\n713924856\n961537284\n287419635\n345286179\n'],['534678912\n677195348\n198342567\n859761423\n426853791\n713924856\n961537284\n287419635\n345286179\n'],['534678912\n677195348\n197342567\n859761423\n426853791\n713924856\n961537284\n287419635\n345286179\n'],['\n534678912\n677195348\n198342567\n859761423\n426873791\n713924856\n961537284\n287419635\n345286179\n']]" \
--ignoreio 1

clara feedback clusters/sudoku/part-f/c*.py incorrect/sudoku/part-f/i1.py  --entryfnc check_sudoku  \
--args "[['534678912\n672195348\n198342567\n859761423\n426853791\n713924856\n961537284\n287419635\n345286179\n'],['534678912\n672195348\n198342567\n859761423\n426853791\n713924856\n961537284\n287419635\n'],['534678912\n67219534\n198342567\n859761423\n426853791\n713924856\n961537284\n287419635\n345286179\n'],['504678912\n672195348\n198342567\n859761423\n426853791\n713924856\n961537284\n287419635\n345286179\n'],['534678912\n677195348\n198342567\n859761423\n426853791\n713924856\n961537284\n287419635\n345286179\n'],['534678912\n677195348\n197342567\n859761423\n426853791\n713924856\n961537284\n287419635\n345286179\n'],['\n534678912\n677195348\n198342567\n859761423\n426873791\n713924856\n961537284\n287419635\n345286179\n']]" \
--ignoreio 1 --feedtype python
