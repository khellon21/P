# Make standard commands safer and more verbose
alias rm='rm -i'
alias cp='cp -iv'
alias mv='mv -iv'

# Better directory listing
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'

# Colorize grep output
alias grep='grep --color=auto'

# Quick system update (Debian/Ubuntu/WSL specific)
alias update='sudo apt update && sudo apt upgrade -y'

# Quick navigation
alias ..='cd ..'
alias ...='cd ../..'

