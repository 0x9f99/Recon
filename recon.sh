#!/bin/bash

TARGET="$1"

TIME=`date +"%Y%m%d%H%M"`
WORKING_DIR="$(cd "$(dirname "$0")" ; pwd -P)"
NRESULTS_PATH="$WORKING_DIR/$TIME/nresults"
ERESULTS_PATH="$WORKING_DIR/$TIME/eresults"

RED="\033[1;31m"
GREEN="\033[1;32m"
BLUE="\033[1;36m"
YELLOW="\033[1;33m"
RESET="\033[0m"


checkArgs(){
    if [[ $# -eq 0 ]]; then
        echo -e "\t${RED}[!] ERROR:${RESET} Invalid argument!\n"
        echo -e "\t${GREEN}[+] USAGE:${RESET}$0 ip.txt or $0 domain.com\n"
        exit 1
    elif [ $1 != "ip.txt" ]; then
        echo -e "\t${RED}[!] ERROR:${RESET} Invalid argument!\n"
        echo -e "\t${GREEN}[+] USAGE:${RESET}$0 ip.txt or $0 domain.com\n"
        exit 1
    elif [ ! -s $1 ]; then
        echo -e "\t${RED}[!] ERROR:${RESET} Invalid argument!\n"
        echo -e "\t${GREEN}[+] USAGE:${RESET}$0 ip.txt or $0 domain.com\n"
        exit 1
    fi
}

setupTools(){
    echo -e "${GREEN}[+] Setting things up.${RESET}"
    sudo apt update -y
    #sudo apt upgrade -y
    #sudo apt autoremove -y
    #sudo apt clean
    sudo apt install -y gcc g++ make libpcap-dev xsltproc snap
    
    echo -e "${GREEN}[+] Creating results directory.${RESET}"
    mkdir -p $NRESULTS_PATH
}

installTools(){
    
    echo -e "${RED}[+] Installing the latest version of Go...${RESET}"
    LATEST_GO=$(wget -qO- https://golang.org/dl/ | grep -oP 'go([0-9\.]+)\.linux-amd64\.tar\.gz' | head -n 1 | grep -oP 'go[0-9\.]+' | grep -oP '[0-9\.]+' | head -c -2)
    wget https://dl.google.com/go/go$LATEST_GO.linux-amd64.tar.gz
    sudo tar -C /usr/local -xzf go$LATEST_GO.linux-amd64.tar.gz
    echo 'export PATH=$PATH:/usr/local/go/bin' >> ~/.profile
    source ~/.profile
    rm -rf go$LATEST_GO*
    
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

    if [ -d "tomcat-weak-password-scanner" ];then
        echo -e "${BLUE}[-] Latest version of tomcat-weak-password-scanner already installed. Skipping...${RESET}"
    else
        echo -e "${GREEN}[+] Installing tomcat-weak-password-scanner.${RESET}"
        git clone https://github.com/magicming200/tomcat-weak-password-scanner
    fi
    
    if [ -e /usr/local/go/bin/go ]; then
        echo -e "${BLUE}[-] Latest version of golang-go already installed. Skipping...${RESET}"
    else 
        echo -e "${GREEN}[+] Installing the latest version of Go...${RESET}"
        LATEST_GO=$(wget -qO- https://golang.org/dl/ | grep -oP 'go([0-9\.]+)\.linux-amd64\.tar\.gz' | head -n 1 | grep -oP 'go[0-9\.]+' | grep -oP '[0-9\.]+' | head -c -2)
        wget https://dl.google.com/go/go$LATEST_GO.linux-amd64.tar.gz
        sudo tar -C /usr/local -xzf go$LATEST_GO.linux-amd64.tar.gz
        echo 'export PATH=$PATH:/usr/local/go/bin' >> ~/.profile
        source ~/.profile
        rm -rf go$LATEST_GO*
    fi
    
    if [ -e /snap/bin/amass ]; then
        echo -e "${BLUE}[-] Latest version of amass already installed. Skipping...${RESET}"
    else 
        snap install amass
    fi
    
    if [ -e /usr/bin/subfinder ]; then
        echo -e "${BLUE}[-] Latest version of Subfinder already installed. Skipping...${RESET}"
    else 
        wget https://github.com/projectdiscovery/subfinder/releases/download/v2.2.4/subfinder-linux-amd64.tar
        mv subfinder-linux-amd64 /usr/bin/subfinder
        rm -rf subfinder-linux-amd64.tar
    fi

}

enumSubs(domain){
    /usr/bin/subfinder -d $2 -v -o dns.tmp
    /snap/bin/amass enum -d $2 > dns.tmp
    cat dns.tmp |sort|uniq > dns.target 
    for i in `cat dns.target`;do host $i|grep -E -o "([0-9]{1,3}[\.]){3}[0-9]{1,3}";done |sort|uniq|grep -E -o "([0-9]{1,3}[\.]){3}"|uniq -c|awk '{if ($1>=3) print $2"0/24"}' >ip.txt
}

portScan(){
    echo -e "${GREEN}[+] Running Masscan.${RESET}"
    sudo masscan -p1-65535 --rate 30000 --open -iL $TARGET -oX $NRESULTS_PATH/masscan.xml
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
    $WORKING_DIR/nmap-parse-output/nmap-parse-output $NRESULTS_PATH/nmap.xml http-ports | tee url.tmp
    $WORKING_DIR/nmap-parse-output/nmap-parse-output $NRESULTS_PATH/nmap.xml tls-ports | awk '{print "https://"$1}'|tee -a url.tmp
    cat url.tmp |sort|uniq >url_list && rm -rf url.tmp
    $WORKING_DIR/nmap-parse-output/nmap-parse-output $NRESULTS_PATH/nmap.xml service-names > $NRESULTS_PATH/service-names.txt
    $WORKING_DIR/nmap-parse-output/nmap-parse-output $NRESULTS_PATH/nmap.xml product > $NRESULTS_PATH/product.txt
    IFS_old=$IFS;IFS=$'\n'
    for line in `$WORKING_DIR/nmap-parse-output/nmap-parse-output $NRESULTS_PATH/nmap.xml http-title`;do echo -e $line;done | tee $NRESULTS_PATH/http-title.txt
    IFS=$IFS_old
    $WORKING_DIR/nmap-parse-output/nmap-parse-output $NRESULTS_PATH/nmap.xml search-product "Apache Tomcat" | awk -F : '{print $1}'>tomcat-weak-password-scanner/ip.txt
    $WORKING_DIR/nmap-parse-output/nmap-parse-output $NRESULTS_PATH/nmap.xml search-product "Apache Tomcat" | awk -F : '{print $2}'>tomcat-weak-password-scanner/port.txt

}

vulScanner(){
    sudo pip install -r requrement.txt     
    echo -e "${GREEN}[+] Running vul-scanner.${RESET}"
    python3 $WORKING_DIR/epfa.py url_list | tee  $NRESULTS_PATH/vul_result.txt
    echo -e "${GREEN}[+] Running Eyewitness.${RESET}"
    sudo -i python3 $WORKING_DIR/EyeWitness/EyeWitness.py -x $NRESULTS_PATH/nmap.xml --no-prompt -d $ERESULTS_PATH  --no-dns --ocr
    echo -e "${GREEN}[+] Running weak-password-scanner.${RESET}"
    cd $WORKING_DIR/tomcat-weak-password-scanner/ && python koala_tomcat_cmd.py -h ip.txt -p port.txt && cd -
}

checkArgs $TARGET
setupTools
installTools
portScan
vulScanner
