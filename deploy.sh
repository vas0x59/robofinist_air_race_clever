#!/bin/bash

host="192.168.1.159"

# read -sp 'password: ' passvar
echo ""

passvar=$(cat raspi_pass.txt)

src_to_deploy=$(ls ./src --color=never)
scripts_to_deploy=$(cat deploy_conf/scripts_to_deploy.txt)
src_to_deploy=""


for var in $(ls ./src --color=never)
do 
    # echo "$var"
    src_to_deploy="$src_to_deploy ./src/$var"
    # sshpass -p "$passvar" scp "drone_scripts/$var" pi@$host:
done

for var in $(ls ./drone_scripts --color=never)
do 
    # echo "$var"
    scripts_to_deploy="$scripts_to_deploy ./drone_scripts/$var"
    # sshpass -p "$passvar" scp "drone_scripts/$var" pi@$host:
done

echo "src: $src_to_deploy"
echo "script: $scripts_to_deploy"
# for var in $(ls ./configs --color=never)
# do 
#     # echo "$var"
#     configs_to_deploy="$configs_to_deploy ./configs/$var"
#     # sshpass -p "$passvar" scp "drone_scripts/$var" pi@$host:
# done

# to_deploy="$lib_to_deploy $bin_to_deploy $scripts_to_deploy"

sshpass -p "$passvar" scp $src_to_deploy pi@$host:src
sshpass -p "$passvar" scp $scripts_to_deploy pi@$host: