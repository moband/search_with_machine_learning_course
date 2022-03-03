#!/bin/bash
# This is the module for hyperparameter optimisation of the fasttext supervised learning.
# author: "joydeep bhattacharjee"<joydeepubuntu@gmail.com>

###########################################################################################
###########################  read options ##################################
###########################################################################################
usage() { echo "Usage: $0 -l <training file> -t <test file>" 1>&2; exit 1; }

while getopts ":l:t:" o; do
    case "${o}" in
        l)
            training_file=${OPTARG}
            ;;
        t)
            testing_file=${OPTARG}
            ;;
        *)
            usage
            ;;
    esac
done
shift $((OPTIND-1))

if [ -z "${training_file}" ] && [ -z "${testing_file}" ]; then
	usage
else
	if ! [ -s "$training_file" ]; then
		echo "Training file is either not correct path or is empty."
		usage
	fi
	if ! [ -s "$testing_file" ]; then
		echo "Testing file is either not correct path or is empty."
		usage
	fi
	echo "Training file found: $training_file"
	echo "Testing file found: $testing_file"
fi

###############################################################
# constants
dim=(100)
lr=(0.15)
wordNgrams=(1 2 3)
final=(0 0 0 0)
epoch=(100)
performance=0
i=0


fasttext="/home/gitpod/fastText-0.9.2/fasttext"


# make the comparisons
for z in ${dim[@]}
do
    for y in ${lr[@]}
    do
        for w in ${wordNgrams[@]}
        do
            for e in ${epoch[@]}
            do
                # train with the current set of parameters
                "$fasttext" supervised -input "$training_file" -output _hyper_parameter_tmp_model -dim "$z" -lr "$y" -wordNgrams "$w" -epoch "$e" 

                # test the current model
                "$fasttext" test _hyper_parameter_tmp_model.bin "$testing_file" 1 > performance.txt

                # selecting the best performance
                present_performance=$(cat performance.txt | awk 'NR==2 {print $2}')
                if (( $(echo "$present_performance > $performance" | bc -l) )); then
                    final[0]="$z"
                    final[1]="$y"
                    final[2]="$w"
                    final[3]="$e"
                    echo "Performance values changed to ${final[@]}"
                    echo "Present precision recall values are:"
                    cat performance.txt
                fi
            done
        done
    done
done

echo "Publish the final results"
echo "the final model parameters are:"
echo "dim: ${final[0]}"
echo "lr: ${final[1]}"
echo "wordNgrams: ${final[2]}"
echo "epoch: ${final[3]}"

# clean up
rm _hyper_parameter_tmp_model*  performance.txt