
# Custom Bash Aliases

# Easier navigation
alias ..='cd ..'
alias ...='cd ../..'
alias clr='clear'

# Better list commands
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'

# System updates (assumes Debian/Ubuntu based on typical WSL2 setups)
alias update='sudo apt update && sudo apt upgrade -y'
