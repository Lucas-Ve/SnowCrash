FROM kalilinux/kali-rolling

# Installer les outils utiles
RUN apt update && apt install -y \
    john \
    curl \
    vim \
    nano \
    net-tools \
    iputils-ping \
    && apt clean && rm -rf /var/lib/apt/lists/*

# Lancer un shell par défaut
CMD ["/bin/bash"]