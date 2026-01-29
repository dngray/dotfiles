function loc --description 'A safer, faster locate alternative using fd'
    env LD_PRELOAD="" fd --hidden --exclude .git $argv
end

function fl --description 'Interactive file finder using fd and fzf'
    env LD_PRELOAD="" fd --type f --hidden --exclude .git $argv | fzf
end
