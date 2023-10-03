#!/bin/sh
function loggit() {
    echo "[INSTALLER] $date | $1"
}

apk update

apt add --update --no-cache gcc g++ make nmap

tools_dir=/home/root/tools
#mkdir -p /home/root/tools
#
#if [ $INSTALL_CVES = yes ]; then 
#    cd $tools_dir
#    loggit "Installing CVEScanner2 .. takes a long time .."
#    git clone --recursive https://github.com/scmanjarrez/CVEScannerV2.git
#    cd CVEScannerV2/
#    pip3 install -r requirements.txt
#    python3 ./database.py
#fi;
#
#cd $tools_dir
#loggit "Installing wapiti3"
#git clone --recursive https://github.com/wapiti-scanner/wapiti.git
#cd wapiti/ && ls
#python3 -m pip install wapiti3
#
#cd $tools_dir
#loggit "Installing Dirby";
#git clone https://github.com/BrainiacRawkib/dirby.git
#cd dirby/
#pip install -r requirements.txt
#
#cd $tools_dir
#loggit "Installing scanvus";
#git clone https://github.com/leonov-av/scanvus.git
#cd scanvus/
#pip install -r requirements.txt
#
#cd $tools_dir
#loggit "installing sslyze";
#git clone https://github.com/nabla-c0d3/sslyze.git
#cd sslyze/
#pip install --upgrade pip setuptools wheel
#pip install --upgrade sslyze
#
#cd $tools_dir
#loggit "Installing wafw00f";
#git clone https://github.com/EnableSecurity/wafw00f.git
#cd wafw00f/
#python3 setup.py install
