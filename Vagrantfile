# WARNING: You will need the following plugin:
# vagrant plugin install vagrant-docker-compose
if Vagrant.plugins_enabled?
  unless Vagrant.has_plugin?('vagrant-docker-compose')
    puts 'Plugin missing.'
    system('vagrant plugin install vagrant-docker-compose')
    puts 'Dependencies installed, please try the command again.'
    exit
  end
end


# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility).
Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/xenial64"
  # set up network ip and port forwarding
  config.vm.network "forwarded_port", guest: 5000, host: 5000, host_ip: "127.0.0.1"
  config.vm.network "forwarded_port", guest: 5005, host: 5005, host_ip: "127.0.0.1"
  config.vm.network "private_network", ip: "192.168.33.10"

  config.vm.provider "virtualbox" do |vb|
    # Customize the amount of memory on the VM:
    vb.memory = "1024"
    vb.cpus = 1
    # Fixes some DNS issues on some networks
    vb.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
    vb.customize ["modifyvm", :id, "--natdnsproxy1", "on"]
  end

  # Copy your .gitconfig file so that your git credentials are correct
  if File.exists?(File.expand_path("~/.gitconfig"))
    config.vm.provision "file", source: "~/.gitconfig", destination: "~/.gitconfig"
  end

  # Copy your ssh keys for github so that your git credentials work
  if File.exists?(File.expand_path("~/.ssh/id_rsa"))
    config.vm.provision "file", source: "~/.ssh/id_rsa", destination: "~/.ssh/id_rsa"
  end

  # Copy your ~/.vimrc file so that vi looks the same
  if File.exists?(File.expand_path("~/.vimrc"))
    config.vm.provision "file", source: "~/.vimrc", destination: "~/.vimrc"
  end

  config.vm.synced_folder ".", "/vagrant", mount_options: ["dmode=775,fmode=664"]
  ######################################################################
  # Add a few docker images
  ######################################################################
  config.vm.provision "docker" do |d|
    # d.pull_images "alpine:3.7"
    # d.pull_images "ubuntu"
    d.pull_images "rasa/rasa_core:latest"
    d.pull_images "rasa/rasa_nlu:latest-spacy"
    # d.run "redis:alpine",
    #   args: "--restart=always -d --name redis -p 6379:6379 -v redis_volume:/data"
  end

  # Add Docker compose
  config.vm.provision :docker_compose
  # config.vm.provision :docker_compose,
  #   yml: "/vagrant/docker-compose.yml",
  #   rebuild: true,
  #   run: "always"

  config.vm.provision "shell", inline: <<-SHELL
    # create swap file of 1GB
    sudo dd if=/dev/zero of=/swapfile bs=1024 count=1048576
    # modify permissions
    sudo chown root:root /swapfile
    sudo chmod 0600 /swapfile
    # setup swap area
    sudo mkswap /swapfile
    # turn swap on
    sudo swapon /swapfile

    # increase max shared memory segment from 32mb to 128mb
    # sudo /bin/su -c "echo 'kernel.shmmax=134217728' >> /etc/sysctl.conf"
    # sudo /bin/su -c "echo 'kernel.shmall=134217728' >> /etc/sysctl.conf"

    # cd into pwd
    cd /vagrant

    # train nlu
    docker run \
      -v $(pwd):/app/project \
      -v $(pwd)/models/rasa_nlu:/app/models \
      -v $(pwd)/config:/app/config \
      rasa/rasa_nlu:latest-spacy \
      run \
        python -m rasa_nlu.train \
        -c config/nlu_config.yml \
        --data project/data/nlu.md \
        -o models \
        --project current \
        -t 1 \
        --verbose

    # train core
    docker run \
      -v $(pwd):/app/project \
      -v $(pwd)/models/rasa_core:/app/models \
      rasa/rasa_core:latest \
      train \
        --domain project/domain.yml \
        --stories project/data/stories.md \
        --out models \
        -c project/config/policies.yml

    # cd /vagrant
    docker-compose up

    # install python
    # sudo apt-get install build-essential python3-dev python3-pip -y

    # sudo pip3 install --upgrade https://storage.googleapis.com/tensorflow/linux/cpu/tensorflow-1.10.0-cp35-cp35m-linux_x86_64.whl --no-cache-dir
    # cd /vagrant
    # sudo pip3 install --no-cache-dir spacy
    # sudo pip3 install --no-cache-dir -r requirements.txt
    # sudo python3 -m spacy download en

    # set aliases
    # alias python=python3
    # alias pip=pip3
  SHELL


end