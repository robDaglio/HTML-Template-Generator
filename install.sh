#!/usr/bin/env bash

# Assure that you have created and activated a virtual environment
# and that pip is currently installed on your system.

# Get admin credentials.
read -p "[?] Admin password: " -s ADMIN; echo ""

# Get target installation directory.
read -p "[?] Installation directory: " INSTALL_DIR; echo ""

REQUIREMENTS="requirements.txt"
DIST_DIRECTORY="temp"
BINARY="dist/ptg"
SYMLINK_PATH="/usr/local/bin/ptg"

declare -a COMPONENTS=(
    "ptg.py"
    "api"
    "generator"
)

declare -a BUILD_FILES=(
    "ptg.py"
    "api/__init__.py"
    "api/downloader.py"
    "generator/__init__.py"
    "generator/generator.py"
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

    for file in "${COMPONENTS[@]}"; do
        log "Copying ${file} to ${DIST_DIRECTORY}"
        cp -r $file $DIST_DIRECTORY
    done
}

function build_binary () {
    log "Building application."
    cd $DIST_DIRECTORY

    if [ $? -ne 0 ]; then
        log "Unable to change directory."
        exit 1
    fi

    pyinstaller --onefile "${BUILD_FILES[0]}" "${BUILD_FILES[1]}" "${BUILD_FILES[2]}" \
                        "${BUILD_FILES[3]}" "${BUILD_FILES[4]}"

    check_return_code $? "Success!" "Failed." "exit 1"
}

function create_installation_directory () {
    if ! [ -e "${1}" ]; then
        log "Creating ${1}."
        echo "${2}" | sudo -S mkdir -p "${1}"

        check_return_code $? "Success!" "Failed." "exit 1"
    else
        log "${1} exists. Skipping."
    fi
}

function copy_binary_and_create_symlink () {
    # $1 = $INSTALL_DIR
    # $2 = $BINARY
    # $3 = SYMLINK_PATH

    if ! [ -e "${2}" ]; then
        log "Binary not found."
    else
        log "Copying ${2} to ${1}."
        echo "${4}" | sudo -S cp "${2}" "${1}"
        check_return_code $? "Success!" "Failed." "exit 1"

        log "Creating symlink at ${3}"

        echo "${4}" | sudo -S ln -s "${1}/ptg" "${3}"
        check_return_code $? "Installation complete." "Failed." "exit 1"
    fi
}

function cleanup () {
    log "Cleaning up!"
    cd ..

    if [ -e "${1}" ]; then
        log "Deleting ${1}."
        rm -rf "${1}"
    fi
}


install_dependencies

create_distribution_directory
copy_files_to_distribution
check_return_code $? "Success!" "Failed." "exit 1"

build_binary

create_installation_directory "${INSTALL_DIR}" "${ADMIN}"
copy_binary_and_create_symlink "${INSTALL_DIR}" "${BINARY}" "${SYMLINK_PATH}" "${ADMIN}"
cleanup "${DIST_DIRECTORY}"
