install_if_not_installed <- function(package_list){
    
    uninstalled_pkgs <- package_list[!(package_list %in% installed.packages()[,"Package"])]
    if(length(uninstalled_pkgs)) install.packages(uninstalled_pkgs)
    }

install_if_not_installed(c("ggplotify", "imager"))
