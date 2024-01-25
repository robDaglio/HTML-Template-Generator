#!/usr/bin/env bash

# Note: This script must be run as root.
# Assure that you have created and activated a virtual environment
# and that pip is currently installed on your system
# Get admin credentials
# read -p "[?] Admin password: " -s ADMIN

REQUIREMENTS="requirements.txt"
DIST_DIRECTORY="temp"

declare -a BUILD_FILES=(
    "ptg.py"
    "api"
    "generator"
)

function log () {
    echo "${BASHPID} $(date '+%d-%m-%Y %H:%M:%S'): $1"
}

function verify_file_exists () {
    if ! [[ -e $1 ]]; then
        log "File ${1} does not exist."
        exit 1
    fi
}

function check_return_code () {
    # $1: return code
    # $2: success message
    # $3: failed message
    # $4: optional command to execute

    if [ "${1}" -ne 0 ]; then
        log "${3}"
        if [ -n "${4}" ]; then
            eval "${4}"
        else
            return 1
        fi
    else
        log "${2}"
    fi
}


function install_dependencies () {
    # This function will install all necessary dependencies.
    log "Verifying requirements."
    verify_file_exists $REQUIREMENTS

    log "Installing dependencies from ${REQUIREMENTS}."
    python -m pip install --upgrade pip; python -m pip install -r requirements.txt
}

function create_distribution_directory () {
    log "Creating temporary distribution directory."
    mktemp -d $DIST_DIRECTORY

    check_return_code $? "Success." "Failed." "exit 1"
}

function copy_files_to_distribution () {
    log "Copying files to distribution directory."

    for file in "${BUILD_FILES[@]}"; do
        log "Copying ${file} to ${DIST_DIRECTORY}"
        cp -r $file $DIST_DIRECTORY
    done
}

function build_binary () {
    log "Building application."
#    cd $DIST_DIRECTORY

#    if [ $? -ne 0 ]; then
#        log "Unable to change directory."
#        exit 1
#    fi

    pyinstaller --onefile "${BUILD_FILES[0]}" "${BUILD_FILES[1]}/*" "${BUILD_FILES[2]}/*"
#    check_return_code $? "Success!" "Failed." "exit 1"
}


#verify_root
#install_dependencies
#
#create_distribution_directory
#copy_files_to_distribution
#check_return_code $? "Success!" "Failed." "exit 1"
#
build_binary
