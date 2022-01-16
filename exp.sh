clara cluster submissions/exp/term1/p1/a*.py --clusterdir clusters/exp/term1/p1 --entryfnc search_position \
--args  "[[[1,3,5,6],7],[[1,3,5,6],0],[[1],0]]" \
--ignoreio 1

#clara feedback clusters/exp/term1/p2/c*.py incorrect/incorrect.py  --entryfnc add_two  \
#--args  "[[[2,4,3],[5,6,4]],[[0],[0]],[[9,9,9,9,9,9,9],[9,9,9,9]]]" \
#--ignoreio 1 --feedtype python \
#--verbose
#

#clara cluster submissions/exp/term3/p1/a*.py --clusterdir clusters/exp/term3/p1 --entryfnc two_sum \
#--args  "[[[2,7,11,15],9],[[3,2,4],6],[[3,3],6]]" \
#--ignoreio 1
