#!/bin/bash -ue

file_list=(
    '../kpt4a/KPT4A_01.png' #0
    '../kpt4a/KPT4A_02.png'
    '../kpt4a/KPT4A_03.png'
    '../kpt4a/KPT4A_04.png' #3

    '../HIH/HIH_01.png' #4
    '../HIH/HIH_02.png'
    '../HIH/HIH_03.png'
    '../HIH/HIH_04.png' #7
    
    '../E5/E5_1.png' #8
    '../E5/E5_2.png'
    '../E5/E5_3.png'
    '../E5/E5_4.png'
    '../E5/E5_5.png'
    '../E5/E5_6.png'
    '../E5/E5_7.png'
    '../E5/E5_8.png'
    '../E5/E5_9.png'
    '../E5/E5_10.png'
    '../E5/E5_11.png'
    '../E5/E5_12.png'
    '../E5/E5_13.png'
    '../E5/E5_14.png' #21

    '../F5/F5_1.png' #22
    '../F5/F5_2.png'
    '../F5/F5_3.png'
    '../F5/F5_4.png'
    '../F5/F5_5.png'
    '../F5/F5_6.png'
    '../F5/F5_7.png'
    '../F5/F5_8.png'
    '../F5/F5_9.png'
    '../F5/F5_10.png'
    '../F5/F5_11.png'
    '../F5/F5_12.png'
    '../F5/F5_13.png'
    '../F5/F5_14.png' #35

    # layouts
    '../HIH/HIH_layout.png' #36
    '../E5/E5_layout.png' #37
    '../F5/F5_layout.png' #38
    '../kpt4a/kpt4a_layout.png' #39
)


####################################### KPT
s=0
e=3
for idx1 in $(seq $s 1 $e)
do
    for idx2 in $(seq $(($idx1+1)) 1 $e)
    do
    	img_src=${file_list[$idx1]}
    	img_dst=${file_list[$idx2]}
    	echo $idx1 $idx2 - $img_src and $img_dst
    	python manual_associator.py --img_src $img_src --img_dst $img_dst
    done
    idx2=39
    img_src=${file_list[$idx1]}
    img_dst=${file_list[$idx2]}
    echo $idx1 $idx2 - $img_src and $img_dst
    python manual_associator.py --img_src $img_src --img_dst $img_dst
done

# ####################################### HIH
# s=4
# e=7
# for idx1 in $(seq $s 1 $e)
# do
#     for idx2 in $(seq $(($idx1+1)) 1 $e)
#     do
# 	img_src=${file_list[$idx1]}
# 	img_dst=${file_list[$idx2]}
# 	echo $idx1 $idx2 - $img_src and $img_dst
#     	python manual_associator.py --img_src $img_src --img_dst $img_dst
#     done
#     idx2=36
#     img_src=${file_list[$idx1]}
#     img_dst=${file_list[$idx2]}
#     echo $idx1 $idx2 - $img_src and $img_dst
#     python manual_associator.py --img_src $img_src --img_dst $img_dst
# done

# ####################################### E5
# s=8
# e=21
# for idx1 in $(seq $s 1 $e)
# do
#     for idx2 in $(seq $(($idx1+1)) 1 $e)
#     do
# 	img_src=${file_list[$idx1]}
# 	img_dst=${file_list[$idx2]}
# 	echo $idx1 $idx2 - $img_src and $img_dst
#     	python manual_associator.py --img_src $img_src --img_dst $img_dst
#     done
#     idx2=37
#     img_src=${file_list[$idx1]}
#     img_dst=${file_list[$idx2]}
#     echo $idx1 $idx2 - $img_src and $img_dst
#     python manual_associator.py --img_src $img_src --img_dst $img_dst
# done

# ####################################### F5
# s=22
# e=35
# for idx1 in $(seq $s 1 $e)
# do
#     for idx2 in $(seq $(($idx1+1)) 1 $e)
#     do
# 	img_src=${file_list[$idx1]}
# 	img_dst=${file_list[$idx2]}
# 	echo $idx1 $idx2 - $img_src and $img_dst
#     	python manual_associator.py --img_src $img_src --img_dst $img_dst
#     done
#     idx2=38
#     img_src=${file_list[$idx1]}
#     img_dst=${file_list[$idx2]}
#     echo $idx1 $idx2 - $img_src and $img_dst
#     python manual_associator.py --img_src $img_src --img_dst $img_dst
# done



