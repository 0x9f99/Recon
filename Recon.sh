#!/bin/bash

TARGET="$1"

WORKING_DIR="$(cd "$(dirname "$0")" ; pwd -P)"
NRESULTS_PATH="$WORKING_DIR/nresults"
ERESULTS_PATH="$WORKING_DIR/eresults"

RED="\033[1;31m"
GREEN="\033[1;32m"
BLUE="\033[1;36m"
YELLOW="\033[1;33m"
RESET="\033[0m"


checkArgs(){
    if [[ $# -eq 0 ]]; then
        echo -e "\t${RED}[!] ERROR:${RESET} Invalid argument!\n"
        echo -e "\t${GREEN}[+] USAGE:${RESET}$0 ip.txt\n"
        exit 1
    elif [ ! -s $1 ]; then
        echo -e "\t${RED}[!] ERROR:${RESET} File is empty and/or does not exists!\n"
        echo -e "\t${GREEN}[+] USAGE:${RESET}$0 ip.txt\n"
        exit 1
    fi
}


setupTools(){
    echo -e "${GREEN}[+] Setting things up.${RESET}"
    sudo apt update -y
    sudo apt install -y gcc g++ make libpcap-dev xsltproc
    
    echo -e "${GREEN}[+] Creating results directory.${RESET}"
    mkdir -p $NRESULTS_PATH
}


installTools(){
    
    LATEST_MASSCAN="1.0.6"
    if [ ! -x "$(command -v masscan)" ]; then
        echo -e "${GREEN}[+] Installing Masscan.${RESET}"
        git clone https://github.com/robertdavidgraham/masscan
        cd masscan
        make -j
        sudo make -j install
        cd $WORKING_DIR
        rm -rf masscan
    else
        if [ "$LATEST_MASSCAN" == "$(masscan -V | grep "Masscan version" | cut -d " " -f 3)" ]; then
            echo -e "${BLUE}[-] Latest version of Masscan already installed. Skipping...${RESET}"
        else
            echo -e "${GREEN}[+] Upgrading Masscan to the latest version.${RESET}"
            git clone https://github.com/robertdavidgraham/masscan
            cd masscan
            make -j
            sudo make -j install
            cd $WORKING_DIR
            rm -rf masscan*
        fi
    fi

    LATEST_NMAP="$(wget -qO- https://nmap.org/dist/ | grep -oP 'nmap-([0-9\.]+)\.tar\.bz2'| tail -n 1 | grep -oP 'nmap-[0-9\.]+' | grep -oP '[0-9\.]+' | head -c -2)"
    if [ ! -x "$(command -v nmap)" ]; then
        echo -e "${GREEN}[+] Installing Nmap.${RESET}"
        wget https://nmap.org/dist/nmap-$LATEST_NMAP.tar.bz2
        bzip2 -cd nmap-$LATEST_NMAP.tar.bz2 | tar xvf -
        cd nmap-$LATEST_NMAP
        ./configure
        make -j
        sudo make -j install
        cd $WORKING_DIR
        rm -rf nmap-$LATEST_NMAP*
    else 
        if [ "$LATEST_NMAP" == "$(nmap -V | grep "Nmap version" | cut -d " " -f 3)" ]; then
            echo -e "${BLUE}[-] Latest version of Nmap already installed. Skipping...${RESET}"
        else
            echo -e "${GREEN}[+] Upgrading Nmap to the latest version.${RESET}"
            wget https://nmap.org/dist/nmap-$LATEST_NMAP.tar.bz2
            bzip2 -cd nmap-$LATEST_NMAP.tar.bz2 | tar xvf -
            cd nmap-$LATEST_NMAP
            ./configure
            make -j
            sudo make -j install
            cd $WORKING_DIR
            rm -rf nmap-$LATEST_NMAP*
        fi 
    fi
    
    if [ -d "nmap-parse-output" ];then
        echo -e "${BLUE}[-] Latest version of Nmap-parse-output already installed. Skipping...${RESET}"
    else
        echo -e "${GREEN}[+] Installing nmap-parse-output.${RESET}"
        git clone https://github.com/ernw/nmap-parse-output
    fi
    
    if [ -d "EyeWitness" ];then
        echo -e "${BLUE}[-] Latest version of Eyewitness already installed. Skipping...${RESET}"
    else
        echo -e "${GREEN}[+] Installing EyeWitness.${RESET}"
        git clone https://github.com/FortyNorthSecurity/EyeWitness && sudo ./EyeWitness/setup/setup.sh
    fi

}

portScan(){
    echo -e "${GREEN}[+] Running Masscan.${RESET}"
    sudo masscan -p 1-65535 --rate 30000 --wait 0 --open -iL $TARGET -oX $NRESULTS_PATH/masscan.xml
    sudo rm $WORKING_DIR/paused.conf
    xsltproc -o $NRESULTS_PATH/masscan.html $WORKING_DIR/bootstrap-masscan.xsl $RESULTS_PATH/masscan.xml
    open_ports=$(cat $NRESULTS_PATH/masscan.xml | grep portid | cut -d "\"" -f 10 | sort -n | uniq | paste -sd,)
    cat $NRESULTS_PATH/masscan.xml | grep portid | cut -d "\"" -f 4 | sort -V | uniq > $WORKING_DIR/nmap_targets.tmp
    echo -e "${RED}[*] Masscan Done! View the HTML report at $NRESULTS_PATH${RESET}"

    echo -e "${GREEN}[+] Running Nmap.${RESET}"
    sudo nmap -sVC -p $open_ports --open -v -Pn -n -T4 -iL $WORKING_DIR/nmap_targets.tmp -oX $NRESULTS_PATH/nmap.xml
    sudo rm $WORKING_DIR/nmap_targets.tmp
    xsltproc -o $NRESULTS_PATH/nmap-bootstrap.html $WORKING_DIR/bootstrap-nmap.xsl $NRESULTS_PATH/nmap.xml
    echo -e "${RED}[*] Nmap Done! View the HTML reports at $NRESULTS_PATH${RESET}"
    echo -e "${RED}[*] Nmap-parse-output Done!${RESET}"
    
    echo -e "${GREEN}[+] Running Nmap-parse-output.${RESET}"
    nmap-parse-output/nmap-parse-output $NRESULTS_PATH/nmap.xml http-ports | tee url.tmp
    nmap-parse-output/nmap-parse-output $NRESULTS_PATH/nmap.xml tls-ports | awk '{print "https://"$1}'|tee -a url.tmp
    cat url.tmp |sort|uniq >url_list && rm -rf url.tmp
    nmap-parse-output/nmap-parse-output $NRESULTS_PATH/nmap.xml service-names > $NRESULTS_PATH/service-names.txt
    nmap-parse-output/nmap-parse-output $NRESULTS_PATH/nmap.xml product > $NRESULTS_PATH/product.txt
    IFS_old=$IFS;IFS=$'\n'
    for line in `./nmap-parse-output/nmap-parse-output nresults/nmap.xml http-title`;do echo -e $line;done | tee $NRESULTS_PATH/http-title.txt
    IFS=$IFS_old
}

vulCheck(){
    sudo pip install -r requrement.txt
    echo -e "${GREEN}[+] Running vul_check.${RESET}"
    python3 vul_check.py url_list
    echo -e "${GREEN}[+] Running Eyewitness.${RESET}"
    sudo python3 ./EyeWitness/EyeWitness.py -x $NRESULTS_PATH/nmap.xml --no-prompt -d $ERESULTS_PATH
}

checkArgs $TARGET
setupTools
installTools
portScan
vulCheck
